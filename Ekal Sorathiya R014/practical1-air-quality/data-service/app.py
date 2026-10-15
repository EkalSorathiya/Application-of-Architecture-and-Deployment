from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def health():
    return jsonify({"status": "healthy", "service": "air-data"})

@app.get("/reading")
def reading():
    # Demonstration values only; these are not live or official sensor readings.
    return jsonify({
        "station": "Central Ward",
        "pm25_ug_m3": 34,
        "pm10_ug_m3": 61,
        "aqi_category": "Moderate",
        "source": "Demo sensor payload"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
