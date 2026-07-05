# Telco Customer Churn MLOps

Production-style customer churn prediction app built with React, FastAPI, XGBoost, MLflow, Docker, and GitHub Actions.

Live app: https://telcochurn-mlops.vercel.app/

Note for users: the backend is deployed on Render, so the first request can take about 2 minutes while the service wakes up. If the app looks like it is loading or the first prediction is slow, wait a bit and try again.

## What It Does

This project predicts whether a telecom customer is likely to churn based on account, contract, billing, and service usage fields. The frontend collects customer details and calls the FastAPI backend, which loads the trained model artifact and returns a churn prediction, probability, risk level, confidence, and recommendation.

## Tech Stack

- Frontend: React, Vite, Axios, Tailwind CSS
- Backend: FastAPI, Pydantic, Uvicorn
- ML: XGBoost, scikit-learn, pandas, NumPy
- Experiment tracking: MLflow
- Testing: pytest, FastAPI TestClient
- Deployment: Vercel frontend, Render backend
- Containers: Docker, Docker Compose

## Project Structure

```text
.
+-- backend/
|   +-- app/                 # FastAPI app, routes, schemas, services
|   +-- artifacts/           # Trained model and metadata artifacts
|   +-- data/                # Raw and processed Telco churn data
|   +-- src/                 # Data, feature, training, and prediction code
|   +-- tests/               # API and ML pipeline tests
+-- frontend/
|   +-- src/                 # React app, pages, components, API client
|   +-- public/              # Static assets
+-- reports/                 # Model reports and plots
+-- docker-compose.yml
+-- README.md
```

## API Endpoints

Base URL locally: `http://127.0.0.1:8000`

Interactive docs: `http://127.0.0.1:8000/docs`

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | API welcome message with docs and health links. |
| `GET` | `/health` | Health status, model load status, API version, uptime, and timestamp. |
| `GET` | `/metrics` | Model metrics such as accuracy, precision, recall, F1, and ROC AUC. |
| `GET` | `/model-info` | Model name, algorithm, version, feature count, training timestamp, and artifact path. |
| `GET` | `/sample-payload` | Example customer payload for testing predictions. |
| `GET` | `/metadata` | Combined health, metrics, and model info response. |
| `POST` | `/predict` | Returns churn prediction for a customer payload. |

## Prediction Payload

`POST /predict` expects this customer shape:

```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 12,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "Fiber optic",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "Yes",
  "StreamingMovies": "Yes",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 79.85,
  "TotalCharges": 950.25
}
```

Response shape:

```json
{
  "prediction": "Yes",
  "probability": 0.72,
  "risk_level": "High",
  "confidence": 0.72,
  "recommendation": "Customer is at high churn risk. Consider retention offer."
}
```

## Unit Tests

Backend tests live in `backend/tests`.

API tests:

- `test_health_endpoint`: verifies `/health` returns status, model load state, API version, and timestamp.
- `test_metadata_endpoint`: verifies `/metadata` returns health, metrics, and model info.
- `test_valid_prediction`: fetches `/sample-payload`, posts it to `/predict`, and validates prediction fields.
- `test_invalid_payload`: verifies invalid payloads return validation error `422`.
- `test_model_loads_successfully`: verifies the model artifact loads successfully.

Pipeline tests:

- `test_preprocessing_pipeline_transforms_features`: verifies preprocessing transforms a sample customer row.
- `test_prediction_probability_between_zero_and_one`: verifies model prediction probability stays between `0` and `1`.

Run tests:

```bash
cd backend
pytest
```

## Run Locally

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend uses `VITE_API_URL` when provided. Without it, it defaults to `http://127.0.0.1:8000`.

## Docker

Run the full local stack:

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- MLflow UI: `http://localhost:5000`

## Model Artifacts And Reports

Model artifacts are stored under `backend/artifacts`:

- `model.pkl`
- `feature_columns.pkl`
- `model_info.json`
- `model_metrics.json`

Reports are stored under `reports`:

- `classification_report.md`
- `model_card.md`
- `confusion_matrix.png`
- `feature_importance.png`
- `roc_curve.png`
