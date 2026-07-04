from fastapi import APIRouter, HTTPException, Request, status

from app.schemas.metadata import HealthResponse, MetadataResponse, MetricsResponse, ModelInfoResponse
from app.schemas.prediction import CustomerPayload, PredictionResponse

router = APIRouter()


def get_model_service(request: Request):
    return request.app.state.model_service


@router.get("/")
def root():
    return {
        "message": "Telco Customer Churn API",
        "docs": "/docs",
        "health": "/health",
    }


@router.get("/health", response_model=HealthResponse)
def health(request: Request):
    return get_model_service(request).health()


@router.get("/metrics", response_model=MetricsResponse)
def metrics(request: Request):
    return get_model_service(request).metrics()


@router.get("/model-info", response_model=ModelInfoResponse)
def model_info(request: Request):
    return get_model_service(request).model_info()


@router.get("/sample-payload")
def sample_payload(request: Request):
    return get_model_service(request).sample_payload()


@router.get("/metadata", response_model=MetadataResponse)
def metadata(request: Request):
    service = get_model_service(request)
    return {
        "health": service.health(),
        "metrics": service.metrics(),
        "model_info": service.model_info(),
    }


@router.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerPayload, request: Request):
    try:
        return get_model_service(request).predict(customer)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
