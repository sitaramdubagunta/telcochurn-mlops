from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    api_version: str
    uptime: str
    timestamp: str


class MetricsResponse(BaseModel):
    accuracy: float | None = None
    precision: float | None = None
    recall: float | None = None
    f1: float | None = None
    roc_auc: float | None = None


class ModelInfoResponse(BaseModel):
    model_name: str
    algorithm: str
    version: str
    feature_count: int | None = None
    training_timestamp: str | None = None
    artifact_path: str


class MetadataResponse(BaseModel):
    health: HealthResponse
    metrics: MetricsResponse
    model_info: ModelInfoResponse
