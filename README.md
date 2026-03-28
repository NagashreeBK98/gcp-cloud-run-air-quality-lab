# GCP Cloud Run — Air Quality Monitoring Lab

A cloud-native Air Quality Monitoring API built with Flask, containerized
with Docker, and deployed on Google Cloud Run — integrating BigQuery
(EPA public dataset) and Cloud Storage for real-time AQI insights.

---

## Labs

| Lab | Description | Live URL |
|---|---|---|
| Beginner Lab | Simple Flask AQI API for US cities | https://air-quality-beginner-932441309698.us-central1.run.app |
| Intermediate Lab | Full API with BigQuery + Cloud Storage | https://air-quality-intermediate-932441309698.us-central1.run.app |

---

## Repository Structure
```
gcp-cloud-run-air-quality-lab/
├── Beginner_Lab/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── Intermediate_Lab/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
└── README.md
```

---

## Tech Stack
- **Python** — Flask, Gunicorn
- **Docker** — Containerization
- **Google Cloud Run** — Serverless deployment
- **Google BigQuery** — EPA Historical Air Quality public dataset
- **Google Cloud Storage** — JSON report export
- **GCP IAM** — Service account with least-privilege roles

---

## Dataset
**EPA Historical Air Quality** — BigQuery Public Dataset
- Table: `bigquery-public-data.epa_historical_air_quality.daily_aqi_by_county`
- Daily AQI readings by county across the United States

---

## Screenshots
<!-- Add your screenshots here -->

---

## Setup & Deployment
See individual lab READMEs for detailed setup and deployment instructions:
- [Beginner Lab](./Beginner_Lab/README.md)
- [Intermediate Lab](./Intermediate_Lab/README.md)
