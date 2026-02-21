"""Configurações centralizadas da aplicação."""
from functools import lru_cache
from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações carregadas de variáveis de ambiente."""

    # Aplicação
    APP_NAME: str = "NARA Diagnostic API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENV: str = "development"

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    ADMIN_API_KEY: str = ""
    ADMIN_USERNAME: str = ""
    ADMIN_PASSWORD: str = ""
    ADMIN_JWT_SECRET: str = ""
    ADMIN_TOKEN_TTL_MINUTES: int = 60

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL_QUESTIONS: str = "gpt-4o-mini"
    OPENAI_MODEL_ANALYSIS: str = "gpt-4o"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Resend (Email) – domínio: phellipeoliveira.org
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "diagnostic.nara@phellipeoliveira.org"
    RESEND_REPLY_TO: str = "contato@phellipeoliveira.org"

    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"

    # RAG
    RAG_TOP_K: int = 10
    RAG_SIMILARITY_THRESHOLD: float = 0.5
    RAG_CHUNK_VERSION: int = 2      # versão ativa no banco; altere aqui ao migrar chunks
    RAG_CHUNK_STRATEGY: str = "semantic"  # estratégia padrão usada pelo seed ativo

    # Diagnóstico
    MIN_QUESTIONS_TO_FINISH: int = 40
    MIN_WORDS_TO_FINISH: int = 3500
    QUESTIONS_PER_PHASE: int = 15
    MIN_AREAS_COVERED: int = 12

    # CORS (aceita JSON array ou string separada por vírgula)
    CORS_ORIGINS: Union[List[str], str] = "http://localhost:5173,https://nara.app"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            if v.strip().startswith("["):
                import json
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    def validate_runtime_requirements(self) -> None:
        """
        Valida variáveis obrigatórias em ambientes não-locais.
        Em desenvolvimento local permitimos startup sem todas as chaves para DX.
        """
        if self.ENV.lower() in {"development", "dev", "local"}:
            return

        required = {
            "SUPABASE_URL": self.SUPABASE_URL,
            "SUPABASE_SERVICE_KEY": self.SUPABASE_SERVICE_KEY,
            "OPENAI_API_KEY": self.OPENAI_API_KEY,
        }
        admin_credentials_ok = all(
            [
                str(self.ADMIN_USERNAME).strip(),
                str(self.ADMIN_PASSWORD).strip(),
                str(self.ADMIN_JWT_SECRET).strip(),
            ]
        )
        # Aceita modelo novo (login+token) ou fallback legado (X-Admin-Key)
        if not admin_credentials_ok and not str(self.ADMIN_API_KEY).strip():
            required["ADMIN_AUTH"] = ""
        missing = [name for name, value in required.items() if not str(value).strip()]
        if missing:
            raise ValueError(
                "Variáveis obrigatórias ausentes para ambiente "
                f"{self.ENV}: {', '.join(missing)}"
            )

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Singleton para configurações."""
    return Settings()


settings = get_settings()
