"""Testes de integração do fluxo de diagnóstico (com mocks de Supabase/OpenAI)."""
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Env mínimo para importar app
import os
os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_SERVICE_KEY", "test-key")
os.environ.setdefault("OPENAI_API_KEY", "sk-test")
os.environ.setdefault("RESEND_API_KEY", "re_test")

from app.main import app

client = TestClient(app)


def test_health():
    """GET /health retorna 200 e status healthy."""
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_health_detailed():
    """GET /health/detailed retorna checks (database pode falhar sem Supabase real)."""
    r = client.get("/health/detailed")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert "checks" in data
    assert "database" in data["checks"]


def test_start_diagnostic_requires_consent():
    """POST /api/v1/diagnostic/start sem consent_privacy retorna 422 ou 400."""
    r = client.post(
        "/api/v1/diagnostic/start",
        json={
            "email": "test@example.com",
            "consent_privacy": False,
            "consent_marketing": False,
        },
    )
    assert r.status_code in (400, 422)


@patch("app.rag.pipeline.supabase")
def test_start_diagnostic_success(mock_supabase):
    """POST /api/v1/diagnostic/start com consent retorna diagnostic_id e perguntas (mock)."""
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "status": "in_progress",
            "current_phase": 1,
            "result_token": "nara_abc123def456",
        }
    ]
    r = client.post(
        "/api/v1/diagnostic/start",
        json={
            "email": "test@example.com",
            "consent_privacy": True,
            "consent_marketing": False,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "diagnostic_id" in data
    assert data["phase"] == 1
    assert data["total_questions"] == 15
    assert "result_token" in data
    assert len(data["questions"]) == 15


def test_waitlist_count():
    """GET /api/v1/waitlist/count retorna count (pode ser 0)."""
    with patch("app.api.v1.waitlist.supabase") as mock_sb:
        mock_resp = MagicMock()
        mock_resp.data = []
        mock_resp.count = 0
        mock_sb.table.return_value.select.return_value.execute.return_value = mock_resp
        r = client.get("/api/v1/waitlist/count")
    assert r.status_code == 200
    assert "count" in r.json()
