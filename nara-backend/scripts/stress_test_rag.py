"""
Stress test do RAG com 3 queries que eram gaps.

Uso:
  python -m scripts.stress_test_rag

O script executa o fluxo:
1) retrieve_relevant_chunks
2) montagem de prompt com contexto RAG
3) chamada LLM para resposta final de chat

Resultados sao salvos em docs/RAG_STRESS_TEST_REPORT.md para auditoria continua.
"""
import asyncio
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.rag.retriever import retrieve_relevant_chunks

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

QUERIES = [
    "questionamento socrático evidência alternativa utilidade",
    "motor da conquista metas tangíveis",
    "âncoras de ambiente referências objetos ambientes grupo",
]

REPORT_PATH = Path(__file__).resolve().parent.parent.parent / "docs" / "RAG_STRESS_TEST_REPORT.md"


def _chunk_label(chunk: dict[str, Any]) -> str:
    chapter = chunk.get("chapter", "-")
    section = chunk.get("section", "-")
    source = chunk.get("source", "-")
    score = chunk.get("similarity") or chunk.get("score") or "-"
    return f"source={source} | chapter={chapter} | section={section} | similarity={score}"


def _build_context(chunks: list[dict[str, Any]]) -> str:
    if not chunks:
        return "Nenhum chunk encontrado."

    parts: list[str] = []
    for idx, chunk in enumerate(chunks, start=1):
        parts.append(
            "\n".join(
                [
                    f"[Chunk {idx}]",
                    _chunk_label(chunk),
                    chunk.get("content", ""),
                ]
            )
        )
    return "\n\n---\n\n".join(parts)


def _build_prompt(query: str, rag_context: str) -> tuple[str, str]:
    system_prompt = (
        "Voce e a NARA em modo de orientacao diagnostica narrativa. "
        "Responda em portugues, linguagem clara, sem jargao desnecessario, "
        "e integrando explicitamente os conceitos do contexto RAG."
    )

    user_prompt = f"""
QUERY DO USUARIO:
{query}

CONTEXTO RAG:
{rag_context}

TAREFA:
Gere uma resposta completa de chat com:
1) Leitura diagnostica do que a query sugere sobre o estado interno.
2) Integracao explicita do vocabulario metodologico quando aplicavel (motor, ponto de entrada, tecnicas TCC, ancoras).
3) Recomendacao pratica em 3 passos de curto prazo.
4) Fechamento com uma pergunta de acompanhamento.

Formato:
- Use titulos curtos.
- Seja objetivo, mas completo.
"""
    return system_prompt, user_prompt


def _render_report(results: list[dict[str, Any]], top_k: int) -> str:
    now = datetime.now(UTC).isoformat()
    lines = [
        "# Relatório de Stress Test RAG",
        "",
        "- Gerado em: `" + now + "`",
        f"- Queries: {len(results)} (ex-gaps)",
        f"- Configuração: `top_k={top_k}`, `filter_chunk_strategy=semantic`, `threshold={settings.RAG_SIMILARITY_THRESHOLD}`",
        f"- Modelo: `{settings.OPENAI_MODEL_ANALYSIS}`",
        "",
        "---",
        "",
    ]
    for idx, r in enumerate(results, start=1):
        query = r["query"]
        chunks = r["chunks"]
        response_text = r["response_text"]
        lines.append(f"## {idx}. Query: `{query}`")
        lines.append("")
        lines.append(f"**Chunks encontrados:** {len(chunks)}")
        lines.append("")
        if chunks:
            lines.append("| # | source | chapter | section | similarity |")
            lines.append("|---|--------|---------|---------|------------|")
            for i, c in enumerate(chunks, start=1):
                src = (c.get("source") or "-").replace("|", "\\|")
                ch = (c.get("chapter") or "-").replace("|", "\\|")
                sec = (c.get("section") or "-").replace("|", "\\|")[:50]
                sim = c.get("similarity") or c.get("score") or "-"
                lines.append(f"| {i} | {src} | {ch} | {sec} | {sim} |")
        else:
            lines.append("(nenhum chunk acima do threshold)")
        lines.append("")
        lines.append("### Resposta simulada (chat)")
        lines.append("")
        lines.append(response_text)
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


async def _simulate_for_query(
    client: AsyncOpenAI, query: str, top_k: int = 3
) -> dict[str, Any]:
    logger.info("\n%s", "=" * 100)
    logger.info("QUERY: %s", query)

    chunks = await retrieve_relevant_chunks(
        query=query,
        top_k=top_k,
        filter_chunk_strategy="semantic",
    )
    logger.info("CHUNKS ENCONTRADOS: %d", len(chunks))
    for idx, chunk in enumerate(chunks, start=1):
        logger.info("  %d) %s", idx, _chunk_label(chunk))

    rag_context = _build_context(chunks)
    system_prompt, user_prompt = _build_prompt(query, rag_context)

    completion = await client.chat.completions.create(
        model=settings.OPENAI_MODEL_ANALYSIS,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
        max_tokens=1300,
    )
    response_text = completion.choices[0].message.content or "(sem resposta)"
    logger.info("\nRESPOSTA SIMULADA:\n%s\n", response_text)

    return {
        "query": query,
        "chunks": chunks,
        "response_text": response_text,
    }


async def main() -> None:
    if not settings.OPENAI_API_KEY:
        logger.error("Defina OPENAI_API_KEY no .env")
        sys.exit(1)
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        logger.error("Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no .env")
        sys.exit(1)

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    top_k = 3
    results: list[dict[str, Any]] = []
    for query in QUERIES:
        results.append(await _simulate_for_query(client, query=query, top_k=top_k))

    report = _render_report(results, top_k=top_k)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    logger.info("Relatório salvo em: %s", REPORT_PATH)

    logger.info("Stress test concluido para %d queries.", len(QUERIES))


if __name__ == "__main__":
    asyncio.run(main())
