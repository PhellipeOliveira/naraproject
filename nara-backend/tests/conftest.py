"""Pytest fixtures: app, client, mocks."""
import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Garantir que env de teste não use credenciais reais
os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "test-anon-key")
os.environ.setdefault("SUPABASE_SERVICE_KEY", "test-service-key")
os.environ.setdefault("OPENAI_API_KEY", "sk-test")
os.environ.setdefault("RESEND_API_KEY", "re_test")


@pytest.fixture
def app():
    """FastAPI app instance."""
    from app.main import app as fastapi_app
    return fastapi_app


@pytest.fixture
def client(app):
    """Test client (sync)."""
    return TestClient(app)


@pytest.fixture
def mock_supabase():
    """Mock Supabase client para testes que não batem no banco."""
    with patch("app.database.supabase") as m:
        yield m


@pytest.fixture
def mock_openai_embedding():
    """Mock OpenAI embeddings (retorna vetor fixo)."""
    with patch("app.rag.embeddings.generate_embedding") as m:
        m.return_value = [0.1] * 1536
        yield m


@pytest.fixture
def mock_openai_chat():
    """Mock OpenAI chat (retorna JSON mínimo)."""
    with patch("app.rag.generator.client") as m_client:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"questions": [{"area": "Geral", "type": "open_long", "text": "Pergunta?", "follow_up_hint": ""}]}'
        m_client.chat.completions.create = MagicMock(return_value=mock_response)
        yield m_client
