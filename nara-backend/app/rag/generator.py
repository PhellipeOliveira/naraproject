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

    prompt = f"""# TAREFA
Você é um especialista em Transformação Narrativa. Gere exatamente 15 perguntas para a Fase {phase} do diagnóstico.

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
2. Mix de tipos: 5 perguntas de escala (1-5), 8 perguntas abertas longas, 2 curtas
3. Tom empático, curioso e não-julgador
4. Referencie respostas anteriores quando relevante ("Você mencionou que...")
5. Aprofunde em temas onde o usuário demonstrou conflito ou emoção
6. Evite perguntas superficiais - busque a raiz dos padrões

## FORMATO DE SAÍDA
Retorne um JSON com uma chave "questions" contendo um array de 15 objetos no formato:
{{
  "questions": [
    {{
      "area": "Nome da Área (ex: Saúde Física)",
      "type": "scale|open_long|open_short",
      "text": "Texto da pergunta...",
      "follow_up_hint": "Contexto para entender a resposta"
    }}
  ]
}}
"""

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL_QUESTIONS,
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em diagnóstico de transformação narrativa baseado na metodologia do Círculo Narrativo. Retorne apenas JSON válido.",
            },
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

    prompt = f"""# TAREFA
Você é um especialista em Transformação Narrativa. Gere um diagnóstico completo, profundo e transformador.

## RESPOSTAS DO USUÁRIO
{responses_text}

## SCORES CALCULADOS POR ÁREA
{json.dumps(scores_by_area, indent=2, ensure_ascii=False)}

## PADRÕES IDENTIFICADOS
{", ".join(identified_patterns) if identified_patterns else "A serem identificados na análise"}

## CONTEXTO METODOLÓGICO
{rag_context}

## ESTRUTURA DO RELATÓRIO (JSON)
Retorne um JSON com EXATAMENTE esta estrutura:
{{
  "executive_summary": "Resumo executivo de 150-200 palavras. Seja direto mas empático.",
  "overall_score": 0.0-10.0,
  "phase_identified": "germinar|enraizar|desenvolver|florescer|frutificar|realizar",
  "motor_dominante": "Necessidade|Valor|Desejo|Propósito",
  "motor_secundario": "Necessidade|Valor|Desejo|Propósito",
  "crise_raiz": "Identidade|Sentido|Execução|Conexão|Incongruência|Transformação",
  "ponto_entrada_ideal": "Simbólico|Cognitivo|Comportamental|Emocional|Ambiental|Temporal",
  "area_analysis": [
    {{
      "area_name": "Nome da Área",
      "score": 0.0-10.0,
      "status": "crítico|atenção|estável|forte",
      "analysis": "Análise de 2-3 frases baseada nas respostas",
      "key_insight": "Insight principal desta área"
    }}
  ],
  "patterns": {{
    "correlations": ["Padrão 1 identificado entre áreas", "Padrão 2"],
    "contradictions": ["Contradição 1 nas respostas", "Contradição 2"],
    "self_sabotage_cycles": ["Ciclo de autossabotagem identificado"]
  }},
  "strengths": ["Ponto forte 1", "Ponto forte 2", "Ponto forte 3"],
  "development_areas": [
    {{
      "area_name": "Área para desenvolvimento",
      "priority": "alta|média|baixa",
      "reasoning": "Por que esta área precisa de atenção"
    }}
  ],
  "recommendations": [
    {{
      "action": "Ação concreta e específica",
      "timeframe": "imediato|curto_prazo|medio_prazo",
      "area_related": "Área relacionada"
    }}
  ]
}}

## DIRETRIZES
- Seja empático mas direto - evite rodeios
- Use frases do próprio usuário como evidência
- Identifique incongruências entre narrativa, identidade e hábitos
- Termine cada seção com perspectiva de crescimento
- Recomendações devem ser concretas, específicas e realizáveis
- Identifique o motor motivacional dominante baseado nas respostas
"""

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL_ANALYSIS,
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em desenvolvimento humano e transformação narrativa, treinado na metodologia do Círculo Narrativo. Retorne apenas JSON válido.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=4000,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or "{}"
    report = json.loads(content)
    logger.info("Generated final report with overall_score: %s", report.get("overall_score"))
    return report
