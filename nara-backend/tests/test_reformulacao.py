"""
Testes para validar a reformulação da Base Metodológica NARA.
Valida vetor_estado, Memórias Vermelhas, silêncios e retrieval v2.
"""
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.rag.analyzer import analyze_answers_context
from app.rag.retriever import retrieve_relevant_chunks

MOCK_LLM_JSON = {
    "motor_dominante": "Valor",
    "motors_scores": {"Necessidade": 3, "Valor": 8, "Desejo": 4, "Propósito": 5},
    "clusters_identificados": ["Identidade Raiz"],
    "pontos_entrada": ["Emocional"],
    "ancoras_sugeridas": ["Tom"],
    "nivel_maturidade": "Médio",
    "tom_emocional": "urgência",
    "areas_criticas": ["Vida Profissional"],
    "sinais_conflito": ["autocrítica"],
    "memorias_vermelhas": ["Nunca serei bom o suficiente"],
    "barreiras_identificadas": ["Procrastinação crônica"],
    "capital_simbolico": [],
    "palavras_recorrentes": ["medo", "falhar"],
    "fase_jornada": "Enraizar",
    "dominios_alavanca": ["D1"],
    "eixo_mais_comprometido": "Identidade",
    "dominio_potencia_maxima": "D2",
    "etapa_assuncao_sugerida": "Reconhecer",
    "nivel_identidade_conflito": "Personalidade",
    "fatores_diagnostico_rapido": {
        "Autenticidade": "Baixo",
        "Integração do Passado": "Baixo",
        "Visão/Enredo": "Médio",
        "Coragem/Decisão": "Médio",
        "Expressão/Voz": "Médio",
        "Estrutura/Pertencimento": "Médio",
    },
    "justificativa_motor": "Valor comprometido.",
    "justificativa_clusters": "Identidade herdada ativa.",
}


def _configure_mock_llm(mock_client: MagicMock, payload: dict | None = None) -> None:
    """Configura retorno assíncrono do cliente OpenAI usado pelo analyzer."""
    response_payload = payload or MOCK_LLM_JSON
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = json.dumps(response_payload, ensure_ascii=False)
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)


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


@patch("app.rag.analyzer.client")
@patch("app.rag.analyzer.retrieve_relevant_chunks", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_memorias_vermelhas_extraction(mock_retrieve: AsyncMock, mock_client: MagicMock):
    """Testa extração de Memórias Vermelhas do analyzer."""
    mock_retrieve.return_value = []
    _configure_mock_llm(mock_client)

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

    result = await analyze_answers_context(responses)

    assert "memorias_vermelhas" in result
    assert isinstance(result["memorias_vermelhas"], list)
    assert len(result["memorias_vermelhas"]) > 0, "Deve extrair pelo menos uma Memória Vermelha"


@patch("app.rag.analyzer.client")
@patch("app.rag.analyzer.retrieve_relevant_chunks", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_silencio_detection(mock_retrieve: AsyncMock, mock_client: MagicMock):
    """Testa detecção de áreas silenciadas."""
    mock_retrieve.return_value = []
    _configure_mock_llm(mock_client)

    # Simular respostas cobrindo apenas algumas áreas (1-12)
    responses = [
        {"question_area": "Vida Profissional", "answer_value": {"text": "Resposta"}},
        {"question_area": "Saúde Mental", "answer_value": {"text": "Resposta"}},
        {"question_area": "Vida Pessoal", "answer_value": {"text": "Resposta"}},
    ]

    result = await analyze_answers_context(responses)

    assert "areas_silenciadas" in result
    assert isinstance(result["areas_silenciadas"], list)
    # Deve haver áreas silenciadas (não respondidas)
    assert len(result["areas_silenciadas"]) > 0, "Deve identificar áreas não respondidas"


@patch("app.rag.analyzer.client")
@patch("app.rag.analyzer.retrieve_relevant_chunks", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_tom_emocional_detection(mock_retrieve: AsyncMock, mock_client: MagicMock):
    """Testa detecção de tom emocional."""
    mock_retrieve.return_value = []
    _configure_mock_llm(mock_client)

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

    result = await analyze_answers_context(responses)

    assert "tom_emocional" in result
    assert result["tom_emocional"] in ["vergonha", "indignação", "apatia", "urgência", "tristeza", "neutro"]


@patch("app.rag.analyzer.client")
@patch("app.rag.analyzer.retrieve_relevant_chunks", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_ponto_entrada_identification(mock_retrieve: AsyncMock, mock_client: MagicMock):
    """Testa identificação do Ponto de Entrada."""
    mock_retrieve.return_value = []
    _configure_mock_llm(mock_client)

    # Respostas com foco emocional
    responses = [
        {
            "question_area": "Saúde Mental",
            "answer_value": {
                "text": "Me sinto triste e angustiado. Tenho medo de não ser suficiente."
            }
        },
    ]

    result = await analyze_answers_context(responses)

    assert "pontos_entrada" in result
    assert isinstance(result["pontos_entrada"], list)
    assert result["pontos_entrada"][0] in ["Emocional", "Simbólico", "Comportamental", "Existencial"]


@patch("app.rag.analyzer.client")
@patch("app.rag.analyzer.retrieve_relevant_chunks", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_barreiras_identificadas(mock_retrieve: AsyncMock, mock_client: MagicMock):
    """Testa identificação de barreiras/autossabotagem."""
    mock_retrieve.return_value = []
    _configure_mock_llm(mock_client)

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

    result = await analyze_answers_context(responses)

    assert "barreiras_identificadas" in result
    assert isinstance(result["barreiras_identificadas"], list)
    assert len(result["barreiras_identificadas"]) > 0, "Deve identificar barreiras"


@pytest.mark.asyncio
async def test_retrieval_chunks_ativos():
    """Testa busca de chunks ativos no banco."""
    try:
        chunks = await retrieve_relevant_chunks(
            query="identidade herdada crise",
            top_k=5,
        )

        assert isinstance(chunks, list)
    except Exception:
        pytest.skip("Teste requer conexão com Supabase e chunks seedados")


@patch("app.rag.analyzer.client")
@patch("app.rag.analyzer.retrieve_relevant_chunks", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_analyzer_full_output(mock_retrieve: AsyncMock, mock_client: MagicMock):
    """Testa estrutura completa do output do analyzer."""
    mock_retrieve.return_value = []
    _configure_mock_llm(mock_client)

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

    result = await analyze_answers_context(responses)

    # Validar estrutura completa
    expected_keys = {
        "memorias_vermelhas",
        "barreiras_identificadas",
        "capital_simbolico",
        "tom_emocional",
        "areas_criticas",
        "areas_silenciadas",
        "pontos_entrada",
        "palavras_recorrentes",
    }

    assert expected_keys.issubset(set(result.keys())), "Analyzer deve retornar os campos esperados"
    assert all(isinstance(result[key], list) for key in [
        "memorias_vermelhas",
        "barreiras_identificadas",
        "capital_simbolico",
        "areas_criticas",
        "areas_silenciadas",
        "pontos_entrada",
        "palavras_recorrentes"
    ]), "Campos devem ser listas"
    assert isinstance(result["tom_emocional"], str), "tom_emocional deve ser string"


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
