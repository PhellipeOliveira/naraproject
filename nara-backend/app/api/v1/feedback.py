"""Endpoints de feedback NPS."""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.database import supabase

router = APIRouter()


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
async def submit_feedback(request: FeedbackRequest):
    """
    Submete feedback NPS após conclusão do diagnóstico.
    """
    payload = {
        "diagnostic_id": request.diagnostic_id,
        "nps_score": request.nps_score,
        "rating": request.rating,
        "feedback_text": request.feedback_text,
        "feedback_type": request.feedback_type,
    }
    try:
        supabase.table("feedback").insert(payload).execute()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao registrar feedback: {e}",
        ) from e
    return FeedbackResponse(
        status="ok",
        message="Obrigado pelo seu feedback!",
    )
