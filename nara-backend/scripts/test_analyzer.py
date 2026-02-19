"""
Testa o analyzer com respostas de exemplo.
Validação do fluxo backend completo.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.analyzer import analyze_answers_context


# Respostas de exemplo simulando um diagnóstico real
SAMPLE_RESPONSES = [
    {
        "question_area": "Vida Pessoal",
        "question_text": "Se você tivesse que dar um título para o momento que está vivendo agora, qual seria?",
        "answer_value": {
            "text": "Estou em um momento de transição. Sinto que carrego muitas expectativas dos outros e não sei mais quem eu sou de verdade. Tenho medo de decepcionar, mas ao mesmo tempo não aguento mais viver essa vida que não é minha."
        }
    },
    {
        "question_area": "Saúde Mental",
        "question_text": "Quando as coisas ficam difíceis, que tipo de pensamentos aparecem?",
        "answer_value": {
            "text": "Sempre penso que não sou bom o suficiente, que vou falhar. Fico paralisado porque tenho medo de errar e ser julgado. Isso me impede de agir e fico preso nesse ciclo."
        }
    },
    {
        "question_area": "Vida Profissional",
        "question_text": "No seu trabalho, você sente que pode ser você mesmo?",
        "answer_value": {
            "text": "Não. Sinto que estou fingindo ser alguém que não sou. Tenho um papel a desempenhar mas no fundo sei que não é isso que quero fazer da vida. Só estou ali pelo dinheiro e pela segurança."
        }
    },
    {
        "question_area": "Saúde Espiritual",
        "question_text": "O que faz você sentir que sua vida vale a pena?",
        "answer_value": {
            "text": "Honestamente, estou questionando isso. Não vejo mais sentido no que faço. Antes tinha um sonho, uma visão clara, mas agora parece que perdi o fio da meada. Tudo virou obrigação."
        }
    },
    {
        "question_area": "Vida Familiar",
        "question_text": "Quais hábitos você carrega da sua família sem ter escolhido?",
        "answer_value": {
            "text": "Carrego a crença de que 'trabalho duro é o único caminho' e que 'não posso decepcionar ninguém'. Meus pais sempre sacrificaram tudo pela família e eu sinto que preciso fazer o mesmo, mas isso me sufoca."
        }
    },
]


async def test_analyzer():
    print("\n=== TESTE DO ANALYZER ===\n")
    print(f"Analisando {len(SAMPLE_RESPONSES)} respostas de exemplo...\n")
    
    try:
        analysis = await analyze_answers_context(
            responses=SAMPLE_RESPONSES,
            user_profile=None
        )
        
        print("✓ Análise concluída com sucesso!\n")
        print("RESULTADOS:\n")
        print(f"Motor Dominante: {analysis.get('motor_dominante')}")
        print(f"  Justificativa: {analysis.get('justificativa_motor', 'N/A')[:200]}...")
        print()
        print(f"Clusters Identificados: {', '.join(analysis.get('clusters_identificados', []))}")
        print(f"  Justificativa: {analysis.get('justificativa_clusters', 'N/A')[:200]}...")
        print()
        print(f"Pontos de Entrada: {', '.join(analysis.get('pontos_entrada', []))}")
        print()
        print(f"Nível de Maturidade: {analysis.get('nivel_maturidade')}")
        print(f"Tom Emocional: {analysis.get('tom_emocional')}")
        print()
        print(f"Áreas Críticas: {', '.join(analysis.get('areas_criticas', []))}")
        print()
        print(f"Âncoras Sugeridas: {', '.join(analysis.get('ancoras_sugeridas', [])[:5])}")
        print()
        print("Scores dos Motores:")
        for motor, score in analysis.get('motors_scores', {}).items():
            print(f"  - {motor}: {score}/10")
        print()
        print("=== TESTE CONCLUÍDO ===\n")
        
    except Exception as e:
        print(f"❌ Erro ao testar analyzer: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(test_analyzer())
    sys.exit(exit_code or 0)
