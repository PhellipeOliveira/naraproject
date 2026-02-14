"""
Pipeline completo de diagnóstico NARA.
Orquestra todas as etapas do fluxo de diagnóstico.
"""
from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.config import settings
from app.database import supabase
from app.rag.generator import generate_adaptive_questions, generate_final_report
from app.rag.retriever import retrieve_for_question_generation, retrieve_for_report_generation

logger = logging.getLogger(__name__)

# Áreas na mesma ordem que a tabela areas (id 1..12) para mapeamento
AREAS = [
    "Saúde Física",
    "Saúde Mental",
    "Saúde Espiritual",
    "Vida Pessoal",
    "Vida Amorosa",
    "Vida Familiar",
    "Vida Social",
    "Vida Profissional",
    "Finanças",
    "Educação",
    "Inovação",
    "Lazer",
]


def _area_name_to_id(area_name: str) -> int:
    """Mapeia nome da área para id (1-based) conforme tabela areas."""
    try:
        return AREAS.index(area_name) + 1
    except ValueError:
        return 0


def _area_ids_to_names(area_ids: List[int]) -> List[str]:
    """Converte lista de IDs (1-based) para nomes."""
    return [AREAS[i - 1] for i in area_ids if 1 <= i <= len(AREAS)]


@dataclass
class EligibilityResult:
    """Resultado da verificação de elegibilidade."""

    can_finish: bool
    total_answers: int
    total_words: int
    areas_covered: int
    missing_areas: List[str]
    questions_progress: float
    words_progress: float
    coverage_progress: float
    overall_progress: float


