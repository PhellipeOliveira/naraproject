"""Dependencies para rotas (auth, db, etc.)."""
import secrets
from typing import Optional

from fastapi import Header, HTTPException, status

from app.config import settings
from app.core.admin_auth import verify_admin_token


def get_current_user_optional(optional: bool = True) -> Optional[str]:
    """Retorna user_id se autenticado; caso contrário None (para rotas opcionais)."""
    return None


def require_admin_access(
    authorization: str = Header(default=""),
    x_admin_key: str = Header(default="", alias="X-Admin-Key"),
) -> None:
    """
    Controle administrativo:
    - Preferencial: Authorization Bearer <admin_token>
    - Fallback legado: X-Admin-Key
    Nota: controle de UI no frontend é apenas visual; a API faz o bloqueio real.
    """
    if authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1].strip()
        payload = verify_admin_token(token)
        if payload:
            return

    legacy = settings.ADMIN_API_KEY.strip()
    if legacy and x_admin_key and secrets.compare_digest(x_admin_key, legacy):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acesso administrativo não autorizado.",
    )
