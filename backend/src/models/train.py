"""
Train the Telco Customer Churn prediction pipeline.
"""

import os
import random
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from tabulate import tabulate
from xgboost import XGBClassifier

from src.features.build_features import create_preprocessor

SEED = 42

os.environ["PYTHONHASHSEED"] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)

DATA_PATH = Path("./data/processed/cleaned_telco.csv")
MODEL_PATH = Path("./artifacts/model.pkl")

mlflow.set_experiment("Telco Customer Churn")


def load_dataset():
    df = pd.read_csv(DATA_PATH)

    if "customerID" in df.columns:
        df = df.drop(columns="customerID")

    df["Churn"] = (
        df["Churn"]
        .map({"No": 0, "Yes": 1})
        .astype(np.int8)
    )

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    return train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=SEED,
    )


def evaluate(model, X_test, y_test):
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    return {
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(y_test, predictions),
        "Recall": recall_score(y_test, predictions),
        "F1": f1_score(y_test, predictions),
        "ROC-AUC": roc_auc_score(y_test, probabilities),
    }


def train():

    X_train, X_test, y_train, y_test = load_dataset()

    preprocessor = create_preprocessor(X_train)

    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                XGBClassifier(
                    random_state=SEED,
                    eval_metric="logloss",
                    tree_method="hist",
                    device="cpu",
                    scale_pos_weight=scale_pos_weight,
                ),
            ),
        ]
    )

    param_grid = {
        "classifier__max_depth": [3, 5, 7],
        "classifier__learning_rate": [0.01, 0.1, 0.2],
        "classifier__n_estimators": [50, 100, 200],
    }

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=SEED,
    )

    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring="f1",
        cv=cv,
        n_jobs=1,
        verbose=1,
    )

    with mlflow.start_run():

        grid_search.fit(X_train, y_train)

        best_pipeline = grid_search.best_estimator_

        metrics = evaluate(best_pipeline, X_test, y_test)

        print("\nBest Parameters")
        print(grid_search.best_params_)

        print(
            tabulate(
                [[
                    round(metrics["Accuracy"], 4),
                    round(metrics["Precision"], 4),
                    round(metrics["Recall"], 4),
                    round(metrics["F1"], 4),
                    round(metrics["ROC-AUC"], 4),
                ]],
                headers=[
                    "Accuracy",
                    "Precision",
                    "Recall",
                    "F1",
                    "ROC-AUC",
                ],
                tablefmt="grid",
            )
        )

        mlflow.log_params(grid_search.best_params_)

        mlflow.log_metrics({
            "accuracy": metrics["Accuracy"],
            "precision": metrics["Precision"],
            "recall": metrics["Recall"],
            "f1": metrics["F1"],
            "roc_auc": metrics["ROC-AUC"],
        })

        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(best_pipeline, MODEL_PATH)

        mlflow.sklearn.log_model(
    sk_model=best_pipeline,
    name="model",
    serialization_format="cloudpickle",
)

        print(f"\nPipeline saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()