import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str
    api_version: str
    model_name: str
    model_algorithm: str
    model_version: str
    environment: str
    cors_origin_regex: str
    backend_dir: Path
    model_path: Path
    model_metrics_path: Path
    model_info_path: Path
    data_path: Path


@lru_cache
def get_settings() -> Settings:
    backend_dir = Path(__file__).resolve().parents[2]

    return Settings(
        app_name=os.getenv("APP_NAME", "Telco Customer Churn API"),
        api_version=os.getenv("API_VERSION", "1.1.0"),
        model_name=os.getenv("MODEL_NAME", "Telco Customer Churn Classifier"),
        model_algorithm=os.getenv("MODEL_ALGORITHM", "XGBoostClassifier"),
        model_version=os.getenv("MODEL_VERSION", "local"),
        environment=os.getenv("APP_ENV", "development"),
        cors_origin_regex=os.getenv(
            "CORS_ORIGIN_REGEX",
            r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
        ),
        backend_dir=backend_dir,
        model_path=backend_dir / "artifacts" / "model.pkl",
        model_metrics_path=backend_dir / "artifacts" / "model_metrics.json",
        model_info_path=backend_dir / "artifacts" / "model_info.json",
        data_path=backend_dir / "data" / "processed" / "cleaned_telco.csv",
    )
