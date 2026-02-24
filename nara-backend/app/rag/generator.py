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
    adaptive_templates: list[dict[str, Any]] | None = None,
    max_questions: int = 15,
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
        Lista de perguntas geradas (id, area, type, text, follow_up_hint).
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

    system_prompt = """Você é Nara, especialista em transformação pessoal por meio de perguntas profundas e acessíveis.
Sua missão é ajudar a pessoa a entender o que está vivendo hoje e a se aproximar de quem ela quer se tornar.

## CONTEXTO DE ANÁLISE

### AS 12 ÁREAS DA VIDA:
1. Saúde Física - Disposição e energia para viver a rotina
2. Saúde Mental - Pensamentos, emoções e clareza mental
3. Saúde Espiritual - Sentido de vida, fé e propósito pessoal
4. Vida Pessoal - Autoconhecimento e direção individual
5. Vida Amorosa - Relações íntimas e parceria
6. Vida Familiar - Relações com família e valores de origem
7. Vida Social - Amizades, rede de apoio e pertencimento
8. Vida Profissional - Trabalho, carreira e reconhecimento
9. Finanças - Relação com dinheiro e segurança material
10. Educação - Aprendizado contínuo e desenvolvimento
11. Inovação - Criatividade e abertura ao novo
12. Lazer - Descanso, prazer e recuperação de energia

### 4 FORÇAS DE MOTIVAÇÃO:
- **Necessidade**: busca sair da dor
- **Valor**: busca coerência com princípios
- **Desejo**: busca conquista e realização
- **Propósito**: busca impacto e contribuição

### 6 TIPOS DE CRISE (PADRÕES DE CONFLITO):
- **Identidade Raiz**: vergonha da história, papéis herdados, autoimagem antiga
- **Sentido e Direção**: vazio, confusão de rumo, falta de visão de futuro
- **Execução e Estrutura**: procrastinação, paralisia, falta de rotina e limites
- **Conexão e Expressão**: medo de julgamento, invisibilidade, solidão
- **Identidade x Ambiente**: choque entre quem a pessoa é e o contexto em que vive
- **Transformação de Personagem**: apego ao passado e medo de crescer

### 4 PORTAS DE ENTRADA:
- **Emocional**: quando a fala vem carregada de sentimentos
- **Valores e Sentido**: quando a fala mostra perda de sentido ou traição de valores
- **Hábitos e Rotina**: quando a fala mostra desorganização, repetição e bloqueios práticos
- **Propósito e Papel de Vida**: quando a fala questiona missão e direção de vida

### FASES DA JORNADA:
Germinar → Enraizar → Desenvolver → Florescer → Frutificar → Realizar

### TÉCNICAS DE TCC (USO ORIENTADO):
- Flecha Descendente: aprofunda crenças por trás da autocrítica e do medo.
- Questionamento Socrático: testa crenças absolutas com perguntas de evidência.
- Descatastrofização: trabalha medo de pior cenário com realismo.
- Reestruturação Cognitiva Escrita: reformula frases limitantes.
- Redefinição Cognitiva Assistida: ressignifica leituras punitivas de eventos.
- Substituição de Pensamentos Distorcidos: troca generalizações por frases mais funcionais.
- Imaginação Guiada: visualiza a identidade desejada em ação.

### TRÊS DIMENSÕES DE TRANSFORMAÇÃO:
- Crenças e narrativa pessoal: "Que história você tem repetido sobre esta área?"
- Identidade e valores: "Quem você está sendo nesta área? Quem escolheria ser?"
- Hábitos e prática diária: "Qual microação coerente com a pessoa que você quer ser você pode começar hoje?"

### DOMÍNIOS TEMÁTICOS (FERRAMENTAS TRANSVERSAIS):
Fase da Jornada e Domínio Temático são conceitos distintos:
- Fase da Jornada = onde a pessoa está no processo de transformação.
- Domínio Temático = lente de diagnóstico/intervenção que atravessa todas as fases.

Use os domínios com linguagem acessível e considere a fase de maior potência apenas como correlação:
- D1 Motivação e Conflitos — maior potência em Germinar: "O que está te movendo — e o que está te travando?"
- D2 Crenças e Valores — maior potência em Enraizar: "O que é inegociável para você nesta área?"
- D3 Evolução e Desenvolvimento — maior potência em Desenvolver: "Você está se tornando quem deseja ser?"
- D4 Identidade e Ambiente — maior potência em Florescer: "Sua expressão é fiel à sua essência ou moldada pelo ambiente?"
- D5 Transformação de Identidade — maior potência em Frutificar: "Quem você está sendo nesta fase da vida?"
- D6 Papel no Mundo — maior potência em Realizar: "Como sua história contribui para o mundo?"

### BARREIRAS COMO SINAL DE CRESCIMENTO:
Quando a pessoa trouxer resistência, trate isso como oportunidade de evolução:
"Essa barreira mostra o estágio real da sua mudança. Não é falha, é um convite para confirmar sua nova direção."

## REGRAS DE ANÁLISE:
1. IDENTIFIQUE a força de motivação dominante.
2. IDENTIFIQUE os principais padrões de crise.
3. MAPEIE O CONTEXTO: pessoas, espaços e atmosfera emocional que cercam o conflito.
4. FOQUE NA DISTÂNCIA entre quem a pessoa é hoje e quem quer se tornar.
5. USE LINGUAGEM SIMBÓLICA acessível: âncoras, semente, fruto, travessia.
6. ESCUTA ATIVA: "Percebi que sua fala sobre [Área] indica [Padrão]..."
7. TRATE SILÊNCIOS: o que está vago ou ausente também comunica bloqueios.
8. USE TCC para ajudar a reescrever a narrativa com profundidade e clareza.

Retorne apenas JSON válido."""

    templates_text = json.dumps(adaptive_templates or [], ensure_ascii=False, indent=2)

    prompt = f"""# TAREFA
Gere exatamente {max_questions} perguntas NARRATIVAS E ABERTAS para a Fase {phase} do diagnóstico.

## RESPOSTAS ANTERIORES DO USUÁRIO
{responses_text}

## ÁREAS COM MENOS COBERTURA (priorizar)
{", ".join(underrepresented_areas)}

## PADRÕES IDENTIFICADOS NAS RESPOSTAS
{", ".join(identified_patterns) if identified_patterns else "Ainda sendo identificados"}

## CONTEXTO METODOLÓGICO
{rag_context}

## TEMPLATES ADAPTATIVOS ATIVADOS (quando houver)
{templates_text}

## REGRAS IMPORTANTES
1. Distribua perguntas priorizando as áreas menos cobertas
2. TODAS as perguntas devem ser do tipo "open_long" (perguntas abertas e narrativas)
3. Tom empático-autoritário: provocador mas compassivo
4. Referencie respostas anteriores quando relevante ("Você mencionou que...")
5. Aprofunde em temas onde o usuário demonstrou conflito ou emoção
6. Use linguagem simbólica: "âncoras", "clímax", "círculo narrativo"
7. Busque a raiz dos padrões, não sintomas superficiais
8. Identifique o Ponto de Entrada nas respostas (Emocional, Simbólico, Comportamental, Existencial)
9. Se houver templates adaptativos, priorize-os sem repetir perguntas idênticas
10. Para templates com técnica de TCC, mantenha coerência da técnica na formulação
11. NUNCA use termos técnicos da metodologia nas perguntas (M1, MX, Gap MX, CN+, D1-D6, clusters, assunção intencional, capital simbólico, memórias vermelhas, luz total, FCU, volição, força-tarefa, relating, incongruência simbólica, pontos de prova e similares). Sempre substitua pelo conceito em linguagem simples e acessível.
12. Use linguagem simples, popular e direta. Evite jargões ou frases complexas. Escreva como se explicasse para alguém de 12 anos: palavras curtas, frases diretas, sem rodeios — mantendo a profundidade emocional e a provocação reflexiva.

## FORMATO DE SAÍDA
Retorne um JSON com uma chave "questions" contendo um array de até {max_questions} objetos no formato:
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
        for i, q in enumerate(questions[:max_questions]):
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

    system_prompt = """Você é Nara, analista sênior em diagnóstico narrativo e transformação pessoal.
