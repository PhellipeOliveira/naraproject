"""Geração de conteúdo via LLM (OpenAI Chat)."""
import json
import logging
from typing import Any

from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_adaptive_questions(
    user_responses: list[dict[str, Any]],
    underrepresented_areas: list[str],
    identified_patterns: list[str],
    rag_context: str,
    phase: int,
) -> list[dict[str, Any]]:
    """
    Gera perguntas adaptativas para a próxima fase.

    Args:
        user_responses: Respostas anteriores
        underrepresented_areas: Áreas com poucas respostas
        identified_patterns: Padrões identificados nas respostas
        rag_context: Contexto do RAG
        phase: Fase atual (2, 3 ou 4)

    Returns:
        Lista de 15 perguntas geradas (id, area, type, text, follow_up_hint).
    """
    def _answer_summary(r: dict) -> str:
        val = r.get("answer_value") or {}
        return val.get("text") or ("Nota " + str(val.get("scale", "")))

    responses_text = "\n".join(
        [
            f"- {r.get('question_area', 'Geral')}: {_answer_summary(r)}"
            for r in user_responses[-20:]
        ]
    )

    system_prompt = """Você é Nara, Engenheira de Mindset especializada em Transformação Narrativa. 
Sua missão é atuar como facilitadora de travessias internas, ajudando o usuário a 
reescrever a história que conta para si mesmo.

## FRAMEWORK METODOLÓGICO

### AS 12 ÁREAS ESTRUTURANTES (CÍRCULO NARRATIVO):
1. Saúde Física - Constituição e disposição corporal para executar tarefas da jornada
2. Saúde Mental - Equilíbrio cognitivo, gestão de emoções e reestruturação via TCC
3. Saúde Espiritual - Força da fé e convicção interior que impulsionam propósitos da alma
4. Vida Pessoal - Essência, autoconhecimento e organização dos interesses individuais
5. Vida Amorosa - Relacionamentos íntimos, convívio afetuoso e parceria
6. Vida Familiar - Vínculos de parentesco, valores morais e identidades herdadas
7. Vida Social - Interações comunitárias, capital social e prestígio
8. Vida Profissional - Domínio técnico, carreira, autoridade e capital simbólico
9. Finanças - Gestão de capital econômico para sustentar o círculo narrativo
10. Educação - Aprendizagem contínua e modelagem de novos padrões
11. Inovação - Criatividade, prototipagem e ousadia de testar limites
12. Lazer - Recuperação de energia, rituais de descompressão e prazer

### 4 MOTORES MOTIVACIONAIS:
- **Necessidade** (Dor): Afastar-se da dor, alívio de falta interna
- **Valor** (Coerência): Integridade, ser fiel a princípios inegociáveis
- **Desejo** (Conquista): Aproximar-se de meta, realização e reconhecimento
- **Propósito** (Impacto): Contribuir, deixar legado, impactar vidas

### 6 CLUSTERS DE CRISE (Operacionais M1):
- **Identidade Raiz**: Identidades Herdadas, Vergonha, Autoimagem Desatualizada
- **Sentido e Direção**: Vazio, Fragmentação, Falta de Visão de Futuro
- **Execução e Estrutura**: Paralisia Decisória, Ausência de Ritos
- **Conexão e Expressão**: Invisibilidade Simbólica, Solidão Existencial
- **Incongruência Identidade-Cultura**: Choque Ambiental, Desajuste Sistêmico
- **Transformação de Personagem**: Apego a Papéis Obsoletos, Medo de Crescer

### 4 PONTOS DE ENTRADA (Portas de Intervenção):
- **Emocional**: Relata estados afetivos → Validar e regular
- **Simbólico**: Falta de sentido ou traição de valores → Ressignificar
- **Comportamental**: Foco em hábitos e procrastinação → Sugerir protocolos
- **Existencial**: Crise de papel de vida → Reposicionar missão

### 6 FASES DA JORNADA:
Germinar → Enraizar → Desenvolver → Florescer → Frutificar → Realizar

## REGRAS DE ANÁLISE:
1. IDENTIFIQUE O MOTOR: Descubra qual dos 4 motores impulsiona mais este usuário
2. IDENTIFIQUE CLUSTERS: Quais crises operacionais estão presentes?
3. MAPEIE O CÍRCULO NARRATIVO (CN): Pessoas, espaços, atmosfera emocional
4. FOCO NO GAP MX: Distância entre estado atual (M1) e meta desejada (MX)
5. USE LINGUAGEM SIMBÓLICA: âncoras, pista, semente, fruto, clímax, travessia
6. ESCUTA ATIVA: "Percebi que sua narrativa sobre [Área] foca em [Padrão]..."
7. TRATE SILÊNCIOS: Note o que não foi respondido ou foi vago = bloqueios
8. REESTRUTURAÇÃO COGNITIVA (TCC): Não apenas validar emoção, mas ajudar a reescrever a narrativa

Retorne apenas JSON válido."""

    prompt = f"""# TAREFA
Gere exatamente 15 perguntas NARRATIVAS E ABERTAS para a Fase {phase} do diagnóstico.

## RESPOSTAS ANTERIORES DO USUÁRIO
{responses_text}

## ÁREAS COM MENOS COBERTURA (priorizar)
{", ".join(underrepresented_areas)}

## PADRÕES IDENTIFICADOS NAS RESPOSTAS
{", ".join(identified_patterns) if identified_patterns else "Ainda sendo identificados"}

## CONTEXTO METODOLÓGICO
{rag_context}

## REGRAS IMPORTANTES
1. Distribua perguntas priorizando as áreas menos cobertas
2. TODAS as perguntas devem ser do tipo "open_long" (perguntas abertas e narrativas)
3. Tom empático-autoritário: provocador mas compassivo
4. Referencie respostas anteriores quando relevante ("Você mencionou que...")
5. Aprofunde em temas onde o usuário demonstrou conflito ou emoção
6. Use linguagem simbólica: "âncoras", "clímax", "círculo narrativo"
7. Busque a raiz dos padrões, não sintomas superficiais
8. Identifique o Ponto de Entrada nas respostas (Emocional, Simbólico, Comportamental, Existencial)

## FORMATO DE SAÍDA
Retorne um JSON com uma chave "questions" contendo um array de 15 objetos no formato:
{{
  "questions": [
    {{
      "area": "Nome da Área (ex: Saúde Física)",
      "type": "open_long",
      "text": "Texto da pergunta narrativa...",
      "follow_up_hint": "Contexto para entender a resposta"
    }}
  ]
}}
"""

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL_QUESTIONS,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=3000,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or "{}"
    try:
        data = json.loads(content)
        questions = data.get("questions", data) if isinstance(data, dict) else data
        if not isinstance(questions, list):
            questions = []

        formatted = []
        for i, q in enumerate(questions[:15]):
            formatted.append({
                "id": (phase - 1) * 15 + i + 1,
                "area": q.get("area", "Geral"),
                "type": q.get("type", "open_long"),
                "text": q.get("text", ""),
                "follow_up_hint": q.get("follow_up_hint", ""),
            })

        logger.info("Generated %s questions for phase %s", len(formatted), phase)
        return formatted

    except json.JSONDecodeError as e:
        logger.error("Error parsing questions JSON: %s", e)
        raise ValueError("Erro ao gerar perguntas. Por favor, tente novamente.") from e


