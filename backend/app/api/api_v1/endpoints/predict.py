from typing import Any

from fastapi import APIRouter, HTTPException

from app.ml.model import predict, get_model

router = APIRouter()


@router.post("/predict")
def predict_endpoint(data: list[float]) -> dict[str, Any]:
    """
    Make a prediction using the ML model with latency measurement.
    
    Expects exactly 5 float features.
    
    Args:
        data: List of 5 float values
        
    Returns:
        Dictionary containing:
        - prediction: The model's prediction
        - latency_ms: Inference time in milliseconds
        - total_time_ms: Total request processing time
        - model_format: "ONNX"
        - features_count: Number of input features
        
    Raises:
        HTTPException: If input validation fails
    """
    try:
        result = predict(data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
def health_check() -> dict[str, Any]:
    """Check if ML model is loaded and healthy."""
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

