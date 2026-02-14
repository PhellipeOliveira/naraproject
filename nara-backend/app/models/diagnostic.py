"""Modelos Pydantic para diagnóstico."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ===== REQUESTS =====


class DiagnosticStartRequest(BaseModel):
    """Request para iniciar diagnóstico."""

    email: EmailStr
    full_name: Optional[str] = None
    session_id: Optional[str] = None
    consent_privacy: bool = Field(..., description="Consentimento obrigatório")
    consent_marketing: bool = False
    device_info: Optional[Dict[str, Any]] = None
    utm_source: Optional[str] = None


class AnswerSubmitRequest(BaseModel):
    """Request para submeter uma resposta."""

    question_id: int
    question_text: str
    question_area: str
    answer_text: Optional[str] = Field(None, max_length=10000)
    answer_scale: Optional[int] = Field(None, ge=1, le=5)
    response_time_seconds: Optional[int] = Field(None, ge=0)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question_id": 1,
                "question_text": "De 1 a 5, como você avalia sua energia física?",
                "question_area": "Saúde Física",
                "answer_scale": 4,
            }
        }
    )


# ===== RESPONSES =====


class QuestionResponse(BaseModel):
    """Uma pergunta (baseline ou adaptativa)."""

    id: int
    area: str
    type: str = Field(..., pattern="^(scale|open_long|open_short)$")
    text: str
    scale_labels: Optional[List[str]] = None
    follow_up_hint: Optional[str] = None


class ProgressResponse(BaseModel):
    """Progresso do diagnóstico (percentuais)."""

    overall: float = Field(..., ge=0, le=100)
    questions: float = Field(..., ge=0, le=100)
    words: float = Field(..., ge=0, le=100)
    coverage: float = Field(..., ge=0, le=100)


class DiagnosticStartResponse(BaseModel):
    """Resposta ao iniciar diagnóstico."""

    diagnostic_id: str
    status: str
    phase: int
    questions: List[QuestionResponse]
    total_questions: int
    result_token: str


class AnswerSubmitResponse(BaseModel):
    """Resposta ao submeter resposta."""

    status: str
    can_finish: bool
    phase_complete: bool
    progress: ProgressResponse
    total_answers: int
    total_words: int
    areas_covered: int


class NextQuestionsResponse(BaseModel):
    """Resposta com próximas perguntas (fase adaptativa)."""

    phase: int
    questions: List[QuestionResponse]
    total_questions: int


class CriteriaDetail(BaseModel):
    """Detalhe de um critério de elegibilidade."""

    current: int
    required: int
    percentage: float
    met: bool
    missing_areas: Optional[List[str]] = None


class EligibilityResponse(BaseModel):
    """Resposta de elegibilidade para finalizar."""

    can_finish: bool
    criteria: Dict[str, Any]  # questions, words, coverage
    overall_progress: float


class AreaAnalysis(BaseModel):
    """Análise de uma área no relatório."""

    area_name: str
    score: float
    status: str
    analysis: str
    key_insight: str


class Recommendation(BaseModel):
    """Recomendação no relatório."""

    action: str
    timeframe: str
    area_related: Optional[str] = None


class DiagnosticResultResponse(BaseModel):
    """Resposta com resultado do diagnóstico (relatório)."""

    model_config = ConfigDict(extra="allow")

    overall_score: Optional[float] = None
    phase_identified: Optional[str] = None
    motor_dominante: Optional[str] = None
    motor_secundario: Optional[str] = None
    crise_raiz: Optional[str] = None
    ponto_entrada_ideal: Optional[str] = None
    executive_summary: Optional[str] = None
    area_analysis: Optional[List[AreaAnalysis]] = None
    patterns: Optional[Dict[str, List[str]]] = None
    strengths: Optional[List[str]] = None
    development_areas: Optional[List[Dict[str, Any]]] = None
    recommendations: Optional[List[Recommendation]] = None
