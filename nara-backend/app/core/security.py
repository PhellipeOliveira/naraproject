"""JWT e autenticação (para uso futuro)."""
from typing import Any, Optional

# Stub para Fase 2; implementar quando auth for exigida.


def create_access_token(data: dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """Cria um JWT de acesso. Placeholder."""
    raise NotImplementedError("Auth será implementada em iteração futura.")


def decode_token(token: str) -> Optional[dict[str, Any]]:
    """Decodifica e valida um JWT. Placeholder."""
    return None
