"""Configuração centralizada de rate limiting."""
from slowapi import Limiter
from slowapi.util import get_remote_address

# Key por IP; em produção idealmente combinar com request ID/sessão.
limiter = Limiter(key_func=get_remote_address)
