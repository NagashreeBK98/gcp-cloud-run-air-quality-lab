from flask import Flask, jsonify, request
from google.cloud import storage, bigquery
import os
import json
import datetime

app = Flask(__name__)


def get_aqi_category(aqi):
    if aqi is None:
        return "Unknown"
    aqi = float(aqi)
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


def get_health_recommendation(aqi):
    if aqi is None:
        return "No data available."
    aqi = float(aqi)
    if aqi <= 50:
        return "Air quality is satisfactory. Enjoy outdoor activities."
    elif aqi <= 100:
        return "Acceptable. Sensitive individuals should limit prolonged outdoor exertion."
    elif aqi <= 150:
        return "Sensitive groups should reduce outdoor activity."
    elif aqi <= 200:
        return "Everyone may experience health effects. Reduce outdoor exertion."
    elif aqi <= 300:
        return "Health alert: everyone may experience serious health effects."
    else:
        return "Health emergency. Stay indoors."


@app.route("/")
def home():
    return """
    <html>
    <head><title>Air Quality Monitoring API</title></head>
    <body style="font-family: Arial, sans-serif; max-width: 750px; margin: 40px auto; padding: 20px;">
        <h1>🌍 Air Quality Monitoring API</h1>
        <p>Intermediate Cloud Run lab integrating BigQuery and Cloud Storage
        for real-time US air quality insights.</p>
        <h2>Endpoints</h2>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:100%;">
            <tr style="background:#f0f0f0;">
                <th>Endpoint</th><th>Description</th>
            </tr>
            <tr><td><a href="/health">/health</a></td><td>Service health check</td></tr>
            <tr><td><a href="/aqi/state/CA">/aqi/state/&lt;state&gt;</a></td><td>Top polluted counties in a US state</td></tr>
            <tr><td><a href="/aqi/worst">/aqi/worst</a></td><td>Top 10 worst air quality counties nationally</td></tr>
            <tr><td><a href="/aqi/summary">/aqi/summary</a></td><td>National AQI summary by state</td></tr>
            <tr><td>/aqi/export/&lt;state&gt;</td><td>Export state report to Cloud Storage</td></tr>
        </table>
        <h2>Example Calls</h2>
        <ul>
            <li><a href="/aqi/state/CA">/aqi/state/CA</a></li>
            <li><a href="/aqi/state/TX">/aqi/state/TX</a></li>
            <li><a href="/aqi/worst">/aqi/worst</a></li>
            <li><a href="/aqi/summary">/aqi/summary</a></li>
        </ul>
    </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "air-quality-monitoring-api",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route("/aqi/state/<state_code>")
def aqi_by_state(state_code):
    state_code = state_code.upper()
    limit = request.args.get("limit", 10, type=int)
    try:
        client = bigquery.Client()
        query = """
            SELECT
                county_name,
                state_name,
                ROUND(AVG(aqi), 2)  AS avg_aqi,
                MAX(aqi)            AS max_aqi,
                MIN(aqi)            AS min_aqi,
                COUNT(*)            AS record_count
            FROM `bigquery-public-data.epa_historical_air_quality.daily_aqi_by_county`
            WHERE state_abbr = @state_code
              AND EXTRACT(YEAR FROM date_local) = 2023
            GROUP BY county_name, state_name
            ORDER BY avg_aqi DESC
            LIMIT @limit
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("state_code", "STRING", state_code),
                bigquery.ScalarQueryParameter("limit", "INT64", limit),
            ]
        )
        results = client.query(query, job_config=job_config, location="US").result()
        rows = list(results)

        if not rows:
            return jsonify({
                "error": f"No data found for state '{state_code}'.",
                "tip": "Use a valid US state abbreviation e.g. CA, TX, NY"
            }), 404

        counties = []
        for row in rows:
            counties.append({
                "county": row.county_name,
                "state": row.state_name,
                "avg_aqi": row.avg_aqi,
                "max_aqi": row.max_aqi,
                "min_aqi": row.min_aqi,
                "record_count": row.record_count,
                "category": get_aqi_category(row.avg_aqi),
                "health_recommendation": get_health_recommendation(row.avg_aqi)
            })

        return jsonify({
            "state": state_code,
            "year": 2023,
            "total_counties": len(counties),
            "source": "EPA Historical Air Quality — BigQuery Public Dataset",
            "data": counties
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/aqi/worst")
def aqi_worst():
    try:
        client = bigquery.Client()
        query = """
            SELECT
                county_name,
                state_name,
                state_abbr,
                ROUND(AVG(aqi), 2) AS avg_aqi,
                MAX(aqi)           AS max_aqi,
                COUNT(*)           AS record_count
            FROM `bigquery-public-data.epa_historical_air_quality.daily_aqi_by_county`
            WHERE EXTRACT(YEAR FROM date_local) = 2023
            GROUP BY county_name, state_name, state_abbr
            ORDER BY avg_aqi DESC
            LIMIT 10
        """
        results = client.query(query, location="US").result()
        counties = []
        for row in results:
            counties.append({
                "rank": len(counties) + 1,
                "county": row.county_name,
                "state": row.state_name,
                "state_abbr": row.state_abbr,
                "avg_aqi": row.avg_aqi,
                "max_aqi": row.max_aqi,
                "record_count": row.record_count,
                "category": get_aqi_category(row.avg_aqi),
                "health_recommendation": get_health_recommendation(row.avg_aqi)
            })
        return jsonify({
            "title": "Top 10 Worst Air Quality Counties — USA 2023",
            "source": "EPA Historical Air Quality — BigQuery Public Dataset",
            "data": counties
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/aqi/summary")
def aqi_summary():
    try:
        client = bigquery.Client()
        query = """
            SELECT
                state_name,
                state_abbr,
                ROUND(AVG(aqi), 2)  AS avg_aqi,
                MAX(aqi)            AS max_aqi,
                MIN(aqi)            AS min_aqi,
                COUNT(*)            AS total_records,
                COUNTIF(aqi > 100)  AS unhealthy_days
            FROM `bigquery-public-data.epa_historical_air_quality.daily_aqi_by_county`
            WHERE EXTRACT(YEAR FROM date_local) = 2023
            GROUP BY state_name, state_abbr
            ORDER BY avg_aqi DESC
            LIMIT 20
        """
        results = client.query(query, location="US").result()
        states = []
        for row in results:
            states.append({
                "state": row.state_name,
                "state_abbr": row.state_abbr,
                "avg_aqi": row.avg_aqi,
                "max_aqi": row.max_aqi,
                "min_aqi": row.min_aqi,
                "total_records": row.total_records,
                "unhealthy_days": row.unhealthy_days,
                "category": get_aqi_category(row.avg_aqi)
            })
        return jsonify({
            "title": "National AQI Summary by State — 2023",
            "source": "EPA Historical Air Quality — BigQuery Public Dataset",
            "total_states": len(states),
            "data": states
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/aqi/export/<state_code>")
def export_state_report(state_code):
    state_code = state_code.upper()
    bucket_name = os.environ.get("BUCKET_NAME")
    if not bucket_name:
        return jsonify({"error": "BUCKET_NAME environment variable is not set."}), 500
    try:
        bq_client = bigquery.Client()
        query = """
            SELECT
                county_name,
                state_name,
                ROUND(AVG(aqi), 2) AS avg_aqi,
                MAX(aqi)           AS max_aqi,
                MIN(aqi)           AS min_aqi,
                COUNT(*)           AS record_count
            FROM `bigquery-public-data.epa_historical_air_quality.daily_aqi_by_county`
            WHERE state_abbr = @state_code
              AND EXTRACT(YEAR FROM date_local) = 2023
            GROUP BY county_name, state_name
            ORDER BY avg_aqi DESC
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("state_code", "STRING", state_code),
            ]
        )
        results = bq_client.query(query, job_config=job_config, location="US").result()
        rows = list(results)

        if not rows:
            return jsonify({"error": f"No data found for state '{state_code}'."}), 404

        report = {
            "state": state_code,
            "year": 2023,
            "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
            "source": "EPA Historical Air Quality — BigQuery Public Dataset",
            "total_counties": len(rows),
            "data": [
                {
                    "county": row.county_name,
                    "state": row.state_name,
                    "avg_aqi": row.avg_aqi,
                    "max_aqi": row.max_aqi,
                    "min_aqi": row.min_aqi,
                    "record_count": row.record_count,
                    "category": get_aqi_category(row.avg_aqi)
                }
                for row in rows
            ]
        }

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        filename = f"aqi-reports/{state_code}_aqi_report_2023.json"
        blob = bucket.blob(filename)
        blob.upload_from_string(
            json.dumps(report, indent=2),
            content_type="application/json"
        )

        return jsonify({
            "message": f"Report for '{state_code}' exported successfully.",
            "bucket": bucket_name,
            "file": filename,
            "total_counties": len(rows)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)