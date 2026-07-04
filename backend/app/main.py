import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.services.model_service import ModelService

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model_service = ModelService(settings)
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown complete")


app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://telcochurn-mlops.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging(request: Request, call_next):
    started_at = time.perf_counter()

    response = await call_next(request)

    duration_ms = (time.perf_counter() - started_at) * 1000

    logger.info(
        "%s %s -> %s %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled error for %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_server_error",
                "message": "An unexpected error occurred.",
            }
        },
    )


app.include_router(router)