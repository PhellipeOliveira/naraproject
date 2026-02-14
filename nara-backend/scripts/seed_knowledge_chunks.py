"""
Script para popular a tabela knowledge_chunks com dados mínimos e gerar embeddings.

Uso (na raiz do nara-backend):
  python -m scripts.seed_knowledge_chunks

Requer: SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY no .env
"""
import asyncio
import logging
import sys
from pathlib import Path

# Garantir que app seja encontrado
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.database import supabase
from app.rag.embeddings import generate_embeddings_batch

from scripts.seed_knowledge_chunks_data import CHUNKS

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


async def main() -> None:
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        logger.error("Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no .env")
        sys.exit(1)
    if not settings.OPENAI_API_KEY:
        logger.error("Defina OPENAI_API_KEY no .env para gerar embeddings")
        sys.exit(1)

    texts = [c["content"] for c in CHUNKS]
    logger.info("Gerando embeddings para %d chunks...", len(texts))
    embeddings = await generate_embeddings_batch(texts)

    rows = []
    for i, chunk in enumerate(CHUNKS):
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
                "sintomas_comportamentais": chunk.get("sintomas", []),
                "tom_emocional_base": chunk.get("tom_emocional"),
                "source": "seed_script",
                "version": "1.0",
            },
            "motor_motivacional": chunk.get("motor_motivacional"),
            "estagio_jornada": chunk.get("estagio_jornada"),
            "tipo_crise": chunk.get("tipo_crise"),
            "ponto_entrada": chunk.get("ponto_entrada"),
            "sintomas": chunk.get("sintomas"),
            "tom_emocional": chunk.get("tom_emocional"),
            "is_active": True,
            "version": 1,
        }
        rows.append(row)

    logger.info("Inserindo %d chunks no Supabase...", len(rows))
    result = supabase.table("knowledge_chunks").insert(rows).execute()
    logger.info("Inseridos %d registros.", len(result.data))
    logger.info("Pronto. Execute a migração 20260213000005 para criar o índice vetorial (ou rode após este seed).")


if __name__ == "__main__":
    asyncio.run(main())
