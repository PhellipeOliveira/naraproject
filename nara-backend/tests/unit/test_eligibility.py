"""Testes unitários da lógica de elegibilidade."""
import pytest

from app.config import settings
from app.rag.pipeline import NaraDiagnosticPipeline

pipeline = NaraDiagnosticPipeline()


def test_eligible_when_all_criteria_met():
    """Pode finalizar quando ≥40 respostas e ≥12 áreas."""
    result = pipeline._check_eligibility(
        total_answers=45,
        total_words=4000,
        areas_covered=pipeline.AREAS,
    )
    assert result.can_finish is True
    assert result.questions_progress >= 100
    assert result.words_progress >= 100
    assert result.coverage_progress >= 100
    assert result.missing_areas == []


def test_eligible_by_words_only():
    """Pode finalizar só por palavras (≥3500) com 12 áreas."""
    result = pipeline._check_eligibility(
        total_answers=30,
        total_words=4000,
        areas_covered=pipeline.AREAS,
    )
    assert result.can_finish is True


def test_not_eligible_missing_areas():
    """Não pode finalizar se faltam áreas (< 12)."""
    result = pipeline._check_eligibility(
        total_answers=50,
        total_words=5000,
        areas_covered=pipeline.AREAS[:10],
    )
    assert result.can_finish is False
    assert len(result.missing_areas) == 2


def test_not_eligible_insufficient_quantity():
    """Não pode finalizar com poucas respostas e poucas palavras."""
    result = pipeline._check_eligibility(
        total_answers=20,
        total_words=1000,
        areas_covered=pipeline.AREAS,
    )
    assert result.can_finish is False
    assert result.questions_progress < 100
    assert result.words_progress < 100


def test_progress_percentages_bounded():
    """Progressos ficam entre 0 e 100."""
    result = pipeline._check_eligibility(
        total_answers=100,
        total_words=10000,
        areas_covered=pipeline.AREAS,
    )
    assert 0 <= result.questions_progress <= 100
    assert 0 <= result.words_progress <= 100
    assert 0 <= result.coverage_progress <= 100
    assert 0 <= result.overall_progress <= 100
