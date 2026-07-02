"""
Make predictions using the trained Telco Customer Churn pipeline.
"""

from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path("./artifacts/model.pkl")


def load_pipeline():
    """
    Load the trained preprocessing and model pipeline.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at '{MODEL_PATH}'. Train the model first."
        )

    return joblib.load(MODEL_PATH)


def predict(data):
    """
    Predict customer churn.

    Parameters
    ----------
    data : pandas.DataFrame
        Raw customer data.

    Returns
    -------
    tuple
        Predicted class and probability.
    """

    pipeline = load_pipeline()

    predictions = pipeline.predict(data)
    probabilities = pipeline.predict_proba(data)[:, 1]

    return predictions, probabilities


if __name__ == "__main__":

    sample = pd.DataFrame(
        [
            {
                "gender": "Female",
                "SeniorCitizen": 0,
                "Partner": "Yes",
                "Dependents": "No",
                "tenure": 12,
                "PhoneService": "Yes",
                "MultipleLines": "No",
                "InternetService": "Fiber optic",
                "OnlineSecurity": "No",
                "OnlineBackup": "Yes",
                "DeviceProtection": "No",
                "TechSupport": "No",
                "StreamingTV": "Yes",
                "StreamingMovies": "Yes",
                "Contract": "Month-to-month",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 79.85,
                "TotalCharges": 950.25,
            }
        ]
    )

    prediction, probability = predict(sample)

    churn = "Yes" if prediction[0] == 1 else "No"

    print("=" * 50)
    print("Prediction")
    print("=" * 50)
    print(f"Churn       : {churn}")
    print(f"Probability : {probability[0]:.2%}")