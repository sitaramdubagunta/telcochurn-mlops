from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

app = FastAPI(
    title="Telco Customer Churn API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = Path("./artifacts/model.pkl")
DATA_PATH = Path("./data/processed/cleaned_telco.csv")

pipeline = joblib.load(MODEL_PATH)


def load_dataset():
    df = pd.read_csv(DATA_PATH)

    if "customerID" in df.columns:
        df = df.drop(columns="customerID")

    df["Churn"] = df["Churn"].map({"No": 0, "Yes": 1}).astype(int)

    X = df.drop(columns="Churn")
    y = df["Churn"]

    return train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42,
    )


def build_model_metrics():
    _, X_test, _, y_test = load_dataset()

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    return {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions)), 4),
        "recall": round(float(recall_score(y_test, predictions)), 4),
        "f1": round(float(f1_score(y_test, predictions)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
    }


MODEL_METRICS = build_model_metrics()


class Customer(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/")
def root():
    return {"message": "Telco Customer Churn API"}


@app.post("/predict")
def predict(customer: Customer):

    df = pd.DataFrame([customer.model_dump()])

    prediction = pipeline.predict(df)[0]
    probability = pipeline.predict_proba(df)[0][1]

    return {
        "prediction": "Yes" if prediction else "No",
        "probability": round(float(probability), 4),
        "metrics": MODEL_METRICS,
    }