"""
Ingestão da Parte V (Knowledge Base) do documento base metodológico.

Como usar:
  python -m scripts.ingest_knowledge_base

Esse script:
1. Lê `documentos/01_BASE_METODOLOGICA_NARA.md`
2. Extrai apenas os blocos JSON da PARTE V
3. Gera embeddings
4. Insere em `knowledge_chunks` com metadados ricos
"""
import asyncio
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.rag.embeddings import generate_embeddings_batch
from app.rag.ingest import upsert_chunks_for_source

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)
KNOWLEDGE_BASE_SOURCE = "documentos/01_BASE_METODOLOGICA_NARA.md"


def _extract_part_v_json_blocks(doc_text: str) -> list[dict[str, Any]]:
    start_marker = "# PARTE V: KNOWLEDGE BASE"
    end_marker = "# PARTE VI:"
    start = doc_text.find(start_marker)
    if start == -1:
        return []
    end = doc_text.find(end_marker, start)
    section = doc_text[start:end if end != -1 else len(doc_text)]

    blocks = re.findall(r"```json\s*(\{.*?\})\s*```", section, flags=re.DOTALL)
    parsed: list[dict[str, Any]] = []
    for raw in blocks:
        try:
            parsed.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return parsed


def _to_row(entry: dict[str, Any], embedding: list[float]) -> dict[str, Any]:
    chapter = entry.get("chapter", "Metodologia")
    area_id = entry.get("area_id")
    section = entry.get("section", "Knowledge Base")
    content = entry.get("content", "")
    componentes_dominio_m2 = entry.get("componentes_dominio_m2", [])
    sinais_conflito_m1 = entry.get("sinais_conflito_m1", [])

    # Extrair motor_motivacional de conexao_motores.
    conexao = entry.get("conexao_motores", {})
    motores_ativos = []
    if isinstance(conexao, dict):
        motores_ativos = [k for k, v in conexao.items() if v and str(v).strip()]
    motor_motivacional = motores_ativos[:2] if motores_ativos else None

    # Inferir ponto_entrada a partir de sinais de conflito do M1.
    sinais_lower = [str(s).lower() for s in sinais_conflito_m1 if s]
    if sinais_lower:
        if any("vergonha" in s or "autoimagem" in s for s in sinais_lower):
            ponto_entrada = "Emocional"
        elif any("sentido" in s or "valores" in s for s in sinais_lower):
            ponto_entrada = "Simbolico"
        elif any("paralisia" in s or "hábito" in s or "habito" in s for s in sinais_lower):
            ponto_entrada = "Comportamental"
        else:
            ponto_entrada = "Existencial"
    else:
        ponto_entrada = None

    # Heurística de relevância para retrieval:
    # - Domínios são lentes transversais e não substituem as fases.
    # - Aqui inferimos domínios sugeridos e uma fase de maior correlação para priorização.
    componentes_texto = " ".join([str(c).lower() for c in componentes_dominio_m2 if c])
    dominios_sugeridos: list[str] = []
    if any(k in componentes_texto for k in ["motiva", "conflito", "semente"]):
        dominios_sugeridos.append("D1")
    if any(k in componentes_texto for k in ["crença", "crenca", "valor", "princípio", "principio"]):
        dominios_sugeridos.append("D2")
    if any(k in componentes_texto for k in ["disciplina", "hábito", "habito", "desenvolv"]):
        dominios_sugeridos.append("D3")
    if any(k in componentes_texto for k in ["congruência", "congruencia", "cultura", "expressão", "expressao"]):
        dominios_sugeridos.append("D4")
    if any(k in componentes_texto for k in ["personagem", "transformação", "transformacao"]):
        dominios_sugeridos.append("D5")
    if any(k in componentes_texto for k in ["sociedade", "impacto", "legado"]):
        dominios_sugeridos.append("D6")

    # Fase de maior correlação usada como fallback de ranqueamento semântico.
    if "D1" in dominios_sugeridos:
        estagio_jornada = "Germinar"
    elif "D2" in dominios_sugeridos:
        estagio_jornada = "Enraizar"
    elif "D3" in dominios_sugeridos:
        estagio_jornada = "Desenvolver"
    elif "D4" in dominios_sugeridos:
        estagio_jornada = "Florescer"
    elif "D5" in dominios_sugeridos:
        estagio_jornada = "Frutificar"
    elif "D6" in dominios_sugeridos:
        estagio_jornada = "Realizar"
    else:
        estagio_jornada = None

    metadata = {
        "source_file": "01_BASE_METODOLOGICA_NARA.md",
        "source": KNOWLEDGE_BASE_SOURCE,
        "chunk_strategy": "knowledge_base_json",
        "area_id": area_id,
        "componentes_dominio_m2": componentes_dominio_m2,
        "dominios_sugeridos": dominios_sugeridos,
        "sinais_conflito_m1": sinais_conflito_m1,
        "perguntas_diagnosticas": entry.get("perguntas_diagnosticas", []),
        "indicadores_positivos": entry.get("indicadores_positivos", []),
        "indicadores_negativos": entry.get("indicadores_negativos", []),
        "padroes_autossabotagem": entry.get("padroes_autossabotagem", []),
        "conexao_motores": entry.get("conexao_motores", {}),
        "tipo_conteudo": "knowledge_base",
    }

    # Conteúdo principal + anexos importantes para melhorar recall semântico.
    extended_content_parts = [
        content,
        "\nComponentes de domínio: " + " | ".join(componentes_dominio_m2),
        "\nSinais de conflito: " + " | ".join(sinais_conflito_m1),
        "\nPerguntas diagnósticas: " + " | ".join(entry.get("perguntas_diagnosticas", [])),
    ]
    extended_content = "".join([part for part in extended_content_parts if part.strip()])

    return {
        "source": KNOWLEDGE_BASE_SOURCE,
        "chapter": chapter,
        "section": section,
        "content": extended_content,
        "embedding": embedding,
        "metadata": metadata,
        "motor_motivacional": motor_motivacional,
        "estagio_jornada": estagio_jornada,
        "tipo_crise": None,
        "ponto_entrada": ponto_entrada,
        "sintomas_comportamentais": entry.get("padroes_autossabotagem", []),
        "tom_emocional": None,
        "nivel_maturidade": None,
        "subtipo_crise": None,
        "tipo_conteudo": "knowledge_base",
        "dominio": dominios_sugeridos or None,
        "is_active": True,
    }


