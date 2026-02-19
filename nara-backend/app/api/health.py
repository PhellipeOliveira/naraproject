"""
Health check endpoints para monitoramento.
Conforme 07_DEPLOY_QUALIDADE.md - Seção 5
"""
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, status
from app.database import supabase
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    """
    Health check básico.
    Usado por Render/Railway, Kubernetes, etc.
    """
    return {
        "status": "healthy",
        "version": getattr(settings, "APP_VERSION", "1.0.0"),
        "timestamp": datetime.utcnow().isoformat(),
        "service": "nara-backend"
    }


@router.get("/health/detailed")
async def health_detailed():
    """
    Health check detalhado com verificação de dependências.
    Útil para troubleshooting e monitoramento avançado.
    """
    checks: Dict[str, Any] = {}
    overall_status = "healthy"
    
    # 1. Verificar Supabase (banco de dados)
    try:
        result = supabase.table("areas").select("id").limit(1).execute()
        if result.data:
            checks["database"] = {
                "status": "healthy",
                "message": "Supabase conectado"
            }
        else:
            checks["database"] = {
                "status": "degraded",
                "message": "Supabase conectado mas sem dados"
            }
            overall_status = "degraded"
    except Exception as e:
        logger.error(f"Health check - Database error: {e}")
        checks["database"] = {
            "status": "unhealthy",
            "message": f"Erro: {str(e)[:100]}"
        }
        overall_status = "unhealthy"
    
    # 2. Verificar OpenAI API Key configurada
    if settings.OPENAI_API_KEY and len(settings.OPENAI_API_KEY) > 10:
        checks["openai"] = {
            "status": "healthy",
            "message": "API key configurada"
        }
    else:
        checks["openai"] = {
            "status": "unhealthy",
            "message": "API key não configurada"
        }
        overall_status = "unhealthy"
    
    # 3. Verificar Resend API Key configurada
    if settings.RESEND_API_KEY and len(settings.RESEND_API_KEY) > 10:
        checks["email"] = {
            "status": "healthy",
            "message": "Resend configurado"
        }
    else:
        checks["email"] = {
            "status": "degraded",
            "message": "Resend não configurado (email desabilitado)"
        }
        # Email não é crítico
        if overall_status == "healthy":
            overall_status = "degraded"
    
    # 4. Verificar chunks de conhecimento
    try:
        result = supabase.table("knowledge_chunks").select("id", count="exact").eq("is_active", True).limit(1).execute()
        if result.count and result.count > 0:
            checks["knowledge_base"] = {
                "status": "healthy",
                "message": f"{result.count} chunks ativos"
            }
        else:
            checks["knowledge_base"] = {
                "status": "degraded",
                "message": "Nenhum chunk ativo"
            }
            if overall_status == "healthy":
                overall_status = "degraded"
    except Exception as e:
        logger.error(f"Health check - Knowledge base error: {e}")
        checks["knowledge_base"] = {
            "status": "unhealthy",
            "message": f"Erro: {str(e)[:100]}"
        }
        overall_status = "unhealthy"
    
    # Se algum check crítico falhou, retornar 503
    if overall_status == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": overall_status,
                "checks": checks,
                "version": getattr(settings, "APP_VERSION", "1.0.0"),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    return {
        "status": overall_status,
        "checks": checks,
        "version": getattr(settings, "APP_VERSION", "1.0.0"),
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENV
    }


@router.get("/health/ready")
async def health_ready():
    """
    Readiness probe - verifica se o serviço está pronto para receber tráfego.
    Usado por Kubernetes, load balancers, etc.
    """
    try:
        # Verificação mínima: banco de dados acessível
        supabase.table("areas").select("id").limit(1).execute()
        
        return {
            "ready": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"ready": False, "error": str(e)}
        )


@router.get("/health/live")
async def health_live():
    """
    Liveness probe - verifica se o serviço está vivo (não travado).
    Usado por Kubernetes para restart automático.
    """
    return {
        "alive": True,
        "timestamp": datetime.utcnow().isoformat()
    }
