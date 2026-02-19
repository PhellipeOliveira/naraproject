"""Endpoints de feedback NPS."""
import logging

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field

from app.core.rate_limit import limiter
from app.database import supabase

router = APIRouter()
logger = logging.getLogger(__name__)


class FeedbackRequest(BaseModel):
    """Request para submeter feedback NPS."""

    diagnostic_id: str
    nps_score: int = Field(..., ge=0, le=10, description="NPS 0-10")
    rating: int | None = Field(None, ge=1, le=5, description="Rating 1-5 estrelas")
    feedback_text: str | None = Field(None, max_length=2000)
    feedback_type: str = Field("private", pattern="^(public|private)$")


class FeedbackResponse(BaseModel):
    """Resposta ao submeter feedback."""

    status: str
    message: str


@router.post("", response_model=FeedbackResponse)
@limiter.limit("30/minute")
async def submit_feedback(request: Request, payload: FeedbackRequest):
    """
    Submete feedback NPS após conclusão do diagnóstico.
    """
    payload = {
        "diagnostic_id": payload.diagnostic_id,
        "nps_score": payload.nps_score,
        "rating": payload.rating,
        "feedback_text": payload.feedback_text,
        "feedback_type": payload.feedback_type,
    }
    try:
        supabase.table("feedback").insert(payload).execute()
    except Exception as e:
        logger.exception("submit_feedback failed for diagnostic_id=%s: %s", payload.diagnostic_id, e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao registrar feedback. Tente novamente.",
        ) from e
    return FeedbackResponse(
        status="ok",
        message="Obrigado pelo seu feedback!",
    )
