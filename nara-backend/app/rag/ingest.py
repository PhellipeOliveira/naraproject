"""
Ingestão de documentos para a base RAG (knowledge_chunks).

Conforme 01_FUNDAMENTOS.md § 3 (Inteligência Contextual via RAG):
- Cada chunk deve responder: "Que tipo de ser humano este texto ajuda a identificar?"
- Metadados: motor_motivacional, estagio_jornada, tipo_crise, ponto_entrada, etc.

Fontes: pasta docs-rag/ (e opcionalmente documentos/01_FUNDAMENTOS.md como guia).
"""

import logging
import re
import json
from pathlib import Path
from typing import Any, Literal, Optional

from app.core.constants import AREAS
from app.config import settings
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)
_metadata_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


# Tamanho alvo por chunk (caracteres); overlap para manter contexto
# Valores maiores = menos chunks, menos custo de embedding, RAG mais estável
CHUNK_MAX_CHARS = 1500
CHUNK_OVERLAP_CHARS = 200
# Ignorar chunks menores que isso (evita 47k+ fragmentos)
CHUNK_MIN_CHARS = 100

# Estratégias: "size" = por tamanho/overlap, "semantic" = por parágrafos completos, "both" = as duas
ChunkStrategy = Literal["size", "semantic", "both"]

MOTORES_VALIDOS = ["Necessidade", "Valor", "Desejo", "Propósito"]
ESTAGIOS_VALIDOS = ["Germinar", "Enraizar", "Desenvolver", "Florescer", "Frutificar", "Realizar"]
TIPOS_CRISE_VALIDOS = [
    "Identidade Raiz",
    "Sentido e Direção",
    "Execução e Estrutura",
    "Conexão e Expressão",
    "Incongruência Identidade-Cultura",
    "Transformação de Personagem",
]
PONTOS_ENTRADA_VALIDOS = ["Emocional", "Simbólico", "Comportamental", "Existencial"]
TIPOS_CONTEUDO_VALIDOS = ["Ponto de Entrada", "Âncora Prática", "Técnica de TCC", "Conceito", "Exemplo de Caso"]
DOMINIOS_VALIDOS = ["D1", "D2", "D3", "D4", "D5", "D6"]
NIVEIS_MATURIDADE_VALIDOS = ["baixo", "médio", "alto"]


def _normalize_heading(line: str) -> str:
    """Remove marcadores markdown do cabeçalho."""
    return line.lstrip("#").strip().strip()


def _split_by_headers(content: str) -> list[tuple[str, str]]:
    """
    Divide o texto por cabeçalhos ## (apenas nível 2, para menos fragmentação).
    Retorna lista de (titulo, trecho).
    """
    parts: list[tuple[str, str]] = []
    # Apenas ## (não ###) para ter menos seções e chunks maiores
    pattern = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    last_end = 0
    current_title = "Conteúdo"
    for m in pattern.finditer(content):
        start = m.start()
        if start > last_end:
            chunk_text = content[last_end:start].strip()
            if chunk_text:
                parts.append((current_title, chunk_text))
        current_title = _normalize_heading(m.group(1))
        last_end = m.end()
    if last_end < len(content):
        chunk_text = content[last_end:].strip()
        if chunk_text:
            parts.append((current_title, chunk_text))
    if not parts and content.strip():
        parts.append(("Conteúdo", content.strip()))
    return parts


def _split_large_chunk(text: str, max_chars: int = CHUNK_MAX_CHARS, overlap: int = CHUNK_OVERLAP_CHARS) -> list[str]:
    """Quebra um trecho grande em blocos com overlap."""
    if len(text) <= max_chars:
        return [text] if text.strip() else []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            # Quebrar em fim de frase ou parágrafo
            break_at = text.rfind("\n\n", start, end + 1)
            if break_at == -1:
                break_at = text.rfind(". ", start, end + 1)
            if break_at == -1:
                break_at = text.rfind(" ", start, end + 1)
            if break_at != -1:
                end = break_at + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        # Avançar sempre (evitar loop infinito se overlap >= max_chars)
        start = max(start + 1, end - overlap)
        if start >= len(text):
            break
    return chunks


def _split_into_paragraphs(text: str) -> list[str]:
    """Divide o texto em parágrafos (blocos separados por \\n\\n)."""
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def _chunk_by_paragraphs(
    paragraphs: list[str],
    max_chars: int = CHUNK_MAX_CHARS,
    min_chars: int = CHUNK_MIN_CHARS,
) -> list[str]:
    """
    Agrupa parágrafos consecutivos até atingir max_chars.
    Nunca corta no meio de um parágrafo = chunks semânticos (unidade de sentido).
    """
    if not paragraphs:
        return []
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for p in paragraphs:
        p_len = len(p) + 2  # +2 para \n\n
        if current_len + p_len > max_chars and current:
            chunks.append("\n\n".join(current))
            current = []
            current_len = 0
        current.append(p)
        current_len += p_len
    if current:
        merged = "\n\n".join(current)
        if len(merged) >= min_chars or not chunks:
            chunks.append(merged)
        elif chunks:
            chunks[-1] = chunks[-1].rstrip() + "\n\n" + merged
    return chunks


