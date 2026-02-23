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
    AREAS,
    CLUSTERS_CRISE,
    MOTORES,
    EIXOS_TRANSFORMACAO,
    DOMINIOS_TEMATICOS_COMPLETOS,
    ASSUNCAO_INTENCIONAL,
    PONTOS_ENTRADA,
    ANCORAS_PRATICAS,
    NIVEIS_IDENTIDADE,
    FATORES_DIAGNOSTICO,
)
from app.rag.retriever import retrieve_relevant_chunks
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


def _compute_silent_areas(responses: list[dict[str, Any]]) -> list[str]:
    """Computa áreas sem resposta textual no conjunto informado."""
    covered = {
        r.get("question_area")
        for r in responses
        if r.get("question_area")
        and isinstance((r.get("answer_value") or {}).get("text"), str)
        and ((r.get("answer_value") or {}).get("text") or "").strip()
    }
    return [area for area in AREAS if area not in covered]


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
                    "content": (
                        "Você é Nara, analista sênior em Engenharia de Mindset da Metodologia "
                        "de Phellipe Oliveira.\n\n"
                        "MISSÃO: Diagnosticar em qual dos 3 Eixos de Transformação "
                        "(Narrativa, Identidade, Hábitos) reside o principal desalinhamento "
                        "do usuário, identificar o Motor dominante, a Fase da Jornada, o "
                        "Cluster de Crise e o Domínio Temático de maior alavancagem.\n\n"
                        "EIXOS DE TRANSFORMAÇÃO:\n"
                        "- Narrativa (=Crença): história que o indivíduo conta sobre si. "
                        "Ferramenta: TCC.\n"
                        "- Identidade (=Valores): quem o indivíduo acredita ser. "
                        "Ferramenta: Assunção Intencional.\n"
                        "- Hábitos (=Princípios): ações práticas que materializam narrativa "
                        "e identidade. Ferramenta: Assunção Intencional.\n\n"
                        "ESTADOS DA TRANSFORMAÇÃO:\n"
                        "- Situação atual: estado de crise ou conflito (o que o usuário vive hoje)\n"
                        "- Estado desejado: identidade e vida que a pessoa quer assumir\n"
                        "- Caminho de transição: comportamentos e práticas que aproximam da mudança\n"
                        "- Referências externas: pessoas, ambientes e grupos que ajudam a consolidar "
                        "a nova identidade\n\n"
                        "Analise estritamente pela metodologia NARA. Nunca use frameworks externos."
                    ),
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
        gap_mx = compute_gap_mx(responses, analysis)
        incongruencias = detect_symbolic_incongruences(analysis)
        areas_silenciadas = _compute_silent_areas(responses)
        analysis["gap_mx"] = gap_mx
        analysis["incongruencias_simbolicas"] = incongruencias
        analysis["areas_silenciadas"] = areas_silenciadas
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
    areas_desc = "\n".join([f"- {i + 1}. {area}" for i, area in enumerate(AREAS)])
    niveis_desc = "\n".join([f"- {nivel}" for nivel in NIVEIS_IDENTIDADE])
    fatores_desc = "\n".join([f"- {fator}" for fator in FATORES_DIAGNOSTICO])
    eixos_desc = "\n".join(
        [
            f"- **{nome}**: {dados['essencia']} | Ferramenta: {dados['ferramenta_principal']} | Objetivo: {dados['objetivo']}"
            for nome, dados in EIXOS_TRANSFORMACAO.items()
        ]
    )
    dominios_desc = "\n".join(
        [
            f"- **{codigo} ({dados['nome']})** → fase {dados['fase_potencia_maxima']}: {dados['pergunta_chave']}"
            for codigo, dados in DOMINIOS_TEMATICOS_COMPLETOS.items()
        ]
    )
    assuncao_desc = "\n".join(
        [
            f"- **{etapa}** ({dados['fase_jornada']}): {dados['foco']} — {dados['acao']}"
            for etapa, dados in ASSUNCAO_INTENCIONAL.items()
        ]
    )
    
    prompt = f"""
Analise as respostas e classifique sob a ótica da Engenharia de Mindset:

## FRAMEWORK METODOLÓGICO

### 12 ÁREAS ESTRUTURANTES:
{areas_desc}

### 4 MOTORES MOTIVACIONAIS:
{motors_desc}

### CLUSTERS DE CRISE:
{clusters_desc}

### PONTOS DE ENTRADA (Portas de Intervenção):
{pontos_desc}

### 4 NÍVEIS DE IDENTIDADE (Luz Total):
{niveis_desc}

### PROTOCOLO DE DIAGNÓSTICO RÁPIDO (6 fatores):
{fatores_desc}

### TÉCNICAS DE TCC INTERNAS:
- Identificação de Pensamentos Automáticos
- Questionamento Socrático
- Reestruturação Cognitiva Escrita
- Descatastrofização
- Redefinição Cognitiva Assistida
- Substituição de Pensamentos Distorcidos
- Imaginação Guiada

### EIXOS DE TRANSFORMAÇÃO (diagnose qual está comprometido):
{eixos_desc}
- Narrativa comprometida: histórias autolimitantes, crenças disfuncionais, frases da velha narrativa
- Identidade comprometida: confusão sobre quem é, valores incoerentes, rótulos herdados sem questionamento
- Hábitos comprometidos: reconhece o que quer mas não age, paralisia e autossabotagem

### DOMÍNIOS TEMÁTICOS — use o domínio de maior potência para a fase identificada:
{dominios_desc}

### ASSUNÇÃO INTENCIONAL (para prescrever reforços):
{assuncao_desc}

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
6. **Áreas Críticas**: Quais das 12 áreas estão em maior conflito? (use linguagem simples em texto livre)
7. **Sinais de Conflito**: Padrões específicos detectados (descreva em linguagem simples)
8. **Âncoras Sugeridas**: Das 19 âncoras práticas, quais 3-5 são mais relevantes?
9. **Memórias Vermelhas**: 2-4 frases literais do usuário que revelam conflito (explique sem jargões)
10. **Barreiras Identificadas**: desafios, autossabotagem ou ambiente hostil (descreva sem jargões)
11. **Capital Simbólico**: recursos sociais/culturais já presentes (descreva sem jargões)
12. **FCU**: Forma, Conteúdo e Uso da expressão do usuário
13. **Palavras Recorrentes**: termos frequentes da narrativa
14. **Fase da Jornada**: Germinar|Enraizar|Desenvolver|Florescer|Frutificar|Realizar
15. **Domínios Alavanca**: 1-3 domínios entre D1..D6
16. **Nível de Identidade em Conflito**: Personalidade|Cultura|Realizações|Posição
17. **Fatores do Protocolo Rápido**: classifique os 6 fatores como Alto|Médio|Baixo
18. **Eixo mais comprometido**: Narrativa|Identidade|Habitos
19. **Domínio de potência máxima**: D1|D2|D3|D4|D5|D6
20. **Etapa de Assunção sugerida**: Reconhecer|Modelar|Assumir|Reforcar

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
  "memorias_vermelhas": ["frase 1", "frase 2"],
  "barreiras_identificadas": ["barreira 1", "barreira 2"],
  "capital_simbolico": ["recurso 1", "recurso 2"],
  "fcu": {{
    "forma": "descrição",
    "conteudo": "descrição",
    "uso": "descrição"
  }},
  "palavras_recorrentes": ["palavra 1", "palavra 2"],
  "fase_jornada": "Germinar|Enraizar|Desenvolver|Florescer|Frutificar|Realizar",
  "dominios_alavanca": ["D1", "D3"],
  "eixo_mais_comprometido": "Narrativa|Identidade|Habitos",
  "dominio_potencia_maxima": "D1|D2|D3|D4|D5|D6",
  "etapa_assuncao_sugerida": "Reconhecer|Modelar|Assumir|Reforcar",
  "nivel_identidade_conflito": "Personalidade|Cultura|Realizações|Posição",
  "fatores_diagnostico_rapido": {{
    "Autenticidade": "Alto|Médio|Baixo",
    "Integração do Passado": "Alto|Médio|Baixo",
    "Visão/Enredo": "Alto|Médio|Baixo",
    "Coragem/Decisão": "Alto|Médio|Baixo",
    "Expressão/Voz": "Alto|Médio|Baixo",
    "Estrutura/Pertencimento": "Alto|Médio|Baixo"
  }},
  "justificativa_motor": "Breve explicação do motor dominante",
  "justificativa_clusters": "Breve explicação dos clusters"
}}

IMPORTANTE: Nos campos de texto livre (como `sinais_conflito`, `memorias_vermelhas`, `barreiras_identificadas`, `capital_simbolico`, `justificativa_motor` e `justificativa_clusters`), use linguagem simples e direta, evitando siglas e termos técnicos da metodologia.
"""
    return prompt


