"""
Valida a inserção de chunks no Supabase.
Executa as queries de validação do plano de ingestão.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import supabase

def validate_insertion():
    print("\n=== VALIDAÇÃO DA INGESTÃO ===\n")
    
    # Query 1: Contar chunks inseridos
    print("1. Total de chunks inseridos:")
    result = supabase.table("knowledge_chunks").select("id", count="exact").execute()
    total = result.count if result.count is not None else 0
    print(f"   ✓ {total} chunks\n")
    
    # Query 2: Distribuição por fonte e estratégia
    print("2. Distribuição por fonte e estratégia:")
    result = supabase.table("knowledge_chunks").select("metadata").execute()
    if result.data:
        fontes = {}
        strategies = {}
        for row in result.data:
            meta = row.get('metadata') or {}
            fonte = meta.get('ingest_source', 'unknown')
            strategy = meta.get('chunk_strategy', 'unknown')
            fontes[fonte] = fontes.get(fonte, 0) + 1
            strategies[strategy] = strategies.get(strategy, 0) + 1
        
        print("   Por fonte:")
        for fonte, qtd in sorted(fontes.items()):
            print(f"     - {fonte}: {qtd} chunks")
        print("\n   Por estratégia:")
        for strat, qtd in sorted(strategies.items()):
            print(f"     - {strat}: {qtd} chunks")
    print()
    
    # Query 3: Amostra de chunks da base metodológica
    print("3. Amostra de chunks de 01_BASE_METODOLOGICA_NARA.md:")
    result = supabase.table("knowledge_chunks").select(
        "chapter, section, content, metadata"
    ).limit(500).execute()
    
    if result.data:
        # Procurar por chunks de "documentos" (contém o 01_BASE_METODOLOGICA_NARA.md)
        doc_chunks = [
            c for c in result.data 
            if (c.get('metadata') or {}).get('ingest_source') == 'documentos'
        ]
        print(f"   Encontrados {len(doc_chunks)} chunks da fonte 'documentos'\n")
        for i, chunk in enumerate(doc_chunks[:3], 1):
            meta = chunk.get('metadata') or {}
            strategy = meta.get('chunk_strategy')
            source_file = meta.get('source_file', 'unknown')
            content_preview = chunk.get('content', '')[:80].replace('\n', ' ')
            print(f"   [{i}] source_file={source_file}")
            print(f"       chapter={chunk.get('chapter')}, strategy={strategy}")
            print(f"       section={chunk.get('section')}")
            print(f"       preview: {content_preview}...\n")
    
    print("=== VALIDAÇÃO CONCLUÍDA ===\n")

if __name__ == "__main__":
    validate_insertion()
