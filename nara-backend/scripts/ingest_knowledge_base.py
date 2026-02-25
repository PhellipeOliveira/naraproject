"""
Ingestão robusta do documento base metodológico.

Como usar:
  python -m scripts.ingest_knowledge_base
  python -m scripts.ingest_knowledge_base --strategy both
  python -m scripts.ingest_knowledge_base --skip-metadata-enrichment

Esse script usa a mesma lógica de ingestão de docs-rag, via `ingest_single_file`.
"""
import argparse
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.rag.ingest import ChunkStrategy, ingest_single_file

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)
KNOWLEDGE_BASE_SOURCE = "documentos/01_BASE_METODOLOGICA_NARA.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingestão do documento base metodológico em knowledge_chunks."
    )
    parser.add_argument(
        "--strategy",
        type=str,
        choices=["size", "semantic", "both"],
        default="semantic",
        help="Estratégia de chunking (default: semantic).",
    )
    parser.add_argument(
        "--skip-metadata-enrichment",
        action="store_true",
        help="Desativa classificação LLM de metadados.",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        logger.error("Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no .env")
        sys.exit(1)
    if not settings.OPENAI_API_KEY:
        logger.error("Defina OPENAI_API_KEY no .env")
        sys.exit(1)

    backend_root = Path(__file__).resolve().parent.parent
    repo_root = backend_root.parent
    doc_path = repo_root / "documentos" / "01_BASE_METODOLOGICA_NARA.md"
    if not doc_path.exists():
        logger.error("Documento não encontrado: %s", doc_path)
        sys.exit(1)

    strategy: ChunkStrategy = args.strategy  # type: ignore[assignment]
    enrich_metadata = not args.skip_metadata_enrichment
    logger.info("Reindexando source %s", KNOWLEDGE_BASE_SOURCE)
    logger.info("Estratégia: %s", strategy)

    inserted_count = await ingest_single_file(
        file_path=doc_path,
        repo_root=repo_root,
        strategy=strategy,
        enrich_metadata=enrich_metadata,
    )

    logger.info("Upsert concluído. Registros inseridos: %d", inserted_count)


if __name__ == "__main__":
    asyncio.run(main())
