"""Entry point da aplicação FastAPI."""
import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1.router import api_router
from app.config import settings
from app.core.observability import (
    configure_logging,
    get_request_id,
    reset_request_id,
    set_request_id,
)
from app.core.rate_limit import limiter

# Configurar logging em formato JSON + request_id
configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle hooks da aplicação."""
    settings.validate_runtime_requirements()
    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)
app.state.limiter = limiter

# CORS (com allow_credentials=True, métodos e headers devem ser explícitos, não "*")
origins = settings.CORS_ORIGINS
if isinstance(origins, str):
    origins = [o.strip() for o in origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["Content-Type", "Authorization", "Accept", "X-Request-ID", "Origin"],
    expose_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    """Retorna payload padronizado para excesso de requisições."""
    request_id = getattr(request.state, "request_id", get_request_id())
    logger.warning(
        "rate_limited method=%s path=%s client=%s request_id=%s",
        request.method,
        request.url.path,
        request.client.host if request.client else "-",
        request_id,
    )
    headers = _cors_headers(request)
    headers["X-Request-ID"] = request_id
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Muitas requisições. Tente novamente em instantes.",
            "request_id": request_id,
        },
        headers=headers,
    )


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    """Adiciona request_id para correlação de logs e resposta HTTP."""
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    token = set_request_id(request_id)
    request.state.request_id = request_id
    started = time.perf_counter()

    try:
        response = await call_next(request)
    finally:
        duration_ms = (time.perf_counter() - started) * 1000
        status_code = getattr(locals().get("response", None), "status_code", 500)
        logger.info(
            "request_completed method=%s path=%s status=%s duration_ms=%.2f client=%s",
            request.method,
            request.url.path,
            status_code,
            duration_ms,
            request.client.host if request.client else "-",
        )
        reset_request_id(token)

    response.headers["X-Request-ID"] = request_id
    return response


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Headers básicos de segurança para reduzir superfície de ataque."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


def _cors_headers(request: Request) -> dict:
    """Headers CORS para respostas de erro (evita bloqueio no browser)."""
    origin = request.headers.get("origin", "")
    allow = origin if origin in origins else (origins[0] if origins else "*")
    return {
        "Access-Control-Allow-Origin": allow,
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Garante que respostas de erro incluam headers CORS."""
    request_id = getattr(request.state, "request_id", get_request_id())
    logger.exception(
        "unhandled_exception method=%s path=%s request_id=%s error=%s",
        request.method,
        request.url.path,
        request_id,
        exc,
    )
    headers = _cors_headers(request)
    headers["X-Request-ID"] = request_id
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erro interno do servidor. Tente novamente.",
            "request_id": request_id,
        },
        headers=headers,
    )


# Rotas da API
app.include_router(api_router, prefix="/api/v1")

# Health checks
from app.api.health import router as health_router
app.include_router(health_router)
