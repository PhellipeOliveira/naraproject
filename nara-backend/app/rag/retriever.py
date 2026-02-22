"""Recuperação de chunks relevantes via pgvector (Supabase RPC)."""
import logging
from typing import Any, Optional

from app.config import settings
from app.database import supabase
from app.rag.embeddings import generate_embedding

logger = logging.getLogger(__name__)

RAG_QUERY_TEMPLATE = """
Com base na Metodologia de Phellipe Oliveira, busque estratégias para:

ÁREA DO CÍRCULO NARRATIVO: {areas}
DOMÍNIO TEMÁTICO: {temas}
FASE DA JORNADA: {fase}
CONTEXTO DE CONFLITO: {contexto}

MOTOR MOTIVACIONAL IDENTIFICADO: {motor}
TIPO DE CRISE: {tipo_crise}
PONTO DE ENTRADA: {ponto_entrada}
TOM EMOCIONAL: {tom_emocional}

Retorne documentos que ajudem a:
1. Identificar o ponto de entrada ideal para intervenção
2. Sugerir práticas alinhadas ao estágio da jornada
3. Revelar conexões entre áreas para diagnóstico integrado
4. Prescrever Âncoras Práticas específicas para a fase de Assunção
"""


def _build_structured_query(
    *,
    areas: str,
    temas: str,
    fase: str,
    contexto: str,
    motor: str,
    tipo_crise: str,
    ponto_entrada: str,
    tom_emocional: str,
) -> str:
    return RAG_QUERY_TEMPLATE.format(
        areas=areas or "Não identificado",
        temas=temas or "Domínios D1-D6",
        fase=fase or "Não identificado",
        contexto=contexto or "Não identificado",
        motor=motor or "Não identificado",
        tipo_crise=tipo_crise or "Não identificado",
        ponto_entrada=ponto_entrada or "Não identificado",
        tom_emocional=tom_emocional or "neutro",
    )


async def retrieve_relevant_chunks(
    query: str,
    top_k: int | None = None,
    filter_chapter: Optional[str] = None,
    filter_motor: Optional[list[str]] = None,
    filter_crise: Optional[list[str]] = None,
    similarity_threshold: float | None = None,
    filter_chunk_strategy: Optional[str] = None,
) -> list[dict[str, Any]]:
    """
    Busca chunks relevantes para uma query usando similaridade semântica.

    Args:
        query: Texto da busca
        top_k: Número máximo de resultados
        filter_chapter: Filtrar por área/capítulo (ex: "Saúde Física")
        filter_motor: Filtrar por motor motivacional
        filter_crise: Filtrar por tipo de crise
        similarity_threshold: Score mínimo de similaridade
        filter_chunk_strategy: Filtrar por metadata.chunk_strategy (ex: "semantic").
            None = sem filtro (retorna todos os chunks ativos).

    Returns:
        Lista de chunks com similarity score
    """
    top_k = top_k or settings.RAG_TOP_K
    similarity_threshold = similarity_threshold or settings.RAG_SIMILARITY_THRESHOLD

    query_embedding = await generate_embedding(query)

    # filter_chunk_strategy é sempre enviado (mesmo como null) para o PostgREST
    # resolver a assinatura correta da RPC sem ambiguidade de overload (PGRST203).
    payload: dict[str, Any] = {
        "query_embedding": query_embedding,
        "match_threshold": similarity_threshold,
        "match_count": top_k,
        "filter_chapter": filter_chapter,
        "filter_estagio": None,
        "filter_motor": filter_motor,
        "filter_crise": filter_crise,
        "filter_chunk_strategy": filter_chunk_strategy,
    }

    result = supabase.rpc("match_knowledge_chunks", payload).execute()
    chunks = result.data or []

    logger.info(
        "RAG retrieved %d chunks for query (threshold=%.2f)",
        len(chunks),
        similarity_threshold,
    )
    return chunks


