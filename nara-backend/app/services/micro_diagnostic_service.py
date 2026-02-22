"""Serviço de micro-diagnóstico guiado (5 perguntas -> 5 perguntas -> resultado).

Estrutura esperada da tabela `micro_diagnostics`:
- id (uuid)
- diagnostic_id (uuid fk diagnostics.id)
- area (text)
- status (text: in_progress|completed)
- phase (int: 1|2)
- questions_phase1 (jsonb)
- answers_phase1 (jsonb)
- questions_phase2 (jsonb)
- answers_phase2 (jsonb)
- result (jsonb)
- created_at (timestamp)
"""
from __future__ import annotations

import json
from typing import Any

from openai import AsyncOpenAI

from app.config import settings
from app.core.constants import AREAS
from app.database import supabase
from app.rag.generator import generate_adaptive_questions
from app.rag.retriever import retrieve_relevant_chunks
from app.services.micro_report_service import INSIGHT_SYSTEM_PROMPT

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class MicroDiagnosticService:
    """Fluxo de micro-diagnóstico orientado por área com regra de 1 conclusão por usuário."""

    @staticmethod
    def _normalize_micro_questions(questions: list[dict[str, Any]], phase: int) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        base = 0 if phase == 1 else 5
        for idx, q in enumerate(questions[:5], start=1):
            out.append({
                "id": base + idx,
                "area": q.get("area", "Geral"),
                "type": "open_long",
                "text": q.get("text", ""),
                "follow_up_hint": q.get("follow_up_hint", ""),
            })
        return out

    @staticmethod
    def _diagnostic_id_from_token(token: str) -> str:
        diag_result = (
            supabase.table("diagnostics")
            .select("id")
            .eq("result_token", token)
            .single()
            .execute()
        )
        if not diag_result.data:
            raise ValueError("Token inválido.")
        return str(diag_result.data["id"])

    async def start_micro_diagnostic(self, token: str, area: str) -> dict[str, Any]:
        """Inicia micro-diagnóstico em uma área com 5 perguntas da fase 1."""
        if area not in AREAS:
            raise ValueError("Área inválida para micro-diagnóstico.")

        diagnostic_id = self._diagnostic_id_from_token(token)

        completed = (
            supabase.table("micro_diagnostics")
            .select("id")
            .eq("diagnostic_id", diagnostic_id)
            .eq("status", "completed")
            .limit(1)
            .execute()
        )
        if completed.data:
            raise ValueError("Usuário já possui um micro-diagnóstico concluído para este diagnóstico.")

        existing = (
            supabase.table("micro_diagnostics")
            .select("*")
            .eq("diagnostic_id", diagnostic_id)
            .eq("status", "in_progress")
            .limit(1)
            .execute()
        )
        if existing.data:
            micro = existing.data[0]
            phase = int(micro.get("phase") or 1)
            current_questions = (micro.get("questions_phase1") or []) if phase == 1 else (micro.get("questions_phase2") or [])
            return {
                "micro_id": str(micro["id"]),
                "status": micro.get("status", "in_progress"),
                "phase": phase,
                "questions": current_questions,
                "total_questions": len(current_questions),
            }

        area_answers = (
            supabase.table("answers")
            .select("question_area, answer_value")
            .eq("diagnostic_id", diagnostic_id)
            .eq("question_area", area)
            .order("answered_at")
            .execute()
        )
        answers = area_answers.data or []
        rag_chunks = await retrieve_relevant_chunks(
            query=f"micro diagnóstico da área {area} com intervenção metodológica",
            top_k=6,
            filter_chapter=area,
        )
        rag_context = "\n\n".join([c.get("content", "")[:700] for c in rag_chunks])

        phase1_questions = await generate_adaptive_questions(
            user_responses=answers,
            underrepresented_areas=[area],
            identified_patterns=[f"micro_diagnostico_area:{area}"],
            rag_context=rag_context,
            phase=1,
            adaptive_templates=[],
            max_questions=5,
        )
        phase1_questions = self._normalize_micro_questions(phase1_questions, phase=1)

        inserted = (
            supabase.table("micro_diagnostics")
            .insert({
                "diagnostic_id": diagnostic_id,
                "area": area,
                "status": "in_progress",
                "phase": 1,
                "questions_phase1": phase1_questions,
                "answers_phase1": [],
                "questions_phase2": [],
                "answers_phase2": [],
                "result": {},
            })
            .execute()
        )
        micro_row = (inserted.data or [{}])[0]
        return {
            "micro_id": str(micro_row.get("id")),
            "status": "in_progress",
            "phase": 1,
            "questions": phase1_questions,
            "total_questions": len(phase1_questions),
        }

    async def get_micro_diagnostic_state(self, token: str, micro_id: str) -> dict[str, Any]:
        """Obtém estado do micro-diagnóstico."""
        diagnostic_id = self._diagnostic_id_from_token(token)
        row = (
            supabase.table("micro_diagnostics")
            .select("*")
            .eq("id", micro_id)
            .eq("diagnostic_id", diagnostic_id)
            .single()
            .execute()
        )
        data = row.data
        if not data:
            raise ValueError("Micro-diagnóstico não encontrado.")
        phase = int(data.get("phase") or 1)
        status = data.get("status", "in_progress")
        if status == "completed":
            return {
                "micro_id": str(data["id"]),
                "status": status,
                "phase": phase,
                "questions": [],
                "total_questions": 0,
                "result": data.get("result") or {},
            }
        questions = (data.get("questions_phase1") or []) if phase == 1 else (data.get("questions_phase2") or [])
        return {
            "micro_id": str(data["id"]),
            "status": status,
            "phase": phase,
            "questions": questions,
            "total_questions": len(questions),
        }

    async def submit_phase_answers(
        self,
        token: str,
        micro_id: str,
        answers: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Submete respostas da fase atual; se fase 1, gera fase 2."""
        diagnostic_id = self._diagnostic_id_from_token(token)
        row = (
            supabase.table("micro_diagnostics")
            .select("*")
            .eq("id", micro_id)
            .eq("diagnostic_id", diagnostic_id)
            .single()
            .execute()
        )
        data = row.data
        if not data:
            raise ValueError("Micro-diagnóstico não encontrado.")
        if data.get("status") == "completed":
            raise ValueError("Micro-diagnóstico já finalizado.")

        area = data.get("area")
        phase = int(data.get("phase") or 1)

        if phase == 1:
            rag_chunks = await retrieve_relevant_chunks(
                query=f"aprofundamento metodológico na área {area} para fase 2 de micro diagnóstico",
                top_k=6,
                filter_chapter=area,
            )
            rag_context = "\n\n".join([c.get("content", "")[:700] for c in rag_chunks])
            llm_input_answers = [
                {
                    "question_area": a.get("question_area", area),
                    "question_text": a.get("question_text", ""),
                    "answer_value": {"text": a.get("answer_text", "")},
                }
                for a in answers
            ]
            phase2_questions = await generate_adaptive_questions(
                user_responses=llm_input_answers,
                underrepresented_areas=[area],
                identified_patterns=[f"micro_fase2:{area}"],
                rag_context=rag_context,
                phase=2,
                adaptive_templates=[],
                max_questions=5,
            )
            phase2_questions = self._normalize_micro_questions(phase2_questions, phase=2)

            supabase.table("micro_diagnostics").update({
                "answers_phase1": answers,
                "phase": 2,
                "questions_phase2": phase2_questions,
            }).eq("id", micro_id).execute()

            return {
                "micro_id": micro_id,
                "status": "in_progress",
                "phase": 2,
                "questions": phase2_questions,
                "total_questions": len(phase2_questions),
            }

        supabase.table("micro_diagnostics").update({
            "answers_phase2": answers,
        }).eq("id", micro_id).execute()

        return {
            "micro_id": micro_id,
            "status": "in_progress",
            "phase": 2,
            "questions": [],
            "total_questions": 0,
        }

    async def finish_micro_diagnostic(self, token: str, micro_id: str) -> dict[str, Any]:
        """Finaliza micro-diagnóstico e gera micro-relatório dedicado."""
        diagnostic_id = self._diagnostic_id_from_token(token)
        row = (
            supabase.table("micro_diagnostics")
            .select("*")
            .eq("id", micro_id)
            .eq("diagnostic_id", diagnostic_id)
            .single()
            .execute()
        )
        data = row.data
        if not data:
            raise ValueError("Micro-diagnóstico não encontrado.")
        if data.get("status") == "completed":
            return data.get("result") or {}

        phase1_answers = data.get("answers_phase1") or []
        phase2_answers = data.get("answers_phase2") or []
        if not phase1_answers or not phase2_answers:
            raise ValueError("Micro-diagnóstico incompleto. Conclua as duas fases antes de finalizar.")

        area = data.get("area")
        all_answers = phase1_answers + phase2_answers
        answers_text = "\n\n".join(
            [
                f"Pergunta: {a.get('question_text', '')}\nResposta: {a.get('answer_text', '')}"
                for a in all_answers
            ]
        )

        rag_chunks = await retrieve_relevant_chunks(
            query=f"micro diagnóstico final da área {area} com gap mx e intervenção tcc",
            top_k=8,
            filter_chapter=area,
        )
        rag_context = "\n\n".join([c.get("content", "")[:700] for c in rag_chunks])

        prompt = f"""
Área escolhida: {area}

Respostas do micro-diagnóstico:
{answers_text}

Contexto RAG:
{rag_context}
"""
        completion = await client.chat.completions.create(
            model=settings.OPENAI_MODEL_ANALYSIS,
            messages=[
                {"role": "system", "content": INSIGHT_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            response_format={"type": "json_object"},
            max_tokens=1800,
        )
        result = json.loads(completion.choices[0].message.content or "{}")

        supabase.table("micro_diagnostics").update({
            "status": "completed",
            "result": result,
        }).eq("id", micro_id).execute()

        return result


micro_diagnostic_service = MicroDiagnosticService()
