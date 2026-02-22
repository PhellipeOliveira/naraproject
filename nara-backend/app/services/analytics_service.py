"""
Serviço de Analytics e Métricas do NARA.
Tracking de eventos e geração de relatórios.
"""
import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

from app.database import supabase

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Serviço para tracking de eventos e métricas."""
    
    async def track_event(
        self,
        event_name: str,
        event_category: str,
        diagnostic_id: Optional[str] = None,
        session_id: Optional[str] = None,
        event_data: Optional[Dict[str, Any]] = None,
        user_agent: Optional[str] = None,
        utm_source: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Registra um evento de analytics.
        
        Args:
            event_name: Nome do evento (ex: 'diagnostic_started', 'answer_submitted')
            event_category: Categoria ('diagnostic', 'user', 'navigation', 'error', 'conversion')
            diagnostic_id: ID do diagnóstico (opcional)
            session_id: ID da sessão
            event_data: Dados adicionais do evento (JSONB)
            user_agent: User agent do browser
            utm_source: Source de marketing
            
        Returns:
            Dados do evento criado
        """
        try:
            event = {
                "event_name": event_name,
                "event_category": event_category,
                "diagnostic_id": diagnostic_id,
                "session_id": session_id,
                "event_data": event_data or {},
                "user_agent": user_agent,
                "utm_source": utm_source,
            }
            
            result = supabase.table("analytics_events").insert(event).execute()
            logger.info(f"Event tracked: {event_name} (category: {event_category})")
            return result.data[0] if result.data else {}
            
        except Exception as e:
            logger.error(f"Error tracking event {event_name}: {e}")
            # Não falhar silenciosamente - analytics não deve quebrar o fluxo
            return {}
    
    async def get_realtime_metrics(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Obtém métricas em tempo real dos últimos N dias.
        
        Args:
            days: Número de dias para buscar
            
        Returns:
            Lista de métricas por dia
        """
        try:
            result = supabase.table("analytics_realtime").select("*").execute()
            return result.data[:days] if result.data else []
        except Exception as e:
            logger.error(f"Error fetching realtime metrics: {e}")
            return []
    
    async def get_motores_distribution(self) -> List[Dict[str, Any]]:
        """
        Obtém distribuição de motores motivacionais.
        
        Returns:
            Lista com contagem e percentual por motor
        """
        try:
            result = supabase.table("analytics_motores_distribution").select("*").execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error fetching motores distribution: {e}")
            return []
    
    async def get_crises_distribution(self) -> List[Dict[str, Any]]:
        """
        Obtém distribuição de crises raiz.
        
        Returns:
            Lista com contagem e percentual por crise
        """
        try:
            result = supabase.table("analytics_crises_distribution").select("*").execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error fetching crises distribution: {e}")
            return []
    
    async def get_areas_silenciadas_heatmap(self) -> List[Dict[str, Any]]:
        """
        Obtém heatmap de áreas silenciadas.
        
        Returns:
            Lista com área, contagem e percentual
        """
        try:
            result = supabase.table("analytics_areas_silenciadas").select("*").execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error fetching areas silenciadas: {e}")
            return []
    
    async def get_aggregated_metrics(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        metric_type: str = "daily"
    ) -> List[Dict[str, Any]]:
        """
        Obtém métricas agregadas (pré-computadas).
        
        Args:
            start_date: Data inicial (padrão: 30 dias atrás)
            end_date: Data final (padrão: hoje)
            metric_type: Tipo de métrica ('daily', 'weekly', 'monthly')
            
        Returns:
            Lista de métricas agregadas
        """
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        try:
            result = (
                supabase.table("analytics_metrics")
                .select("*")
                .eq("metric_type", metric_type)
                .gte("date", start_date.isoformat())
                .lte("date", end_date.isoformat())
                .order("date", desc=True)
                .execute()
            )
            return result.data or []
        except Exception as e:
            logger.error(f"Error fetching aggregated metrics: {e}")
            return []
    
    async def get_dashboard_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        Obtém resumo completo para dashboard (métricas principais).
        
        Returns:
            Dicionário com todas as métricas principais
        """
        try:
            # Métricas dos últimos N dias
            realtime = await self.get_realtime_metrics(days=days)
            
            # Distribuições
            motores = await self.get_motores_distribution()
            crises = await self.get_crises_distribution()
            areas_silenciadas = await self.get_areas_silenciadas_heatmap()
            
            # Totalizadores
            total_diagnostics = sum(day.get("total_diagnostics", 0) for day in realtime)
            total_completed = sum(day.get("completed", 0) for day in realtime)
            avg_completion_rate = (
                sum(day.get("completion_rate", 0) for day in realtime) / len(realtime)
                if realtime else 0
            )
            
            return {
                "period": {
                    "days": days,
                    "start_date": (date.today() - timedelta(days=max(days - 1, 0))).isoformat(),
                    "end_date": date.today().isoformat(),
                },
                "totals": {
                    "diagnostics_started": total_diagnostics,
                    "diagnostics_completed": total_completed,
                    "completion_rate": round(avg_completion_rate, 2),
                },
                "realtime_metrics": realtime,
                "motores_distribution": motores,
                "crises_distribution": crises,
                "areas_silenciadas": areas_silenciadas,
            }
        except Exception as e:
            logger.error(f"Error generating dashboard summary: {e}")
            return {}

    async def get_recent_completed_diagnostics(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Lista diagnósticos completados mais recentes para painel do analista."""
        try:
            rows = (
                supabase.table("diagnostic_results")
                .select("diagnostic_id, motor_dominante, crise_raiz, phase_identified, created_at")
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return rows.data or []
        except Exception as e:
            logger.error(f"Error fetching recent diagnostics: {e}")
            return []
    
    async def aggregate_metrics_for_date(self, target_date: Optional[date] = None):
        """
        Agrega métricas para uma data específica.
        Deve ser executado via CRON diariamente.
        
        Args:
            target_date: Data para agregar (padrão: ontem)
        """
        if not target_date:
            target_date = date.today() - timedelta(days=1)
        
        try:
            # Executar função SQL de agregação
            supabase.rpc("aggregate_daily_metrics", {
                "target_date": target_date.isoformat()
            }).execute()
            logger.info(f"Metrics aggregated for {target_date}")
        except Exception as e:
            logger.error(f"Error aggregating metrics for {target_date}: {e}")
            raise


# Instância global do serviço
analytics_service = AnalyticsService()


# ============================================
# Helper Functions para Tracking Comum
# ============================================

async def track_diagnostic_started(
    diagnostic_id: str,
    session_id: str,
    utm_source: Optional[str] = None
):
    """Track: Diagnóstico iniciado."""
    await analytics_service.track_event(
        event_name="diagnostic_started",
        event_category="diagnostic",
        diagnostic_id=diagnostic_id,
        session_id=session_id,
        utm_source=utm_source,
    )


async def track_answer_submitted(
    diagnostic_id: str,
    question_id: int,
    word_count: int,
    area: str,
):
    """Track: Resposta submetida."""
    await analytics_service.track_event(
        event_name="answer_submitted",
        event_category="diagnostic",
        diagnostic_id=diagnostic_id,
        event_data={
            "question_id": question_id,
            "word_count": word_count,
            "area": area,
        },
    )


async def track_phase_completed(
    diagnostic_id: str,
    phase: int,
    total_answers: int,
):
    """Track: Fase completada."""
    await analytics_service.track_event(
        event_name="phase_completed",
        event_category="diagnostic",
        diagnostic_id=diagnostic_id,
        event_data={
            "phase": phase,
            "total_answers": total_answers,
        },
    )


async def track_diagnostic_finished(
    diagnostic_id: str,
    motor_dominante: str,
    crise_raiz: str,
    total_words: int,
    completion_time_minutes: int,
):
    """Track: Diagnóstico finalizado."""
    await analytics_service.track_event(
        event_name="diagnostic_finished",
        event_category="conversion",
        diagnostic_id=diagnostic_id,
        event_data={
            "motor_dominante": motor_dominante,
            "crise_raiz": crise_raiz,
            "total_words": total_words,
            "completion_time_minutes": completion_time_minutes,
        },
    )


async def track_result_viewed(
    diagnostic_id: str,
    result_token: str,
    motor_dominante: str,
):
    """Track: Resultado visualizado."""
    await analytics_service.track_event(
        event_name="result_viewed",
        event_category="user",
        diagnostic_id=diagnostic_id,
        event_data={
            "result_token": result_token,
            "motor_dominante": motor_dominante,
        },
    )


async def track_nps_submitted(
    diagnostic_id: str,
    nps_score: int,
):
    """Track: NPS submetido."""
    await analytics_service.track_event(
        event_name="nps_submitted",
        event_category="user",
        diagnostic_id=diagnostic_id,
        event_data={
            "nps_score": nps_score,
        },
    )
