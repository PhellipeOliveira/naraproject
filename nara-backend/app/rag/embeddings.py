"""Geração de embeddings via OpenAI."""
import logging

from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_embedding(text: str) -> list[float]:
    """
    Gera embedding para um texto.

    Args:
        text: Texto para gerar embedding

    Returns:
        Lista de floats (vetor, ex.: 1536 dimensões para text-embedding-3-small)
    """
    response = await client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


async def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """
    Gera embeddings para múltiplos textos em batch.

    Args:
        texts: Lista de textos

    Returns:
        Lista de vetores
    """
    response = await client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]
