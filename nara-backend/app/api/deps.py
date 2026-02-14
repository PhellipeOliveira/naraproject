"""Dependencies para rotas (auth, db, etc.)."""
from typing import Optional

# Placeholder para uso futuro: get_current_user_optional, etc.
# from fastapi import Depends
# from app.core.security import decode_token


def get_current_user_optional(optional: bool = True) -> Optional[str]:
    """Retorna user_id se autenticado; caso contrário None (para rotas opcionais)."""
    return None