def compute_gap_mx(
    responses: list[dict[str, Any]],
    context_analysis: dict[str, Any],
) -> dict[str, Any]:
    """Computa o Gap MX (M1->MX) usando regras determinísticas."""
    motor = context_analysis.get("motor_dominante") or "Necessidade"
    areas_criticas = context_analysis.get("areas_criticas") or []
    clusters = context_analysis.get("clusters_identificados") or []
    crise_raiz = clusters[0] if clusters else "não identificada"

    motor_weights = {
        "Necessidade": 1.0,
        "Valor": 0.8,
        "Desejo": 0.6,
        "Propósito": 0.4,
    }
    weight = motor_weights.get(motor, 1.0)

    mx_text = ""
    for response in responses:
        if response.get("question_id") == 15:
            mx_text = ((response.get("answer_value") or {}).get("text") or "").strip()
            if mx_text:
                break
    if not mx_text:
        for response in responses:
            q_text = (response.get("question_text") or "").lower()
            if "melhor versão" in q_text or "daqui a um ano" in q_text:
                mx_text = ((response.get("answer_value") or {}).get("text") or "").strip()
                if mx_text:
                    break
    if not mx_text:
        mx_text = "Visão de futuro não explicitada com clareza nas respostas."

    gap_score = round(len(areas_criticas) * weight, 2)
    estado_m1 = f"Motor={motor}; CriseRaiz={crise_raiz}; AreasCriticas={len(areas_criticas)}"
    gap_description = (
        f"A distância entre onde você está hoje e onde quer chegar é marcada por "
        f"{len(areas_criticas)} áreas em conflito e pela sua força de motivação dominante ({motor})."
    )
    return {
        "estado_m1": estado_m1,
        "estado_mx": mx_text,
        "gap_score": gap_score,
        "gap_description": gap_description,
    }


