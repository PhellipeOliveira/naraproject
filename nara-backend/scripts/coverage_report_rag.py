"""
Gera relatório de cobertura conceitual do RAG.

Uso (com venv ativado, na raiz do nara-backend):
  python -m scripts.coverage_report_rag

Opcional:
  python -m scripts.coverage_report_rag --top-k 5 --filter-chunk-strategy semantic
  python -m scripts.coverage_report_rag --fail-on-gaps
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.rag.retriever import retrieve_relevant_chunks


@dataclass
class CoverageRow:
    group_id: str
    group_title: str
    query: str
    chunks_found: int
    status: str
    sample_chapter: str
    sample_section: str
    sample_strategy: str
    sample_source: str
    error: str


def parse_args() -> argparse.Namespace:
    backend_root = Path(__file__).resolve().parent.parent
    repo_root = backend_root.parent

    parser = argparse.ArgumentParser(description="Relatório de cobertura do RAG por conceitos")
    parser.add_argument(
        "--topics-file",
        type=Path,
        default=backend_root / "scripts" / "rag_coverage_topics.json",
        help="Arquivo JSON com grupos e queries (default: scripts/rag_coverage_topics.json)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "docs" / "RAG_COVERAGE_REPORT.md",
        help="Arquivo de saída markdown (default: docs/RAG_COVERAGE_REPORT.md)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Número máximo de chunks por query (default: 3)",
    )
    parser.add_argument(
        "--filter-chunk-strategy",
        type=str,
        default=None,
        choices=["size", "semantic"],
        help="Filtra chunks por estratégia (size|semantic). Default: sem filtro",
    )
    parser.add_argument(
        "--fail-on-gaps",
        action="store_true",
        help="Retorna exit code 1 se houver lacunas (status=gap) ou erros",
    )
    return parser.parse_args()


def load_topics(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo de tópicos não encontrado: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "groups" not in data:
        raise ValueError("Formato inválido: esperado objeto JSON com chave 'groups'.")

    groups = data.get("groups")
    if not isinstance(groups, list) or not groups:
        raise ValueError("Formato inválido: 'groups' deve ser uma lista não vazia.")

    return data


async def evaluate_query(
    group_id: str,
    group_title: str,
    query: str,
    top_k: int,
    filter_chunk_strategy: str | None,
) -> CoverageRow:
    try:
        chunks = await retrieve_relevant_chunks(
            query=query,
            top_k=top_k,
            filter_chunk_strategy=filter_chunk_strategy,
        )
    except Exception as exc:
        return CoverageRow(
            group_id=group_id,
            group_title=group_title,
            query=query,
            chunks_found=0,
            status="error",
            sample_chapter="-",
            sample_section="-",
            sample_strategy="-",
            sample_source="-",
            error=str(exc).replace("\n", " ").strip(),
        )

    chunks_found = len(chunks)
    status = "covered" if chunks_found > 0 else "gap"

    if chunks_found == 0:
        return CoverageRow(
            group_id=group_id,
            group_title=group_title,
            query=query,
            chunks_found=0,
            status=status,
            sample_chapter="-",
            sample_section="-",
            sample_strategy="-",
            sample_source="-",
            error="",
        )

    first = chunks[0]
    meta = first.get("metadata") or {}
    strategy = str(meta.get("chunk_strategy", "-"))
    source = str(first.get("source", "-"))

    return CoverageRow(
        group_id=group_id,
        group_title=group_title,
        query=query,
        chunks_found=chunks_found,
        status=status,
        sample_chapter=str(first.get("chapter", "-")),
        sample_section=str(first.get("section", "-")),
        sample_strategy=strategy,
        sample_source=source,
        error="",
    )


def render_markdown(
    rows: list[CoverageRow],
    topics_source: str,
    topics_file: Path,
    top_k: int,
    filter_chunk_strategy: str | None,
) -> str:
    now = datetime.now(UTC).isoformat()
    total = len(rows)
    covered = sum(1 for r in rows if r.status == "covered")
    gaps = sum(1 for r in rows if r.status == "gap")
    errors = sum(1 for r in rows if r.status == "error")
    coverage_pct = (covered / total * 100.0) if total else 0.0

    lines: list[str] = []
    lines.append("# Relatório de Cobertura RAG")
    lines.append("")
    lines.append(f"- Gerado em: `{now}`")
    lines.append(f"- Fonte conceitual: `{topics_source}`")
    lines.append(f"- Arquivo de tópicos: `{topics_file}`")
    lines.append(
        f"- Configuração: `top_k={top_k}`, `filter_chunk_strategy={filter_chunk_strategy or 'none'}`, "
        f"`threshold={settings.RAG_SIMILARITY_THRESHOLD}`"
    )
    lines.append("")
    lines.append("## Resumo")
    lines.append("")
    lines.append(f"- Total de queries auditadas: **{total}**")
    lines.append(f"- Cobertas: **{covered}**")
    lines.append(f"- Lacunas (0 chunks): **{gaps}**")
    lines.append(f"- Erros de consulta: **{errors}**")
    lines.append(f"- Cobertura bruta: **{coverage_pct:.1f}%**")
    lines.append("")

    if gaps:
        lines.append("## Lacunas Prioritárias (status=gap)")
        lines.append("")
        for r in rows:
            if r.status == "gap":
                lines.append(f"- `{r.group_title}`: `{r.query}`")
        lines.append("")

    if errors:
        lines.append("## Erros de Consulta")
        lines.append("")
        for r in rows:
            if r.status == "error":
                lines.append(f"- `{r.group_title}`: `{r.query}` -> `{r.error}`")
        lines.append("")

    lines.append("## Resultados por Grupo")
    lines.append("")

    grouped: dict[str, list[CoverageRow]] = {}
    for row in rows:
        grouped.setdefault(row.group_title, []).append(row)

    for group_title in grouped:
        group_rows = grouped[group_title]
        g_total = len(group_rows)
        g_cov = sum(1 for r in group_rows if r.status == "covered")
        g_gap = sum(1 for r in group_rows if r.status == "gap")
        g_err = sum(1 for r in group_rows if r.status == "error")

        lines.append(f"### {group_title}")
        lines.append("")
        lines.append(f"- Cobertas: **{g_cov}/{g_total}** | Lacunas: **{g_gap}** | Erros: **{g_err}**")
        lines.append("")
        lines.append("| Query | Status | Chunks | Chapter (amostra) | Section (amostra) | Strategy | Source |")
        lines.append("|---|---|---:|---|---|---|---|")
        for r in group_rows:
            query = r.query.replace("|", "\\|")
            lines.append(
                f"| `{query}` | `{r.status}` | {r.chunks_found} | `{r.sample_chapter}` | "
                f"`{r.sample_section}` | `{r.sample_strategy}` | `{r.sample_source}` |"
            )
        lines.append("")

    lines.append("## Interpretação")
    lines.append("")
    lines.append("- `covered`: retornou pelo menos 1 chunk para a query.")
    lines.append("- `gap`: retornou 0 chunks. Priorizar reforço de conteúdo ou ajuste de query.")
    lines.append("- `error`: falha de execução (RPC/config/credenciais). Corrigir antes de analisar cobertura.")
    lines.append("")
    return "\n".join(lines)


async def run() -> int:
    args = parse_args()
    topics_data = load_topics(args.topics_file)
    groups = topics_data["groups"]

    rows: list[CoverageRow] = []
    for group in groups:
        group_id = str(group.get("id", "unknown"))
        group_title = str(group.get("title", group_id))
        queries = group.get("queries") or []
        if not isinstance(queries, list):
            continue
        for query in queries:
            row = await evaluate_query(
                group_id=group_id,
                group_title=group_title,
                query=str(query),
                top_k=args.top_k,
                filter_chunk_strategy=args.filter_chunk_strategy,
            )
            rows.append(row)
            print(
                f"[{group_title}] {query} -> {row.status} ({row.chunks_found})"
            )

    report = render_markdown(
        rows=rows,
        topics_source=str(topics_data.get("source", "-")),
        topics_file=args.topics_file,
        top_k=args.top_k,
        filter_chunk_strategy=args.filter_chunk_strategy,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")

    total = len(rows)
    covered = sum(1 for r in rows if r.status == "covered")
    gaps = sum(1 for r in rows if r.status == "gap")
    errors = sum(1 for r in rows if r.status == "error")
    print("\n=== COBERTURA RAG ===")
    print(f"Relatório: {args.output}")
    print(f"Total: {total} | Covered: {covered} | Gaps: {gaps} | Errors: {errors}")

    if args.fail_on_gaps and (gaps > 0 or errors > 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run()))
