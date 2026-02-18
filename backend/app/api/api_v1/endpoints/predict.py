from typing import Any

from fastapi import APIRouter

from app.ml.model import predict

router = APIRouter()


@router.post("/predict")
def predict_endpoint(data: list[float]) -> dict[str, Any]:
    """
    Make a prediction using the ML model.
    
    Args:
        data: List of floats to make prediction on
        
    Returns:
        Dictionary containing the prediction
    """
    result = predict(data)
    return result