def detect_symbolic_incongruences(context_analysis: dict[str, Any]) -> list[str]:
    """Detecta incongruências simbólicas por regras explícitas da metodologia."""
    incongruencias: list[str] = []
    motor = context_analysis.get("motor_dominante")
    areas_criticas = context_analysis.get("areas_criticas") or []
    fase = context_analysis.get("fase_jornada")
    pontos_entrada = context_analysis.get("pontos_entrada") or []
    clusters = context_analysis.get("clusters_identificados") or []

    if motor == "Valor" and "Vida Profissional" in areas_criticas:
        incongruencias.append(
            "Incongruência: declara agir por valores, mas Vida Profissional está em crise "
            "(possível capitulação simbólica)."
        )

    if fase == "Realizar" and "Emocional" in pontos_entrada:
        incongruencias.append(
            "Usuário em fase avançada, mas operando em modo reativo emocional "
            "(regressão de jornada)."
        )

    if "Identidade Raiz" in clusters and "Transformação de Personagem" in clusters:
        incongruencias.append(
            "Dupla âncora: preso ao passado e com medo do próximo personagem."
        )

    return incongruencias


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
        "areas_silenciadas": [],
        "memorias_vermelhas": [],
        "barreiras_identificadas": [],
        "capital_simbolico": [],
        "fcu": {"forma": "", "conteudo": "", "uso": ""},
        "palavras_recorrentes": [],
        "fase_jornada": "Germinar",
        "dominios_alavanca": [],
        "eixo_mais_comprometido": "Narrativa",
        "dominio_potencia_maxima": "D1",
        "etapa_assuncao_sugerida": "Reconhecer",
        "nivel_identidade_conflito": "Personalidade",
        "fatores_diagnostico_rapido": {
            "Autenticidade": "Médio",
            "Integração do Passado": "Médio",
            "Visão/Enredo": "Médio",
            "Coragem/Decisão": "Médio",
            "Expressão/Voz": "Médio",
            "Estrutura/Pertencimento": "Médio",
        },
        "gap_mx": {
            "estado_m1": "Dados insuficientes",
            "estado_mx": "Dados insuficientes",
            "gap_score": 0.0,
            "gap_description": "Dados insuficientes para mapear a distância entre situação atual e meta.",
        },
        "incongruencias_simbolicas": [],
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
