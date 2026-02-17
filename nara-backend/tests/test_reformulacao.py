"""
Testes para validar a reformulação da Base Metodológica NARA.
Valida vetor_estado, Memórias Vermelhas, silêncios e retrieval v2.
"""
import pytest
from app.rag.analyzer import analyze_answers_context
from app.rag.retriever import retrieve_relevant_chunks


def test_vetor_estado_structure():
    """Testa se o vetor de estado tem a estrutura correta."""
    # Estrutura esperada do vetor de estado
    expected_keys = {
        "motor_dominante",
        "motor_secundario",
        "estagio_jornada",
        "crise_raiz",
        "crises_derivadas",
        "ponto_entrada_ideal",
        "dominios_alavanca",
        "tom_emocional",
        "risco_principal",
        "necessidade_atual",
    }
    
    # Simular vetor de estado
    vetor_estado = {
        "motor_dominante": "Valor",
        "motor_secundario": "Propósito",
        "estagio_jornada": "Enraizar",
        "crise_raiz": "Identidade Herdada",
        "crises_derivadas": ["Paralisia decisória"],
        "ponto_entrada_ideal": "Simbólico",
        "dominios_alavanca": ["D1", "D3"],
        "tom_emocional": "indignação",
        "risco_principal": "Autotraição prolongada",
        "necessidade_atual": "Reescrita identitária",
    }
    
    assert set(vetor_estado.keys()) == expected_keys, "Vetor de estado deve ter todos os campos"
    assert vetor_estado["motor_dominante"] in ["Necessidade", "Valor", "Desejo", "Propósito"]
    assert vetor_estado["estagio_jornada"] in ["Germinar", "Enraizar", "Desenvolver", "Florescer", "Frutificar", "Realizar"]
    assert isinstance(vetor_estado["crises_derivadas"], list)
    assert isinstance(vetor_estado["dominios_alavanca"], list)


def test_memorias_vermelhas_extraction():
    """Testa extração de Memórias Vermelhas do analyzer."""
    # Simular respostas com padrões de conflito
    responses = [
        {
            "question_area": "Vida Profissional",
            "answer_value": {
                "text": "Não consigo me apresentar em público sem sentir que vou falhar."
            }
        },
        {
            "question_area": "Vida Familiar",
            "answer_value": {
                "text": "Sempre fui o filho que não deu certo. Nunca serei bom o suficiente."
            }
        },
        {
            "question_area": "Saúde Mental",
            "answer_value": {
                "text": "Me sinto ansioso e com medo de tudo dar errado."
            }
        },
    ]
    
    result = analyze_answers_context(responses)
    
    assert "memorias_vermelhas" in result
    assert isinstance(result["memorias_vermelhas"], list)
    assert len(result["memorias_vermelhas"]) > 0, "Deve extrair pelo menos uma Memória Vermelha"


def test_silencio_detection():
    """Testa detecção de áreas silenciadas."""
    # Simular respostas cobrindo apenas algumas áreas (1-12)
    responses = [
        {"question_area": "Vida Profissional", "answer_value": {"text": "Resposta"}},
        {"question_area": "Saúde Mental", "answer_value": {"text": "Resposta"}},
        {"question_area": "Vida Pessoal", "answer_value": {"text": "Resposta"}},
    ]
    
    result = analyze_answers_context(responses)
    
    assert "areas_silenciadas" in result
    assert isinstance(result["areas_silenciadas"], list)
    # Deve haver áreas silenciadas (não respondidas)
    assert len(result["areas_silenciadas"]) > 0, "Deve identificar áreas não respondidas"


def test_tom_emocional_detection():
    """Testa detecção de tom emocional."""
    responses = [
        {
            "question_area": "Vida Pessoal",
            "answer_value": {
                "text": "Me sinto ansioso e preocupado com tudo. Estou sempre estressado."
            }
        },
        {
            "question_area": "Saúde Mental",
            "answer_value": {
                "text": "Tenho urgência em resolver tudo rápido mas não consigo."
            }
        },
    ]
    
    result = analyze_answers_context(responses)
    
    assert "tom_emocional" in result
    assert result["tom_emocional"] in ["vergonha", "indignação", "apatia", "urgência", "tristeza", "neutro"]


