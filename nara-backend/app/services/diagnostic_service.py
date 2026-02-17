"""Serviço de orquestração do diagnóstico."""
from typing import Any, Dict, Optional

from app.config import settings
from app.rag.pipeline import NaraDiagnosticPipeline
from app.services.email_service import EmailService

pipeline = NaraDiagnosticPipeline()
email_service = EmailService()


class DiagnosticService:
    """Interface de alto nível para operações de diagnóstico."""

    async def start_diagnostic(
        self,
        email: str,
        full_name: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        consent_privacy: bool = False,
        consent_marketing: bool = False,
        device_info: Optional[Dict[str, Any]] = None,
        utm_source: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Inicia um novo diagnóstico."""
        return await pipeline.start(
            email=email,
            full_name=full_name,
            user_id=user_id,
            session_id=session_id,
            consent_privacy=consent_privacy,
            consent_marketing=consent_marketing,
            device_info=device_info,
            utm_source=utm_source,
        )

    async def submit_answer(
        self,
        diagnostic_id: str,
        question_id: int,
        question_text: str,
        question_area: str,
        answer_text: Optional[str] = None,
        answer_scale: Optional[int] = None,
        response_time_seconds: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Submete uma resposta."""
        return await pipeline.submit_answer(
            diagnostic_id=diagnostic_id,
            question_id=question_id,
            question_text=question_text,
            question_area=question_area,
            answer_text=answer_text,
            answer_scale=answer_scale,
            response_time_seconds=response_time_seconds,
        )

    async def get_next_questions(self, diagnostic_id: str) -> Dict[str, Any]:
        """Gera perguntas da próxima fase."""
        return await pipeline.generate_next_phase(diagnostic_id)

    async def check_eligibility(self, diagnostic_id: str) -> Dict[str, Any]:
        """Verifica elegibilidade para finalização."""
        result = await pipeline.check_eligibility(diagnostic_id)
        return {
            "can_finish": result.can_finish,
            "criteria": {
                "questions": {
                    "current": result.total_answers,
                    "required": settings.MIN_QUESTIONS_TO_FINISH,
                    "percentage": result.questions_progress,
                    "met": result.total_answers >= settings.MIN_QUESTIONS_TO_FINISH,
                },
                "words": {
                    "current": result.total_words,
                    "required": settings.MIN_WORDS_TO_FINISH,
                    "percentage": result.words_progress,
                    "met": result.total_words >= settings.MIN_WORDS_TO_FINISH,
                },
                "coverage": {
                    "current": result.areas_covered,
                    "required": settings.MIN_AREAS_COVERED,
                    "percentage": result.coverage_progress,
                    "met": result.areas_covered >= settings.MIN_AREAS_COVERED,
                    "missing_areas": result.missing_areas,
                },
            },
            "overall_progress": result.overall_progress,
        }

    async def finish_diagnostic(self, diagnostic_id: str) -> Dict[str, Any]:
        """Finaliza o diagnóstico e gera relatório."""
        report = await pipeline.finish(diagnostic_id)

        from app.database import supabase

        diag = (
            supabase.table("diagnostics")
            .select("email, full_name, result_token")
            .eq("id", diagnostic_id)
            .single()
            .execute()
        )
        if diag.data and report:
            try:
                await email_service.send_diagnostic_result(
                    to=diag.data["email"],
                    user_name=diag.data.get("full_name"),
                    diagnostic_id=diagnostic_id,
                    result_token=diag.data.get("result_token", ""),
                    overall_score=report.get("overall_score", 0),
                    summary=(report.get("executive_summary") or "")[:500],
                )
            except Exception:
                pass

        return report

    async def get_result(self, diagnostic_id: str) -> Optional[Dict[str, Any]]:
        """Obtém resultado de um diagnóstico finalizado."""
        from app.database import supabase

        result = (
            supabase.table("diagnostic_results")
            .select("detailed_analysis")
            .eq("diagnostic_id", diagnostic_id)
            .single()
            .execute()
        )
        if not result.data:
            return None
        return result.data.get("detailed_analysis")

    async def get_result_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Obtém resultado pelo token público."""
        from app.database import supabase

        diag_result = (
            supabase.table("diagnostics")
            .select("id")
            .eq("result_token", token)
            .single()
            .execute()
        )
        if not diag_result.data:
            return None
        return await self.get_result(str(diag_result.data["id"]))

    async def check_existing_diagnostic(self, email: str) -> Dict[str, Any]:
        """Verifica se existe diagnóstico em andamento para o email."""
        from app.database import supabase

        result = (
            supabase.table("diagnostics")
            .select("id, status, current_phase, total_answers, created_at")
            .eq("email", email)
            .eq("status", "in_progress")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if result.data and len(result.data) > 0:
            d = result.data[0]
            return {
                "exists": True,
                "diagnostic_id": str(d["id"]),
                "status": d["status"],
                "current_phase": d["current_phase"],
                "total_answers": d["total_answers"],
                "started_at": d["created_at"],
            }
        return {"exists": False}

    async def get_current_state(self, diagnostic_id: str) -> Dict[str, Any]:
        """Retorna o estado atual do diagnóstico para retomada."""
        from app.core.constants import BASELINE_QUESTIONS

        from app.database import supabase

        diag_result = (
            supabase.table("diagnostics")
            .select("*")
            .eq("id", diagnostic_id)
            .single()
            .execute()
        )
        if not diag_result.data:
            raise ValueError("Diagnóstico não encontrado")
        diagnostic = diag_result.data
        current_q = diagnostic.get("current_question", 0)
        phase = diagnostic.get("current_phase", 1)
        result_token = diagnostic.get("result_token")
        if phase == 1:
            questions = BASELINE_QUESTIONS[current_q:]
            questions = [
                {
                    "id": q["id"],
                    "area": q["area"],
                    "type": q["type"],
                    "text": q["text"],
                    "scale_labels": q.get("scale_labels"),
                }
                for q in questions
            ]
        else:
            # Para fases 2+, as perguntas vêm de current_phase_questions (persistidas ao gerar)
            raw = diagnostic.get("current_phase_questions") or []
            remaining = raw[current_q:] if isinstance(raw, list) else []
            questions = [
                {
                    "id": q.get("id", (phase - 1) * 15 + current_q + i),
                    "area": q.get("area", "Geral"),
                    "type": q.get("type", "open_long"),
                    "text": q.get("text", ""),
                    "scale_labels": q.get("scale_labels"),
                }
                for i, q in enumerate(remaining)
            ]
        total_answers = diagnostic.get("total_answers", 0)
        total_words = diagnostic.get("total_words", 0)
        areas_covered = diagnostic.get("areas_covered") or []
        areas_count = len(areas_covered) if isinstance(areas_covered, list) else 0
        eligibility = await self.check_eligibility(diagnostic_id)
        return {
            "diagnostic_id": diagnostic_id,
            "result_token": result_token,
            "email": diagnostic.get("email"),  # Adicionar email para SaveAndExitButton
            "status": diagnostic["status"],
            "current_phase": phase,
            "current_question": current_q,
            "total_answers": total_answers,
            "total_words": total_words,
            "areas_covered": areas_covered,
            "questions": questions,
            "can_finish": eligibility["can_finish"],
            "progress": {
                "overall": min(100, eligibility["overall_progress"]),
                "questions": min(100, (total_answers / max(1, settings.MIN_QUESTIONS_TO_FINISH)) * 100),
                "words": min(100, (total_words / max(1, settings.MIN_WORDS_TO_FINISH)) * 100),
                "coverage": min(100, (areas_count / max(1, settings.MIN_AREAS_COVERED)) * 100),
            },
        }
