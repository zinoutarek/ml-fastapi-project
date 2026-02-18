"""API v1 router configuration."""

from fastapi import APIRouter

from app.api.api_v1.endpoints.predict import router as predict_router

api_router = APIRouter()

# Include ML prediction endpoints
api_router.include_router(
    predict_router,
    prefix="/predict",
    tags=["ml"],
)

__all__ = ["api_router"]
