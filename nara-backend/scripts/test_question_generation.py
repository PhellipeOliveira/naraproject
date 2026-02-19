"""
Testa a geração de perguntas adaptativas com o analyzer integrado.
Validação end-to-end do fluxo backend.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.analyzer import analyze_answers_context
from app.rag.generator import generate_adaptive_questions
from app.rag.retriever import retrieve_for_question_generation


# Respostas de exemplo simulando fase 1 completa
SAMPLE_RESPONSES = [
    {
        "question_area": "Vida Pessoal",
        "question_text": "Título do momento atual?",
        "answer_value": {"text": "Transição forçada. Sinto que perdi quem eu sou."}
    },
    {
        "question_area": "Saúde Mental",
        "question_text": "Pensamentos quando fica difícil?",
        "answer_value": {"text": "Não sou bom o suficiente. Medo de falhar e ser julgado."}
    },
    {
        "question_area": "Vida Profissional",
        "question_text": "Pode ser você mesmo no trabalho?",
        "answer_value": {"text": "Não. Finjo ser alguém que não sou. Só estou por dinheiro."}
    },
    {
        "question_area": "Saúde Espiritual",
        "question_text": "O que faz sua vida valer a pena?",
        "answer_value": {"text": "Não vejo mais sentido. Perdi o fio da meada. Tudo virou obrigação."}
    },
    {
        "question_area": "Vida Familiar",
        "question_text": "Hábitos herdados da família?",
        "answer_value": {"text": "Trabalho duro é o único caminho. Não posso decepcionar. Isso me sufoca."}
    },
]


async def test_question_generation():
    print("\n=== TESTE DE GERAÇÃO DE PERGUNTAS ADAPTATIVAS ===\n")
    
    try:
        # 1. Análise contextual
        print("1. Analisando contexto das respostas...")
        context_analysis = await analyze_answers_context(
            responses=SAMPLE_RESPONSES,
            user_profile=None
        )
        print(f"   ✓ Motor identificado: {context_analysis.get('motor_dominante')}")
        print(f"   ✓ Clusters: {', '.join(context_analysis.get('clusters_identificados', [])[:2])}")
        print()
        
        # 2. Buscar contexto RAG
        print("2. Buscando contexto metodológico no RAG...")
        underrepresented_areas = ["Saúde Física", "Vida Amorosa", "Vida Social", "Finanças"]
        rag_context = await retrieve_for_question_generation(
            user_responses=SAMPLE_RESPONSES,
            underrepresented_areas=underrepresented_areas,
            phase=2
        )
        print(f"   ✓ Contexto RAG recuperado: {len(rag_context)} caracteres")
        print()
        
        # 3. Montar padrões identificados
        patterns = []
        if context_analysis.get("motor_dominante"):
            patterns.append(f"Motor dominante: {context_analysis['motor_dominante']}")
        if context_analysis.get("clusters_identificados"):
            patterns.append(f"Clusters: {', '.join(context_analysis['clusters_identificados'][:2])}")
        if context_analysis.get("areas_criticas"):
            patterns.append(f"Áreas críticas: {', '.join(context_analysis['areas_criticas'][:2])}")
        
        # 4. Gerar perguntas adaptativas
        print("3. Gerando 15 perguntas adaptativas para Fase 2...")
        questions = await generate_adaptive_questions(
            user_responses=SAMPLE_RESPONSES,
            underrepresented_areas=underrepresented_areas,
            identified_patterns=patterns,
            rag_context=rag_context,
            phase=2
        )
        
        print(f"   ✓ {len(questions)} perguntas geradas!\n")
        
        # 5. Mostrar primeiras 5 perguntas
        print("PRIMEIRAS 5 PERGUNTAS GERADAS:\n")
        for i, q in enumerate(questions[:5], 1):
            print(f"{i}. [{q['area']}]")
            print(f"   {q['text'][:120]}...")
            print()
        
        print("=== TESTE CONCLUÍDO COM SUCESSO ===\n")
        return 0
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(test_question_generation())
    sys.exit(exit_code)
