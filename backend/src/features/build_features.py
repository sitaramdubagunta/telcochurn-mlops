"""
Telco Customer Churn - Feature Engineering

Steps:
- Load cleaned dataset
- Encode target variable
- One-hot encode categorical features
- Split data into train and test sets
"""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

INPUT_PATH = Path("./data/processed/cleaned_telco.csv")


def build_features():
    df = pd.read_csv(INPUT_PATH)

    df["Churn"] = df["Churn"].map({
        "No": 0,
        "Yes": 1
    })

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    X = pd.get_dummies(
        X,
        drop_first=True,
        dtype=int
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("=" * 50)
    print("Feature Engineering Complete")
    print("=" * 50)
    print(f"Training Samples : {X_train.shape[0]}")
    print(f"Testing Samples  : {X_test.shape[0]}")
    print(f"Number of Features : {X_train.shape[1]}")

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    build_features()