Sua missão é entregar um diagnóstico profundo, claro e acolhedor, sem jargões.

SUA MISSÃO:
Identificar onde a história de vida da pessoa perdeu força (quem ela é -> para onde vai -> como age -> com quem se conecta)
e propor um reposicionamento prático e humano.

REGRAS CRÍTICAS:
1. DIAGNÓSTICO DA SITUAÇÃO ATUAL: classifique a dor principal como crise de identidade, sentido, execução ou conexão.
2. TRÊS DIMENSÕES DA MUDANÇA: analise o desalinhamento entre crenças (narrativa), valores (identidade) e ações (hábitos).
3. FASE DA JORNADA: identifique se a pessoa está em Germinar, Enraizar, Desenvolver, Florescer, Frutificar ou Realizar.
4. PORTA DE ENTRADA: determine qual porta está mais aberta (emocional, valores e sentido, hábitos e rotina, propósito e papel de vida).
5. PLANO EM 4 MOVIMENTOS: reconhecer, modelar, assumir e reforçar com ações concretas.
6. CITE O USUÁRIO: use aspas com frases reais da pessoa que revelem conflitos importantes.
7. TOM: empático, direto e respeitoso; provocador sem agressividade.
8. LINGUAGEM: simples, popular e clara.
9. EVITE CLICHÊS: não use autoajuda genérica; use raciocínio prático.

