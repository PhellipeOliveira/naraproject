"""
Testa o retriever RAG com chunks semantic.
Parte da validação do plano de ingestão.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.retriever import retrieve_relevant_chunks

async def test_retriever():
    print("\n=== TESTE DO RETRIEVER ===\n")
    
    query = 'motores motivacionais jornada transformação'
    print(f"Query: '{query}'\n")
    
    try:
        chunks = await retrieve_relevant_chunks(query, top_k=5)
        print(f"✓ Chunks recuperados: {len(chunks)}\n")
        
        if not chunks:
            print("⚠️  Nenhum chunk retornado. Verificar:")
            print("   - Embeddings foram gerados corretamente?")
            print("   - Threshold de similaridade está muito alto?")
            return
        
        all_semantic = all(
            (c.get('metadata') or {}).get('chunk_strategy') == 'semantic' 
            for c in chunks
        )
        
        if all_semantic:
            print("✓ Todos os chunks são SEMANTIC (filtro funcionando)\n")
        else:
            print("⚠️  Alguns chunks NÃO são semantic\n")
        
        print("Amostra dos chunks retornados:\n")
        for i, c in enumerate(chunks[:3], 1):
            meta = c.get('metadata') or {}
            strat = meta.get('chunk_strategy')
            src = meta.get('source_file')
            content_preview = c.get('content', '')[:80].replace('\n', ' ')
            print(f"{i}. {src}")
            print(f"   strategy={strat} | chapter={c.get('chapter')}")
            print(f"   section={c.get('section')}")
            print(f"   preview: {content_preview}...")
            print()
        
        print("=== TESTE CONCLUÍDO COM SUCESSO ===\n")
        
    except Exception as e:
        print(f"❌ Erro ao testar retriever: {e}")
        print("\nVerificar:")
        print("  - OPENAI_API_KEY está válida no .env")
        print("  - Migration filter_chunk_strategy foi aplicada no Supabase")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_retriever())
    sys.exit(exit_code or 0)
