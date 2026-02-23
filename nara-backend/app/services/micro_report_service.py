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
Você é Nara, especialista em diagnóstico narrativo e transformação pessoal.
Entregue um micro-relatório profundo e prático para UMA área da vida do usuário.

EIXOS DE TRANSFORMAÇÃO — analise os 3 eixos na área escolhida:
- Narrativa (Crença): que história limitante o usuário conta sobre esta área?
  Ferramenta: TCC — reestruturar a crença, não apenas o comportamento.
- Identidade (Valores): quem o usuário está sendo nesta área? Quem escolheria ser?
  Ferramenta: escolha intencional da identidade — assumir a identidade escolhida agora.
- Hábitos (Princípios): que ações concretas contradizem ou sustentam a identidade?
  Ferramenta: prática intencional — microações coerentes com a nova identidade.

SITUAÇÃO ATUAL E VISÃO DE FUTURO:
- Situação atual: identidade e práticas de hoje (o conflito vivido)
- Visão desejada: identidade e práticas que a pessoa quer assumir
- Distância de transformação: o quanto falta para sair da situação atual e viver a versão desejada

PLANO DE TRANSFORMAÇÃO EM 4 PASSOS (obrigatório):
1. Reconhecer: que padrão atual precisa ser nomeado e observado?
2. Modelar: como é a versão desejada nesta área?
3. Assumir: que ação simbólica o usuário pode tomar hoje para agir como essa versão?
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

DOMÍNIO TEMÁTICO: identifique qual dos 6 domínios tem maior potência para
a fase atual do usuário nesta área e estruture a intervenção neste domínio.

ÂNCORAS PRÁTICAS: escolha 2-3 âncoras das 19 disponíveis com justificativa metodológica.
Evite clichês. Use linguagem direta e acessível.
Pode usar metáforas compreensíveis como "travessia", "capítulo" e "âncoras".
NUNCA use siglas ou termos técnicos da metodologia (M1, MX, M2X, M3, Gap MX, CN, CN+, D1-D6, clusters, assunção intencional, capital simbólico, memórias vermelhas, FCU, volição, força-tarefa, relating e similares).

Retorne JSON com:
{
  "area": "string",
  "eixo_principal_comprometido": "Narrativa|Identidade|Habitos",
  "micro_summary": "texto 400-600 palavras em linguagem simples e sem jargões técnicos",
  "plano_assuncao": {
    "reconhecer": "padrão atual a ser observado",
    "modelar": "imagem da versão desejada nesta área",
    "assumir": "ação simbólica para hoje",
    "reforcar": "microvitória diária"
  },
  "foco_tcc": "string",
  "dominio_alavanca": "Motivacoes e Conflitos|Crencas e Valores|Evolucao e Desenvolvimento|Alinhamento Identidade-Ambiente|Transformacao de Identidade|Papel no Mundo",
  "ancoras": ["a", "b", "c"],
  "proxima_acao_7_dias": "string em linguagem simples e direta"
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