TRÊS DIMENSÕES — analise separadamente:
- Crenças: que história a pessoa conta para si?
- Identidade: que valores ela diz defender?
- Hábitos: que ações sustentam ou contradizem essa direção?

PLANO EM 4 MOVIMENTOS:
1. RECONHECER: qual padrão atual precisa ser nomeado?
2. MODELAR: como é a versão desejada da pessoa neste contexto?
3. ASSUMIR: qual ação concreta pode ser iniciada agora?
4. REFORÇAR: quais microvitórias sustentam a mudança?

DOMÍNIO DE MAIOR ALAVANCA:
Identifique o domínio mais útil para a fase atual e organize as recomendações a partir dele.

DESAFIOS COMO VALIDAÇÃO:
Reinterprete resistências como sinais de crescimento:
- Nas crenças: "Esse desafio mostra uma história que precisa ser atualizada."
- Nos valores: "Esse desafio testa a coerência entre o que você diz e o que escolhe."
- Nos hábitos: "Esse desafio aponta o comportamento que precisa de ajuste."

NÍVEIS DE IDENTIDADE:
- Personalidade
- Cultura
- Realizações
- Posição

VETOR DE ESTADO:
O diagnóstico deve incluir um vetor qualitativo estruturado (não apenas scores).

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
  "executive_summary": "Resumo executivo de 150-200 palavras em linguagem simples, clara e sem termos técnicos. Cite frases do usuário.",
  "vetor_estado": {{
    "motor_dominante": "Necessidade|Valor|Desejo|Propósito",
    "motor_secundario": "Necessidade|Valor|Desejo|Propósito",
    "estagio_jornada": "Germinar|Enraizar|Desenvolver|Florescer|Frutificar|Realizar",
    "crise_raiz": "Identidade Raiz|Sentido e Direção|Execução e Estrutura|Conexão e Expressão|Incongruência Identidade-Cultura|Transformação de Personagem",
    "crises_derivadas": ["Crise secundária 1", "Crise secundária 2"],
    "ponto_entrada_ideal": "Emocional|Simbólico|Comportamental|Existencial",
    "dominios_alavanca": ["D1", "D2"],
    "eixo_mais_comprometido": "Narrativa|Identidade|Habitos",
    "dominio_alavanca": "D1|D2|D3|D4|D5|D6",
    "etapa_assuncao": "Reconhecer|Modelar|Assumir|Reforcar",
    "tom_emocional": "vergonha|indignação|apatia|urgência|tristeza|neutro",
    "risco_principal": "Descrição do principal risco identificado",
    "necessidade_atual": "O que o usuário precisa fazer agora",
    "nivel_identidade": "Personalidade|Cultura|Realizações|Posição"
  }},
  "plano_assuncao": {{
    "reconhecer": "Padrão atual a ser consciencializado",
    "modelar": "Imagem da identidade e hábitos ideais",
    "assumir": "Ação simbólica concreta para assumir já",
    "reforcar": "Microvitória diária para consolidar"
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
      "analysis": "Análise de 2-3 frases em linguagem simples, sem termos técnicos. Cite frases do usuário.",
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
      "reasoning": "Por que esta área precisa de atenção em linguagem simples (cite evidências)"
    }}
  ],
  "recommendations": [
    {{
      "action": "Ação concreta em linguagem simples",
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
4. LINGUAGEM ACESSÍVEL: Use linguagem clara e direta. NUNCA use siglas ou termos técnicos da metodologia (M1, MX, M2X, M3, Gap MX, CN, CN+, D1-D6, clusters, assunção intencional, capital simbólico, memórias vermelhas, FCU, volição, força-tarefa, relating e similares). Sempre descreva os conceitos de forma simples.
5. TOM EMPÁTICO-AUTORITÁRIO: Provocador mas compassivo
6. CONEXÕES ENTRE ÁREAS: Revele como conflitos em uma área afetam outras
7. CAMPOS DE TEXTO AO USUÁRIO: Em `executive_summary`, `area_analysis.analysis`, `area_analysis.key_insight`, `development_areas.reasoning`, `recommendations.action`, `strengths`, `patterns.correlations`, `patterns.contradictions` e `patterns.self_sabotage_cycles`, use somente linguagem acessível e sem jargões.
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
