"""Endpoints de waitlist."""
import logging

from fastapi import APIRouter, Request
from pydantic import BaseModel, EmailStr

from app.core.rate_limit import limiter
from app.database import supabase
from app.services.email_service import EmailService

router = APIRouter()
email_service = EmailService()
logger = logging.getLogger(__name__)


class WaitlistRequest(BaseModel):
    """Request para entrar na lista de espera."""

    email: EmailStr
    full_name: str | None = None
    diagnostic_id: str | None = None
    source: str = "diagnostic"
    utm_source: str | None = None


class WaitlistResponse(BaseModel):
    """Resposta ao se inscrever na waitlist."""

    status: str
    message: str
    position: int | None = None


@router.post("", response_model=WaitlistResponse)
@limiter.limit("20/hour")
async def join_waitlist(request: Request, payload: WaitlistRequest):
    """
    Adiciona email à lista de espera.
    Se já existir, retorna status already_registered.
    """
    existing = (
        supabase.table("waitlist").select("id").eq("email", payload.email).execute()
    )

    if existing.data and len(existing.data) > 0:
        return WaitlistResponse(
            status="already_registered",
            message="Você já está na lista de espera!",
        )

    supabase.table("waitlist").insert({
        "email": payload.email,
        "full_name": payload.full_name,
        "diagnostic_id": payload.diagnostic_id,
        "source": payload.source,
        "utm_source": payload.utm_source,
    }).execute()

    count_result = supabase.table("waitlist").select("id", count="exact").execute()
    position = getattr(count_result, "count", None)
    if position is None and count_result.data is not None:
        position = len(count_result.data)

    try:
        await email_service.send_waitlist_welcome(
            to=payload.email,
            user_name=payload.full_name,
        )
    except Exception as e:
        logger.warning("Erro ao enviar email de boas-vindas da waitlist: %s", e)

    return WaitlistResponse(
        status="registered",
        message="Você está na lista! Verifique seu email.",
        position=position,
    )


@router.get("/count")
@limiter.limit("60/minute")
async def get_waitlist_count(request: Request):
    """Retorna contagem da lista de espera (para social proof)."""
    result = supabase.table("waitlist").select("id", count="exact").execute()
    count = getattr(result, "count", None)
    if count is None and result.data is not None:
        count = len(result.data)
    return {"count": count or 0}
