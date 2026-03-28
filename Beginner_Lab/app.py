from flask import Flask, jsonify
import os

app = Flask(__name__)

CITIES = {
    "New York": {"aqi": 45, "category": "Good", "main_pollutant": "PM2.5"},
    "Los Angeles": {"aqi": 102, "category": "Unhealthy for Sensitive Groups", "main_pollutant": "Ozone"},
    "Chicago": {"aqi": 58, "category": "Moderate", "main_pollutant": "PM10"},
    "Houston": {"aqi": 78, "category": "Moderate", "main_pollutant": "NO2"},
    "Boston": {"aqi": 32, "category": "Good", "main_pollutant": "PM2.5"},
}

def get_aqi_color(aqi):
    if aqi <= 50:
        return "green"
    elif aqi <= 100:
        return "yellow"
    elif aqi <= 150:
        return "orange"
    else:
        return "red"

def get_health_advice(aqi):
    if aqi <= 50:
        return "Air quality is good. Enjoy outdoor activities."
    elif aqi <= 100:
        return "Acceptable. Sensitive people should limit outdoor exertion."
    elif aqi <= 150:
        return "Sensitive groups may experience effects. Reduce outdoor activity."
    else:
        return "Everyone may experience health effects. Avoid outdoors."

@app.route("/")
def home():
    return """
    <html>
    <head><title>Air Quality Monitor</title></head>
    <body style="font-family: Arial; max-width: 700px; margin: 40px auto; padding: 20px;">
        <h1>🌍 Air Quality Monitor</h1>
        <p>Welcome to the Air Quality Monitoring Service.</p>
        <h2>Available Endpoints:</h2>
        <ul>
            <li><a href="/aqi">/aqi</a> — Get AQI for all cities</li>
            <li><a href="/aqi/Boston">/aqi/Boston</a> — Get AQI for a specific city</li>
            <li><a href="/health">/health</a> — Health check</li>
        </ul>
    </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "air-quality-monitor"}), 200

@app.route("/aqi")
def get_all_aqi():
    result = []
    for city, data in CITIES.items():
        result.append({
            "city": city,
            "aqi": data["aqi"],
            "category": data["category"],
            "main_pollutant": data["main_pollutant"],
            "color": get_aqi_color(data["aqi"])
        })
    return jsonify({
        "source": "Air Quality Monitor",
        "total_cities": len(result),
        "data": result
    })

@app.route("/aqi/<city>")
def get_city_aqi(city):
    city_title = city.title()
    if city_title not in CITIES:
        return jsonify({
            "error": f"City '{city_title}' not found.",
            "available_cities": list(CITIES.keys())
        }), 404
    data = CITIES[city_title]
    return jsonify({
        "city": city_title,
        "aqi": data["aqi"],
        "category": data["category"],
        "main_pollutant": data["main_pollutant"],
        "color": get_aqi_color(data["aqi"]),
        "health_advice": get_health_advice(data["aqi"])
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)