async def retrieve_for_question_generation(
    user_responses: list[dict[str, Any]],
    underrepresented_areas: list[str],
    phase: int,
    context_analysis: Optional[dict[str, Any]] = None,
) -> str:
    """
    Busca contexto relevante para geração de perguntas adaptativas.

    Args:
        user_responses: Respostas anteriores do usuário
        underrepresented_areas: Áreas com poucas respostas
        phase: Fase atual do diagnóstico (2, 3 ou 4)

    Returns:
        Contexto concatenado para o prompt
    """
    response_texts = " ".join(
        [
            (r.get("answer_value") or {}).get("text", "")
            for r in user_responses[-15:]
            if (r.get("answer_value") or {}).get("text")
        ]
    )

    all_chunks: list[dict[str, Any]] = []

    context_analysis = context_analysis or {}
    phase_name = context_analysis.get("fase_jornada") or f"Fase {phase}"
    crisis_list = context_analysis.get("clusters_identificados") or []
    crisis_text = ", ".join(crisis_list) if crisis_list else "Não identificado"
    structured_query = _build_structured_query(
        areas=", ".join(underrepresented_areas[:4]) if underrepresented_areas else "Todas as áreas",
        temas=", ".join(context_analysis.get("dominios_alavanca", [])) if context_analysis.get("dominios_alavanca") else "Domínios D1-D6",
        fase=str(phase_name),
        contexto=(response_texts[:500] if response_texts else "Respostas iniciais do usuário"),
        motor=context_analysis.get("motor_dominante", "Não identificado"),
        tipo_crise=crisis_text,
        ponto_entrada=(context_analysis.get("pontos_entrada") or ["Não identificado"])[0],
        tom_emocional=context_analysis.get("tom_emocional", "neutro"),
    )

    methodology_chunks = await retrieve_relevant_chunks(
        query=structured_query,
        top_k=5,
    )
    all_chunks.extend(methodology_chunks)

    for area in underrepresented_areas[:3]:
        area_chunks = await retrieve_relevant_chunks(
            query=f"critérios de análise {area} sinais conflito",
            top_k=2,
            filter_chapter=area,
        )
        all_chunks.extend(area_chunks)

    context = "\n\n---\n\n".join(
        [
            f"**{chunk.get('chapter', 'Geral')}** ({chunk.get('section', '')})\n{chunk.get('content', '')}"
            for chunk in all_chunks
        ]
    )
    return context


async def retrieve_for_report_generation(
    diagnostic_id: str,
    scores_by_area: dict[str, Any],
    all_responses: list[dict[str, Any]],
    context_analysis: Optional[dict[str, Any]] = None,
) -> str:
    """
    Busca contexto relevante para geração do relatório final usando RAG.

    Args:
        diagnostic_id: ID do diagnóstico
        scores_by_area: Scores calculados por área
        all_responses: Todas as respostas do usuário
        context_analysis: Análise contextual do analyzer (Memórias Vermelhas, etc.)

    Returns:
        Contexto concatenado para o prompt
    """
    context_analysis = context_analysis or {}

    areas_criticas = context_analysis.get("areas_criticas", [])
    if areas_criticas:
        if isinstance(areas_criticas[0], str):
            critical_areas = areas_criticas[:4]
        else:
            critical_areas = [f"Área {i}" for i in areas_criticas[:4]]
    else:
        critical_areas = [
            area_name
            for area_name, data in scores_by_area.items()
            if (data or {}).get("score", 10) < 5.0
        ]

    response_summary = " ".join(
        [
            ((r.get("answer_value") or {}).get("text", ""))[:200]
            for r in all_responses
            if (r.get("answer_value") or {}).get("text")
        ]
    )[:2000]

    context_chunks: list[dict[str, Any]] = []

    phase_name = context_analysis.get("fase_jornada") or context_analysis.get("nivel_maturidade") or "Não identificado"
    crisis_list = context_analysis.get("clusters_identificados") or []
    crisis_text = ", ".join(crisis_list) if crisis_list else "Não identificado"
    structured_query = _build_structured_query(
        areas=", ".join(critical_areas[:4]) if critical_areas else "Não identificado",
        temas=", ".join(context_analysis.get("dominios_alavanca", [])) if context_analysis.get("dominios_alavanca") else "Domínios D1-D6",
        fase=str(phase_name),
        contexto=response_summary or "Sem contexto textual consolidado",
        motor=context_analysis.get("motor_dominante", "Não identificado"),
        tipo_crise=crisis_text,
        ponto_entrada=(context_analysis.get("pontos_entrada") or ["Não identificado"])[0],
        tom_emocional=context_analysis.get("tom_emocional", "neutro"),
    )

    methodology = await retrieve_relevant_chunks(
        query=structured_query,
        top_k=5,
    )
    context_chunks.extend(methodology)

    for area in critical_areas[:4]:
        if "Área" not in area:
            chunks = await retrieve_relevant_chunks(
                query=f"{area} sinais conflito componentes domínio intervenção autossabotagem",
                top_k=2,
                filter_chapter=area,
            )
            context_chunks.extend(chunks)

    if response_summary:
        response_chunks = await retrieve_relevant_chunks(
            query=response_summary,
            top_k=3,
        )
        context_chunks.extend(response_chunks)

    tcc_chunks = await retrieve_relevant_chunks(
        query="técnicas TCC âncoras práticas ponto de entrada",
        top_k=3,
    )
    context_chunks.extend(tcc_chunks)

    context = "\n\n---\n\n".join(
        [
            f"**{chunk.get('chapter', 'Metodologia')}** - {chunk.get('section', '')}\n{chunk.get('content', '')}"
            for chunk in context_chunks
        ]
    )
    return context