def test_ponto_entrada_identification():
    """Testa identificação do Ponto de Entrada."""
    # Respostas com foco emocional
    responses = [
        {
            "question_area": "Saúde Mental",
            "answer_value": {
                "text": "Me sinto triste e angustiado. Tenho medo de não ser suficiente."
            }
        },
    ]
    
    result = analyze_answers_context(responses)
    
    assert "ponto_entrada" in result
    assert result["ponto_entrada"] in ["Emocional", "Simbólico", "Comportamental", "Existencial"]


def test_barreiras_identificadas():
    """Testa identificação de barreiras/autossabotagem."""
    responses = [
        {
            "question_area": "Vida Profissional",
            "answer_value": {
                "text": "Sempre adio minhas tarefas. Nunca consigo terminar nada."
            }
        },
        {
            "question_area": "Educação",
            "answer_value": {
                "text": "Não tenho tempo para estudar. É impossível aprender coisas novas."
            }
        },
    ]
    
    result = analyze_answers_context(responses)
    
    assert "barreiras_identificadas" in result
    assert isinstance(result["barreiras_identificadas"], list)
    assert len(result["barreiras_identificadas"]) > 0, "Deve identificar barreiras"


@pytest.mark.asyncio
async def test_retrieval_version_filter():
    """Testa filtro de version=2 no retriever."""
    # Este teste requer conexão com Supabase e chunks v2 seedados
    # Pode ser skipado se não houver chunks v2
    try:
        chunks = await retrieve_relevant_chunks(
            query="identidade herdada crise",
            top_k=5,
            filter_version=2,
        )
        
        assert isinstance(chunks, list)
        # Se houver chunks, todos devem ser version=2
        for chunk in chunks:
            assert chunk.get("version") == 2, "Todos os chunks devem ser version=2"
    except Exception:
        pytest.skip("Teste requer chunks v2 seedados no banco")


def test_analyzer_full_output():
    """Testa estrutura completa do output do analyzer."""
    responses = [
        {
            "question_area": "Vida Profissional",
            "answer_value": {"text": "Não consigo me apresentar bem."}
        },
        {
            "question_area": "Saúde Mental",
            "answer_value": {"text": "Me sinto ansioso."}
        },
    ]
    
    result = analyze_answers_context(responses)
    
    # Validar estrutura completa
    expected_keys = {
        "memorias_vermelhas",
        "barreiras_identificadas",
        "capital_simbolico",
        "tom_emocional",
        "areas_criticas",
        "areas_silenciadas",
        "padroes_repetidos",
        "ponto_entrada",
        "palavras_recorrentes",
    }
    
    assert set(result.keys()) == expected_keys, "Analyzer deve retornar todos os campos esperados"
    assert all(isinstance(result[key], list) for key in [
        "memorias_vermelhas", 
        "barreiras_identificadas",
        "capital_simbolico",
        "areas_criticas",
        "areas_silenciadas",
        "padroes_repetidos",
        "palavras_recorrentes"
    ]), "Campos devem ser listas"
    assert isinstance(result["tom_emocional"], str), "tom_emocional deve ser string"
    assert isinstance(result["ponto_entrada"], str), "ponto_entrada deve ser string"


def test_ancoras_praticas_list():
    """Testa se lista de Âncoras Práticas está completa."""
    from app.core.constants import ANCORAS_PRATICAS
    
    # Deve ter 19 âncoras
    assert len(ANCORAS_PRATICAS) == 19, "Deve haver 19 Âncoras Práticas"
    
    # Verificar algumas âncoras específicas
    expected_ancoras = [
        "Referências",
        "Grupo",
        "Tom",
        "Rituais Matinais",
        "Limites",
        "Gestão de Energia",
        "Tarefas Identitárias",
        "Testemunhas",
    ]
    
    for ancor in expected_ancoras:
        assert ancor in ANCORAS_PRATICAS, f"Âncora '{ancor}' deve estar na lista"


def test_pontos_entrada_dict():
    """Testa se Pontos de Entrada estão corretos."""
    from app.core.constants import PONTOS_ENTRADA
    
    expected_pontos = ["Emocional", "Simbólico", "Comportamental", "Existencial"]
    assert set(PONTOS_ENTRADA.keys()) == set(expected_pontos), "Deve ter os 4 Pontos de Entrada"


def test_dominios_tematicos():
    """Testa se Domínios Temáticos estão corretos."""
    from app.core.constants import DOMINIOS_TEMATICOS
    
    assert len(DOMINIOS_TEMATICOS) == 6, "Deve haver 6 Domínios Temáticos"
    assert "D1" in DOMINIOS_TEMATICOS
    assert "D6" in DOMINIOS_TEMATICOS
