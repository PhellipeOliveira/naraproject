"""
Ingere documentos da pasta docs-rag (e opcionalmente documentos/01_FUNDAMENTOS.md)
para a tabela knowledge_chunks: chunking, embeddings e insert.

Guia: documentos/01_FUNDAMENTOS.md § 3 (Estrutura do Chunk para RAG).

Uso (na raiz do nara-backend):
  python -m scripts.ingest_docs_rag

Ou com caminhos explícitos:
  python -m scripts.ingest_docs_rag --docs-dir ../docs-rag --fundamentos ../documentos/01_FUNDAMENTOS.md

Requer: SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY no .env
"""
import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Garantir que app seja encontrado
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.rag.ingest import (
    ChunkStrategy,
    build_chunks_from_docs,
    ingest_single_file,
)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def get_default_paths() -> tuple[Path, Path | None]:
    """Raiz do repositório = pai do nara-backend. docs-rag e documentos ficam na raiz."""
    backend_root = Path(__file__).resolve().parent.parent
    repo_root = backend_root.parent
    docs_rag = repo_root / "docs-rag"
    fundamentos = repo_root / "documentos" / "01_FUNDAMENTOS.md"
    return docs_rag, fundamentos if fundamentos.is_file() else None


async def main() -> None:
    parser = argparse.ArgumentParser(description="Ingestão docs-rag → knowledge_chunks")
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=None,
        help="Pasta com .md (ex.: docs-rag). Default: <repo>/docs-rag",
    )
    parser.add_argument(
        "--fundamentos",
        type=Path,
        default=None,
        help="Arquivo 01_FUNDAMENTOS.md (guia). Default: <repo>/documentos/01_FUNDAMENTOS.md",
    )
    parser.add_argument(
        "--no-fundamentos",
        action="store_true",
        help="Não incluir 01_FUNDAMENTOS.md na ingestão",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Só montar chunks e contar; não gerar embeddings nem inserir",
    )
    parser.add_argument(
        "--strategy",
        type=str,
        choices=["size", "semantic", "both"],
        default="size",
        help="size=por tamanho, semantic=por parágrafos, both=os dois (default: size)",
    )
    parser.add_argument(
        "--skip-metadata-enrichment",
        action="store_true",
        help="Desativa classificação LLM de metadados (motor/crise/ponto_entrada).",
    )
    args = parser.parse_args()

    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        logger.error("Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no .env")
        sys.exit(1)
    if not args.dry_run:
        if not settings.OPENAI_API_KEY or not settings.OPENAI_API_KEY.strip():
            logger.error("Defina OPENAI_API_KEY no .env para gerar embeddings")
            sys.exit(1)
        # Validar chave antes de processar (evita rodar tudo e falhar no primeiro batch)
        try:
            from app.rag.embeddings import generate_embedding
            await generate_embedding("teste")
        except Exception as e:
            if "401" in str(e) or "invalid_api_key" in str(e) or "Authentication" in str(type(e).__name__):
                logger.error("OPENAI_API_KEY inválida ou expirada. Atualize no .env (nara-backend/.env).")
                logger.error("Gere uma nova chave em: https://platform.openai.com/account/api-keys")
                sys.exit(1)
            raise

    docs_rag, default_fundamentos = get_default_paths()
    docs_dir = args.docs_dir or docs_rag
    extra_files: list[Path] = []
    if not args.no_fundamentos:
        if args.fundamentos and args.fundamentos.is_file():
            extra_files.append(args.fundamentos)
        elif default_fundamentos:
            extra_files.append(default_fundamentos)

    if not docs_dir.is_dir():
        logger.error("Pasta de documentos não encontrada: %s", docs_dir)
        sys.exit(1)

    logger.info("Lendo documentos em %s", docs_dir)
    if extra_files:
        logger.info("Incluindo guia: %s", [str(p) for p in extra_files])
    strategy: ChunkStrategy = args.strategy  # type: ignore[assignment]
    logger.info("Estratégia: %s", strategy)
    repo_root = Path(__file__).resolve().parent.parent.parent
    docs_files = sorted([p for p in docs_dir.rglob("*.md") if p.is_file()])
    all_files = docs_files + extra_files
    if not all_files:
        logger.warning("Nenhum arquivo .md encontrado para ingestão.")
        sys.exit(0)

    if args.dry_run:
        logger.info("Dry-run: montando chunks sem gerar embeddings nem inserir.")
        chunks = build_chunks_from_docs(
            docs_dir,
            extra_files=extra_files if extra_files else None,
            strategy=strategy,
        )
        logger.info("Total de chunks gerados: %d", len(chunks))
        for i, c in enumerate(chunks[:5]):
            logger.info(
                "  [%d] source=%s chapter=%s section=%s len=%d",
                i + 1,
                c.get("source"),
                c.get("chapter"),
                c.get("section"),
                len(c.get("content", "")),
            )
        if len(chunks) > 5:
            logger.info("  ... e mais %d chunks", len(chunks) - 5)
        return

    total_inserted = 0
    total_files = len(all_files)
    enrich_metadata = not args.skip_metadata_enrichment
    for idx, file_path in enumerate(all_files, start=1):
        source = str(file_path.resolve().relative_to(repo_root.resolve()))
        logger.info("[%d/%d] Reindexando %s", idx, total_files, source)
        inserted = await ingest_single_file(
            file_path=file_path,
            repo_root=repo_root,
            strategy=strategy,
            enrich_metadata=enrich_metadata,
        )
        total_inserted += inserted
        logger.info("[%d/%d] Upsert concluído: %d chunks", idx, total_files, inserted)

    logger.info("Pronto. %d chunks inseridos/atualizados em knowledge_chunks.", total_inserted)
    logger.info("O diagnóstico pode usar esses documentos via RAG (match_knowledge_chunks).")


if __name__ == "__main__":
    asyncio.run(main())
