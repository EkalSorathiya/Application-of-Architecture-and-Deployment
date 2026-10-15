from flask import Flask, request, jsonify, send_from_directory
from sklearn.datasets import load_wine
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("wine_model.joblib")
class_names = list(load_wine().target_names)
FEATURE_COUNT = 13

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "Wine classification API is live",
        "expected_feature_count": FEATURE_COUNT
    })

@app.post("/predict")
def predict():
    body = request.get_json(silent=True) or {}
    features = body.get("features")

    if not isinstance(features, list) or len(features) != FEATURE_COUNT:
        return jsonify({"error": f"'features' must be a list of exactly {FEATURE_COUNT} numeric values"}), 400

    try:
        row = np.asarray(features, dtype=float).reshape(1, FEATURE_COUNT)
        if not np.isfinite(row).all():
            raise ValueError("All feature values must be finite numbers")
        code = int(model.predict(row)[0])
        return jsonify({
            "status": "success",
            "input_features": features,
            "prediction_code": code,
            "predicted_class": class_names[code]
        })
    except (ValueError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
