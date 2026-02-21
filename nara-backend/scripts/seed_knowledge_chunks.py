"""
Script para popular a tabela knowledge_chunks com a base metodológica NARA.

Uso (na raiz do nara-backend):
  python -m scripts.seed_knowledge_chunks

Requer: SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY no .env
A versão gravada nos chunks é definida por RAG_CHUNK_VERSION em config.py.
"""
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.database import supabase
from app.rag.embeddings import generate_embeddings_batch
from scripts.seed_knowledge_chunks_data_v2 import CHUNKS_V2

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


async def seed_chunks(chunks: list[dict]) -> None:
    """Gera embeddings e insere chunks na tabela knowledge_chunks."""
    texts = [c["content"] for c in chunks]
    logger.info("Gerando embeddings para %d chunks...", len(texts))
    embeddings = await generate_embeddings_batch(texts)

    rows = []
    for i, chunk in enumerate(chunks):
        sintomas = chunk.get("sintomas_comportamentais") or chunk.get("sintomas", [])
        row = {
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
                "chunk_strategy": settings.RAG_CHUNK_STRATEGY,
                "source": "seed_script",
                "version": str(settings.RAG_CHUNK_VERSION),
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
            "version": settings.RAG_CHUNK_VERSION,
        }
        rows.append(row)

    logger.info("Inserindo %d chunks no Supabase...", len(rows))
    result = supabase.table("knowledge_chunks").insert(rows).execute()
    logger.info("Inseridos %d registros.", len(result.data))


async def main() -> None:
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        logger.error("Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no .env")
        sys.exit(1)
    if not settings.OPENAI_API_KEY:
        logger.error("Defina OPENAI_API_KEY no .env para gerar embeddings")
        sys.exit(1)

    logger.info("Iniciando seed — versão %d (Base Metodológica NARA)", settings.RAG_CHUNK_VERSION)
    await seed_chunks(CHUNKS_V2)
    logger.info("Pronto. Execute a migração de índice vetorial se ainda não tiver executado.")


if __name__ == "__main__":
    asyncio.run(main())
