import pandas as pd

from src.features.build_features import create_preprocessor
from src.models.predict import predict


def test_preprocessing_pipeline_transforms_features():
    frame = pd.DataFrame(
        [
            {
                "gender": "Female",
                "SeniorCitizen": 0,
                "tenure": 12,
                "MonthlyCharges": 79.85,
                "TotalCharges": 950.25,
                "Contract": "Month-to-month",
            }
        ]
    )

    preprocessor = create_preprocessor(frame)
    transformed = preprocessor.fit_transform(frame)

    assert transformed.shape[0] == 1
    assert transformed.shape[1] >= frame.shape[1]


def test_prediction_probability_between_zero_and_one():
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

    _, probabilities = predict(sample)

    assert 0 <= probabilities[0] <= 1
