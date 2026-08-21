"""
Tests for DataForge Enterprise REST API Gateway.
"""
from fastapi.testclient import TestClient
from dataforge.api.app import app

client = TestClient(app)


def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "endpoints" in data


def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_radar_status_endpoint():
    response = client.get("/api/v1/radar/status")
    assert response.status_code == 200
    data = response.json()
    assert "toplam_kayit" in data
    assert "veritabani_konumu" in data
