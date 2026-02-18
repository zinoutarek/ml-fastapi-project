# ML Model Documentation

## Overview

Ce projet inclut un modèle ML production-ready utilisant:
- **Framework**: scikit-learn (Random Forest Regressor)
- **Format**: ONNX (pour performance optimale)
- **Runtime**: ONNX Runtime
- **Mesure**: Latency measurement automatique

## Architecture

### 1. **Model Training & Conversion** ([backend/app/ml/model.py](../backend/app/ml/model.py))

Le modèle:
- S'entraîne automatiquement si les fichiers n'existent pas
- Utilise 1000 samples synthétiques avec 5 features
- Est converti en format ONNX pour inference rapide
- Sauvegarde les fichiers: `model.onnx` et `scaler.npy`

### 2. **Features**

```python
predict([1.0, 2.0, 3.0, 4.0, 5.0])
```

**Input**: Liste de 5 floats (features normalisées)

**Output**:
```json
{
  "prediction": 0.7212,
  "latency_ms": 0.001,
  "total_time_ms": 1.973,
  "model_format": "ONNX",
  "features_count": 5
}
```

### 3. **FastAPI Routes** ([backend/app/api/api_v1/endpoints/predict.py](../backend/app/api/api_v1/endpoints/predict.py))

**POST /api/v1/predict**
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"data": [0.1, 0.2, 0.3, 0.4, 0.5]}'
```

**GET /api/v1/health**
```bash
curl "http://localhost:8000/api/v1/health"
# {"status": "healthy", "model_loaded": true, "model_format": "ONNX"}
```

## Performance

- **Latency**: ~0.1-1ms (avec ONNX Runtime)
- **Memory**: ~50MB (modèle + dépendances)
- **Format**: ONNX (interopérable, optimisé)

## Docker Integration

Le Dockerfile inclut:
- Optimisation des couches de cache
- Compilation bytecode Python
- Pré-entrainement optionnel du modèle (ENV: PRETRAIN_MODEL)

```dockerfile
ENV PRETRAIN_MODEL=1  # Pré-entraîne le modèle au build
```

## Tests

```bash
cd backend
pytest tests/ml/test_model.py -v
```

**Test Coverage**:
- ✓ Model initialization
- ✓ Valid predictions
- ✓ Input validation
- ✓ Performance benchmarking
- ✓ Singleton pattern

## Workflow

```
1. Model initialization (train or load)
   ↓
2. Scaler normalization
   ↓
3. ONNX inference
   ↓
4. Returns prediction + metrics
```

## Installation

```bash
# Backend dependencies
pip install scikit-learn skl2onnx onnxruntime numpy

# Ou via pyproject.toml (déjà configuré)
cd backend && pip install -e .
```

## Améliorations Futures

- [ ] Grid search pour hyperparamètres
- [ ] Cross-validation
- [ ] Model versioning avec MLflow
- [ ] GPU support (CUDA)
- [ ] Batch predictions
- [ ] Model monitoring/logging
- [ ] A/B testing framework
