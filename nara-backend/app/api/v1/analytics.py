"""
Rotas de Analytics e Dashboard.
Métricas e visualizações do sistema NARA.
"""
from datetime import date, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# ============================================
# Schemas de Response
# ============================================

class RealtimeMetric(BaseModel):
    """Métrica de um dia específico."""
    date: str
    total_diagnostics: int
    completed: int
    in_progress: int
    abandoned: int
    completion_rate: float
    avg_answers: Optional[int] = None
    avg_words: Optional[int] = None
    motor_necessidade: Optional[int] = None
    motor_valor: Optional[int] = None
    motor_desejo: Optional[int] = None
    motor_proposito: Optional[int] = None


class DistributionItem(BaseModel):
    """Item de distribuição (motor, crise, etc)."""
    name: str = Field(..., alias="motor_dominante", description="Nome do item")
    count: int
    percentage: float


class AreaSilenciadaItem(BaseModel):
    """Área silenciada com estatísticas."""
    area_id: int
    area_name: str
    silence_count: int
    percentage: float


class DashboardSummary(BaseModel):
    """Resumo completo do dashboard."""
    period: Dict[str, Any]
    totals: Dict[str, Any]
    realtime_metrics: List[Dict[str, Any]]
    motores_distribution: List[Dict[str, Any]]
    crises_distribution: List[Dict[str, Any]]
    areas_silenciadas: List[Dict[str, Any]]


# ============================================
# Endpoints
# ============================================

@router.get("/dashboard", response_model=DashboardSummary)
async def get_dashboard_summary():
    """
    Retorna resumo completo do dashboard com todas as métricas principais.
    
    **Inclui:**
    - Métricas dos últimos 7 dias
    - Distribuição de motores
    - Distribuição de crises
    - Heatmap de áreas silenciadas
    """
    summary = await analytics_service.get_dashboard_summary()
    return summary


@router.get("/realtime", response_model=List[RealtimeMetric])
async def get_realtime_metrics(
    days: int = Query(default=7, ge=1, le=90, description="Número de dias")
):
    """
    Retorna métricas em tempo real dos últimos N dias.
    
    **Parâmetros:**
    - days: Número de dias (1-90)
    """
    metrics = await analytics_service.get_realtime_metrics(days=days)
    return metrics


@router.get("/motores", response_model=List[DistributionItem])
async def get_motores_distribution():
    """
    Retorna distribuição de motores motivacionais.
    
    **Retorna:**
    - motor_dominante: Nome do motor
    - count: Quantidade de diagnósticos
    - percentage: Percentual do total
    """
    distribution = await analytics_service.get_motores_distribution()
    return distribution


@router.get("/crises", response_model=List[DistributionItem])
async def get_crises_distribution():
    """
    Retorna distribuição de crises raiz.
    
    **Retorna:**
    - crise_raiz: Nome da crise
    - count: Quantidade de diagnósticos
    - percentage: Percentual do total
    """
    distribution = await analytics_service.get_crises_distribution()
    return distribution


@router.get("/areas-silenciadas", response_model=List[AreaSilenciadaItem])
async def get_areas_silenciadas():
    """
    Retorna heatmap de áreas mais silenciadas pelos usuários.
    
    **Retorna:**
    - area_id: ID da área (1-12)
    - area_name: Nome da área
    - silence_count: Quantidade de vezes silenciada
    - percentage: Percentual do total
    """
    heatmap = await analytics_service.get_areas_silenciadas_heatmap()
    return heatmap


@router.get("/metrics/aggregated")
async def get_aggregated_metrics(
    start_date: Optional[str] = Query(
        default=None, 
        description="Data inicial (YYYY-MM-DD). Padrão: 30 dias atrás"
    ),
    end_date: Optional[str] = Query(
        default=None, 
        description="Data final (YYYY-MM-DD). Padrão: hoje"
    ),
    metric_type: str = Query(
        default="daily", 
        regex="^(daily|weekly|monthly)$",
        description="Tipo de métrica"
    ),
):
    """
    Retorna métricas agregadas (pré-computadas) para um período.
    
    **Útil para:**
    - Gráficos históricos
    - Análise de tendências
    - Reports mensais
    """
    # Parse dates
    start = date.fromisoformat(start_date) if start_date else None
    end = date.fromisoformat(end_date) if end_date else None
    
    metrics = await analytics_service.get_aggregated_metrics(
        start_date=start,
        end_date=end,
        metric_type=metric_type
    )
    return metrics


@router.get("/kpis")
async def get_kpis():
    """
    Retorna KPIs principais (números grandes para cards).
    
    **Retorna:**
    - Total de diagnósticos iniciados
    - Total de diagnósticos completados
    - Taxa de conclusão média
    - Motor mais comum
    - Crise mais comum
    - Área mais silenciada
    """
    # Métricas dos últimos 30 dias
    realtime = await analytics_service.get_realtime_metrics(days=30)
    motores = await analytics_service.get_motores_distribution()
    crises = await analytics_service.get_crises_distribution()
    areas = await analytics_service.get_areas_silenciadas_heatmap()
    
    total_started = sum(day.get("total_diagnostics", 0) for day in realtime)
    total_completed = sum(day.get("completed", 0) for day in realtime)
    avg_completion_rate = (
        sum(day.get("completion_rate", 0) for day in realtime) / len(realtime)
        if realtime else 0
    )
    
    motor_mais_comum = motores[0] if motores else {"motor_dominante": "N/A", "count": 0}
    crise_mais_comum = crises[0] if crises else {"crise_raiz": "N/A", "count": 0}
    area_mais_silenciada = areas[0] if areas else {"area_name": "N/A", "silence_count": 0}
    
    return {
        "period_days": 30,
        "total_diagnostics_started": total_started,
        "total_diagnostics_completed": total_completed,
        "avg_completion_rate": round(avg_completion_rate, 2),
        "motor_mais_comum": {
            "name": motor_mais_comum.get("motor_dominante"),
            "count": motor_mais_comum.get("count"),
        },
        "crise_mais_comum": {
            "name": crise_mais_comum.get("crise_raiz"),
            "count": crise_mais_comum.get("count"),
        },
        "area_mais_silenciada": {
            "name": area_mais_silenciada.get("area_name"),
            "count": area_mais_silenciada.get("silence_count"),
        },
    }


@router.post("/aggregate")
async def trigger_aggregation(
    target_date: Optional[str] = Query(
        default=None,
        description="Data para agregar (YYYY-MM-DD). Padrão: ontem"
    )
):
    """
    Trigger manual de agregação de métricas.
    
    **Uso:**
    - Normalmente executado via CRON diariamente
    - Endpoint útil para reprocessamento manual
    """
    target = date.fromisoformat(target_date) if target_date else None
    await analytics_service.aggregate_metrics_for_date(target)
    return {"status": "success", "date": target or (date.today() - timedelta(days=1))}
