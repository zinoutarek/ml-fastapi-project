#!/usr/bin/env python3
"""Initialize and benchmark the ML model."""

import json
import time
from pathlib import Path

from app.ml.model import get_model, predict


def print_section(title: str) -> None:
    """Print a formatted section title."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main() -> None:
    """Initialize and test the ML model."""
    print_section("ML Model Initialization & Benchmark")

    # 1. Initialize model
    print("\n[1] Loading model...")
    start = time.time()
    model = get_model()
    init_time = (time.time() - start) * 1000

    print(f"✓ Model initialized in {init_time:.2f}ms")
    print(f"  - ONNX Session: {'✓' if model.session else '✗'}")
    print(f"  - Scaler: {'✓' if model.scaler else '✗'}")
    print(f"  - Model file: {model.model_path.exists()}")
    print(f"  - Scaler file: {model.scaler_path.exists()}")

    # 2. Test predictions
    print("\n[2] Testing predictions...")
    test_cases = [
        ([0.0, 0.0, 0.0, 0.0, 0.0], "All zeros"),
        ([1.0, 1.0, 1.0, 1.0, 1.0], "All ones"),
        ([0.5, -0.5, 1.5, -1.5, 0.75], "Mixed values"),
    ]

    for data, label in test_cases:
        result = predict(data)
        print(
            f"✓ {label:20} -> prediction={result['prediction']:.4f}, "
            f"latency={result['latency_ms']:.4f}ms"
        )

    # 3. Performance benchmark
    print("\n[3] Latency Benchmark (100 predictions)...")
    latencies = []
    for i in range(100):
        result = predict([i / 100, (100 - i) / 100, 0.5, 0.25, 0.75])
        latencies.append(result["latency_ms"])

    print(f"✓ Completed 100 predictions")
    print(f"  - Min: {min(latencies):.4f}ms")
    print(f"  - Avg: {sum(latencies)/len(latencies):.4f}ms")
    print(f"  - Max: {max(latencies):.4f}ms")

    # 4. Model info
    print("\n[4] Model Information")
    print(f"  - Format: ONNX")
    print(f"  - Framework: scikit-learn (Random Forest)")
    print(f"  - Input features: 5")
    print(f"  - Output: Float32")
    print(f"  - Estimators: 50")
    print(f"  - Max depth: 10")

    print_section("Initialization Complete ✓")

    # 5. Sample response
    print("\n[5] Sample API Response")
    sample = predict([0.1, 0.2, 0.3, 0.4, 0.5])
    print(json.dumps(sample, indent=2))


if __name__ == "__main__":
    main()
