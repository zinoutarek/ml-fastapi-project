"""
ML API Usage Examples in Python

Usage:
    python examples_ml_api.py

Make sure the API is running:
    fastapi run backend/app/main.py
"""

import json
import time

import httpx


BASE_URL = "http://localhost:8000/api/v1/predict"


def print_header(title: str) -> None:
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def example_basic_prediction() -> None:
    """Example 1: Basic prediction."""
    print_header("Example 1: Basic Prediction")

    data = {"data": [0.1, 0.2, 0.3, 0.4, 0.5]}
    print(f"Input: {data['data']}")

    with httpx.Client() as client:
        response = client.post(BASE_URL, json=data)
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(result, indent=2)}")


def example_all_zeros() -> None:
    """Example 2: All zeros prediction."""
    print_header("Example 2: All Zeros Prediction")

    data = {"data": [0.0, 0.0, 0.0, 0.0, 0.0]}
    print(f"Input: {data['data']}")

    with httpx.Client() as client:
        response = client.post(BASE_URL, json=data)
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(result, indent=2)}")


def example_negative_values() -> None:
    """Example 3: Negative values prediction."""
    print_header("Example 3: Negative Values Prediction")

    data = {"data": [-1.0, -2.0, -3.0, -4.0, -5.0]}
    print(f"Input: {data['data']}")

    with httpx.Client() as client:
        response = client.post(BASE_URL, json=data)
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(result, indent=2)}")


def example_large_values() -> None:
    """Example 4: Large values prediction."""
    print_header("Example 4: Large Values Prediction")

    data = {"data": [10.0, 20.0, 30.0, 40.0, 50.0]}
    print(f"Input: {data['data']}")

    with httpx.Client() as client:
        response = client.post(BASE_URL, json=data)
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(result, indent=2)}")


def example_health_check() -> None:
    """Example 5: Health check."""
    print_header("Example 5: Health Check")

    with httpx.Client() as client:
        response = client.get(f"{BASE_URL.rsplit('/', 1)[0]}/health")
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(result, indent=2)}")


def example_invalid_input() -> None:
    """Example 6: Invalid input (wrong number of features)."""
    print_header("Example 6: Invalid Input (should fail with 400)")

    data = {"data": [0.1, 0.2, 0.3]}  # Only 3 features, needs 5
    print(f"Input: {data['data']} (only 3 features, needs 5)")

    with httpx.Client() as client:
        response = client.post(BASE_URL, json=data)
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(result, indent=2)}")


def example_performance_test() -> None:
    """Example 7: Performance test with multiple predictions."""
    print_header("Example 7: Performance Test (10 predictions)")

    latencies = []

    with httpx.Client() as client:
        for i in range(1, 11):
            value = i / 10.0
            data = {"data": [value, value, value, value, value]}

            response = client.post(BASE_URL, json=data)
            result = response.json()
            latencies.append(result["latency_ms"])

            print(
                f"Prediction {i:2d}: {result['prediction']:8.4f} "
                f"(latency: {result['latency_ms']:.4f}ms)"
            )

    print(f"\nLatency Statistics:")
    print(f"  Min:    {min(latencies):.4f}ms")
    print(f"  Avg:    {sum(latencies)/len(latencies):.4f}ms")
    print(f"  Max:    {max(latencies):.4f}ms")


def example_batch_test() -> None:
    """Example 8: Batch prediction test."""
    print_header("Example 8: Batch Predictions (Different Scenarios)")

    test_cases = [
        ("Zeros", [0.0, 0.0, 0.0, 0.0, 0.0]),
        ("Ones", [1.0, 1.0, 1.0, 1.0, 1.0]),
        ("Incremental", [0.2, 0.4, 0.6, 0.8, 1.0]),
        ("Decremental", [1.0, 0.8, 0.6, 0.4, 0.2]),
        ("Mixed", [0.5, -0.5, 1.5, -1.5, 0.75]),
    ]

    with httpx.Client() as client:
        for label, values in test_cases:
            data = {"data": values}
            response = client.post(BASE_URL, json=data)
            result = response.json()

            print(
                f"{label:15} -> prediction={result['prediction']:8.4f}, "
                f"latency={result['latency_ms']:.4f}ms"
            )


def main() -> None:
    """Run all examples."""
    print("\n" + "="*60)
    print("  ML API Usage Examples")
    print("="*60)
    print("\nMake sure the API is running:")
    print("  fastapi run backend/app/main.py")

    try:
        example_basic_prediction()
        example_all_zeros()
        example_negative_values()
        example_large_values()
        example_health_check()
        example_invalid_input()
        example_performance_test()
        example_batch_test()

        print_header("All Examples Complete ✓")

    except httpx.ConnectError:
        print(
            "\n❌ Error: Could not connect to API."
            "\n\nMake sure to run the API first:"
            "\n  fastapi run backend/app/main.py"
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
