import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
@pytest.fixture
def client(tmp_path,monkeypatch):
    monkeypatch.setenv('AEGIS_DB_PATH',str(tmp_path/'test.db'))
    monkeypatch.setenv('AEGIS_API_KEY','test-key')
    return TestClient(app)
@pytest.fixture
def headers(): return {'X-API-Key':'test-key'}
def test_alerts_reject_missing_key(client):
    response = client.get("/alerts")
    assert response.status_code == 401