"""Tests for ML model predictions and performance."""

import pytest

from app.ml.model import get_model, predict


def test_model_initialization():
    """Test that model loads successfully."""
    model = get_model()
    assert model is not None
    assert model.session is not None
    assert model.scaler is not None


def test_predict_valid_input():
    """Test prediction with valid input."""
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    result = predict(data)

    assert isinstance(result, dict)
    assert "prediction" in result
    assert "latency_ms" in result
    assert "total_time_ms" in result
    assert isinstance(result["prediction"], float)
    assert result["latency_ms"] > 0
    assert result["total_time_ms"] > 0
    assert result["model_format"] == "ONNX"
    assert result["features_count"] == 5


def test_predict_invalid_input_length():
    """Test prediction with invalid input length."""
    data = [1.0, 2.0, 3.0]  # Only 3 features instead of 5
    with pytest.raises(ValueError, match="Expected 5 features"):
        predict(data)


def test_predict_with_negative_values():
    """Test prediction with negative values."""
    data = [-1.0, -2.0, -3.0, -4.0, -5.0]
    result = predict(data)
    assert isinstance(result["prediction"], float)


def test_predict_with_zeros():
    """Test prediction with zero values."""
    data = [0.0, 0.0, 0.0, 0.0, 0.0]
    result = predict(data)
    assert isinstance(result["prediction"], float)


def test_model_latency():
    """Test that inference latency is reasonable (<100ms)."""
    data = [0.5, 1.5, 2.5, 3.5, 4.5]
    result = predict(data)

    # ONNX inference should be very fast
    assert result["latency_ms"] < 100, f"Latency {result['latency_ms']}ms is too high"


def test_singleton_model():
    """Test that model is loaded as singleton."""
    model1 = get_model()
    model2 = get_model()
    assert model1 is model2
