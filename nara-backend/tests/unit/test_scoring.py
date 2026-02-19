"""Testes unitários de scoring (cálculo de scores por área)."""
import pytest
from unittest.mock import patch, MagicMock

from app.rag.pipeline import NaraDiagnosticPipeline

pipeline = NaraDiagnosticPipeline()


@pytest.mark.asyncio
async def test_calculate_area_scores_empty_answers():
    """Sem respostas, scores vazios."""
    with patch("app.rag.pipeline.supabase") as mock_sb:
        result = MagicMock()
        result.data = []
        mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = result
        scores = await pipeline._calculate_area_scores("fake-id")
        assert scores == {}


@pytest.mark.asyncio
async def test_calculate_area_scores_scale_conversion():
    """Escala 1-5 é convertida para 0-10 (média * 2)."""
    with patch("app.rag.pipeline.supabase") as mock_sb:
        result = MagicMock()
        result.data = [
            {"question_area": "Saúde Física", "answer_value": {"scale": 4, "text": None}},
            {"question_area": "Saúde Física", "answer_value": {"scale": 2, "text": None}},
        ]
        mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = result
        scores = await pipeline._calculate_area_scores("fake-id")
        assert "Saúde Física" in scores
        assert scores["Saúde Física"]["score"] == 6.0  # (4+2)/2 * 2
        assert scores["Saúde Física"]["questions_answered"] == 2
