"""
Train the Telco Customer Churn prediction pipeline.
"""

import os
import json
import random
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    ConfusionMatrixDisplay,
    f1_score,
    precision_score,
    recall_score,
    RocCurveDisplay,
    roc_auc_score,
)
from sklearn.model_selection import (
    GridSearchCV,
    cross_validate,
    StratifiedKFold,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from tabulate import tabulate
from xgboost import XGBClassifier

from src.features.build_features import create_preprocessor

SEED = 42
BASE_DIR = Path(__file__).resolve().parents[2]

os.environ["PYTHONHASHSEED"] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)

DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_telco.csv"
MODEL_PATH = BASE_DIR / "artifacts" / "model.pkl"
MODEL_METRICS_PATH = BASE_DIR / "artifacts" / "model_metrics.json"
MODEL_INFO_PATH = BASE_DIR / "artifacts" / "model_info.json"
REPORTS_DIR = BASE_DIR.parent / "reports"
PRIMARY_SELECTION_METRIC = "ROC-AUC"
MODEL_NAME = "Telco Customer Churn Classifier"
MODEL_ALGORITHM = "XGBoostClassifier"
MODEL_VERSION = os.getenv("MODEL_VERSION", "local")

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


def load_saved_model() -> Any | None:
    """Load the currently deployed model if it exists."""

    if not MODEL_PATH.exists():
        return None

    return joblib.load(MODEL_PATH)


def load_saved_model_metrics() -> dict[str, float] | None:
    """Load metrics for the currently deployed model if available."""

    if not MODEL_METRICS_PATH.exists():
        return None

    with MODEL_METRICS_PATH.open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def selection_metric_value(metrics: dict[str, float]) -> float:
    """Read the primary model-selection metric from either display or artifact keys."""

    return metrics.get(PRIMARY_SELECTION_METRIC, metrics.get("roc_auc", 0.0))


def cross_validate_model(model: Pipeline, X_train: pd.DataFrame, y_train: pd.Series) -> dict[str, float]:
    """Compute cross-validation metrics for the selected model."""

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=SEED,
    )

    scores = cross_validate(
        estimator=model,
        X=X_train,
        y=y_train,
        scoring={
            "accuracy": "accuracy",
            "precision": "precision",
            "recall": "recall",
            "f1": "f1",
            "roc_auc": "roc_auc",
        },
        cv=cv,
        n_jobs=1,
        error_score="raise",
        return_train_score=False,
    )

    return {
        "cv_accuracy": float(scores["test_accuracy"].mean()),
        "cv_precision": float(scores["test_precision"].mean()),
        "cv_recall": float(scores["test_recall"].mean()),
        "cv_f1": float(scores["test_f1"].mean()),
        "cv_roc_auc": float(scores["test_roc_auc"].mean()),
    }


def should_replace_existing_model(candidate_metrics: dict[str, float], current_metrics: dict[str, float] | None) -> bool:
    """Decide whether the candidate model should replace the saved model."""

    if current_metrics is None:
        return True

    return selection_metric_value(candidate_metrics) >= selection_metric_value(current_metrics)


def save_model_artifacts(
    model: Pipeline,
    metrics: dict[str, float],
    feature_count: int,
    training_timestamp: str,
) -> None:
    """Persist the promoted model and its evaluation metrics."""

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    with MODEL_METRICS_PATH.open("w", encoding="utf-8") as file_handle:
        json.dump(metrics, file_handle, indent=2)

    with MODEL_INFO_PATH.open("w", encoding="utf-8") as file_handle:
        json.dump(
            {
                "model_name": MODEL_NAME,
                "algorithm": MODEL_ALGORITHM,
                "version": MODEL_VERSION,
                "feature_count": feature_count,
                "training_timestamp": training_timestamp,
                "artifact_path": str(MODEL_PATH),
            },
            file_handle,
            indent=2,
        )


