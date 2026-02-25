"""
Watcher de docs-rag para reindexacao automatica por arquivo.

Eventos monitorados:
- create/modify de .md: reindexa apenas o arquivo alterado (com debounce)
- delete de .md: remove chunks daquele source do Supabase

Uso (na raiz do nara-backend):
  python -m scripts.watch_docs_rag

Opcoes:
  python -m scripts.watch_docs_rag --strategy semantic --skip-metadata-enrichment
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import sys
import threading
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler, FileSystemMovedEvent
from watchdog.observers import Observer

# Garantir que app seja encontrado
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.rag.ingest import ChunkStrategy, ingest_single_file, upsert_chunks_for_source

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

DEBOUNCE_SECONDS = 2.0


def _resolve_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


class _DocsRagHandler(FileSystemEventHandler):
    def __init__(
        self,
        *,
        docs_dir: Path,
        repo_root: Path,
        strategy: ChunkStrategy,
        enrich_metadata: bool,
    ) -> None:
        super().__init__()
        self._docs_dir = docs_dir.resolve()
        self._repo_root = repo_root.resolve()
        self._strategy = strategy
        self._enrich_metadata = enrich_metadata
        self._timers: dict[str, threading.Timer] = {}
        self._lock = threading.Lock()

    def _is_target_markdown(self, path_str: str) -> bool:
        path = Path(path_str)
        return (
            path.suffix.lower() == ".md"
            and not path.name.startswith(".")
        )

    def _source_for_path(self, path_str: str) -> str | None:
        try:
            path = Path(path_str).resolve()
            return str(path.relative_to(self._repo_root))
        except ValueError:
            return None

    def _cancel_timer(self, source: str) -> None:
        with self._lock:
            timer = self._timers.pop(source, None)
        if timer:
            timer.cancel()

    def _schedule_reindex(self, file_path: Path) -> None:
        source = self._source_for_path(str(file_path))
        if not source:
            return

        self._cancel_timer(source)

        timer = threading.Timer(
            DEBOUNCE_SECONDS,
            self._run_reindex,
            args=(file_path, source),
        )
        timer.daemon = True
        with self._lock:
            self._timers[source] = timer
        timer.start()

    def _run_reindex(self, file_path: Path, source: str) -> None:
        with self._lock:
            self._timers.pop(source, None)

        if not file_path.is_file():
            # Arquivo pode ter sido deletado entre o evento e o debounce.
            logger.info("Arquivo nao existe mais apos debounce, removendo source: %s", source)
            upsert_chunks_for_source(source, [])
            return

        try:
            inserted = asyncio.run(
                ingest_single_file(
                    file_path=file_path,
                    repo_root=self._repo_root,
                    strategy=self._strategy,
                    enrich_metadata=self._enrich_metadata,
                )
            )
            logger.info("Reindexado %s (%d chunks).", source, inserted)
        except Exception as exc:
            logger.error("Falha ao reindexar %s: %s", source, exc)

    def _remove_source_for_path(self, path_str: str) -> None:
        source = self._source_for_path(path_str)
        if not source or not source.startswith("docs-rag/"):
            return
        self._cancel_timer(source)
        try:
            upsert_chunks_for_source(source, [])
            logger.info("Removido source deletado: %s", source)
        except Exception as exc:
            logger.error("Falha ao remover source %s: %s", source, exc)

    def _handle_write_event(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        if not self._is_target_markdown(event.src_path):
            return
        file_path = Path(event.src_path).resolve()
        if not str(file_path).startswith(str(self._docs_dir)):
            return
        self._schedule_reindex(file_path)

    def on_created(self, event: FileSystemEvent) -> None:
        self._handle_write_event(event)

    def on_modified(self, event: FileSystemEvent) -> None:
        self._handle_write_event(event)

    def on_deleted(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        if not self._is_target_markdown(event.src_path):
            return
        self._remove_source_for_path(event.src_path)

    def on_moved(self, event: FileSystemMovedEvent) -> None:
        if event.is_directory:
            return
        if self._is_target_markdown(event.src_path):
            self._remove_source_for_path(event.src_path)
        if self._is_target_markdown(event.dest_path):
            self._schedule_reindex(Path(event.dest_path).resolve())


def parse_args() -> argparse.Namespace:
    repo_root = _resolve_repo_root()
    parser = argparse.ArgumentParser(
        description="Monitora docs-rag e reindexa arquivo alterado/deletado."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=repo_root / "docs-rag",
        help="Pasta docs-rag (default: <repo>/docs-rag).",
    )
    parser.add_argument(
        "--strategy",
        choices=["size", "semantic", "both"],
        default="semantic",
        help="Estrategia de chunking para reindexacao (default: semantic).",
    )
    parser.add_argument(
        "--skip-metadata-enrichment",
        action="store_true",
        help="Desativa enriquecimento LLM durante reindexacao.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        logger.error("Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no .env")
        return 1

    docs_dir = args.docs_dir.resolve()
    if not docs_dir.is_dir():
        logger.error("Pasta docs-rag nao encontrada: %s", docs_dir)
        return 1

    repo_root = _resolve_repo_root().resolve()
    strategy: ChunkStrategy = args.strategy
    enrich_metadata = not args.skip_metadata_enrichment

    handler = _DocsRagHandler(
        docs_dir=docs_dir,
        repo_root=repo_root,
        strategy=strategy,
        enrich_metadata=enrich_metadata,
    )

    observer = Observer()
    observer.schedule(handler, str(docs_dir), recursive=True)
    observer.start()

    logger.info("Watcher ativo em %s", docs_dir)
    logger.info(
        "Configuracao: strategy=%s enrich_metadata=%s debounce=%.1fs",
        strategy,
        enrich_metadata,
        DEBOUNCE_SECONDS,
    )
    logger.info("Pressione Ctrl+C para parar.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Encerrando watcher...")
    finally:
        observer.stop()
        observer.join()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
