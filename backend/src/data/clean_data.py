"""
Telco Customer Churn - Data Cleaning

Dataset:
- Rows: 7043
- Columns: 21

Target Distribution:
- No  : 5174
- Yes : 1869

Cleaning Steps:
- Remove customerID
- Convert TotalCharges to numeric
- Replace invalid values with the median
- Save cleaned dataset
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "telco_customer_churn.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_telco.csv"


def clean_data():
    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Original Shape: {df.shape}")

    df = df.drop(columns=["customerID"])

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    missing = df["TotalCharges"].isna().sum()
    print(f"Missing TotalCharges: {missing}")

    median = df["TotalCharges"].median()
    df["TotalCharges"] = df["TotalCharges"].fillna(median)

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print(f"Saved cleaned dataset to {PROCESSED_DATA_PATH}")
    print(f"Final Shape: {df.shape}")


if __name__ == "__main__":
    clean_data()
