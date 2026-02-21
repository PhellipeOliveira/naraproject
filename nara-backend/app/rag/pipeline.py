"""
Pipeline completo de diagnóstico NARA.
Orquestra todas as etapas do fluxo de diagnóstico.
"""
from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.config import settings
from app.core.constants import AREAS
from app.database import supabase
from app.rag.analyzer import analyze_answers_context
from app.rag.generator import generate_adaptive_questions, generate_final_report
from app.rag.retriever import retrieve_for_question_generation, retrieve_for_report_generation

logger = logging.getLogger(__name__)


def _area_name_to_id(area_name: str) -> int:
    """Mapeia nome da área para id (1-based) conforme tabela areas.
    Retorna 0 para áreas não mapeadas (ex.: 'Geral'), que são ignoradas no areas_covered."""
    if not area_name or area_name not in AREAS:
        return 0
    return AREAS.index(area_name) + 1


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

    AREAS = AREAS  # 12 Áreas Estruturantes (01_FUNDAMENTOS); mesma ordem que tabela areas

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
        email_normalized = (email or "").strip().lower()

        diagnostic_data: Dict[str, Any] = {
            "user_id": user_id,
            "anonymous_session_id": session_id if not user_id else None,
            "email": email_normalized,
            "full_name": full_name,
            "status": "in_progress",
            "current_phase": 1,
            "current_question": 0,
            "current_phase_questions_count": 15,
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
        # Só persiste IDs das 12 áreas estruturantes; "Geral" não está em AREAS
        areas_covered_ids = [
            AREAS.index(a) + 1 for a in areas_covered_names if a in AREAS
        ]
        areas_for_eligibility = [a for a in areas_covered_names if a in AREAS]

        supabase.table("diagnostics").update({
            "total_answers": new_total,
            "total_words": new_words,
            "areas_covered": areas_covered_ids if areas_covered_ids else [],
            "scores_by_area": scores_by_area,
            "current_question": new_current_question,
            "last_activity_at": datetime.utcnow().isoformat(),
        }).eq("id", diagnostic_id).execute()

        eligibility = self._check_eligibility(new_total, new_words, areas_for_eligibility)
        phase_questions_count = diagnostic.get("current_phase_questions_count") or settings.QUESTIONS_PER_PHASE
        phase_complete = new_current_question >= phase_questions_count

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
            "areas_covered": len(areas_for_eligibility),
        }

    MAX_PHASE = 4  # Constraint do banco: current_phase BETWEEN 1 AND 4

    async def generate_next_phase(self, diagnostic_id: str) -> Dict[str, Any]:
        """Gera perguntas para a próxima fase usando RAG+LLM."""
        diag_result = (
            supabase.table("diagnostics").select("*").eq("id", diagnostic_id).single().execute()
        )
        diagnostic = diag_result.data
        if not diagnostic:
            raise ValueError("Diagnóstico não encontrado")

        current = diagnostic.get("current_phase", 1)
        if current >= self.MAX_PHASE:
            raise ValueError(
                "Não há próxima fase. Você completou todas as fases. Finalize o diagnóstico para ver seu resultado."
            )

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

        # Análise contextual para enriquecer geração de perguntas
        logger.info("Analisando contexto das respostas para próxima fase")
        context_analysis = await analyze_answers_context(answers, user_profile=None)
        
        patterns = self._identify_patterns(answers)
        # Enriquecer com insights do analyzer
        if context_analysis.get("motor_dominante"):
            patterns.append(f"Motor dominante: {context_analysis['motor_dominante']}")
        if context_analysis.get("clusters_identificados"):
            patterns.append(f"Clusters: {', '.join(context_analysis['clusters_identificados'][:2])}")
        
        next_phase = diagnostic["current_phase"] + 1

        rag_context = await retrieve_for_question_generation(
            user_responses=answers,
            underrepresented_areas=underrepresented,
            phase=next_phase,
        )
        if not rag_context or not rag_context.strip():
            logger.warning(
                "RAG context empty for phase %s. Ensure knowledge_chunks has rows with embeddings.",
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
            "current_phase_questions_count": len(questions),
            "current_phase_questions": questions,
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
        coverage_progress = min(
            100, (len(set(areas_covered)) / settings.MIN_AREAS_COVERED) * 100
        )
        overall_progress = min(
            100,
            questions_progress * 0.4 + words_progress * 0.3 + coverage_progress * 0.3,
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

    def _safe_answer_value(self, answer: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna answer_value como dict; suporta JSON string vinda do DB."""
        raw = answer.get("answer_value")
        if raw is None:
            return {}
        if isinstance(raw, dict):
            return raw
        if isinstance(raw, str):
            try:
                return json.loads(raw) if raw else {}
            except (ValueError, TypeError):
                return {}
        return {}

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
            scales = []
            for a in area_answers:
                val = self._safe_answer_value(a)
                scale = val.get("scale")
                if scale is not None and isinstance(scale, (int, float)):
                    scales.append(float(scale))
            avg_scale = sum(scales) / len(scales) if scales else None
            score = (avg_scale * 2) if avg_scale is not None else 5.0

            scores[area] = {
                "score": round(score, 1),
                "questions_answered": len(area_answers),
                "has_text_responses": any(
                    bool(self._safe_answer_value(a).get("text")) for a in area_answers
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
            # Análise contextual das respostas (Motor, Clusters, Âncoras, etc.)
            logger.info("Analisando contexto das respostas para diagnostic %s", diagnostic_id)
            context_analysis = await analyze_answers_context(answers, user_profile=None)
            
            # Manter scores por compatibilidade (LEGACY - usar vetor_estado)
            scores_by_area = await self._calculate_area_scores(diagnostic_id)
            
            # Usar analyzer para identificar padrões (complementa _identify_patterns)
            patterns = self._identify_patterns(answers)
            if context_analysis.get("sinais_conflito"):
                patterns.extend(context_analysis["sinais_conflito"])

            # Salvar análise intermediária no diagnóstico
            supabase.table("diagnostics").update({
                "analise_intermediaria": {
                    "motor_dominante": context_analysis.get("motor_dominante"),
                    "clusters_identificados": context_analysis.get("clusters_identificados", []),
                    "pontos_entrada": context_analysis.get("pontos_entrada", []),
                    "ancoras_sugeridas": context_analysis.get("ancoras_sugeridas", []),
                    "nivel_maturidade": context_analysis.get("nivel_maturidade"),
                    "tom_emocional": context_analysis.get("tom_emocional"),
                    "areas_criticas": context_analysis.get("areas_criticas", []),
                    "padroes": patterns,
                }
            }).eq("id", diagnostic_id).execute()

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

            # Extrair vetor de estado do report
            vetor_estado = report.get("vetor_estado", {})
            # overall_score no banco é NUMÉRICO; nunca enviar nome de estágio (ex.: "Desenvolver")
            raw_score = report.get("overall_score")
            overall_score_legacy = None
            if raw_score is not None and isinstance(raw_score, (int, float)):
                overall_score_legacy = float(raw_score)
            # Se o report não devolver número, deixar None ou padrão; phase_identified guarda o estágio (string)
            if overall_score_legacy is None:
                overall_score_legacy = 5.0  # padrão para compatibilidade com coluna NOT NULL se existir

            result_data = {
                "diagnostic_id": diagnostic_id,
                # Novos campos (V2)
                "vetor_estado": vetor_estado,
                "memorias_vermelhas": report.get("memorias_vermelhas", []),
                "areas_silenciadas": report.get("areas_silenciadas", []),
                "ancoras_sugeridas": report.get("ancoras_sugeridas", []),
                # Campos legacy (manter por compatibilidade) — overall_score sempre numérico
                "overall_score": overall_score_legacy,
                "area_scores": scores_by_area,
                "motor_scores": {
                    "dominante": vetor_estado.get("motor_dominante"),
                    "secundario": vetor_estado.get("motor_secundario"),
                },
                "phase_identified": report.get("phase_identified") or vetor_estado.get("estagio_jornada", "").lower(),
                "motor_dominante": vetor_estado.get("motor_dominante"),
                "motor_secundario": vetor_estado.get("motor_secundario"),
                "crise_raiz": vetor_estado.get("crise_raiz"),
                "ponto_entrada_ideal": vetor_estado.get("ponto_entrada_ideal"),
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
                "overall_score": result_data.get("overall_score"),  # Legacy
                "scores_by_area": scores_by_area,  # Legacy
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
