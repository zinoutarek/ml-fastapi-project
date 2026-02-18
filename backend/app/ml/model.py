import numpy as np

def predict(data):
    x = np.array(data)
    result = x.mean()
    return {"prediction": float(result)}