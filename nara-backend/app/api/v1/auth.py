"""Endpoints de autenticação do usuário (Supabase Auth)."""
from __future__ import annotations

from typing import Any

import httpx
from fastapi import APIRouter, Header, HTTPException, status

from app.config import settings
from app.database import supabase

router = APIRouter(prefix="/auth", tags=["Auth"])


async def _get_user_from_supabase(access_token: str) -> dict[str, Any]:
    """Valida token do Supabase consultando o endpoint oficial de user."""
    base = settings.SUPABASE_URL.rstrip("/")
    apikey = settings.SUPABASE_ANON_KEY or settings.SUPABASE_KEY or settings.SUPABASE_SERVICE_KEY
    if not base or not apikey:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase Auth não configurado no backend.",
        )

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            f"{base}/auth/v1/user",
            headers={
                "apikey": apikey,
                "Authorization": f"Bearer {access_token}",
            },
        )

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido ou expirado.",
        )
    user_data = response.json()
    if not isinstance(user_data, dict):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário autenticado inválido.",
        )
    return user_data


@router.get("/me")
async def auth_me(authorization: str = Header(default="")):
    """Retorna dados básicos do usuário autenticado via Supabase."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cabeçalho Authorization ausente.",
        )
    access_token = authorization.split(" ", 1)[1].strip()
    user_data = await _get_user_from_supabase(access_token)
    email = user_data.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário autenticado sem email.",
        )
    return {
        "id": user_data.get("id"),
        "email": email,
        "user_metadata": user_data.get("user_metadata") or {},
    }


@router.get("/my-diagnostics")
async def auth_my_diagnostics(authorization: str = Header(default="")):
    """Retorna diagnósticos do usuário autenticado (por email)."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cabeçalho Authorization ausente.",
        )
    access_token = authorization.split(" ", 1)[1].strip()
    user_data = await _get_user_from_supabase(access_token)
    email = (user_data.get("email") or "").strip().lower()
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário autenticado sem email.",
        )

    rows = (
        supabase.table("diagnostics")
        .select("id, result_token, status, created_at, completed_at, current_phase, total_answers")
        .eq("email", email)
        .order("created_at", desc=True)
        .execute()
    )
    return {"items": rows.data or []}
