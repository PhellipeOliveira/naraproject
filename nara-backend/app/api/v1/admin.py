"""Endpoints de autenticação administrativa."""
import secrets

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.config import settings
from app.core.admin_auth import create_admin_token

router = APIRouter(prefix="/admin", tags=["Admin"])


class AdminLoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=200)


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int


@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(payload: AdminLoginRequest):
    """Login administrativo simples para obter token bearer."""
    username_ok = settings.ADMIN_USERNAME and secrets.compare_digest(
        payload.username, settings.ADMIN_USERNAME
    )
    password_ok = settings.ADMIN_PASSWORD and secrets.compare_digest(
        payload.password, settings.ADMIN_PASSWORD
    )
    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais administrativas inválidas.",
        )

    token = create_admin_token(payload.username)
    return AdminLoginResponse(
        access_token=token,
        expires_in_seconds=settings.ADMIN_TOKEN_TTL_MINUTES * 60,
    )
