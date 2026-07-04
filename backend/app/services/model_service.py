import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic
from typing import Any

import joblib
import pandas as pd

from app.core.config import Settings
from app.schemas.metadata import HealthResponse, MetricsResponse, ModelInfoResponse
from app.schemas.prediction import CustomerPayload

logger = logging.getLogger(__name__)

SAMPLE_PAYLOAD = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "No",
    "Dependents": "No",
    "tenure": 8,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 84.85,
    "TotalCharges": 678.8,
}


class ModelService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.started_at = monotonic()
        self.pipeline: Any | None = None
        self.load_error: str | None = None
        self.load_model()

    def load_model(self) -> None:
        if not self.settings.model_path.exists():
            self.load_error = f"Model artifact not found at {self.settings.model_path}"
            logger.warning(self.load_error)
            return

        try:
            self.pipeline = joblib.load(self.settings.model_path)
            self.load_error = None
            logger.info("Loaded model artifact from %s", self.settings.model_path)
        except Exception as exc:  # pragma: no cover - defensive startup path
            self.pipeline = None
            self.load_error = str(exc)
            logger.exception("Failed to load model artifact")

    @property
    def model_loaded(self) -> bool:
        return self.pipeline is not None

    def health(self) -> HealthResponse:
        return HealthResponse(
            status="healthy" if self.model_loaded else "degraded",
            model_loaded=self.model_loaded,
            api_version=self.settings.api_version,
            uptime=f"{monotonic() - self.started_at:.0f}s",
            timestamp=datetime.now(UTC).isoformat(),
        )

    def metrics(self) -> MetricsResponse:
        artifact = self._load_json(self.settings.model_metrics_path)
        if not artifact:
            return MetricsResponse()

        return MetricsResponse(
            accuracy=artifact.get("accuracy"),
            precision=artifact.get("precision"),
            recall=artifact.get("recall"),
            f1=artifact.get("f1"),
            roc_auc=artifact.get("roc_auc"),
        )

    def model_info(self) -> ModelInfoResponse:
        artifact = self._load_json(self.settings.model_info_path) or {}

        return ModelInfoResponse(
            model_name=artifact.get("model_name", self.settings.model_name),
            algorithm=artifact.get("algorithm", self.settings.model_algorithm),
            version=artifact.get("version", self.settings.model_version),
            feature_count=artifact.get("feature_count", self._infer_feature_count()),
            training_timestamp=artifact.get("training_timestamp"),
            artifact_path=str(self.settings.model_path),
        )

    def sample_payload(self) -> dict[str, Any]:
        return SAMPLE_PAYLOAD

    def predict(self, payload: CustomerPayload) -> dict[str, Any]:
        if self.pipeline is None:
            raise RuntimeError(self.load_error or "Model is not loaded")

        frame = pd.DataFrame([payload.model_dump()])
        prediction = int(self.pipeline.predict(frame)[0])
        probability = float(self.pipeline.predict_proba(frame)[0][1])
        confidence = probability if prediction == 1 else 1 - probability
        risk_level = self._risk_level(probability)

        return {
            "prediction": "Yes" if prediction else "No",
            "probability": round(probability, 4),
            "risk_level": risk_level,
            "confidence": round(confidence, 4),
            "recommendation": self._recommendation(risk_level),
        }

    def _infer_feature_count(self) -> int | None:
        if not self.settings.data_path.exists():
            return None

        try:
            columns = pd.read_csv(self.settings.data_path, nrows=1).columns
            return len([column for column in columns if column != "Churn"])
        except Exception:
            logger.exception("Unable to infer feature count")
            return None

    @staticmethod
    def _risk_level(probability: float) -> str:
        if probability >= 0.7:
            return "High"
        if probability >= 0.4:
            return "Medium"
        return "Low"

    @staticmethod
    def _recommendation(risk_level: str) -> str:
        recommendations = {
            "High": "Prioritize immediate retention outreach with a tailored offer.",
            "Medium": "Monitor engagement and consider proactive support follow-up.",
            "Low": "Maintain the current service experience and watch for changes.",
        }
        return recommendations[risk_level]

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None

        with path.open("r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
