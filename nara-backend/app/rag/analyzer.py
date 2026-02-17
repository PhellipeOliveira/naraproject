"""
Análise contextual das respostas do diagnóstico.
Conforme 01_BASE_METODOLOGICA — Protocolo de Diagnóstico Rápido e Clusters de Crise.

Identifica:
- Motor motivacional dominante (Necessidade, Valor, Desejo, Propósito)
- Clusters de crise presentes
- Pontos de entrada para intervenção
- Nível de maturidade narrativa
- Âncoras práticas relevantes
"""
import logging
from typing import Any, Optional

from app.config import settings
from app.core.constants import (
    CLUSTERS_CRISE,
    MOTORES,
    PONTOS_ENTRADA,
    ANCORAS_PRATICAS,
)
from app.rag.retriever import retrieve_relevant_chunks
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def analyze_answers_context(
    responses: list[dict[str, Any]],
    user_profile: Optional[dict[str, Any]] = None
) -> dict[str, Any]:
    """
    Analisa respostas para identificar motor, clusters de crise,
    pontos de entrada e âncoras práticas relevantes.
    
    Args:
        responses: Lista de respostas do usuário
        user_profile: Perfil do usuário (opcional)
        
    Returns:
        {
            "motor_dominante": str,
            "motors_scores": dict,
            "clusters_identificados": list[str],
            "pontos_entrada": list[str],
            "ancoras_sugeridas": list[str],
            "nivel_maturidade": str,
            "tom_emocional": str,
            "areas_criticas": list[str],
            "sinais_conflito": list[str]
        }
    """
    if not responses:
        return _empty_analysis()
    
    # Concatenar respostas para análise
    response_texts = "\n\n".join([
        f"Área: {r.get('question_area', 'Geral')}\n"
        f"Pergunta: {r.get('question_text', '')}\n"
        f"Resposta: {r.get('answer_value', {}).get('text', '')}"
        for r in responses[-20:]  # Últimas 20 respostas
        if r.get('answer_value', {}).get('text')
    ])
    
    if not response_texts:
        return _empty_analysis()
    
    # Buscar contexto RAG relevante
    rag_chunks = await retrieve_relevant_chunks(
        query=response_texts[:500],  # Resumo das respostas
        top_k=5,
        filter_chunk_strategy="semantic"
    )
    
    rag_context = "\n\n".join([
        f"**{c.get('chapter')}**: {c.get('content', '')[:200]}"
        for c in rag_chunks[:3]
    ])
    
    # Montar prompt de análise
    prompt = _build_analysis_prompt(response_texts, rag_context)
    
    # Chamar LLM
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL_ANALYSIS,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um analista especializado em Transformação Narrativa."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        import json
        analysis = json.loads(response.choices[0].message.content)
        logger.info(f"Análise contextual concluída: motor={analysis.get('motor_dominante')}")
        return analysis
        
    except Exception as e:
        logger.error(f"Erro na análise contextual: {e}")
        return _empty_analysis()