class NaraDiagnosticPipeline:
    """
    Pipeline principal do diagnóstico NARA.

    Fluxo:
    1. start() -> Cria diagnóstico + retorna perguntas Fase 1
    2. submit_answer() -> Processa resposta + atualiza scores
    3. generate_next_phase() -> Gera perguntas adaptativas via RAG+LLM
    4. check_eligibility() -> Verifica se pode finalizar
    5. finish() -> Gera relatório final via RAG+LLM
    """

    AREAS = AREAS

    def __init__(self) -> None:
        self.baseline_questions = self._load_baseline_questions()

    def _load_baseline_questions(self) -> List[Dict[str, Any]]:
        """Carrega as perguntas fixas da Fase 1."""
        from app.core.constants import BASELINE_QUESTIONS

        return BASELINE_QUESTIONS

    async def start(
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
        result_token = f"nara_{uuid.uuid4().hex[:12]}"

        diagnostic_data: Dict[str, Any] = {
            "user_id": user_id,
            "anonymous_session_id": session_id if not user_id else None,
            "email": email,
            "full_name": full_name,
            "status": "in_progress",
            "current_phase": 1,
            "current_question": 0,
            "total_answers": 0,
            "total_words": 0,
            "areas_covered": [],  # DB pode ser SMALLINT[]; Supabase aceita lista vazia
            "result_token": result_token,
            "consent_privacy": consent_privacy,
            "consent_marketing": consent_marketing,
            "device_info": device_info or {},
            "utm_source": utm_source,
        }

        result = supabase.table("diagnostics").insert(diagnostic_data).execute()
        diagnostic = result.data[0]

        logger.info("Started diagnostic %s for %s", diagnostic["id"], email)

        return {
            "diagnostic_id": str(diagnostic["id"]),
            "status": "in_progress",
            "phase": 1,
            "questions": self.baseline_questions,
            "total_questions": len(self.baseline_questions),
            "result_token": result_token,
        }

    def _get_areas_covered_names(self, diagnostic: Dict[str, Any]) -> List[str]:
        """Retorna areas_covered como lista de nomes (DB pode retornar IDs ou nomes)."""
        raw = diagnostic.get("areas_covered") or []
        if not raw:
            return []
        if isinstance(raw[0], (int, float)):
            return _area_ids_to_names([int(x) for x in raw])
        return list(raw)

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
        """Submete ou atualiza uma resposta (permite voltar e alterar resposta)."""
        diag_result = (
            supabase.table("diagnostics").select("*").eq("id", diagnostic_id).single().execute()
        )
        diagnostic = diag_result.data
        if not diagnostic:
            raise ValueError("Diagnóstico não encontrado")

        word_count = len((answer_text or "").split())
        answer_value: Dict[str, Any] = {
            "text": answer_text,
            "scale": answer_scale,
            "words": word_count,
        }

        # Verifica se já existe resposta para esta pergunta (voltar e alterar)
        existing = (
            supabase.table("answers")
            .select("id, word_count")
            .eq("diagnostic_id", diagnostic_id)
            .eq("question_id", question_id)
            .execute()
        )
        is_update = existing.data and len(existing.data) > 0
        old_word_count = int(existing.data[0]["word_count"] or 0) if is_update else 0

        answer_data = {
            "diagnostic_id": diagnostic_id,
            "question_id": question_id,
            "question_text": question_text,
            "question_area": question_area,
            "question_phase": diagnostic["current_phase"],
            "answer_value": answer_value,
            "word_count": word_count,
            "response_time_seconds": response_time_seconds,
        }

        if is_update:
            supabase.table("answers").update({
                "question_text": answer_data["question_text"],
                "question_area": answer_data["question_area"],
                "question_phase": answer_data["question_phase"],
                "answer_value": answer_data["answer_value"],
                "word_count": answer_data["word_count"],
                "response_time_seconds": answer_data["response_time_seconds"],
            }).eq("diagnostic_id", diagnostic_id).eq("question_id", question_id).execute()
            new_total = diagnostic["total_answers"]
            new_words = diagnostic["total_words"] - old_word_count + word_count
            new_current_question = diagnostic["current_question"]
        else:
            supabase.table("answers").insert(answer_data).execute()
            new_total = diagnostic["total_answers"] + 1
            new_words = diagnostic["total_words"] + word_count
            new_current_question = diagnostic["current_question"] + 1

        areas_covered_names = self._get_areas_covered_names(diagnostic)
        if question_area not in areas_covered_names:
            areas_covered_names = list(areas_covered_names) + [question_area]

        scores_by_area = await self._calculate_area_scores(diagnostic_id)
        areas_covered_ids = [_area_name_to_id(a) for a in areas_covered_names if _area_name_to_id(a)]

        supabase.table("diagnostics").update({
            "total_answers": new_total,
            "total_words": new_words,
            "areas_covered": areas_covered_ids if areas_covered_ids else [],
            "scores_by_area": scores_by_area,
            "current_question": new_current_question,
            "last_activity_at": datetime.utcnow().isoformat(),
        }).eq("id", diagnostic_id).execute()

        eligibility = self._check_eligibility(new_total, new_words, areas_covered_names)
        phase_complete = new_current_question >= settings.QUESTIONS_PER_PHASE

        logger.info(
            "Answer %s for %s. Total: %s, Phase complete: %s",
            "updated" if is_update else "submitted",
            diagnostic_id,
            new_total,
            phase_complete,
        )

        return {
            "status": "eligible" if eligibility.can_finish else "in_progress",
            "can_finish": eligibility.can_finish,
            "phase_complete": phase_complete,
            "progress": {
                "overall": eligibility.overall_progress,
                "questions": eligibility.questions_progress,
                "words": eligibility.words_progress,
                "coverage": eligibility.coverage_progress,
            },
            "total_answers": new_total,
            "total_words": new_words,
            "areas_covered": len(areas_covered_names),
        }

    async def generate_next_phase(self, diagnostic_id: str) -> Dict[str, Any]:
        """Gera perguntas para a próxima fase usando RAG+LLM."""
        diag_result = (
            supabase.table("diagnostics").select("*").eq("id", diagnostic_id).single().execute()
        )
        diagnostic = diag_result.data
        if not diagnostic:
            raise ValueError("Diagnóstico não encontrado")

        answers_result = (
            supabase.table("answers")
            .select("*")
            .eq("diagnostic_id", diagnostic_id)
            .order("answered_at")
            .execute()
        )
        answers = answers_result.data or []

        areas_count: Dict[str, int] = {}
        for a in answers:
            area = a.get("question_area", "Geral")
            areas_count[area] = areas_count.get(area, 0) + 1

        underrepresented = [
            area for area in self.AREAS
            if areas_count.get(area, 0) < 3
        ]

        patterns = self._identify_patterns(answers)
        next_phase = diagnostic["current_phase"] + 1

        rag_context = await retrieve_for_question_generation(
            user_responses=answers,
            underrepresented_areas=underrepresented,
            phase=next_phase,
        )
        if not rag_context or not rag_context.strip():
            logger.warning(
                "RAG context empty for phase %s. Ensure knowledge_chunks has rows with embeddings and run scripts/seed_knowledge_chunks.",
                next_phase,
            )

        questions = await generate_adaptive_questions(
            user_responses=answers,
            underrepresented_areas=underrepresented,
            identified_patterns=patterns,
            rag_context=rag_context,
            phase=next_phase,
        )

        supabase.table("diagnostics").update({
            "current_phase": next_phase,
            "current_question": 0,
        }).eq("id", diagnostic_id).execute()

        logger.info("Generated %s questions for phase %s", len(questions), next_phase)

        return {
            "phase": next_phase,
            "questions": questions,
            "total_questions": len(questions),
        }

    async def check_eligibility(self, diagnostic_id: str) -> EligibilityResult:
        """Verifica se o diagnóstico pode ser finalizado."""
        result = (
            supabase.table("diagnostics")
            .select("total_answers, total_words, areas_covered")
            .eq("id", diagnostic_id)
            .single()
            .execute()
        )
        data = result.data
        if not data:
            raise ValueError("Diagnóstico não encontrado")

        raw_areas = data.get("areas_covered") or []
        if raw_areas and isinstance(raw_areas[0], (int, float)):
            areas_covered_names = _area_ids_to_names([int(x) for x in raw_areas])
        else:
            areas_covered_names = list(raw_areas)

        return self._check_eligibility(
            data["total_answers"],
            data["total_words"],
            areas_covered_names,
        )

    def _check_eligibility(
        self,
        total_answers: int,
        total_words: int,
        areas_covered: List[str],
    ) -> EligibilityResult:
        """Verifica critérios de elegibilidade."""
        quantity_ok = (
            total_answers >= settings.MIN_QUESTIONS_TO_FINISH
            or total_words >= settings.MIN_WORDS_TO_FINISH
        )
        coverage_ok = len(set(areas_covered)) >= settings.MIN_AREAS_COVERED

        questions_progress = min(
            100, (total_answers / settings.MIN_QUESTIONS_TO_FINISH) * 100
        )
        words_progress = min(100, (total_words / settings.MIN_WORDS_TO_FINISH) * 100)
        coverage_progress = (len(set(areas_covered)) / settings.MIN_AREAS_COVERED) * 100
        overall_progress = (
            questions_progress * 0.4 + words_progress * 0.3 + coverage_progress * 0.3
        )

        missing_areas = [a for a in self.AREAS if a not in areas_covered]

        return EligibilityResult(
            can_finish=quantity_ok and coverage_ok,
            total_answers=total_answers,
            total_words=total_words,
            areas_covered=len(set(areas_covered)),
            missing_areas=missing_areas,
            questions_progress=questions_progress,
            words_progress=words_progress,
            coverage_progress=coverage_progress,
            overall_progress=overall_progress,
        )

    async def _calculate_area_scores(self, diagnostic_id: str) -> Dict[str, Any]:
        """Calcula scores por área baseado nas respostas."""
        answers_result = (
            supabase.table("answers").select("*").eq("diagnostic_id", diagnostic_id).execute()
        )
        answers = answers_result.data or []
        scores: Dict[str, Any] = {}

        for area in self.AREAS:
            area_answers = [a for a in answers if a.get("question_area") == area]
            if not area_answers:
                continue
            scales = [
                a["answer_value"]["scale"]
                for a in area_answers
                if (a.get("answer_value") or {}).get("scale") is not None
            ]
            avg_scale = sum(scales) / len(scales) if scales else None
            score = (avg_scale * 2) if avg_scale is not None else 5.0

            scores[area] = {
                "score": round(score, 1),
                "questions_answered": len(area_answers),
                "has_text_responses": any(
                    (a.get("answer_value") or {}).get("text") for a in area_answers
                ),
            }

        return scores

    def _identify_patterns(self, answers: List[Dict[str, Any]]) -> List[str]:
        """Identifica padrões nas respostas."""
        patterns: List[str] = []
        low_score_areas: List[str] = []
        for a in answers:
            scale = (a.get("answer_value") or {}).get("scale")
            if scale is not None and scale <= 2:
                low_score_areas.append(a.get("question_area", ""))

        if low_score_areas:
            most_common = max(set(low_score_areas), key=low_score_areas.count)
            if most_common:
                patterns.append(f"Possível área de crise: {most_common}")

        sabotage_keywords = ["sempre", "nunca", "não consigo", "impossível", "fracasso"]
        for a in answers:
            text = ((a.get("answer_value") or {}).get("text") or "").lower()
            for keyword in sabotage_keywords:
                if keyword in text:
                    patterns.append("Possível padrão de autossabotagem detectado")
                    break

        return list(set(patterns))

    async def finish(self, diagnostic_id: str) -> Dict[str, Any]:
        """Finaliza o diagnóstico e gera o relatório completo."""
        eligibility = await self.check_eligibility(diagnostic_id)
        if not eligibility.can_finish:
            raise ValueError(
                f"Diagnóstico não atende aos critérios mínimos. "
                f"Progresso: {eligibility.overall_progress:.1f}%"
            )

        diag_result = (
            supabase.table("diagnostics").select("*").eq("id", diagnostic_id).single().execute()
        )
        diagnostic = diag_result.data
        if not diagnostic:
            raise ValueError("Diagnóstico não encontrado")

        answers_result = (
            supabase.table("answers")
            .select("*")
            .eq("diagnostic_id", diagnostic_id)
            .order("answered_at")
            .execute()
        )
        answers = answers_result.data or []

        supabase.table("diagnostics").update({"status": "processing"}).eq(
            "id", diagnostic_id
        ).execute()

        try:
            scores_by_area = await self._calculate_area_scores(diagnostic_id)
            patterns = self._identify_patterns(answers)

            rag_context = await retrieve_for_report_generation(
                diagnostic_id=diagnostic_id,
                scores_by_area=scores_by_area,
                all_responses=answers,
            )

            report = await generate_final_report(
                all_responses=answers,
                scores_by_area=scores_by_area,
                identified_patterns=patterns,
                rag_context=rag_context,
            )

            result_data = {
                "diagnostic_id": diagnostic_id,
                "overall_score": report.get("overall_score"),
                "area_scores": scores_by_area,
                "motor_scores": {
                    "dominante": report.get("motor_dominante"),
                    "secundario": report.get("motor_secundario"),
                },
                "phase_identified": report.get("phase_identified"),
                "motor_dominante": report.get("motor_dominante"),
                "motor_secundario": report.get("motor_secundario"),
                "crise_raiz": report.get("crise_raiz"),
                "ponto_entrada_ideal": report.get("ponto_entrada_ideal"),
                "executive_summary": report.get("executive_summary"),
                "detailed_analysis": report,
                "recommendations": report.get("recommendations", []),
                "strengths": report.get("strengths", []),
                "opportunities": [
                    area.get("area_name", "")
                    for area in report.get("development_areas", [])
                ],
                "model_used": settings.OPENAI_MODEL_ANALYSIS,
            }

            supabase.table("diagnostic_results").insert(result_data).execute()

            supabase.table("diagnostics").update({
                "status": "completed",
                "overall_score": report.get("overall_score"),
                "scores_by_area": scores_by_area,
                "insights": report.get("executive_summary"),
                "completed_at": datetime.utcnow().isoformat(),
            }).eq("id", diagnostic_id).execute()

            logger.info(
                "Diagnostic %s completed with score %s",
                diagnostic_id,
                report.get("overall_score"),
            )
            return report

        except Exception as e:
            supabase.table("diagnostics").update({"status": "in_progress"}).eq(
                "id", diagnostic_id
            ).execute()
            logger.exception("Error finishing diagnostic %s: %s", diagnostic_id, e)
            raise
