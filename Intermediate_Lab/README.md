# Intermediate Lab — Air Quality Monitoring API

## Live Demo
**Service URL:** https://air-quality-intermediate-932441309698.us-central1.run.app

| Endpoint | Live Link |
|---|---|
| Home | https://air-quality-intermediate-932441309698.us-central1.run.app/ |
| Health Check | https://air-quality-intermediate-932441309698.us-central1.run.app/health |
| California AQI | https://air-quality-intermediate-932441309698.us-central1.run.app/aqi/state/CA |
| Texas AQI | https://air-quality-intermediate-932441309698.us-central1.run.app/aqi/state/TX |
| Worst Counties | https://air-quality-intermediate-932441309698.us-central1.run.app/aqi/worst |
| National Summary | https://air-quality-intermediate-932441309698.us-central1.run.app/aqi/summary |

---

## Overview
A production-style Flask API deployed on Google Cloud Run that delivers
real-time US air quality insights by querying the EPA Historical Air Quality
public dataset on BigQuery and exporting reports to Cloud Storage.

**Modification from professor's lab:**
- Uses EPA public air quality dataset on BigQuery instead of baby names dataset
- Adds meaningful data processing — AQI categorization and health recommendations
- Exports structured JSON reports to Cloud Storage
- Includes clean HTML landing page and health check endpoint
- Uses parameterized BigQuery queries to prevent SQL injection
- Deployed with Gunicorn for production-grade serving

---

## Architecture
```
User Request
     │
     ▼
Cloud Run (Flask API)
     │
     ├──► BigQuery (EPA Air Quality Public Dataset)
     │         └── daily_aqi_by_county table
     │
     └──► Cloud Storage (JSON Report Export)
               └── aqi-reports/ folder
```

---

## Endpoints
| Endpoint | Description |
|---|---|
| `/` | Landing page |
| `/health` | Health check |
| `/aqi/state/<state>` | Top counties by AQI in a US state |
| `/aqi/worst` | Top 10 worst counties nationally |
| `/aqi/summary` | National AQI summary by state |
| `/aqi/export/<state>` | Export state report to Cloud Storage |

---

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```

Then open: http://localhost:8080

---

## Docker
```bash
docker build -t air-quality-intermediate .
docker run -p 8080:8080 air-quality-intermediate
```

---

## Deploy to Cloud Run
```bash
# Build and push image
docker build -t gcr.io/YOUR_PROJECT_ID/air-quality-intermediate .
gcloud auth configure-docker
docker push gcr.io/YOUR_PROJECT_ID/air-quality-intermediate

# Deploy
gcloud run deploy air-quality-intermediate \
  --image gcr.io/YOUR_PROJECT_ID/air-quality-intermediate \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --update-env-vars BUCKET_NAME=YOUR_BUCKET_NAME \
  --service-account YOUR_SERVICE_ACCOUNT_EMAIL \
  --memory 512Mi \
  --timeout 120
```

---

## GCP Setup
```bash
# Enable APIs
gcloud services enable run.googleapis.com containerregistry.googleapis.com bigquery.googleapis.com storage.googleapis.com

# Create bucket
gsutil mb -l us-central1 gs://YOUR_BUCKET_NAME

# Create service account
gcloud iam service-accounts create air-quality-sa \
  --display-name "Air Quality Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:air-quality-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.user"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:air-quality-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:air-quality-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:air-quality-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"
```

---

## Dataset
**EPA Historical Air Quality** — BigQuery Public Dataset
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

---

## Screenshots
<!-- Add your screenshots here -->

---

## What I Learned
- Deploying complex Flask applications to Google Cloud Run
- Querying BigQuery public datasets using parameterized queries
- Uploading structured JSON reports to Cloud Storage from Cloud Run
- Setting up service accounts with least-privilege IAM roles
- Using environment variables for configuration in Cloud Run
- Monitoring logs and metrics via Cloud Console
- Production deployment with Gunicorn
