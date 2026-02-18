"""
Example API usage for the ML prediction endpoint.

This demonstrates how to integrate the ML model with FastAPI.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.ml.model import predict


app = FastAPI(
    title="ML Prediction API",
    description="Production ML inference with ONNX and latency measurement",
    version="1.0.0",
)


class PredictionRequest(BaseModel):
    """Request model for predictions."""

    data: list[float] = Field(
        ...,
        description="List of exactly 5 float features",
        example=[0.1, 0.2, 0.3, 0.4, 0.5],
        min_items=5,
        max_items=5,
    )


class PredictionResponse(BaseModel):
    """Response model for predictions."""

    prediction: float = Field(description="The model's prediction")
    latency_ms: float = Field(description="Model inference latency in milliseconds")
    total_time_ms: float = Field(
        description="Total request processing time in milliseconds"
    )
    model_format: str = Field(description="Model format (ONNX)")
    features_count: int = Field(description="Number of input features")


@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Make a prediction",
    tags=["Predictions"],
)
async def predict_endpoint(request: PredictionRequest) -> PredictionResponse:
    """
    Make a prediction using the ML model.

    The model expects exactly 5 normalized float features.

    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/predict" \\
        -H "Content-Type: application/json" \\
        -d '{"data": [0.1, 0.2, 0.3, 0.4, 0.5]}'
    ```

    **Response:**
    ```json
    {
        "prediction": 0.7212,
        "latency_ms": 0.0001,
        "total_time_ms": 1.97,
        "model_format": "ONNX",
        "features_count": 5
    }
    ```
    """
    result = predict(request.data)
    return PredictionResponse(**result)


@app.get(
    "/health",
    summary="Health check",
    tags=["Health"],
)
async def health_check():
    """Check if ML model is loaded and healthy."""
    from app.ml.model import get_model

    try:
        model = get_model()
        return {
            "status": "healthy",
            "model_loaded": model.session is not None,
            "model_format": "ONNX",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "model_loaded": False,
            "error": str(e),
        }


@app.get("/", tags=["Info"])
async def root():
    """API information."""
    return {
        "name": "ML Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "docs": "/docs",
        },
    }
