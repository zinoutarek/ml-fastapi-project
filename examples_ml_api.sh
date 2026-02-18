#!/bin/bash
# ML API Usage Examples

# Make sure the API is running:
# fastapi run backend/app/main.py

BASE_URL="http://localhost:8000/api/v1/predict"

echo "================================"
echo "ML Prediction API Examples"
echo "================================"
echo

# Example 1: Basic prediction
echo "[1] Basic Prediction"
echo "Input: [0.1, 0.2, 0.3, 0.4, 0.5]"
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"data": [0.1, 0.2, 0.3, 0.4, 0.5]}' \
  -s | python -m json.tool
echo

# Example 2: All zeros
echo "[2] All Zeros Prediction"
echo "Input: [0.0, 0.0, 0.0, 0.0, 0.0]"
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"data": [0.0, 0.0, 0.0, 0.0, 0.0]}' \
  -s | python -m json.tool
echo

# Example 3: Negative values
echo "[3] Negative Values Prediction"
echo "Input: [-1.0, -2.0, -3.0, -4.0, -5.0]"
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"data": [-1.0, -2.0, -3.0, -4.0, -5.0]}' \
  -s | python -m json.tool
echo

# Example 4: Large values
echo "[4] Large Values Prediction"
echo "Input: [10.0, 20.0, 30.0, 40.0, 50.0]"
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"data": [10.0, 20.0, 30.0, 40.0, 50.0]}' \
  -s | python -m json.tool
echo

# Example 5: Health check
echo "[5] Health Check"
curl -X GET "http://localhost:8000/api/v1/predict/health" \
  -s | python -m json.tool
echo

# Example 6: Invalid input (wrong number of features)
echo "[6] Invalid Input (should fail with 400)"
echo "Input: [0.1, 0.2, 0.3] (only 3 features, needs 5)"
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"data": [0.1, 0.2, 0.3]}' \
  -s | python -m json.tool
echo

# Example 7: Performance test
echo "[7] Performance Test (10 sequential predictions)"
for i in {1..10}; do
  value=$(echo "scale=1; $i / 10" | bc)
  curl -X POST "$BASE_URL" \
    -H "Content-Type: application/json" \
    -d "{\"data\": [$value, $value, $value, $value, $value]}" \
    -s | python -c "import sys, json; data = json.load(sys.stdin); print(f'Prediction {i}: {data[\"prediction\"]:.4f} (latency: {data[\"latency_ms\"]:.4f}ms)')"
done
echo

echo "================================"
echo "Examples Complete!"
echo "================================"
