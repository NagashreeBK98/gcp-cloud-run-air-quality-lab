# Beginner Lab — Air Quality Monitor

## Live Demo
**Service URL:** https://air-quality-beginner-932441309698.us-central1.run.app

| Endpoint | Live Link |
|---|---|
| Home | https://air-quality-beginner-932441309698.us-central1.run.app/ |
| Health Check | https://air-quality-beginner-932441309698.us-central1.run.app/health |
| All Cities AQI | https://air-quality-beginner-932441309698.us-central1.run.app/aqi |
| Boston AQI | https://air-quality-beginner-932441309698.us-central1.run.app/aqi/Boston |
| Chicago AQI | https://air-quality-beginner-932441309698.us-central1.run.app/aqi/Chicago |

---

## Overview
A simple Flask application deployed on Google Cloud Run that serves
Air Quality Index (AQI) data for major US cities with health recommendations.

**Modification from professor's lab:** Instead of a basic "Hello World" response,
this app serves real-world air quality data with multiple endpoints, health checks,
AQI color coding, and structured JSON responses.

---

## Endpoints
| Endpoint | Description |
|---|---|
| `/` | Home page with available routes |
| `/health` | Health check endpoint |
| `/aqi` | AQI data for all cities |
| `/aqi/<city>` | AQI data for a specific city |

---

## Run Locally
```bash
