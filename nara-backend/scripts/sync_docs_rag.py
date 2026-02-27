"""
Sincroniza chunks do Supabase com arquivos existentes em docs-rag/.

Remove do banco qualquer source docs-rag/* que nao exista mais no disco.

Uso (na raiz do nara-backend):
  python -m scripts.sync_docs_rag

Dry-run (nao remove nada):
  python -m scripts.sync_docs_rag --dry-run
"""
import argparse
import logging
import sys
from pathlib import Path

# Garantir que app seja encontrado
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.database import supabase
from app.rag.ingest import upsert_chunks_for_source

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def _resolve_repo_root() -> Path:
    """Retorna a raiz do repositorio (pai de nara-backend)."""
    return Path(__file__).resolve().parent.parent.parent


def _get_sources_on_disk(docs_dir: Path, repo_root: Path) -> set[str]:
    """Lista sources validos da pasta docs-rag como caminhos relativos do repo."""
    if not docs_dir.is_dir():
        return set()

    sources: set[str] = set()
    for path in sorted(docs_dir.rglob("*.md")):
        if path.is_file():
            sources.add(str(path.resolve().relative_to(repo_root.resolve())))
    return sources


def _get_sources_in_db(prefix: str = "docs-rag/") -> set[str]:
    """Lista sources docs-rag/* atualmente presentes na tabela knowledge_chunks."""
    result = (
        supabase.table("knowledge_chunks")
        .select("source")
        .like("source", f"{prefix}%")
        .execute()
    )
    return {
        str(row.get("source"))
        for row in (result.data or [])
        if row.get("source")
    }


def parse_args() -> argparse.Namespace:
    repo_root = _resolve_repo_root()
    parser = argparse.ArgumentParser(
        description="Sincroniza knowledge_chunks com arquivos de docs-rag."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=repo_root / "docs-rag",
        help="Pasta docs-rag (default: <repo>/docs-rag).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas lista orfaos; nao remove registros do banco.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        logger.error("Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no .env")
        return 1

    repo_root = _resolve_repo_root()
    docs_dir = args.docs_dir.resolve()

    if not docs_dir.is_dir():
        logger.error("Pasta docs-rag nao encontrada: %s", docs_dir)
        return 1

    disk_sources = _get_sources_on_disk(docs_dir, repo_root)
    db_sources = _get_sources_in_db(prefix="docs-rag/")
    orphan_sources = sorted(db_sources - disk_sources)

    logger.info("Sources no disco: %d", len(disk_sources))
    logger.info("Sources no banco (docs-rag/*): %d", len(db_sources))
    logger.info("Sources orfaos detectados: %d", len(orphan_sources))

    if not orphan_sources:
        logger.info("Nada para remover. Base sincronizada.")
        return 0

    for source in orphan_sources:
        logger.info(" - %s", source)

    if args.dry_run:
        logger.info("Dry-run ativo: nenhuma remocao executada.")
        return 0

    removed_sources = 0
    for source in orphan_sources:
        # Reaproveita a logica de upsert para deletar todos os chunks de um source.
        upsert_chunks_for_source(source, [])
        removed_sources += 1

    logger.info("Sincronizacao concluida. Sources removidos: %d", removed_sources)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
