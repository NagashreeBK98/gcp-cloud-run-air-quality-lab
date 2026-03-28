# Intermediate Lab — Air Quality Monitoring API

## Overview
A production-style Flask API deployed on Google Cloud Run that delivers
real-time US air quality insights by querying the EPA Historical Air Quality
public dataset on BigQuery and exporting reports to Cloud Storage.

## Endpoints
| Endpoint | Description |
|---|---|
| `/` | Landing page |
| `/health` | Health check |
| `/aqi/state/<state>` | Top counties by AQI in a US state |
| `/aqi/worst` | Top 10 worst counties nationally |
| `/aqi/summary` | National AQI summary by state |
| `/aqi/export/<state>` | Export state report to Cloud Storage |

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```

## Docker
```bash
docker build -t air-quality-intermediate .
docker run -p 8080:8080 air-quality-intermediate
```

## Deploy to Cloud Run
```bash
docker build -t gcr.io/YOUR_PROJECT_ID/air-quality-intermediate .
gcloud auth configure-docker
docker push gcr.io/YOUR_PROJECT_ID/air-quality-intermediate

gcloud run deploy air-quality-intermediate \
  --image gcr.io/YOUR_PROJECT_ID/air-quality-intermediate \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --update-env-vars BUCKET_NAME=YOUR_BUCKET_NAME \
  --service-account YOUR_SERVICE_ACCOUNT_EMAIL
```

## Dataset
EPA Historical Air Quality — BigQuery Public Dataset
Table: `bigquery-public-data.epa_historical_air_quality.daily_aqi_by_county`

## AQI Categories
| AQI Range | Category |
|---|---|
| 0–50 | Good |
| 51–100 | Moderate |
| 101–150 | Unhealthy for Sensitive Groups |
| 151–200 | Unhealthy |
| 201–300 | Very Unhealthy |
| 301+ | Hazardous |