def _build_analysis_prompt(response_texts: str, rag_context: str) -> str:
    """Monta o prompt para análise contextual."""
    motors_desc = "\n".join([f"- **{k}**: {v}" for k, v in MOTORES.items()])
    clusters_desc = "\n".join([f"- **{k}**: {', '.join(v['sinais'])}" for k, v in CLUSTERS_CRISE.items()])
    pontos_desc = "\n".join([f"- **{k}**: {v}" for k, v in PONTOS_ENTRADA.items()])
    
    prompt = f"""
Analise as respostas do usuário e identifique:

## FRAMEWORK METODOLÓGICO

### 4 MOTORES MOTIVACIONAIS:
{motors_desc}

### CLUSTERS DE CRISE:
{clusters_desc}

### PONTOS DE ENTRADA (Portas de Intervenção):
{pontos_desc}

### NÍVEIS DE MATURIDADE NARRATIVA:
- **Baixo**: Não reconhece padrões, culpa externa
- **Médio**: Reconhece padrões mas não age consistentemente
- **Alto**: Reconhece, age e busca transformação intencional

## RESPOSTAS DO USUÁRIO:
{response_texts}

## CONTEXTO METODOLÓGICO (RAG):
{rag_context}

## TAREFA:
Identifique:
1. **Motor Dominante**: Qual dos 4 motores impulsiona mais este usuário?
2. **Clusters Identificados**: Quais clusters de crise estão presentes? (máximo 3)
3. **Pontos de Entrada**: Quais portas de intervenção são mais evidentes?
4. **Nível de Maturidade**: Baixo, Médio ou Alto
5. **Tom Emocional**: frustração, esperança, confusão, determinação, etc
6. **Áreas Críticas**: Quais das 12 áreas estão em maior conflito (M1)?
7. **Sinais de Conflito**: Padrões específicos detectados
8. **Âncoras Sugeridas**: Das 19 âncoras práticas, quais 3-5 são mais relevantes?

Lista das 19 Âncoras: {', '.join(ANCORAS_PRATICAS)}

Retorne JSON estrito:
{{
  "motor_dominante": "Necessidade|Valor|Desejo|Propósito",
  "motors_scores": {{"Necessidade": 0-10, "Valor": 0-10, "Desejo": 0-10, "Propósito": 0-10}},
  "clusters_identificados": ["Cluster1", "Cluster2"],
  "pontos_entrada": ["Emocional", "Simbólico", "Comportamental", "Existencial"],
  "ancoras_sugeridas": ["Âncora1", "Âncora2", "Âncora3"],
  "nivel_maturidade": "Baixo|Médio|Alto",
  "tom_emocional": "descrição breve",
  "areas_criticas": ["Área1", "Área2"],
  "sinais_conflito": ["sinal 1", "sinal 2"],
  "justificativa_motor": "Breve explicação do motor dominante",
  "justificativa_clusters": "Breve explicação dos clusters"
}}
"""
    return prompt


def _empty_analysis() -> dict[str, Any]:
    """Retorna análise vazia quando não há dados suficientes."""
    return {
        "motor_dominante": "Necessidade",
        "motors_scores": {"Necessidade": 5, "Valor": 5, "Desejo": 5, "Propósito": 5},
        "clusters_identificados": [],
        "pontos_entrada": [],
        "ancoras_sugeridas": [],
        "nivel_maturidade": "Médio",
        "tom_emocional": "neutro",
        "areas_criticas": [],
        "sinais_conflito": [],
        "justificativa_motor": "Dados insuficientes para análise",
        "justificativa_clusters": "Dados insuficientes para análise"
    }


async def extract_emotional_tone(text: str) -> str:
    """
    Extrai o tom emocional de um texto.
    
    Returns:
        Tom emocional: frustração, esperança, confusão, determinação, etc
    """
    if not text or len(text) < 50:
        return "neutro"
    
    # Palavras-chave para análise rápida
    tone_keywords = {
        "frustração": ["não aguento", "cansado", "difícil", "impossível", "frustrad"],
        "esperança": ["quero", "sonho", "espero", "desejo", "vou conseguir"],
        "confusão": ["não sei", "confuso", "perdido", "dúvida", "incerto"],
        "determinação": ["vou", "vou fazer", "decidido", "compromisso", "foco"],
    }
    
    text_lower = text.lower()
    scores = {}
    
    for tone, keywords in tone_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        scores[tone] = score
    
    if not any(scores.values()):
        return "neutro"
    
    return max(scores, key=scores.get)


def identify_maturity_level(responses: list[dict[str, Any]]) -> str:
    """
    Identifica o nível de maturidade narrativa do usuário.
    
    Returns:
        "Baixo", "Médio" ou "Alto"
    """
    if not responses:
        return "Médio"
    
    # Critérios simplificados
    # Alto: usa "eu decidi", "eu escolhi", fala de ações concretas
    # Médio: reconhece padrões mas fala em termos de "deveria"
    # Baixo: culpa externa, "não tenho escolha", "a vida é assim"
    
    high_markers = ["decidi", "escolhi", "assumo", "responsabilidade", "ação"]
    low_markers = ["culpa", "não posso", "impossível", "vítima", "sem escolha"]
    
    combined_text = " ".join([
        r.get('answer_value', {}).get('text', '').lower()
        for r in responses[-10:]
    ])
    
    high_score = sum(1 for marker in high_markers if marker in combined_text)
    low_score = sum(1 for marker in low_markers if marker in combined_text)
    
    if high_score > low_score + 2:
        return "Alto"
    elif low_score > high_score + 2:
        return "Baixo"
    else:
        return "Médio"