def _infer_chapter_from_content(content: str, filename: str) -> str:
    """
    Tenta inferir a área (chapter) a partir do conteúdo ou nome do arquivo.
    Usa as 12 Áreas Estruturantes de 01_FUNDAMENTOS.
    """
    content_lower = (content + " " + filename).lower()
    for area in AREAS:
        if area.lower() in content_lower:
            return area
    # Mapeamento por prefixo/nome de arquivo comum
    if "publico" in filename.lower() or "público" in content_lower:
        return "Metodologia"
    if "crise" in filename.lower() or "crises" in filename.lower():
        return "Metodologia"
    if "intervenção" in content_lower or "intervencao" in content_lower:
        return "Metodologia"
    if "relating" in content_lower or "comunicacao" in content_lower:
        return "Metodologia"
    return "Metodologia"


def chunk_markdown(
    content: str,
    source_path: str,
    *,
    max_chars: int = CHUNK_MAX_CHARS,
    overlap: int = CHUNK_OVERLAP_CHARS,
    infer_chapter: bool = True,
) -> list[dict[str, Any]]:
    """
    Gera chunks a partir de um único documento markdown.

    Args:
        content: Conteúdo bruto do .md
        source_path: Caminho do arquivo (para metadata e inferência)
        max_chars: Tamanho máximo por chunk
        overlap: Overlap entre chunks
        infer_chapter: Se True, tenta inferir chapter (área) pelo conteúdo

    Returns:
        Lista de dicts com keys: content, chapter, section, source_file, metadata
        (prontos para enriquecer com motor_motivacional, etc. e enviar ao DB)
    """
    chunks_out: list[dict[str, Any]] = []
    parts = _split_by_headers(content)
    source_name = Path(source_path).name

    for section_title, segment in parts:
        if not segment.strip():
            continue
        sub_chunks = _split_large_chunk(segment, max_chars=max_chars, overlap=overlap)
        for i, text in enumerate(sub_chunks):
            if not text.strip():
                continue
            # Juntar trechos muito pequenos ao chunk anterior (reduz 47k+ → ordem de milhares)
            if len(text) < CHUNK_MIN_CHARS and chunks_out:
                last = chunks_out[-1]
                last["content"] = last["content"].rstrip() + "\n\n" + text.strip()
                continue
            chapter = _infer_chapter_from_content(text, source_name) if infer_chapter else "Metodologia"
            section = section_title if len(sub_chunks) == 1 else f"{section_title} (parte {i + 1})"
            metadata: dict[str, Any] = {
                "source_file": source_name,
                "source_path": source_path,
                "section": section,
                "ingest_source": "docs_rag",
                "chunk_strategy": "size",
            }
            chunks_out.append({
                "content": text,
                "chapter": chapter,
                "section": section,
                "metadata": metadata,
                "source_file": source_name,
            })
    return chunks_out


def chunk_markdown_semantic(
    content: str,
    source_path: str,
    *,
    max_chars: int = CHUNK_MAX_CHARS,
    infer_chapter: bool = True,
) -> list[dict[str, Any]]:
    """
    Gera chunks semânticos: agrupa por parágrafos completos (nunca corta no meio).
    Cada chunk = um ou mais parágrafos até max_chars. Melhor coerência para o RAG.
    """
    chunks_out: list[dict[str, Any]] = []
    parts = _split_by_headers(content)
    source_name = Path(source_path).name

    for section_title, segment in parts:
        if not segment.strip():
            continue
        paragraphs = _split_into_paragraphs(segment)
        if not paragraphs:
            continue
        sub_chunks = _chunk_by_paragraphs(paragraphs, max_chars=max_chars, min_chars=CHUNK_MIN_CHARS)
        for i, text in enumerate(sub_chunks):
            if not text.strip():
                continue
            chapter = _infer_chapter_from_content(text, source_name) if infer_chapter else "Metodologia"
            section = section_title if len(sub_chunks) == 1 else f"{section_title} (parte {i + 1})"
            metadata: dict[str, Any] = {
                "source_file": source_name,
                "source_path": source_path,
                "section": section,
                "ingest_source": "docs_rag",
                "chunk_strategy": "semantic",
            }
            chunks_out.append({
                "content": text,
                "chapter": chapter,
                "section": section,
                "metadata": metadata,
                "source_file": source_name,
            })
    return chunks_out


