# Beginner Lab — Air Quality Monitor

## Overview
A simple Flask application deployed on Google Cloud Run that serves
Air Quality Index (AQI) data for major US cities.

## Endpoints
| Endpoint | Description |
|---|---|
| `/` | Home page |
| `/health` | Health check |
| `/aqi` | AQI for all cities |
| `/aqi/<city>` | AQI for a specific city |

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```

## Docker
```bash
docker build -t air-quality-beginner .
docker run -p 8080:8080 air-quality-beginner
```

## Deploy to Cloud Run
```bash
docker build -t gcr.io/YOUR_PROJECT_ID/air-quality-beginner .
gcloud auth configure-docker
docker push gcr.io/YOUR_PROJECT_ID/air-quality-beginner

gcloud run deploy air-quality-beginner \
  --image gcr.io/YOUR_PROJECT_ID/air-quality-beginner \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```