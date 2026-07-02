"""
Telco Customer Churn - Model Training

Models:
- Logistic Regression
- Decision Tree
- Random Forest
- KNN
- SVM
- Naive Bayes
- XGBoost
"""

from pathlib import Path
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

from xgboost import XGBClassifier
from tabulate import tabulate

from src.features.build_features import build_features


MODEL_PATH = Path("../../artifacts/model.pkl")


def evaluate(model, X_test, y_test):
    predictions = model.predict(X_test)

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X_test)[:, 1]
    else:
        probabilities = predictions

    return {
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(y_test, predictions),
        "Recall": recall_score(y_test, predictions),
        "F1": f1_score(y_test, predictions),
        "ROC-AUC": roc_auc_score(y_test, probabilities),
    }


def train_models():

    X_train, X_test, y_train, y_test = build_features()

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42),
        "KNN": KNeighborsClassifier(),
        "SVM": SVC(probability=True, random_state=42),
        "Naive Bayes": GaussianNB(),
        "XGBoost": XGBClassifier(
            random_state=42,
            eval_metric="logloss"
        ),
    }

    results = []
    best_model = None
    best_name = None
    best_score = 0

    for name, model in models.items():

        print(f"Training {name}...")

        model.fit(X_train, y_train)

        metrics = evaluate(model, X_test, y_test)

        results.append([
            name,
            round(metrics["Accuracy"], 4),
            round(metrics["Precision"], 4),
            round(metrics["Recall"], 4),
            round(metrics["F1"], 4),
            round(metrics["ROC-AUC"], 4),
        ])

        if metrics["ROC-AUC"] > best_score:
            best_score = metrics["ROC-AUC"]
            best_model = model
            best_name = name

    print("\nModel Comparison\n")

    print(
        tabulate(
            results,
            headers=[
                "Model",
                "Accuracy",
                "Precision",
                "Recall",
                "F1",
                "ROC-AUC",
            ],
            tablefmt="grid",
        )
    )

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)

    print("\nBest Model :", best_name)
    print(f"ROC-AUC    : {best_score:.4f}")
    print(f"Saved to   : {MODEL_PATH}")


if __name__ == "__main__":
    train_models()