async def main() -> None:
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        logger.error("Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no .env")
        sys.exit(1)
    if not settings.OPENAI_API_KEY:
        logger.error("Defina OPENAI_API_KEY no .env")
        sys.exit(1)

    backend_root = Path(__file__).resolve().parent.parent
    doc_path = backend_root.parent / "documentos" / "01_BASE_METODOLOGICA_NARA.md"
    if not doc_path.exists():
        logger.error("Documento não encontrado: %s", doc_path)
        sys.exit(1)

    text = doc_path.read_text(encoding="utf-8", errors="replace")
    entries = _extract_part_v_json_blocks(text)
    if not entries:
        logger.error("Nenhum bloco JSON da PARTE V foi encontrado.")
        sys.exit(1)

    logger.info("Blocos da PARTE V encontrados: %d", len(entries))
    contents = []
    for entry in entries:
        c = entry.get("content", "")
        c += "\n" + " ".join(entry.get("sinais_conflito_m1", []))
        c += "\n" + " ".join(entry.get("componentes_dominio_m2", []))
        contents.append(c)

    embeddings = await generate_embeddings_batch(contents)
    rows = [_to_row(entry, embeddings[idx]) for idx, entry in enumerate(entries)]

    inserted_count = upsert_chunks_for_source(KNOWLEDGE_BASE_SOURCE, rows)
    logger.info("Upsert concluído. Registros inseridos: %d", inserted_count)


if __name__ == "__main__":
    asyncio.run(main())
