"""
Script para popular a tabela knowledge_chunks com a base metodológica NARA.

Uso (na raiz do nara-backend):
  python -m scripts.seed_knowledge_chunks

Requer: SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY no .env
"""
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.rag.embeddings import generate_embeddings_batch
from app.rag.ingest import upsert_chunks_for_source
from scripts.seed_knowledge_chunks_data_v2 import CHUNKS_V2

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)
SEED_SOURCE = "seed/knowledge_chunks_v2"


async def seed_chunks(chunks: list[dict]) -> None:
    """Gera embeddings e insere chunks na tabela knowledge_chunks."""
    texts = [c["content"] for c in chunks]
    logger.info("Gerando embeddings para %d chunks...", len(texts))
    embeddings = await generate_embeddings_batch(texts)

    rows = []
    for i, chunk in enumerate(chunks):
        sintomas = chunk.get("sintomas_comportamentais") or chunk.get("sintomas", [])
        row = {
            "source": SEED_SOURCE,
            "chapter": chunk["chapter"],
            "section": chunk.get("section"),
            "content": chunk["content"],
            "embedding": embeddings[i] if i < len(embeddings) else None,
            "metadata": {
                "motor_motivacional": chunk.get("motor_motivacional", []),
                "estagio_jornada": chunk.get("estagio_jornada", []),
                "tipo_crise": chunk.get("tipo_crise", []),
                "ponto_entrada": chunk.get("ponto_entrada"),
                "sintomas_comportamentais": sintomas,
                "tom_emocional_base": chunk.get("tom_emocional"),
                "subtipo_crise": chunk.get("subtipo_crise"),
                "tipo_conteudo": chunk.get("tipo_conteudo"),
                "dominio": chunk.get("dominio", []),
                "nivel_maturidade": chunk.get("nivel_maturidade"),
                "chunk_strategy": "semantic",
                "source": SEED_SOURCE,
            },
            "motor_motivacional": chunk.get("motor_motivacional"),
            "estagio_jornada": chunk.get("estagio_jornada"),
            "tipo_crise": chunk.get("tipo_crise"),
            "ponto_entrada": chunk.get("ponto_entrada"),
            "sintomas_comportamentais": sintomas,
            "tom_emocional": chunk.get("tom_emocional"),
            "nivel_maturidade": chunk.get("nivel_maturidade"),
            "subtipo_crise": chunk.get("subtipo_crise"),
            "tipo_conteudo": chunk.get("tipo_conteudo"),
            "dominio": chunk.get("dominio"),
            "is_active": True,
        }
        rows.append(row)

    logger.info("Aplicando upsert de %d chunks no Supabase...", len(rows))
    inserted = upsert_chunks_for_source(SEED_SOURCE, rows)
    logger.info("Inseridos %d registros.", inserted)


async def main() -> None:
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        logger.error("Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no .env")
        sys.exit(1)
    if not settings.OPENAI_API_KEY:
        logger.error("Defina OPENAI_API_KEY no .env para gerar embeddings")
        sys.exit(1)

    logger.info("Iniciando seed da Base Metodológica NARA")
    await seed_chunks(CHUNKS_V2)
    logger.info("Pronto. Execute a migração de índice vetorial se ainda não tiver executado.")


if __name__ == "__main__":
    asyncio.run(main())
