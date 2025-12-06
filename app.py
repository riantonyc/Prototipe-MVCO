from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
import uvicorn

from prediction_utils import (
    models_config,
    load_model,
    normalize_input,
    predict_with_model,
    save_prediction_to_json,
    get_test_inputs
)

app = FastAPI(
    title="AI Prediction API",
    description="FastAPI backend untuk sistem prediksi multi-model",
    version="1.0.0"
)

# ==============================
# Request Model
# ==============================

class PredictionRequest(BaseModel):
    model_name: str
    inputs: Dict[str, Any]


# ==============================
# ROUTES
# ==============================

@app.get("/")
def root():
    return {
        "message": "✅ API Aktif",
        "available_models": [cfg["name"] for cfg in models_config]
    }


@app.post("/predict")
def predict(request: PredictionRequest):
    model_cfg = next((cfg for cfg in models_config if cfg["name"] == request.model_name), None)
    if not model_cfg:
        raise HTTPException(status_code=404, detail=f"Model '{request.model_name}' tidak ditemukan.")

    model, feat_order = load_model(model_cfg["file"])
    features = feat_order or model_cfg["features"]

    try:
        input_values = [normalize_input(request.inputs.get(f, 0), f) for f in features]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error input: {e}")

    prediction, prob = predict_with_model(model, input_values, features)
    save_prediction_to_json(request.model_name, features, input_values, prediction, prob)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model": request.model_name,
        "prediction": prediction,
        "probabilities": prob,
        "inputs_used": {f: request.inputs.get(f, None) for f in features}
    }


@app.get("/test/{model_name}")
def test_model(model_name: str):
    test_data = get_test_inputs()
    if model_name not in test_data:
        raise HTTPException(status_code=404, detail=f"Data test untuk '{model_name}' tidak ada.")

    model_cfg = next((cfg for cfg in models_config if cfg["name"] == model_name), None)
    if not model_cfg:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' tidak ditemukan.")

    model, feat_order = load_model(model_cfg["file"])
    features = feat_order or model_cfg["features"]

    data = test_data[model_name]
    input_values = [normalize_input(data[f], f) for f in features]
    prediction, prob = predict_with_model(model, input_values, features)
    save_prediction_to_json(model_name, features, input_values, prediction, prob)

    return {
        "model": model_name,
        "prediction": prediction,
        "probabilities": prob,
        "test_inputs": data
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
