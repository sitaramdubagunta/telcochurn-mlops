from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] in {"healthy", "degraded"}
    assert "model_loaded" in data
    assert "api_version" in data
    assert "timestamp" in data


def test_metadata_endpoint():
    with TestClient(app) as client:
        response = client.get("/metadata")

    assert response.status_code == 200
    data = response.json()
    assert {"health", "metrics", "model_info"} <= set(data)


def test_valid_prediction():
    with TestClient(app) as client:
        payload = client.get("/sample-payload").json()
        response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in {"Yes", "No"}
    assert 0 <= data["probability"] <= 1
    assert data["risk_level"] in {"Low", "Medium", "High"}
    assert 0 <= data["confidence"] <= 1


def test_invalid_payload():
    with TestClient(app) as client:
        response = client.post("/predict", json={"tenure": -1})

    assert response.status_code == 422


def test_model_loads_successfully():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.json()["model_loaded"] is True