def load_docs_from_directory(docs_dir: Path, extensions: tuple[str, ...] = (".md",)) -> list[tuple[str, str]]:
    """
    Carrega todos os arquivos com extensão dada de um diretório (recursivo).

    Returns:
        Lista de (caminho_relativo_ou_nome, conteúdo)
    """
    if not docs_dir.is_dir():
        return []
    out: list[tuple[str, str]] = []
    for path in sorted(docs_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in extensions:
            try:
                raw = path.read_text(encoding="utf-8", errors="replace")
                out.append((str(path), raw))
            except Exception:
                continue
    return out


def build_chunks_from_docs(
    docs_dir: Path,
    *,
    extra_files: Optional[list[Path]] = None,
    max_chars: int = CHUNK_MAX_CHARS,
    overlap: int = CHUNK_OVERLAP_CHARS,
    strategy: ChunkStrategy = "size",
) -> list[dict[str, Any]]:
    """
    Monta todos os chunks a partir de docs_dir e de arquivos extras (ex.: 01_FUNDAMENTOS.md).

    Args:
        docs_dir: Pasta principal (ex.: docs-rag)
        extra_files: Arquivos adicionais (ex.: documentos/01_FUNDAMENTOS.md)
        max_chars: Tamanho máximo por chunk
        overlap: Overlap entre chunks (só para strategy="size")
        strategy: "size" = por tamanho/overlap, "semantic" = por parágrafos, "both" = os dois

    Returns:
        Lista de dicts no formato esperado por knowledge_chunks (sem embedding ainda).
    """
    all_chunks: list[dict[str, Any]] = []
    seen_paths: set[str] = set()

    def process(content: str, path_str: str, ingest_source: str = "docs_rag") -> None:
        if strategy in ("size", "both"):
            for c in chunk_markdown(content, path_str, max_chars=max_chars, overlap=overlap):
                if ingest_source != "docs_rag":
                    c["metadata"] = {**c.get("metadata", {}), "ingest_source": ingest_source}
                all_chunks.append(c)
        if strategy in ("semantic", "both"):
            for c in chunk_markdown_semantic(content, path_str, max_chars=max_chars):
                if ingest_source != "docs_rag":
                    c["metadata"] = {**c.get("metadata", {}), "ingest_source": ingest_source}
                all_chunks.append(c)

    files_from_dir = load_docs_from_directory(docs_dir)
    total_files = len(files_from_dir) + (len(extra_files) if extra_files else 0)
    n = 0

    for path_str, content in files_from_dir:
        if path_str in seen_paths:
            continue
        seen_paths.add(path_str)
        n += 1
        logger.info("  Processando %d/%d: %s", n, total_files, Path(path_str).name)
        process(content, path_str)

    if extra_files:
        for path in extra_files:
            if not path.is_file():
                continue
            path_str = str(path)
            if path_str in seen_paths:
                continue
            seen_paths.add(path_str)
            n += 1
            logger.info("  Processando %d/%d: %s", n, total_files, path.name)
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            process(content, path_str, ingest_source="documentos")

    return all_chunks


def chunks_to_knowledge_rows(
    chunks: list[dict[str, Any]],
    embeddings: list[list[float]],
    *,
    source_version: str = "docs_rag",
) -> list[dict[str, Any]]:
    """
    Converte lista de chunks + embeddings em linhas para insert em knowledge_chunks.

    A versão ativa é lida de settings.RAG_CHUNK_VERSION (centralizado em config.py).
    """
    from app.config import settings

    rows: list[dict[str, Any]] = []
    for i, ch in enumerate(chunks):
        emb = embeddings[i] if i < len(embeddings) else None
        meta = ch.get("metadata") or {}
        meta["source_version"] = source_version
        motor_motivacional = meta.get("motor_motivacional")
        estagio_jornada = meta.get("estagio_jornada")
        tipo_crise = meta.get("tipo_crise")
        ponto_entrada = meta.get("ponto_entrada")
        sintomas_comportamentais = meta.get("sintomas_comportamentais")
        tom_emocional = meta.get("tom_emocional_base")
        nivel_maturidade = meta.get("nivel_maturidade")
        subtipo_crise = meta.get("subtipo_crise")
        tipo_conteudo = meta.get("tipo_conteudo")
        dominio = meta.get("dominio")
        row = {
            "chapter": ch.get("chapter", "Metodologia"),
            "section": ch.get("section"),
            "content": ch["content"],
            "embedding": emb,
            "metadata": meta,
            "motor_motivacional": motor_motivacional,
            "estagio_jornada": estagio_jornada,
            "tipo_crise": tipo_crise,
            "ponto_entrada": ponto_entrada,
            "sintomas_comportamentais": sintomas_comportamentais,
            "tom_emocional": tom_emocional,
            "nivel_maturidade": nivel_maturidade,
            "subtipo_crise": subtipo_crise,
            "tipo_conteudo": tipo_conteudo,
            "dominio": dominio,
            "is_active": True,
            "version": settings.RAG_CHUNK_VERSION,
        }
        rows.append(row)
    return rows


def _safe_list(values: Any, valid_options: list[str]) -> list[str]:
    if not isinstance(values, list):
        return []
    return [v for v in values if isinstance(v, str) and v in valid_options]


def _safe_string(value: Any, valid_options: list[str]) -> Optional[str]:
    if isinstance(value, str) and value in valid_options:
        return value
    return None


def _normalize_llm_metadata(raw: dict[str, Any]) -> dict[str, Any]:
    """Normaliza saída do LLM para os campos de metadata suportados."""
    return {
        "motor_motivacional": _safe_list(raw.get("motor_motivacional"), MOTORES_VALIDOS),
        "estagio_jornada": _safe_list(raw.get("estagio_jornada"), ESTAGIOS_VALIDOS),
        "tipo_crise": _safe_list(raw.get("tipo_crise"), TIPOS_CRISE_VALIDOS),
        "subtipo_crise": raw.get("subtipo_crise") if isinstance(raw.get("subtipo_crise"), str) else None,
        "dominio": _safe_list(raw.get("dominio"), DOMINIOS_VALIDOS),
        "ponto_entrada": _safe_string(raw.get("ponto_entrada"), PONTOS_ENTRADA_VALIDOS),
        "tipo_conteudo": _safe_string(raw.get("tipo_conteudo"), TIPOS_CONTEUDO_VALIDOS),
        "sintomas_comportamentais": [
            s for s in (raw.get("sintomas_comportamentais") or []) if isinstance(s, str)
        ][:6],
        "tom_emocional_base": raw.get("tom_emocional_base")
        if isinstance(raw.get("tom_emocional_base"), str)
        else None,
        "nivel_maturidade": _safe_string(raw.get("nivel_maturidade"), NIVEIS_MATURIDADE_VALIDOS),
    }


async def enrich_chunks_metadata_with_llm(
    chunks: list[dict[str, Any]],
    *,
    model: Optional[str] = None,
) -> list[dict[str, Any]]:
    """
    Enriquece metadados dos chunks usando LLM.
    Essa etapa melhora o RAG ao preencher motor/crise/ponto de entrada no momento da ingestão.
    """
    if not chunks:
        return []
    if not settings.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY ausente; pulando enriquecimento de metadata.")
        return chunks

    metadata_model = model or settings.OPENAI_MODEL_QUESTIONS
    enriched_chunks: list[dict[str, Any]] = []

    system_prompt = """
Você classifica trechos metodológicos NARA em metadados RAG.
Retorne somente JSON válido com estas chaves:
{
  "motor_motivacional": ["Necessidade|Valor|Desejo|Propósito"],
  "estagio_jornada": ["Germinar|Enraizar|Desenvolver|Florescer|Frutificar|Realizar"],
  "tipo_crise": ["Identidade Raiz|Sentido e Direção|Execução e Estrutura|Conexão e Expressão|Incongruência Identidade-Cultura|Transformação de Personagem"],
  "subtipo_crise": "string ou null",
  "dominio": ["D1|D2|D3|D4|D5|D6"],
  "ponto_entrada": "Emocional|Simbólico|Comportamental|Existencial|null",
  "tipo_conteudo": "Ponto de Entrada|Âncora Prática|Técnica de TCC|Conceito|Exemplo de Caso|null",
  "sintomas_comportamentais": ["string"],
  "tom_emocional_base": "string ou null",
  "nivel_maturidade": "baixo|médio|alto|null"
}
"""

    for idx, chunk in enumerate(chunks, start=1):
        content = (chunk.get("content") or "")[:3000]
        chapter = chunk.get("chapter", "Metodologia")
        section = chunk.get("section", "Conteúdo")
        user_prompt = (
            f"Chapter: {chapter}\n"
            f"Section: {section}\n"
            f"Texto:\n{content}\n\n"
            "Classifique este chunk da metodologia NARA."
        )
        try:
            response = await _metadata_client.chat.completions.create(
                model=metadata_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                response_format={"type": "json_object"},
                max_tokens=500,
            )
            parsed = json.loads(response.choices[0].message.content or "{}")
            normalized = _normalize_llm_metadata(parsed)
            metadata = chunk.get("metadata") or {}
            enriched_chunks.append({
                **chunk,
                "metadata": {**metadata, **normalized},
            })
        except Exception as exc:
            logger.warning("Falha ao enriquecer metadata do chunk %d: %s", idx, exc)
            enriched_chunks.append(chunk)

    return enriched_chunks