def generate_reports(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    metrics: dict[str, float],
    best_params: dict[str, Any],
    training_timestamp: str,
) -> None:
    """Generate lightweight model evaluation artifacts for portfolio review."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    ConfusionMatrixDisplay.from_predictions(y_test, predictions, display_labels=["No", "Yes"])
    plt.title("Telco Churn Confusion Matrix")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "confusion_matrix.png", dpi=160)
    plt.close()

    RocCurveDisplay.from_predictions(y_test, probabilities)
    plt.title("Telco Churn ROC Curve")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "roc_curve.png", dpi=160)
    plt.close()

    classifier = model.named_steps["classifier"]
    preprocessor = model.named_steps["preprocessor"]
    feature_names = preprocessor.get_feature_names_out()
    importances = pd.Series(classifier.feature_importances_, index=feature_names)
    top_importances = importances.sort_values(ascending=False).head(15).sort_values()

    top_importances.plot(kind="barh", figsize=(9, 6), color="#2563eb")
    plt.title("Top Feature Importances")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "feature_importance.png", dpi=160)
    plt.close()

    with (REPORTS_DIR / "classification_report.md").open("w", encoding="utf-8") as file_handle:
        file_handle.write("# Classification Report\n\n")
        file_handle.write("```text\n")
        file_handle.write(classification_report(y_test, predictions, target_names=["No Churn", "Churn"]))
        file_handle.write("```\n")

    with (REPORTS_DIR / "model_card.md").open("w", encoding="utf-8") as file_handle:
        file_handle.write(
            f"""# Telco Customer Churn Model Card

## Overview
This model estimates whether a telecom customer is likely to churn from account, billing, contract, and service attributes.

## Dataset
The training data is the Telco Customer Churn dataset with customer demographics, account tenure, subscribed services, billing method, and churn label.

## Features
The pipeline uses {len(X_test.columns)} raw input features. Categorical features are imputed and one-hot encoded; numeric features are median-imputed.

## Training Method
The model is an XGBoost classifier trained inside a scikit-learn pipeline with stratified train/test splitting and grid search.

## Hyperparameters
```json
{json.dumps(best_params, indent=2)}
```

## Metrics
- Accuracy: {metrics["accuracy"]:.4f}
- Precision: {metrics["precision"]:.4f}
- Recall: {metrics["recall"]:.4f}
- F1: {metrics["f1"]:.4f}
- ROC-AUC: {metrics["roc_auc"]:.4f}

## Limitations
The dataset is static and may not reflect current customer behavior. The model should be monitored for drift before use in a live business workflow.

## Future Improvements
Add drift detection, calibration checks, SHAP explanations, and scheduled retraining with production data snapshots.

## Training Timestamp
{training_timestamp}
"""
        )


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
        cv_metrics = cross_validate_model(best_pipeline, X_train, y_train)
        current_pipeline = load_saved_model()
        current_metrics = load_saved_model_metrics()
        if current_metrics is None and current_pipeline is not None:
            current_metrics = evaluate(current_pipeline, X_test, y_test)
        should_save_model = should_replace_existing_model(metrics, current_metrics)

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

        print("\nCross-Validation Metrics")
        print(
            tabulate(
                [[
                    round(cv_metrics["cv_accuracy"], 4),
                    round(cv_metrics["cv_precision"], 4),
                    round(cv_metrics["cv_recall"], 4),
                    round(cv_metrics["cv_f1"], 4),
                    round(cv_metrics["cv_roc_auc"], 4),
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

        if current_metrics is not None:
            print(f"\nExisting model {PRIMARY_SELECTION_METRIC}: {selection_metric_value(current_metrics):.4f}")
        print(f"Candidate model {PRIMARY_SELECTION_METRIC}: {selection_metric_value(metrics):.4f}")
        print(f"Will replace saved model: {should_save_model}")

        mlflow.log_params(grid_search.best_params_)

        mlflow.log_metrics({
            "accuracy": metrics["Accuracy"],
            "precision": metrics["Precision"],
            "recall": metrics["Recall"],
            "f1": metrics["F1"],
            "roc_auc": metrics["ROC-AUC"],
            **cv_metrics,
        })

        artifact_metrics = {
            "accuracy": metrics["Accuracy"],
            "precision": metrics["Precision"],
            "recall": metrics["Recall"],
            "f1": metrics["F1"],
            "roc_auc": metrics["ROC-AUC"],
            **cv_metrics,
        }
        training_timestamp = datetime.now(UTC).isoformat()
        generate_reports(
            best_pipeline,
            X_test,
            y_test,
            artifact_metrics,
            grid_search.best_params_,
            training_timestamp,
        )

        if should_save_model:
            save_model_artifacts(
                best_pipeline,
                artifact_metrics,
                feature_count=X_train.shape[1],
                training_timestamp=training_timestamp,
            )
            print(f"\nPipeline saved to {MODEL_PATH}")
        else:
            print("\nExisting model is stronger. Skipping model overwrite.")

        mlflow.sklearn.log_model(
            sk_model=best_pipeline,
            name="model",
            serialization_format="cloudpickle",
        )


if __name__ == "__main__":
    train()
