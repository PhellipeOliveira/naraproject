"""
Testa o retriever RAG contra o Supabase.
Valida que os chunks são retornados corretamente após o novo seed.

Uso (com venv ativado, na raiz do nara-backend):
  python -m scripts.test_retriever
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.rag.retriever import retrieve_relevant_chunks, retrieve_for_question_generation


async def run() -> int:
    print("\n=== TESTE DO RETRIEVER RAG ===")
    print(
        f"Config: threshold={settings.RAG_SIMILARITY_THRESHOLD}  "
        f"top_k={settings.RAG_TOP_K}\n"
    )

    queries = [
        "motores motivacionais jornada transformação",
        "saúde física identidade crise",
        "âncoras práticas TCC ponto de entrada",
    ]

    total_ok = 0
    for query in queries:
        print(f"Query: \"{query}\"")
        try:
            chunks = await retrieve_relevant_chunks(query, top_k=3)
            n = len(chunks)
            print(f"  → {n} chunk(s) retornado(s)")
            if n > 0:
                c = chunks[0]
                meta = c.get("metadata") or {}
                source_in_row = c.get("source")
                strategy_in_meta = meta.get("chunk_strategy")
                print(f"     chapter={c.get('chapter')}  section={c.get('section')}")
                print(f"     source={source_in_row}  chunk_strategy={strategy_in_meta}")
                print(f"     preview: {c.get('content', '')[:80].replace(chr(10), ' ')}...")
                total_ok += 1
            else:
                print("  ⚠️  0 chunks — verifique se o seed foi executado e os embeddings gerados.")
        except Exception as e:
            print(f"  ❌ Erro: {e}")
        print()

    # Teste do retrieve_for_question_generation (simula transição de fase)
    print("--- Teste retrieve_for_question_generation (simula fase 2) ---")
    fake_responses = [
        {"answer_value": {"text": "Me sinto travado na vida profissional e sem direção clara."}},
        {"answer_value": {"text": "Tenho dificuldade de manter rotina e energia."}},
    ]
    try:
        context = await retrieve_for_question_generation(
            user_responses=fake_responses,
            underrepresented_areas=["Vida Profissional", "Saúde Física"],
            phase=2,
        )
        if context.strip():
            print(f"  ✓ Contexto gerado: {len(context)} chars")
            print(f"  Preview: {context[:120].replace(chr(10), ' ')}...")
        else:
            print("  ⚠️  Contexto vazio — RAG não retornou chunks para essa query.")
    except Exception as e:
        print(f"  ❌ Erro: {e}")

    print("\n=== RESULTADO ===")
    if total_ok == len(queries):
        print(f"✓ Todos os {total_ok} testes retornaram chunks. RAG funcionando.")
        return 0
    else:
        print(f"⚠️  {total_ok}/{len(queries)} queries retornaram chunks.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
