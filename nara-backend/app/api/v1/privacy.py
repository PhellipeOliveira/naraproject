"""Endpoints LGPD: exportar e excluir dados do titular (por email + result_token)."""
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import EmailStr

from app.core.rate_limit import limiter
from app.database import supabase

router = APIRouter()


@router.get("/my-data")
@limiter.limit("5/minute")
async def export_my_data(
    request: Request,
    email: EmailStr = Query(..., description="Email do titular"),
    result_token: str = Query(
        ...,
        min_length=8,
        max_length=120,
        description="Token do resultado (prova de posse)",
    ),
):
    """
    Exporta dados do titular associados ao diagnóstico (LGPD Art. 18 - Portabilidade).
    Requer email e result_token do diagnóstico para verificação.
    """
    diag = (
        supabase.table("diagnostics")
        .select("id, email, created_at, status")
        .eq("email", email)
        .eq("result_token", result_token)
        .execute()
    )
    if not diag.data or len(diag.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnóstico não encontrado ou token inválido.",
        )
    diagnostic_id = diag.data[0]["id"]
    diagnostics = (
        supabase.table("diagnostics").select("*").eq("id", diagnostic_id).execute()
    )
    answers = (
        supabase.table("answers").select("*").eq("diagnostic_id", diagnostic_id).execute()
    )
    results = (
        supabase.table("diagnostic_results")
        .select("*")
        .eq("diagnostic_id", diagnostic_id)
        .execute()
    )
    return {
        "export_date": datetime.utcnow().isoformat(),
        "data": {
            "diagnostics": diagnostics.data,
            "answers": answers.data or [],
            "results": results.data or [],
        },
    }


@router.delete("/my-data")
@limiter.limit("5/minute")
async def delete_my_data(
    request: Request,
    email: EmailStr = Query(..., description="Email do titular"),
    result_token: str = Query(
        ...,
        min_length=8,
        max_length=120,
        description="Token do resultado (prova de posse)",
    ),
    confirm: bool = Query(False, description="Confirmação de exclusão"),
):
    """
    Exclui dados do titular do diagnóstico (LGPD Art. 18 - Eliminação).
    Requer email, result_token e confirm=true.
    """
    if not confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Confirmação necessária. Envie confirm=true.",
        )
    diag = (
        supabase.table("diagnostics")
        .select("id")
        .eq("email", email)
        .eq("result_token", result_token)
        .execute()
    )
    if not diag.data or len(diag.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnóstico não encontrado ou token inválido.",
        )
    diagnostic_id = diag.data[0]["id"]
    supabase.table("answers").delete().eq("diagnostic_id", diagnostic_id).execute()
    supabase.table("diagnostic_results").delete().eq("diagnostic_id", diagnostic_id).execute()
    supabase.table("feedback").delete().eq("diagnostic_id", diagnostic_id).execute()
    supabase.table("diagnostics").delete().eq("id", diagnostic_id).execute()
    return {
        "status": "deleted",
        "deleted_at": datetime.utcnow().isoformat(),
    }
