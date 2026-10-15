from flask import Flask, jsonify
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.get("/")
def health():
    return jsonify({"status": "healthy", "service": "air-gateway"})

@app.get("/api/reading")
def aggregate():
    try:
        # Use Kubernetes Service DNS, never a Pod IP.
        with urlopen("http://air-data-svc:5000/reading", timeout=4) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return jsonify({
            "gateway": "air-quality-aggregator",
            "service_discovery": "success",
            "reading": payload
        })
    except Exception as exc:
        return jsonify({
            "gateway": "air-quality-aggregator",
            "service_discovery": "failed",
            "error": str(exc)
        }), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
