"""
Verifica quantos chunks existem em knowledge_chunks e mostra um exemplo.

Uso (com venv ativado, na raiz do nara-backend):
  python -m scripts.check_knowledge_chunks

Requer: SUPABASE_URL e SUPABASE_SERVICE_KEY no .env
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import supabase

def main():
    r = supabase.table("knowledge_chunks").select("id, chapter, section, content", count="exact").limit(1).execute()
    total = r.count if hasattr(r, "count") and r.count is not None else "?"
    print(f"Total de chunks em knowledge_chunks: {total}")
    if r.data and len(r.data) > 0:
        row = r.data[0]
        content = (row.get("content") or "")[:200]
        print(f"Exemplo: chapter={row.get('chapter')}, section={row.get('section')}")
        print(f"  content (200 chars): {content}...")
    else:
        print("Nenhum registro encontrado. Rode: python -m scripts.ingest_docs_rag")
    # Contar com embedding preenchido (necessário para RAG)
    r2 = supabase.table("knowledge_chunks").select("id", count="exact").not_.is_("embedding", "null").limit(1).execute()
    with_emb = r2.count if hasattr(r2, "count") and r2.count is not None else "?"
    print(f"Chunks com embedding (usados no RAG): {with_emb}")

if __name__ == "__main__":
    main()
