"""Cliente Supabase configurado."""
from supabase import Client, create_client

from app.config import settings


def get_supabase_client() -> Client:
    """Retorna cliente Supabase com service role (backend)."""
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_KEY,
    )


def get_supabase_anon_client() -> Client:
    """Retorna cliente Supabase com anon key (operações públicas)."""
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY,
    )


# Instância singleton para uso no backend
supabase = get_supabase_client()
