#!/usr/bin/env python3
"""
Verification script for ML model production setup.
Validates all components are correctly installed and working.
"""

import json
import sys
from pathlib import Path


def check_imports() -> bool:
    """Check if all required packages are importable."""
    print("\n[1] Checking imports...")
    required_packages = {
        "numpy": "NumPy",
        "sklearn": "scikit-learn",
        "skl2onnx": "skl2onnx",
        "onnxruntime": "ONNX Runtime",
        "fastapi": "FastAPI",
        "pydantic": "Pydantic",
    }

    all_ok = True
    for module, name in required_packages.items():
        try:
            __import__(module)
            print(f"  ✓ {name:20} - OK")
        except ImportError as e:
            print(f"  ✗ {name:20} - FAILED: {e}")
            all_ok = False

    return all_ok


def check_ml_model() -> bool:
    """Check if ML model files exist."""
    print("\n[2] Checking ML model files...")
    ml_dir = Path(__file__).parent / "backend" / "app" / "ml"

    files_to_check = {
        "model.onnx": "ONNX Model",
        "scaler.npy": "Scaler Parameters",
        "model.py": "Python Module",
        "README.md": "Documentation",
    }

    all_ok = True
    for filename, description in files_to_check.items():
        filepath = ml_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"  ✓ {description:20} - {filename} ({size:,} bytes)")
        else:
            print(f"  ✗ {description:20} - {filename} NOT FOUND")
            all_ok = False

    return all_ok


def check_api_endpoints() -> bool:
    """Check if API endpoint files exist."""
    print("\n[3] Checking API endpoints...")
    api_dir = Path(__file__).parent / "backend" / "app" / "api" / "api_v1"

    files_to_check = {
        "endpoints/predict.py": "Predict Endpoint",
        "main.py": "Router Configuration",
        "__init__.py": "Package Init",
    }

    all_ok = True
    for filepath_str, description in files_to_check.items():
        filepath = api_dir / filepath_str
        if filepath.exists():
            print(f"  ✓ {description:20} - {filepath_str}")
        else:
            print(f"  ✗ {description:20} - {filepath_str} NOT FOUND")
            all_ok = False

    return all_ok


def check_tests() -> bool:
    """Check if test files exist."""
    print("\n[4] Checking tests...")
    test_file = Path(__file__).parent / "backend" / "tests" / "ml" / "test_model.py"

    if test_file.exists():
        print(f"  ✓ ML Tests                - test_model.py")
        return True
    else:
        print(f"  ✗ ML Tests                - test_model.py NOT FOUND")
        return False


def check_documentation() -> bool:
    """Check if documentation exists."""
    print("\n[5] Checking documentation...")
    docs_to_check = {
        "backend/ML_GUIDE_FR.md": "French Guide",
        "backend/app/ml/README.md": "ML README",
        "ML_SUMMARY.md": "Summary",
        "ML_CHECKLIST.md": "Checklist",
        "examples_ml_api.py": "Python Examples",
    }

    all_ok = True
    root = Path(__file__).parent
    for filepath_str, description in docs_to_check.items():
        filepath = root / filepath_str
        if filepath.exists():
            print(f"  ✓ {description:20} - {filepath_str}")
        else:
            print(f"  ✗ {description:20} - {filepath_str} NOT FOUND")
            all_ok = False

    return all_ok


def check_model_functionality() -> bool:
    """Test actual model prediction."""
    print("\n[6] Testing model functionality...")
    try:
        sys.path.insert(0, str(Path(__file__).parent / "backend"))
        from app.ml.model import predict

        result = predict([0.1, 0.2, 0.3, 0.4, 0.5])

        # Check response structure
        expected_keys = {"prediction", "latency_ms", "total_time_ms", "model_format", "features_count"}
        if set(result.keys()) == expected_keys:
            print(f"  ✓ Model prediction       - OK")
            print(f"    - Prediction: {result['prediction']:.4f}")
            print(f"    - Latency: {result['latency_ms']:.4f}ms")
            print(f"    - Model: {result['model_format']}")
            return True
        else:
            print(f"  ✗ Model response structure incorrect")
            print(f"    Expected: {expected_keys}")
            print(f"    Got: {set(result.keys())}")
            return False

    except Exception as e:
        print(f"  ✗ Model prediction       - FAILED: {e}")
        return False


def check_docker_files() -> bool:
    """Check if Docker files exist."""
    print("\n[7] Checking Docker files...")
    docker_files = {
        "backend/Dockerfile": "CPU Dockerfile",
        "backend/Dockerfile.gpu": "GPU Dockerfile",
        "backend/docker-compose.ml.yml": "Docker Compose",
    }

    all_ok = True
    root = Path(__file__).parent
    for filepath_str, description in docker_files.items():
        filepath = root / filepath_str
        if filepath.exists():
            print(f"  ✓ {description:20} - {filepath_str}")
        else:
            print(f"  ✗ {description:20} - {filepath_str} NOT FOUND")
            all_ok = False

    return all_ok


def print_summary(results: dict) -> None:
    """Print verification summary."""
    print("\n" + "="*60)
    print("  VERIFICATION SUMMARY")
    print("="*60)

    checks = [
        ("Imports", results["imports"]),
        ("ML Model Files", results["model"]),
        ("API Endpoints", results["api"]),
        ("Tests", results["tests"]),
        ("Documentation", results["docs"]),
        ("Model Functionality", results["functionality"]),
        ("Docker Support", results["docker"]),
    ]

    all_passed = True
    for check_name, passed in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {check_name:25} {status}")
        if not passed:
            all_passed = False

    print("="*60)

    if all_passed:
        print("\n✅ ALL CHECKS PASSED - ML Model is ready for production!")
    else:
        print(
            "\n⚠️  Some checks failed - Please review the output above"
        )

    return all_passed


def main() -> int:
    """Run all verification checks."""
    print("\n" + "="*60)
    print("  ML Model Production Setup Verification")
    print("="*60)

    results = {
        "imports": check_imports(),
        "model": check_ml_model(),
        "api": check_api_endpoints(),
        "tests": check_tests(),
        "docs": check_documentation(),
        "functionality": check_model_functionality(),
        "docker": check_docker_files(),
    }

    all_passed = print_summary(results)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
