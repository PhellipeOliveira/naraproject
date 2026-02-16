"""Recuperação de chunks relevantes via pgvector (Supabase RPC)."""
import logging
from typing import Any, Optional

from app.config import settings
from app.database import supabase
from app.rag.embeddings import generate_embedding

logger = logging.getLogger(__name__)


async def retrieve_relevant_chunks(
    query: str,
    top_k: int | None = None,
    filter_chapter: Optional[str] = None,
    filter_motor: Optional[list[str]] = None,
    filter_crise: Optional[list[str]] = None,
    similarity_threshold: float | None = None,
    filter_chunk_strategy: Optional[str] = "semantic",
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
            Default "semantic" para respostas mais coerentes. None = não filtra (retrocompatível).

    Returns:
        Lista de chunks com similarity score
    """
    top_k = top_k or settings.RAG_TOP_K
    similarity_threshold = similarity_threshold or settings.RAG_SIMILARITY_THRESHOLD

    query_embedding = await generate_embedding(query)

    payload = {
        "query_embedding": query_embedding,
        "match_threshold": similarity_threshold,
        "match_count": top_k,
        "filter_chapter": filter_chapter,
        "filter_estagio": None,
    }
    if filter_motor is not None:
        payload["filter_motor"] = filter_motor
    if filter_crise is not None:
        payload["filter_crise"] = filter_crise
    if filter_chunk_strategy is not None:
        payload["filter_chunk_strategy"] = filter_chunk_strategy

    result = supabase.rpc("match_knowledge_chunks", payload).execute()

    count = len(result.data) if result.data else 0
    logger.info("RAG retrieved %s chunks for query (threshold=%.2f)", count, similarity_threshold)
    # Teste manual: para confirmar que só vêm chunks semantic, logar o primeiro:
    # if result.data: logger.info("first chunk metadata.chunk_strategy=%s", (result.data[0].get("metadata") or {}).get("chunk_strategy"))
    return result.data or []


async def retrieve_for_question_generation(
    user_responses: list[dict[str, Any]],
    underrepresented_areas: list[str],
    phase: int,
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

    methodology_chunks = await retrieve_relevant_chunks(
        query=response_texts if response_texts else "diagnóstico transformação narrativa",
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
) -> str:
    """
    Busca contexto relevante para geração do relatório final.

    Args:
        diagnostic_id: ID do diagnóstico
        scores_by_area: Scores calculados por área
        all_responses: Todas as respostas do usuário

    Returns:
        Contexto concatenado para o prompt
    """
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

    for area in critical_areas[:4]:
        chunks = await retrieve_relevant_chunks(
            query=f"critérios análise {area} sinais crise intervenção",
            top_k=3,
            filter_chapter=area,
        )
        context_chunks.extend(chunks)

    methodology = await retrieve_relevant_chunks(
        query="fases jornada motores motivacionais clusters crise assunção intencional",
        top_k=5,
    )
    context_chunks.extend(methodology)

    if response_summary:
        response_chunks = await retrieve_relevant_chunks(
            query=response_summary,
            top_k=3,
        )
        context_chunks.extend(response_chunks)

    context = "\n\n---\n\n".join(
        [
            f"**{chunk.get('chapter', 'Metodologia')}**\n{chunk.get('content', '')}"
            for chunk in context_chunks
        ]
    )
    return context
