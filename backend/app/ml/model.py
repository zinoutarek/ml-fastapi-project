import os
import time
from pathlib import Path

import numpy as np
import onnxruntime as ort
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType


class MLModel:
    """ML Model wrapper with ONNX support and latency measurement."""

    def __init__(self):
        self.model_path = Path(__file__).parent / "model.onnx"
        self.scaler_path = Path(__file__).parent / "scaler.npy"
        self.session = None
        self.scaler = None
        self._load_or_train_model()

    def _load_or_train_model(self):
        """Load model from ONNX or train and save if not exists."""
        if self.model_path.exists() and self.scaler_path.exists():
            self._load_model()
        else:
            self._train_and_save_model()

    def _train_and_save_model(self):
        """Train a Random Forest model and save to ONNX format."""
        # Generate synthetic training data
        np.random.seed(42)
        X_train = np.random.randn(1000, 5).astype(np.float32)
        y_train = (
            2 * X_train[:, 0]
            + 3 * X_train[:, 1]
            - X_train[:, 2]
            + 0.5 * X_train[:, 3]
            + np.random.randn(1000) * 0.1
        )

        # Train scaler
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train).astype(np.float32)

        # Train Random Forest model
        model = RandomForestRegressor(
            n_estimators=50,
            max_depth=10,
            random_state=42,
            n_jobs=-1,
        )
        model.fit(X_train_scaled, y_train)

        # Convert to ONNX
        initial_type = [("float_input", FloatTensorType([None, 5]))]
        onnx_model = convert_sklearn(model, initial_types=initial_type)

        # Save ONNX model and scaler
        with open(self.model_path, "wb") as f:
            f.write(onnx_model.SerializeToString())

        np.save(self.scaler_path, [self.scaler.mean_, self.scaler.scale_])

        # Load the model
        self._load_model()

    def _load_model(self):
        """Load ONNX model and scaler from disk."""
        self.session = ort.InferenceSession(
            str(self.model_path),
            providers=["CPUExecutionProvider"],
        )

        scaler_data = np.load(self.scaler_path, allow_pickle=True)
        self.scaler = StandardScaler()
        self.scaler.mean_ = scaler_data[0]
        self.scaler.scale_ = scaler_data[1]

    def predict(self, data: list[float]) -> dict:
        """
        Make prediction on input data.

        Args:
            data: List of 5 float values

        Returns:
            Dictionary with prediction and latency info
        """
        start_time = time.time()

        # Validate input
        if len(data) != 5:
            raise ValueError(f"Expected 5 features, got {len(data)}")

        # Prepare input
        X = np.array(data, dtype=np.float32).reshape(1, -1)

        # Scale features
        X_scaled = self.scaler.transform(X).astype(np.float32)

        # Run inference
        inference_start = time.time()
        input_name = self.session.get_inputs()[0].name
        output_name = self.session.get_outputs()[0].name
        prediction = self.session.run(
            [output_name],
            {input_name: X_scaled},
        )
        inference_time = (time.time() - inference_start) * 1000  # ms

        # Total time
        total_time = (time.time() - start_time) * 1000  # ms

        return {
            "prediction": float(prediction[0][0]),
            "latency_ms": round(inference_time, 4),
            "total_time_ms": round(total_time, 4),
            "model_format": "ONNX",
            "features_count": 5,
        }


# Initialize model on module load
_model_instance = None


def get_model() -> MLModel:
    """Get or create model instance (singleton)."""
    global _model_instance
    if _model_instance is None:
        _model_instance = MLModel()
    return _model_instance


def predict(data: list[float]) -> dict:
    """Convenience function to make predictions."""
    model = get_model()
    return model.predict(data)