async def generate_final_report(
    all_responses: list[dict[str, Any]],
    scores_by_area: dict[str, Any],
    identified_patterns: list[str],
    rag_context: str,
) -> dict[str, Any]:
    """
    Gera o relatório final do diagnóstico.

    Args:
        all_responses: Todas as respostas do usuário
        scores_by_area: Scores por área
        identified_patterns: Padrões identificados
        rag_context: Contexto do RAG

    Returns:
        Relatório estruturado (executive_summary, overall_score, area_analysis, etc.)
    """
    responses_by_area: dict[str, list] = {}
    for r in all_responses:
        area = r.get("question_area", "Geral")
        if area not in responses_by_area:
            responses_by_area[area] = []
        responses_by_area[area].append(r)

    responses_text = ""
    for area, responses in responses_by_area.items():
        responses_text += f"\n### {area}\n"
        for r in responses:
            av = r.get("answer_value") or {}
            text = av.get("text", "")
            scale = av.get("scale")
            qt = (r.get("question_text") or "")[:100]
            if text:
                responses_text += f"- P: {qt}\n  R: {text[:500]}\n"
            elif scale is not None:
                responses_text += f"- {qt}: {scale}/5\n"

    system_prompt = """Você é Nara, analista sênior em Engenharia de Mindset. Sua missão é entregar um 
Diagnóstico Narrativo que revele a Incongruência Simbólica do usuário e aponte 
o caminho para a Nova Identidade.

SUA MISSÃO:
Identificar onde o "fio narrativo" se rompeu (Identidade -> Sentido -> Ação -> Conexão) 
e propor o reposicionamento da personagem.

REGRAS CRÍTICAS:
1. DIAGNÓSTICO M1: Classifique a dor principal como Crise de Identidade, Sentido, Execução ou Conexão.
2. EIXOS DE TRANSFORMAÇÃO: Analise o desalinhamento entre Narrativa (crenças), Identidade (valores) e Hábitos (princípios).
3. FASE DA JORNADA: Identifique se o usuário está em: Germinar, Enraizar, Desenvolver, Florescer, Frutificar ou Realizar.
4. PONTO DE ENTRADA: Determine a porta aberta (Emocional, Simbólico, Comportamental, Existencial).
5. PLANO DE ASSUNÇÃO INTENCIONAL: Proponha ações para: Reconhecer, Modelar, Assumir e Reforçar, usando Âncoras Práticas específicas.
6. CITE O USUÁRIO: Use aspas para destacar as "Memórias Vermelhas" (M1) mencionadas.
7. TOM: Empático-autoritário, como um Engenheiro da Alma (provocador mas compassivo).
8. LINGUAGEM SIMBÓLICA: Use termos como "âncoras", "clímax", "círculo narrativo", "travessia".
9. EVITE CLICHÊS: Não use autoajuda genérica; use técnicas de TCC.

VETOR DE ESTADO:
O diagnóstico deve incluir um vetor de estado qualitativo (não scores numéricos).

Retorne apenas JSON válido."""

    prompt = f"""# TAREFA
Gere um Diagnóstico Narrativo completo, profundo e transformador baseado na metodologia NARA.

## RESPOSTAS DO USUÁRIO (Agrupadas por Área)
{responses_text}

## PADRÕES IDENTIFICADOS (Pré-análise)
{", ".join(identified_patterns) if identified_patterns else "A serem identificados na análise"}

## SCORES CALCULADOS POR ÁREA (Apenas referência interna)
{json.dumps(scores_by_area, indent=2, ensure_ascii=False)}

## CONTEXTO METODOLÓGICO (RAG)
{rag_context}

## ESTRUTURA DO RELATÓRIO (JSON)
Retorne um JSON com EXATAMENTE esta estrutura:
{{
  "executive_summary": "Resumo executivo de 150-200 palavras. Use linguagem simbólica e cite frases do usuário.",
  "vetor_estado": {{
    "motor_dominante": "Necessidade|Valor|Desejo|Propósito",
    "motor_secundario": "Necessidade|Valor|Desejo|Propósito",
    "estagio_jornada": "Germinar|Enraizar|Desenvolver|Florescer|Frutificar|Realizar",
    "crise_raiz": "Identidade Raiz|Sentido e Direção|Execução e Estrutura|Conexão e Expressão|Incongruência Identidade-Cultura|Transformação de Personagem",
    "crises_derivadas": ["Crise secundária 1", "Crise secundária 2"],
    "ponto_entrada_ideal": "Emocional|Simbólico|Comportamental|Existencial",
    "dominios_alavanca": ["D1", "D2"],
    "tom_emocional": "vergonha|indignação|apatia|urgência|tristeza|neutro",
    "risco_principal": "Descrição do principal risco identificado",
    "necessidade_atual": "O que o usuário precisa fazer agora"
  }},
  "memorias_vermelhas": ["Frase literal 1 do usuário", "Frase literal 2 do usuário"],
  "areas_silenciadas": [1, 5],
  "ancoras_sugeridas": ["Âncora Prática 1 das 19", "Âncora Prática 2 das 19", "Âncora Prática 3 das 19"],
  "phase_identified": "germinar|enraizar|desenvolver|florescer|frutificar|realizar",
  "area_analysis": [
    {{
      "area_name": "Nome da Área",
      "area_id": 1,
      "status": "crítico|atenção|estável|forte",
      "analysis": "Análise de 2-3 frases baseada nas respostas. Cite frases do usuário.",
      "key_insight": "Insight principal desta área"
    }}
  ],
  "patterns": {{
    "correlations": ["Padrão 1 identificado entre áreas", "Padrão 2"],
    "contradictions": ["Contradição 1 nas respostas usando aspas do usuário", "Contradição 2"],
    "self_sabotage_cycles": ["Ciclo de autossabotagem identificado"]
  }},
  "strengths": ["Ponto forte 1 baseado em citações", "Ponto forte 2", "Ponto forte 3"],
  "development_areas": [
    {{
      "area_name": "Área para desenvolvimento",
      "priority": "alta|média|baixa",
      "reasoning": "Por que esta área precisa de atenção (cite evidências)"
    }}
  ],
  "recommendations": [
    {{
      "action": "Ação concreta usando uma das 19 Âncoras Práticas",
      "timeframe": "imediato|curto_prazo|medio_prazo",
      "area_related": "Área relacionada",
      "ancor_type": "Nome da Âncora Prática"
    }}
  ]
}}

## DIRETRIZES ESPECÍFICAS
1. USE MEMÓRIAS VERMELHAS: Cite entre aspas frases literais do usuário que revelam conflitos
2. IDENTIFIQUE SILÊNCIOS: Note áreas não respondidas ou respondidas vagamente
3. ÂNCORAS PRÁTICAS: Escolha das 19 disponíveis (Referências, Objetos, Ambientes, Grupo, Tom, Vocabulário, Postura, Vestimenta, Rituais Matinais, Rituais Noturnos, Limites, Marcos, Emoção Projetada, Gestão de Energia, Práticas de Recarga, Tarefas Identitárias, Microentregas, Exposição Gradual, Testemunhas)
4. LINGUAGEM METODOLÓGICA: Use "Gap MX", "M1", "CN+", "Círculo Narrativo"
5. TOM EMPÁTICO-AUTORITÁRIO: Provocador mas compassivo
6. CONEXÕES ENTRE ÁREAS: Revele como conflitos em uma área afetam outras
"""

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL_ANALYSIS,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=5000,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or "{}"
    report = json.loads(content)
    logger.info("Generated final report with overall_score: %s", report.get("overall_score"))
    return report
