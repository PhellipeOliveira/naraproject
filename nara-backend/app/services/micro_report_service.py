"""Serviço para geração de micro-relatórios por área."""
from __future__ import annotations

import json
from typing import Any

from openai import AsyncOpenAI

from app.config import settings
from app.core.constants import AREAS
from app.database import supabase
from app.rag.retriever import retrieve_relevant_chunks

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

INSIGHT_SYSTEM_PROMPT = """
Você é Nara, Engenheira de Mindset e analista da Metodologia de Phellipe Oliveira.
Entregue um micro-relatório cirúrgico para UMA área do Círculo Narrativo.

EIXOS DE TRANSFORMAÇÃO — analise os 3 eixos na área escolhida:
- Narrativa (Crença): que história limitante o usuário conta sobre esta área?
  Ferramenta: TCC — reestruturar a crença, não apenas o comportamento.
- Identidade (Valores): quem o usuário está sendo nesta área? Quem escolheria ser?
  Ferramenta: Assunção Intencional — assumir a identidade escolhida agora.
- Hábitos (Princípios): que ações concretas contradizem ou sustentam a identidade?
  Ferramenta: Assunção Intencional — microações coerentes com a nova identidade.

ESTADOS M1/MX:
- M1: identidade e práticas atuais (o conflito vivido)
- MX: identidade assumida e práticas desejadas
- Gap MX: distância entre M1 e MX nesta área

PLANO DE ASSUNÇÃO INTENCIONAL (obrigatório):
1. Reconhecer: que padrão M1 precisa ser nomeado e observado?
2. Modelar: como é o MX nesta área?
3. Assumir: que ação simbólica o usuário pode tomar hoje como se já fosse MX?
4. Reforçar: qual microvitória diária sustenta essa identidade?

TÉCNICA TCC (seleção por ponto de entrada):
- Emocional -> Flecha Descendente ou Imaginação Guiada
  (autocrítica, vergonha, medo de fracasso)
- Simbólico -> Reestruturação Cognitiva Escrita ou Redefinição Cognitiva Assistida
  (perda de sentido, conflito de valores)
- Comportamental -> Substituição de Pensamentos Distorcidos ou Experimento Comportamental
  (procrastinação, paralisia, autossabotagem)
- Existencial -> Questionamento Socrático ou Descatastrofização
  (vazio, crise de identidade, medo de assumir novo papel)
Sempre explique por que a técnica foi escolhida.

DOMÍNIO TEMÁTICO: identifique qual dos 6 domínios (D1–D6) tem maior potência para
a fase atual do usuário nesta área e estruture a intervenção neste domínio.

ÂNCORAS PRÁTICAS: escolha 2-3 âncoras das 19 disponíveis com justificativa metodológica.
Evite clichês. Use linguagem simbólica: M1, MX, travessia, clímax, Círculo Narrativo.

Retorne JSON com:
{
  "area": "string",
  "eixo_principal_comprometido": "Narrativa|Identidade|Habitos",
  "micro_summary": "texto 400-600 palavras",
  "plano_assuncao": {
    "reconhecer": "padrão M1 a ser observado",
    "modelar": "imagem do MX nesta área",
    "assumir": "ação simbólica para hoje",
    "reforcar": "microvitória diária"
  },
  "foco_tcc": "string",
  "dominio_alavanca": "D1|D2|D3|D4|D5|D6",
  "ancoras": ["a", "b", "c"],
  "proxima_acao_7_dias": "string"
}
"""


async def generate_micro_report_by_token(token: str, area: str) -> dict[str, Any]:
    if area not in AREAS:
        raise ValueError("Área inválida para micro-relatório.")

    diag_result = (
        supabase.table("diagnostics")
        .select("id")
        .eq("result_token", token)
        .single()
        .execute()
    )
    if not diag_result.data:
        raise ValueError("Token inválido.")
    diagnostic_id = str(diag_result.data["id"])

    report_row = (
        supabase.table("diagnostic_results")
        .select("id, detailed_analysis")
        .eq("diagnostic_id", diagnostic_id)
        .single()
        .execute()
    )
    if not report_row.data:
        raise ValueError("Diagnóstico sem relatório final.")

    report_id = report_row.data["id"]
    detailed = report_row.data.get("detailed_analysis") or {}
    micro_reports = detailed.get("micro_reports") or {}
    if area in micro_reports:
        return micro_reports[area]

    answers_result = (
        supabase.table("answers")
        .select("question_text, answer_value")
        .eq("diagnostic_id", diagnostic_id)
        .eq("question_area", area)
        .order("answered_at")
        .execute()
    )
    answers = answers_result.data or []
    answers_text = []
    for item in answers:
        av = item.get("answer_value") or {}
        text = av.get("text")
        if text:
            answers_text.append(f"Pergunta: {item.get('question_text', '')}\nResposta: {text}")

    rag_chunks = await retrieve_relevant_chunks(
        query=f"micro-relatório da área {area} com foco em intervenção e âncoras práticas",
        top_k=6,
        filter_chapter=area,
    )
    rag_context = "\n\n".join([c.get("content", "")[:700] for c in rag_chunks])

    user_prompt = f"""
Área escolhida: {area}

Respostas do usuário nesta área:
{chr(10).join(answers_text) if answers_text else "Sem respostas textuais suficientes nesta área."}

Contexto RAG:
{rag_context}
"""

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL_ANALYSIS,
        messages=[
            {"role": "system", "content": INSIGHT_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.5,
        response_format={"type": "json_object"},
        max_tokens=1600,
    )
    micro_report = json.loads(response.choices[0].message.content or "{}")

    micro_reports[area] = micro_report
    updated_detailed = {**detailed, "micro_reports": micro_reports}
    supabase.table("diagnostic_results").update({"detailed_analysis": updated_detailed}).eq("id", report_id).execute()

    return micro_report
