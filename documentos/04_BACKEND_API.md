# 04 - BACKEND E API

> **Propósito:** Implementação completa do backend Python, sistema RAG, endpoints da API e lógica de negócio do diagnóstico NARA.

---

## 📋 ÍNDICE

1. [Estrutura do Projeto](#1-estrutura-do-projeto)
2. [Configuração e Setup](#2-configuração-e-setup)
3. [Módulo RAG](#3-módulo-rag)
4. [Pipeline de Diagnóstico](#4-pipeline-de-diagnóstico)
5. [Perguntas Baseline (Fase 1)](#5-perguntas-baseline-fase-1)
6. [Serviços de Negócio](#6-serviços-de-negócio)
7. [Endpoints da API](#7-endpoints-da-api)
8. [Modelos de Dados (Pydantic)](#8-modelos-de-dados-pydantic)
9. [Contratos da API (OpenAPI)](#9-contratos-da-api-openapi)

---

## 1. ESTRUTURA DO PROJETO

```
nara-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configurações e env vars
│   ├── database.py             # Supabase client setup
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencies (auth, db)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # Main router
│   │       ├── diagnostic.py   # Endpoints de diagnóstico
│   │       └── feedback.py     # Endpoints de feedback
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # JWT, auth
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── constants.py        # Constantes (áreas, perguntas)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── diagnostic_service.py   # Lógica do diagnóstico
│   │   ├── question_service.py     # Geração de perguntas
│   │   ├── analysis_service.py     # Análise de respostas
│   │   ├── report_service.py       # Geração de relatório
│   │   └── email_service.py        # Envio de emails
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py       # OpenAI embeddings
│   │   ├── retriever.py        # Busca vetorial
│   │   ├── generator.py        # Geração LLM
│   │   ├── analyzer.py         # Análise contextual das respostas (V2)
│   │   └── pipeline.py         # Pipeline completo
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── diagnostic.py       # Modelos Pydantic
│   │   ├── question.py
│   │   ├── answer.py
│   │   └── result.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── scoring.py          # Cálculo de scores
│       └── validators.py       # Validações customizadas
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_diagnostic.py
│   └── test_rag.py
│
├── .env.example
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 2. CONFIGURAÇÃO E SETUP

### config.py

```python
"""Configurações centralizadas da aplicação."""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Configurações carregadas de variáveis de ambiente."""
    
    # Aplicação
    APP_NAME: str = "NARA Diagnostic API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENV: str = "development"
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str  # anon key (frontend)
    SUPABASE_SERVICE_KEY: str  # service role (backend)
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL_QUESTIONS: str = "gpt-4o-mini"
    OPENAI_MODEL_ANALYSIS: str = "gpt-4o"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Resend (Email)
    RESEND_API_KEY: str
    EMAIL_FROM: str = "nara@seudominio.com"
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"
    
    # RAG
    RAG_TOP_K: int = 10
    RAG_SIMILARITY_THRESHOLD: float = 0.5
    
    # Diagnóstico
    MIN_QUESTIONS_TO_FINISH: int = 40
    MIN_WORDS_TO_FINISH: int = 3500
    QUESTIONS_PER_PHASE: int = 15
    MIN_AREAS_COVERED: int = 12
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "https://nara.app"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """Singleton para configurações."""
    return Settings()


settings = get_settings()
```

### database.py

```python
"""Cliente Supabase configurado."""
from supabase import create_client, Client
from app.config import settings


def get_supabase_client() -> Client:
    """Retorna cliente Supabase com service role (backend)."""
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_KEY
    )


def get_supabase_anon_client() -> Client:
    """Retorna cliente Supabase com anon key (operações públicas)."""
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY
    )


# Instância singleton
supabase = get_supabase_client()
```

### main.py

```python
"""Entry point da aplicação FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.api.v1.router import api_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle hooks da aplicação."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    yield
    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Endpoint de health check."""
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.get("/health/detailed")
async def health_check_detailed():
    """Health check com verificação de dependências."""
    from app.database import supabase
    
    checks = {"database": "unknown", "openai": "unknown"}
    
    # Verificar Supabase
    try:
        supabase.table("areas").select("id").limit(1).execute()
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
    
    all_healthy = all(v == "healthy" for v in checks.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "checks": checks,
        "version": settings.APP_VERSION
    }
```

### requirements.txt

```
# Core
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Supabase
supabase==2.3.0

# LangChain & OpenAI
langchain==0.1.0
langchain-openai==0.0.2
openai==1.8.0
tiktoken==0.5.2

# Email
resend==0.7.0

# Utilities
python-dotenv==1.0.0
httpx==0.26.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
```

---

## 3. MÓDULO RAG

### rag/embeddings.py

```python
"""Geração de embeddings via OpenAI."""
from openai import OpenAI
from app.config import settings
import logging

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_embedding(text: str) -> list[float]:
    """
    Gera embedding para um texto.
    
    Args:
        text: Texto para gerar embedding
        
    Returns:
        Lista de floats (vetor 1536 dimensões)
    """
    response = client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


async def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """
    Gera embeddings para múltiplos textos em batch.
    
    Args:
        texts: Lista de textos
        
    Returns:
        Lista de vetores
    """
    response = client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=texts
    )
    return [item.embedding for item in response.data]
```

### rag/retriever.py

```python
"""Recuperação de chunks relevantes via pgvector."""
from typing import Optional, List
from app.database import supabase
from app.rag.embeddings import generate_embedding
import logging

logger = logging.getLogger(__name__)


async def retrieve_relevant_chunks(
    query: str,
    top_k: int = 10,
    filter_chapter: Optional[str] = None,
    filter_motor: Optional[List[str]] = None,
    filter_crise: Optional[List[str]] = None,
    similarity_threshold: float = 0.5
) -> list[dict]:
    """
    Busca chunks relevantes para uma query usando similaridade semântica.
    
    Args:
        query: Texto da busca
        top_k: Número máximo de resultados
        filter_chapter: Filtrar por área/capítulo (ex: "Saúde Física")
        filter_motor: Filtrar por motor motivacional
        filter_crise: Filtrar por tipo de crise
        similarity_threshold: Score mínimo de similaridade
        
    Returns:
        Lista de chunks com similarity score
    """
    # Gerar embedding da query
    query_embedding = await generate_embedding(query)
    
    # Chamar função RPC do Supabase
    result = supabase.rpc(
        "match_knowledge_chunks",
        {
            "query_embedding": query_embedding,
            "match_threshold": similarity_threshold,
            "match_count": top_k,
            "filter_chapter": filter_chapter,
            "filter_motor": filter_motor,
            "filter_crise": filter_crise
        }
    ).execute()
    
    logger.info(f"RAG retrieved {len(result.data)} chunks for query")
    return result.data


async def retrieve_for_question_generation(
    user_responses: list[dict],
    underrepresented_areas: list[str],
    phase: int
) -> str:
    """
    Busca contexto relevante para geração de perguntas adaptativas.
    
    Args:
        user_responses: Respostas anteriores do usuário
        underrepresented_areas: Áreas com poucas respostas
        phase: Fase atual do diagnóstico (2, 3 ou 4)
        
    Returns:
        Contexto concatenado para o prompt
    """
    # Construir query de busca baseada nas respostas
    response_texts = " ".join([
        r.get("answer_value", {}).get("text", "") 
        for r in user_responses[-15:]  # Últimas 15 respostas
        if r.get("answer_value", {}).get("text")
    ])
    
    all_chunks = []
    
    # Buscar chunks de metodologia geral (V2)
    methodology_chunks = await retrieve_relevant_chunks(
        query=response_texts if response_texts else "diagnóstico transformação narrativa",
        top_k=5
    )
    # Nota: A função match_knowledge_chunks já filtra por version=2
    all_chunks.extend(methodology_chunks)
    
    # Buscar chunks das áreas menos cobertas
    for area in underrepresented_areas[:3]:
        area_chunks = await retrieve_relevant_chunks(
            query=f"critérios de análise {area} sinais conflito",
            top_k=2,
            filter_chapter=area
        )
        all_chunks.extend(area_chunks)
    
    # Concatenar contexto
    context = "\n\n---\n\n".join([
        f"**{chunk.get('chapter', 'Geral')}** ({chunk.get('section', '')})\n{chunk['content']}"
        for chunk in all_chunks
    ])
    
    return context


async def retrieve_for_report_generation(
    diagnostic_id: str,
    scores_by_area: dict,
    all_responses: list[dict]
) -> str:
    """
    Busca contexto relevante para geração do relatório final.
    
    Args:
        diagnostic_id: ID do diagnóstico
        scores_by_area: Scores calculados por área
        all_responses: Todas as respostas do usuário
        
    Returns:
        Contexto concatenado para o prompt
    """
    # Identificar áreas críticas (score < 5.0)
    critical_areas = [
        area_name for area_name, data in scores_by_area.items()
        if data.get("score", 10) < 5.0
    ]
    
    # Construir query diagnóstica baseada nas respostas
    response_summary = " ".join([
        r.get("answer_value", {}).get("text", "")[:200]
        for r in all_responses
        if r.get("answer_value", {}).get("text")
    ])[:2000]
    
    context_chunks = []
    
    # Buscar chunks de critérios para áreas críticas
    for area in critical_areas[:4]:
        chunks = await retrieve_relevant_chunks(
            query=f"critérios análise {area} sinais crise intervenção",
            top_k=3,
            filter_chapter=area
        )
        context_chunks.extend(chunks)
    
    # Buscar chunks de metodologia geral
    methodology = await retrieve_relevant_chunks(
        query="fases jornada motores motivacionais clusters crise assunção intencional",
        top_k=5
    )
    context_chunks.extend(methodology)
    
    # Buscar chunks baseados nas respostas
    if response_summary:
        response_chunks = await retrieve_relevant_chunks(
            query=response_summary,
            top_k=3
        )
        context_chunks.extend(response_chunks)
    
    # Concatenar
    context = "\n\n---\n\n".join([
        f"**{chunk.get('chapter', 'Metodologia')}**\n{chunk['content']}"
        for chunk in context_chunks
    ])
    
    return context
```

### rag/generator.py

```python
"""Geração de conteúdo via LLM."""
import json
from openai import OpenAI
from app.config import settings
import logging

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_adaptive_questions(
    user_responses: list[dict],
    underrepresented_areas: list[str],
    identified_patterns: list[str],
    rag_context: str,
    phase: int
) -> list[dict]:
    """
    Gera perguntas adaptativas para a próxima fase.
    
    Args:
        user_responses: Respostas anteriores
        underrepresented_areas: Áreas com poucas respostas
        identified_patterns: Padrões identificados nas respostas
        rag_context: Contexto do RAG
        phase: Fase atual (2, 3 ou 4)
        
    Returns:
        Lista de 15 perguntas geradas
    """
    # Formatar respostas para o prompt
    responses_text = "\n".join([
        f"- {r.get('question_area', 'Geral')}: {r.get('answer_value', {}).get('text', f'Nota {r.get(\"answer_value\", {}).get(\"scale\")}')})"
        for r in user_responses[-20:]
    ])
    
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
2. **100% perguntas narrativas e abertas** (open_long ou open_short) — SEM escalas numéricas
3. Tom empático-autoritário ("Engenheiro da Alma"), curioso e não-julgador
4. Referencie respostas anteriores quando relevante ("Você mencionou que...")
5. Aprofunde em temas onde o usuário demonstrou conflito ou emoção
6. Evite perguntas superficiais - busque a raiz dos padrões
7. Use linguagem simbólica da metodologia: "âncoras", "capítulo", "travessia", "personagem"
8. Inclua `follow_up_hint` para cada pergunta

## FORMATO DE SAÍDA
Retorne APENAS um JSON array válido no formato:
[
  {{
    "area": "Nome da Área (ex: Saúde Física)",
    "type": "open_long|open_short",
    "text": "Texto da pergunta...",
    "follow_up_hint": "Contexto para entender a resposta"
  }}
]
"""

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL_QUESTIONS,
        messages=[
            {"role": "system", "content": "Você é um especialista em diagnóstico de transformação narrativa baseado na metodologia do Círculo Narrativo."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=3000,
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content
    
    try:
        data = json.loads(content)
        questions = data.get("questions", data) if isinstance(data, dict) else data
        
        # Validar e formatar
        formatted = []
        for i, q in enumerate(questions[:15]):
            formatted.append({
                "id": (phase - 1) * 15 + i + 1,
                "area": q.get("area", "Geral"),
                "type": q.get("type", "open_long"),
                "text": q.get("text", ""),
                "follow_up_hint": q.get("follow_up_hint", "")
            })
        
        logger.info(f"Generated {len(formatted)} questions for phase {phase}")
        return formatted
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing questions JSON: {e}")
        raise ValueError("Erro ao gerar perguntas. Por favor, tente novamente.")


async def generate_final_report(
    all_responses: list[dict],
    scores_by_area: dict,
    identified_patterns: list[str],
    rag_context: str
) -> dict:
    """
    Gera o relatório final do diagnóstico.
    
    Args:
        all_responses: Todas as respostas do usuário
        scores_by_area: Scores por área
        identified_patterns: Padrões identificados
        rag_context: Contexto do RAG
        
    Returns:
        Relatório estruturado
    """
    # Formatar respostas agrupadas por área
    responses_by_area = {}
    for r in all_responses:
        area = r.get("question_area", "Geral")
        if area not in responses_by_area:
            responses_by_area[area] = []
        responses_by_area[area].append(r)
    
    responses_text = ""
    for area, responses in responses_by_area.items():
        responses_text += f"\n### {area}\n"
        for r in responses:
            text = r.get("answer_value", {}).get("text", "")
            scale = r.get("answer_value", {}).get("scale")
            if text:
                responses_text += f"- P: {r.get('question_text', '')[:100]}\n  R: {text[:500]}\n"
            elif scale:
                responses_text += f"- {r.get('question_text', '')[:100]}: {scale}/5\n"
    
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
  "vetor_estado": {{
    "motor_dominante": "Necessidade|Valor|Desejo|Propósito",
    "motor_secundario": "Necessidade|Valor|Desejo|Propósito",
    "estagio_jornada": "Germinar|Enraizar|Desenvolver|Florescer|Frutificar|Realizar",
    "crise_raiz": "Identidade Herdada|Vazio Existencial|Paralisia Decisória|...",
    "crises_derivadas": ["Crise derivada 1", "Crise derivada 2"],
    "ponto_entrada_ideal": "Emocional|Simbólico|Comportamental|Existencial",
    "dominios_alavanca": ["D1", "D3"],
    "tom_emocional": "vergonha|indignação|apatia|urgência|tristeza",
    "risco_principal": "Descrição do risco principal",
    "necessidade_atual": "Descrição da necessidade atual"
  }},
  "memorias_vermelhas": [
    "Frase literal do usuário revelando conflito 1",
    "Frase literal do usuário revelando conflito 2"
  ],
  "areas_silenciadas": [5, 6],
  "ancoras_sugeridas": ["Âncora 1", "Âncora 2", "Âncora 3"],
  "phase_identified": "germinar|enraizar|desenvolver|florescer|frutificar|realizar",
  "motor_dominante": "Necessidade|Valor|Desejo|Propósito",
  "motor_secundario": "Necessidade|Valor|Desejo|Propósito",
  "crise_raiz": "Identidade|Sentido|Execução|Conexão|Incongruência|Transformação",
  "ponto_entrada_ideal": "Emocional|Simbólico|Comportamental|Existencial",
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
  "capital_simbolico": ["Recurso identificado 1", "Recurso identificado 2"],
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
      "action": "Ação concreta e específica (Plano de Assunção Intencional)",
      "timeframe": "imediato|curto_prazo|medio_prazo",
      "area_related": "Área relacionada"
    }}
  ]
}}

## DIRETRIZES
- Seja empático mas direto - evite rodeios. Tom "Engenheiro da Alma" (empático-autoritário)
- Use frases do próprio usuário como evidência (Memórias Vermelhas)
- Identifique incongruências entre narrativa, identidade e hábitos (Incongruência Simbólica)
- Termine cada seção com perspectiva de crescimento
- Recomendações devem ser Âncoras Práticas concretas, específicas e realizáveis
- Identifique o motor motivacional dominante baseado nas respostas
- Use linguagem simbólica: "âncoras", "clímax", "travessia", "capítulo", "personagem"
- Foco em TCC e reestruturação cognitiva quando aplicável
- Extraia Memórias Vermelhas (frases literais que revelam conflitos não dominados)
- Identifique áreas silenciadas (não respondidas ou vagas)
- Sugira Âncoras Práticas das 19 disponíveis na metodologia
"""

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL_ANALYSIS,
        messages=[
            {"role": "system", "content": "Você é um especialista em desenvolvimento humano e transformação narrativa, treinado na metodologia do Círculo Narrativo."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=4000,
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content
    report = json.loads(content)
    
    logger.info(f"Generated final report with overall_score: {report.get('overall_score')}")
    return report
```

---

## 4. PIPELINE DE DIAGNÓSTICO

### rag/pipeline.py

```python
"""
Pipeline completo de diagnóstico NARA.
Orquestra todas as etapas do fluxo de diagnóstico.
"""
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import logging

from app.database import supabase
from app.config import settings
from app.rag.retriever import retrieve_for_question_generation, retrieve_for_report_generation
from app.rag.generator import generate_adaptive_questions, generate_final_report

logger = logging.getLogger(__name__)


class DiagnosticPhase(Enum):
    BASELINE = 1      # Fase 1: Perguntas fixas
    DEEPENING_1 = 2   # Fase 2: Primeira rodada adaptativa
    DEEPENING_2 = 3   # Fase 3: Segunda rodada adaptativa
    DEEPENING_3 = 4   # Fase 4: Terceira rodada adaptativa


@dataclass
class EligibilityResult:
    """Resultado da verificação de elegibilidade."""
    can_finish: bool
    total_answers: int
    total_words: int
    areas_covered: int
    missing_areas: List[str]
    questions_progress: float  # 0-100%
    words_progress: float      # 0-100%
    coverage_progress: float   # 0-100%
    overall_progress: float    # 0-100%


class NaraDiagnosticPipeline:
    """
    Pipeline principal do diagnóstico NARA.
    
    Fluxo:
    1. start() -> Cria diagnóstico + retorna perguntas Fase 1
    2. submit_answer() -> Processa resposta + atualiza scores
    3. check_phase_completion() -> Verifica se precisa gerar novas perguntas
    4. generate_next_phase() -> Gera perguntas adaptativas via RAG+LLM
    5. check_eligibility() -> Verifica se pode finalizar
    6. finish() -> Gera relatório final via RAG+LLM
    """
    
    # Lista das 12 áreas estruturantes
    AREAS = [
        "Saúde Física", "Saúde Mental", "Saúde Espiritual",
        "Vida Pessoal", "Vida Amorosa", "Vida Familiar",
        "Vida Social", "Vida Profissional", "Finanças",
        "Educação", "Inovação", "Lazer"
    ]
    
    def __init__(self):
        self.baseline_questions = self._load_baseline_questions()
    
    def _load_baseline_questions(self) -> List[Dict]:
        """Carrega as perguntas fixas da Fase 1."""
        from app.core.constants import BASELINE_QUESTIONS
        return BASELINE_QUESTIONS
    
    async def start(
        self,
        email: str,
        full_name: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        consent_privacy: bool = False,
        consent_marketing: bool = False,
        device_info: Optional[Dict] = None,
        utm_source: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Inicia um novo diagnóstico.
        
        Returns:
            Dict com diagnostic_id, status, phase, questions
        """
        import uuid
        
        # Gerar token único para acesso ao resultado
        result_token = f"nara_{uuid.uuid4().hex[:12]}"
        
        # Criar diagnóstico
        diagnostic_data = {
            "user_id": user_id,
            "anonymous_session_id": session_id if not user_id else None,
            "email": email,
            "full_name": full_name,
            "status": "in_progress",
            "current_phase": 1,
            "current_question": 0,
            "total_answers": 0,
            "total_words": 0,
            "areas_covered": [],
            "result_token": result_token,
            "consent_privacy": consent_privacy,
            "consent_marketing": consent_marketing,
            "device_info": device_info or {},
            "utm_source": utm_source
        }
        
        result = supabase.table("diagnostics").insert(diagnostic_data).execute()
        diagnostic = result.data[0]
        
        logger.info(f"Started diagnostic {diagnostic['id']} for {email}")
        
        return {
            "diagnostic_id": diagnostic["id"],
            "status": "in_progress",
            "phase": 1,
            "questions": self.baseline_questions,
            "total_questions": len(self.baseline_questions),
            "result_token": result_token
        }
    
    async def submit_answer(
        self,
        diagnostic_id: str,
        question_id: int,
        question_text: str,
        question_area: str,
        answer_text: Optional[str] = None,
        answer_scale: Optional[int] = None,
        response_time_seconds: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Submete uma resposta e retorna status atualizado.
        """
        # Buscar diagnóstico atual
        diag_result = supabase.table("diagnostics").select("*").eq(
            "id", diagnostic_id
        ).single().execute()
        diagnostic = diag_result.data
        
        # Calcular word_count
        word_count = len(answer_text.split()) if answer_text else 0
        
        # Preparar valor da resposta
        answer_value = {
            "text": answer_text,
            "scale": answer_scale,
            "words": word_count
        }
        
        # Inserir resposta
        answer_data = {
            "diagnostic_id": diagnostic_id,
            "question_id": question_id,
            "question_text": question_text,
            "question_area": question_area,
            "question_phase": diagnostic["current_phase"],
            "answer_value": answer_value,
            "word_count": word_count,
            "response_time_seconds": response_time_seconds
        }
        
        supabase.table("answers").insert(answer_data).execute()
        
        # Atualizar contadores do diagnóstico
        new_total = diagnostic["total_answers"] + 1
        new_words = diagnostic["total_words"] + word_count
        areas_covered = list(set(diagnostic["areas_covered"] + [question_area]))
        
        # Calcular scores parciais
        scores_by_area = await self._calculate_area_scores(diagnostic_id)
        
        supabase.table("diagnostics").update({
            "total_answers": new_total,
            "total_words": new_words,
            "areas_covered": areas_covered,
            "scores_by_area": scores_by_area,
            "current_question": diagnostic["current_question"] + 1,
            "last_activity_at": datetime.utcnow().isoformat()
        }).eq("id", diagnostic_id).execute()
        
        # Verificar elegibilidade
        eligibility = self._check_eligibility(new_total, new_words, areas_covered)
        
        # Verificar se completou a fase atual
        questions_in_phase = diagnostic["current_question"] + 1
        phase_complete = questions_in_phase >= settings.QUESTIONS_PER_PHASE
        
        logger.info(f"Answer submitted for {diagnostic_id}. Total: {new_total}, Phase complete: {phase_complete}")
        
        return {
            "status": "eligible" if eligibility.can_finish else "in_progress",
            "can_finish": eligibility.can_finish,
            "phase_complete": phase_complete,
            "progress": {
                "overall": eligibility.overall_progress,
                "questions": eligibility.questions_progress,
                "words": eligibility.words_progress,
                "coverage": eligibility.coverage_progress
            },
            "total_answers": new_total,
            "total_words": new_words,
            "areas_covered": len(areas_covered)
        }
    
    async def generate_next_phase(self, diagnostic_id: str) -> Dict[str, Any]:
        """
        Gera perguntas para a próxima fase usando RAG+LLM.
        """
        # Buscar diagnóstico e respostas
        diag_result = supabase.table("diagnostics").select("*").eq(
            "id", diagnostic_id
        ).single().execute()
        diagnostic = diag_result.data
        
        answers_result = supabase.table("answers").select("*").eq(
            "diagnostic_id", diagnostic_id
        ).order("answered_at").execute()
        answers = answers_result.data
        
        # Identificar áreas menos cobertas
        areas_count = {}
        for a in answers:
            area = a.get("question_area", "Geral")
            areas_count[area] = areas_count.get(area, 0) + 1
        
        underrepresented = [
            area for area in self.AREAS 
            if areas_count.get(area, 0) < 3
        ]
        
        # Identificar padrões nas respostas
        patterns = self._identify_patterns(answers)
        
        # Buscar contexto RAG
        next_phase = diagnostic["current_phase"] + 1
        rag_context = await retrieve_for_question_generation(
            user_responses=answers,
            underrepresented_areas=underrepresented,
            phase=next_phase
        )
        
        # Gerar perguntas adaptativas
        questions = await generate_adaptive_questions(
            user_responses=answers,
            underrepresented_areas=underrepresented,
            identified_patterns=patterns,
            rag_context=rag_context,
            phase=next_phase
        )
        
        # Atualizar fase do diagnóstico
        supabase.table("diagnostics").update({
            "current_phase": next_phase,
            "current_question": 0
        }).eq("id", diagnostic_id).execute()
        
        logger.info(f"Generated {len(questions)} questions for phase {next_phase}")
        
        return {
            "phase": next_phase,
            "questions": questions,
            "total_questions": len(questions)
        }
    
    async def check_eligibility(self, diagnostic_id: str) -> EligibilityResult:
        """
        Verifica se o diagnóstico pode ser finalizado.
        """
        result = supabase.table("diagnostics").select(
            "total_answers, total_words, areas_covered"
        ).eq("id", diagnostic_id).single().execute()
        
        data = result.data
        return self._check_eligibility(
            data["total_answers"],
            data["total_words"],
            data["areas_covered"]
        )
    
    async def finish(self, diagnostic_id: str) -> Dict[str, Any]:
        """
        Finaliza o diagnóstico e gera o relatório completo.
        """
        # Verificar elegibilidade
        eligibility = await self.check_eligibility(diagnostic_id)
        if not eligibility.can_finish:
            raise ValueError(
                f"Diagnóstico não atende aos critérios mínimos. "
                f"Progresso: {eligibility.overall_progress:.1f}%"
            )
        
        # Buscar diagnóstico e todas as respostas
        diag_result = supabase.table("diagnostics").select("*").eq(
            "id", diagnostic_id
        ).single().execute()
        diagnostic = diag_result.data
        
        answers_result = supabase.table("answers").select("*").eq(
            "diagnostic_id", diagnostic_id
        ).order("answered_at").execute()
        answers = answers_result.data
        
        # Atualizar status para processing
        supabase.table("diagnostics").update({
            "status": "processing"
        }).eq("id", diagnostic_id).execute()
        
        try:
            # Calcular scores finais
            scores_by_area = await self._calculate_area_scores(diagnostic_id)
            
            # Identificar padrões
            patterns = self._identify_patterns(answers)
            
            # Buscar contexto RAG para relatório
            rag_context = await retrieve_for_report_generation(
                diagnostic_id=diagnostic_id,
                scores_by_area=scores_by_area,
                all_responses=answers
            )
            
            # Gerar relatório via LLM
            report = await generate_final_report(
                all_responses=answers,
                scores_by_area=scores_by_area,
                identified_patterns=patterns,
                rag_context=rag_context
            )
            
            # Salvar resultado
            result_data = {
                "diagnostic_id": diagnostic_id,
                "overall_score": report.get("overall_score"),
                "area_scores": scores_by_area,
                "motor_scores": {
                    "dominante": report.get("motor_dominante"),
                    "secundario": report.get("motor_secundario")
                },
                "phase_identified": report.get("phase_identified"),
                "motor_dominante": report.get("motor_dominante"),
                "motor_secundario": report.get("motor_secundario"),
                "crise_raiz": report.get("crise_raiz"),
                "ponto_entrada_ideal": report.get("ponto_entrada_ideal"),
                # Novos campos V2
                "vetor_estado": report.get("vetor_estado"),
                "memorias_vermelhas": report.get("memorias_vermelhas", []),
                "areas_silenciadas": report.get("areas_silenciadas", []),
                "ancoras_sugeridas": report.get("ancoras_sugeridas", []),
                "executive_summary": report.get("executive_summary"),
                "detailed_analysis": report,
                "recommendations": report.get("recommendations", []),
                "strengths": report.get("strengths", []),
                "opportunities": [
                    area["area_name"] 
                    for area in report.get("development_areas", [])
                ],
                "model_used": settings.OPENAI_MODEL_ANALYSIS
            }
            
            supabase.table("diagnostic_results").insert(result_data).execute()
            
            # Atualizar diagnóstico para completed
            supabase.table("diagnostics").update({
                "status": "completed",
                "overall_score": report.get("overall_score"),
                "scores_by_area": scores_by_area,
                "insights": report.get("executive_summary"),
                "completed_at": datetime.utcnow().isoformat()
            }).eq("id", diagnostic_id).execute()
            
            logger.info(f"Diagnostic {diagnostic_id} completed with score {report.get('overall_score')}")
            
            return report
            
        except Exception as e:
            # Reverter status em caso de erro
            supabase.table("diagnostics").update({
                "status": "in_progress"
            }).eq("id", diagnostic_id).execute()
            logger.error(f"Error finishing diagnostic {diagnostic_id}: {e}")
            raise
    
    def _check_eligibility(
        self, 
        total_answers: int, 
        total_words: int, 
        areas_covered: List[str]
    ) -> EligibilityResult:
        """Verifica critérios de elegibilidade."""
        
        # Critério de quantidade: 40 perguntas OU 3500 palavras
        quantity_ok = (
            total_answers >= settings.MIN_QUESTIONS_TO_FINISH or
            total_words >= settings.MIN_WORDS_TO_FINISH
        )
        
        # Critério de cobertura: todas as 12 áreas
        coverage_ok = len(set(areas_covered)) >= settings.MIN_AREAS_COVERED
        
        # Calcular progresso de cada critério
        questions_progress = min(100, (total_answers / settings.MIN_QUESTIONS_TO_FINISH) * 100)
        words_progress = min(100, (total_words / settings.MIN_WORDS_TO_FINISH) * 100)
        coverage_progress = (len(set(areas_covered)) / settings.MIN_AREAS_COVERED) * 100
        
        # Progresso geral (média ponderada)
        overall_progress = (questions_progress * 0.4 + words_progress * 0.3 + coverage_progress * 0.3)
        
        # Áreas faltantes
        missing_areas = [area for area in self.AREAS if area not in areas_covered]
        
        return EligibilityResult(
            can_finish=quantity_ok and coverage_ok,
            total_answers=total_answers,
            total_words=total_words,
            areas_covered=len(set(areas_covered)),
            missing_areas=missing_areas,
            questions_progress=questions_progress,
            words_progress=words_progress,
            coverage_progress=coverage_progress,
            overall_progress=overall_progress
        )
    
    async def _calculate_area_scores(self, diagnostic_id: str) -> Dict[str, Any]:
        """Calcula scores por área baseado nas respostas."""
        answers_result = supabase.table("answers").select("*").eq(
            "diagnostic_id", diagnostic_id
        ).execute()
        answers = answers_result.data
        
        scores = {}
        for area in self.AREAS:
            area_answers = [a for a in answers if a.get("question_area") == area]
            if area_answers:
                # Calcular média das escalas (se houver)
                scales = [
                    a["answer_value"]["scale"] 
                    for a in area_answers 
                    if a.get("answer_value", {}).get("scale")
                ]
                avg_scale = sum(scales) / len(scales) if scales else None
                
                # Converter escala 1-5 para 0-10
                score = (avg_scale * 2) if avg_scale else 5.0  # Default 5.0 se só texto
                
                scores[area] = {
                    "score": round(score, 1),
                    "questions_answered": len(area_answers),
                    "has_text_responses": any(
                        a.get("answer_value", {}).get("text") 
                        for a in area_answers
                    )
                }
        
        return scores
    
    def _identify_patterns(self, answers: List[Dict]) -> List[str]:
        """Identifica padrões nas respostas."""
        patterns = []
        
        # Identificar áreas com scores baixos
        low_score_areas = []
        for a in answers:
            scale = a.get("answer_value", {}).get("scale")
            if scale and scale <= 2:
                low_score_areas.append(a.get("question_area"))
        
        if low_score_areas:
            most_common = max(set(low_score_areas), key=low_score_areas.count)
            patterns.append(f"Possível área de crise: {most_common}")
        
        # Identificar contradições (alta escala + texto negativo)
        # Isso seria feito com análise de sentimento mais avançada
        
        # Identificar padrões de autossabotagem (palavras-chave)
        sabotage_keywords = ["sempre", "nunca", "não consigo", "impossível", "fracasso"]
        for a in answers:
            text = a.get("answer_value", {}).get("text", "").lower()
            for keyword in sabotage_keywords:
                if keyword in text:
                    patterns.append(f"Possível padrão de autossabotagem detectado")
                    break
        
        return list(set(patterns))  # Remove duplicatas
```

---

## 5. PERGUNTAS BASELINE (FASE 1)

### core/constants.py

```python
"""
Constantes e dados estáticos do sistema NARA.
"""

# As 12 áreas estruturantes
AREAS = [
    "Saúde Física",
    "Saúde Mental", 
    "Saúde Espiritual",
    "Vida Pessoal",
    "Vida Amorosa",
    "Vida Familiar",
    "Vida Social",
    "Vida Profissional",
    "Finanças",
    "Educação",
    "Inovação",
    "Lazer"
]

# Perguntas fixas da Fase 1 (Baseline)
# V2: 100% perguntas narrativas e abertas (open_long ou open_short)
# Foco em escuta ativa — sem escalas numéricas
BASELINE_QUESTIONS = [
    {
        "id": 1,
        "area": "Saúde Física",
        "type": "open_long",
        "text": "Como você descreveria sua relação com seu corpo e sua energia física no dia a dia? O que seu corpo tem te comunicado?",
        "follow_up_hint": "Explorar vitalidade, disposição e sinais corporais"
    },
    {
        "id": 2,
        "area": "Saúde Mental",
        "type": "open_long",
        "text": "Se sua mente tivesse uma voz própria, o que ela repetiria com mais frequência? Como está seu equilíbrio emocional?",
        "follow_up_hint": "Explorar pensamentos recorrentes e estado emocional"
    },
    {
        "id": 3,
        "area": "Saúde Espiritual",
        "type": "open_long",
        "text": "O que te dá um senso de propósito ou significado na vida? De onde vem sua força interior?",
        "follow_up_hint": "Explorar fé, convicção e sentido existencial"
    },
    {
        "id": 4,
        "area": "Vida Pessoal",
        "type": "open_long",
        "text": "Se você pudesse descrever quem você é em um parágrafo, sem mencionar seu trabalho ou papéis sociais, o que diria?",
        "follow_up_hint": "Explorar identidade, autoconhecimento e essência"
    },
    {
        "id": 5,
        "area": "Vida Amorosa",
        "type": "open_long",
        "text": "Como você descreveria a qualidade das suas relações íntimas? O que você sente que falta ou sobra nelas?",
        "follow_up_hint": "Explorar vínculos afetivos e padrões relacionais"
    },
    {
        "id": 6,
        "area": "Vida Familiar",
        "type": "open_long",
        "text": "Qual é sua relação atual com sua família? Existem valores ou padrões familiares que você carrega consigo — por escolha ou por herança?",
        "follow_up_hint": "Explorar identidades herdadas e dinâmicas familiares"
    },
    {
        "id": 7,
        "area": "Vida Social",
        "type": "open_long",
        "text": "Você se sente genuinamente conectado(a) às pessoas ao seu redor? Onde você se sente mais você mesmo(a)?",
        "follow_up_hint": "Explorar pertencimento, autenticidade social e ambientes"
    },
    {
        "id": 8,
        "area": "Vida Profissional",
        "type": "open_long",
        "text": "Se dinheiro não fosse uma preocupação, o que você estaria fazendo profissionalmente? Por que não está fazendo isso agora?",
        "follow_up_hint": "Explorar realização, propósito profissional e barreiras"
    },
    {
        "id": 9,
        "area": "Finanças",
        "type": "open_long",
        "text": "Como você descreveria sua relação com dinheiro? Existe alguma crença sobre finanças que você herdou e nunca questionou?",
        "follow_up_hint": "Explorar crenças financeiras e relação com recursos"
    },
    {
        "id": 10,
        "area": "Educação",
        "type": "open_short",
        "text": "Há algo que você gostaria de aprender ou desenvolver, mas vem adiando? O que te impede?",
        "follow_up_hint": "Explorar crescimento intelectual e bloqueios"
    },
    {
        "id": 11,
        "area": "Inovação",
        "type": "open_long",
        "text": "Quando foi a última vez que você tentou algo novo ou saiu da sua zona de conforto? Como foi essa experiência?",
        "follow_up_hint": "Explorar criatividade, ousadia e medo de recomeçar"
    },
    {
        "id": 12,
        "area": "Lazer",
        "type": "open_short",
        "text": "O que você faz para se divertir e recarregar as energias? Com que frequência consegue fazer isso?",
        "follow_up_hint": "Explorar descanso, prazer e rituais de recarga"
    },
    {
        "id": 13,
        "area": "Geral",
        "type": "open_long",
        "text": "Se você pudesse mudar uma coisa na sua vida agora, o que seria? O que te impede de fazer essa mudança?",
        "follow_up_hint": "Explorar motor motivacional e barreiras centrais"
    },
    {
        "id": 14,
        "area": "Geral",
        "type": "open_long",
        "text": "Existe algo na sua história que você sente que ainda não superou ou ressignificou? Algo que ainda pesa?",
        "follow_up_hint": "Explorar memórias vermelhas e capítulos não resolvidos"
    },
    {
        "id": 15,
        "area": "Geral",
        "type": "open_long",
        "text": "Se sua vida fosse um livro, qual seria o título do capítulo atual? E qual título você gostaria que o próximo capítulo tivesse?",
        "follow_up_hint": "Explorar narrativa atual vs. narrativa desejada (M1 vs. MX)"
    }
]

# Motores motivacionais
MOTORES = {
    "Necessidade": "Dor interna que precisa de alívio",
    "Valor": "Integridade e coerência com princípios",
    "Desejo": "Vontade de conquista e realização",
    "Propósito": "Impacto significativo no mundo"
}

# Fases da jornada
FASES_JORNADA = [
    "Germinar",    # Reconhecendo a insatisfação
    "Enraizar",    # Buscando valores sólidos
    "Desenvolver", # Praticando novos hábitos
    "Florescer",   # Expressando singularidade
    "Frutificar",  # Entregando resultados
    "Realizar"     # Buscando impacto coletivo
]

# Tipos de crise
TIPOS_CRISE = [
    "Identidade",       # Identidade herdada, papéis impostos
    "Sentido",          # Futuro opaco, falta de direção
    "Execução",         # Procrastinação, paralisia decisória
    "Conexão",          # Medo do julgamento, invisibilidade
    "Incongruência",    # Choque pessoa x ambiente
    "Transformação"     # Apego a papéis obsoletos
]

# Os 4 Níveis de Identidade (Luz Total)
NIVEIS_IDENTIDADE = [
    "Personalidade",    # Temperamento, caráter, valores
    "Cultura",          # Gostos, símbolos, crenças pessoais
    "Realizações",      # Resultados e conquistas
    "Posição"           # Como é percebido publicamente
]

# Os 4 Pontos de Entrada (Portas de Intervenção)
PONTOS_ENTRADA = {
    "Emocional": "Usuário relata estados afetivos → Validar e regular emoção",
    "Simbólico": "Falta de sentido ou traição de valores → Ressignificar",
    "Comportamental": "Foco em hábitos e procrastinação → Sugerir protocolos concretos",
    "Existencial": "Crise de papel de vida → Reposicionar missão e legado"
}

# As 19 Âncoras Práticas (Assunção Intencional)
ANCORAS_PRATICAS = [
    # Ambiente e Contexto
    "Referências", "Objetos", "Ambientes", "Grupo",
    # Comunicação e Expressão
    "Tom", "Vocabulário", "Postura", "Vestimenta",
    # Rotina e Estrutura
    "Rituais Matinais", "Rituais Noturnos", "Limites", "Marcos",
    # Emoção e Energia
    "Emoção Projetada", "Gestão de Energia", "Práticas de Recarga",
    # Ação e Entrega
    "Tarefas Identitárias", "Microentregas", "Exposição Gradual", "Testemunhas"
]

# Domínios Temáticos (D1-D6)
DOMINIOS_TEMATICOS = {
    "D1": "Motivações e Conflitos",
    "D2": "Crenças, Valores e Princípios",
    "D3": "Evolução e Desenvolvimento",
    "D4": "Congruência Identidade-Cultura",
    "D5": "Transformação de Identidade",
    "D6": "Papel na Sociedade"
}

# Fatores do Protocolo de Diagnóstico Rápido
FATORES_DIAGNOSTICO = [
    "Autenticidade",
    "Integração do Passado",
    "Visão/Enredo",
    "Coragem/Decisão",
    "Expressão/Voz",
    "Estrutura/Pertencimento"
]

# Clusters de Crise (detalhamento)
CLUSTERS_CRISE = {
    "Identidade Raiz": {
        "sinais": ["Identidade herdada", "Vergonha da história", "Autoimagem desatualizada"],
        "ponto_entrada": "Simbólico",
        "dominios": ["D1", "D2"]
    },
    "Sentido e Direção": {
        "sinais": ["Futuro opaco", "Tempo perdido", "Falta de enredo"],
        "ponto_entrada": "Existencial",
        "dominios": ["D2", "D3"]
    },
    "Execução e Estrutura": {
        "sinais": ["Procrastinação", "Paralisia decisória", "Falta de limites"],
        "ponto_entrada": "Comportamental",
        "dominios": ["D3"]
    },
    "Conexão e Expressão": {
        "sinais": ["Medo do julgamento", "Invisibilidade simbólica", "Desconforto com sucesso"],
        "ponto_entrada": "Emocional",
        "dominios": ["D4"]
    },
    "Incongruência Identidade-Cultura": {
        "sinais": ["Choque ambiental", "Desajuste sistêmico"],
        "ponto_entrada": "Simbólico",
        "dominios": ["D4", "D5"]
    },
    "Transformação de Personagem": {
        "sinais": ["Apego a papéis obsoletos", "Medo de crescer", "Dificuldade em encerrar capítulos"],
        "ponto_entrada": "Existencial",
        "dominios": ["D5", "D6"]
    }
}
```

---

## 6. SERVIÇOS DE NEGÓCIO

### services/diagnostic_service.py

```python
"""Serviço de orquestração do diagnóstico."""
from typing import Optional, Dict, Any
from uuid import UUID

from app.rag.pipeline import NaraDiagnosticPipeline
from app.services.email_service import EmailService

pipeline = NaraDiagnosticPipeline()
email_service = EmailService()


class DiagnosticService:
    """Interface de alto nível para operações de diagnóstico."""
    
    async def start_diagnostic(
        self,
        email: str,
        full_name: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        consent_privacy: bool = False,
        consent_marketing: bool = False,
        device_info: Optional[Dict] = None,
        utm_source: Optional[str] = None
    ) -> Dict[str, Any]:
        """Inicia um novo diagnóstico."""
        return await pipeline.start(
            email=email,
            full_name=full_name,
            user_id=user_id,
            session_id=session_id,
            consent_privacy=consent_privacy,
            consent_marketing=consent_marketing,
            device_info=device_info,
            utm_source=utm_source
        )
    
    async def submit_answer(
        self,
        diagnostic_id: str,
        question_id: int,
        question_text: str,
        question_area: str,
        answer_text: Optional[str] = None,
        answer_scale: Optional[int] = None,
        response_time_seconds: Optional[int] = None
    ) -> Dict[str, Any]:
        """Submete uma resposta."""
        return await pipeline.submit_answer(
            diagnostic_id=diagnostic_id,
            question_id=question_id,
            question_text=question_text,
            question_area=question_area,
            answer_text=answer_text,
            answer_scale=answer_scale,
            response_time_seconds=response_time_seconds
        )
    
    async def get_next_questions(self, diagnostic_id: str) -> Dict[str, Any]:
        """Gera perguntas da próxima fase."""
        return await pipeline.generate_next_phase(diagnostic_id)
    
    async def check_eligibility(self, diagnostic_id: str) -> Dict[str, Any]:
        """Verifica elegibilidade para finalização."""
        result = await pipeline.check_eligibility(diagnostic_id)
        return {
            "can_finish": result.can_finish,
            "criteria": {
                "questions": {
                    "current": result.total_answers,
                    "required": 40,
                    "percentage": result.questions_progress,
                    "met": result.total_answers >= 40
                },
                "words": {
                    "current": result.total_words,
                    "required": 3500,
                    "percentage": result.words_progress,
                    "met": result.total_words >= 3500
                },
                "coverage": {
                    "current": result.areas_covered,
                    "required": 12,
                    "percentage": result.coverage_progress,
                    "met": result.areas_covered >= 12,
                    "missing_areas": result.missing_areas
                }
            },
            "overall_progress": result.overall_progress
        }
    
    async def finish_diagnostic(self, diagnostic_id: str) -> Dict[str, Any]:
        """Finaliza o diagnóstico e gera relatório."""
        report = await pipeline.finish(diagnostic_id)
        
        # Enviar email com resultado
        # (implementação em email_service)
        
        return report
    
    async def get_result(self, diagnostic_id: str) -> Optional[Dict[str, Any]]:
        """Obtém resultado de um diagnóstico finalizado."""
        from app.database import supabase
        
        result = supabase.table("diagnostic_results").select("*").eq(
            "diagnostic_id", diagnostic_id
        ).single().execute()
        
        if not result.data:
            return None
        
        return result.data.get("detailed_analysis")
    
    async def get_result_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Obtém resultado pelo token público."""
        from app.database import supabase
        
        # Buscar diagnóstico pelo token
        diag_result = supabase.table("diagnostics").select("id").eq(
            "result_token", token
        ).single().execute()
        
        if not diag_result.data:
            return None
        
        return await self.get_result(diag_result.data["id"])
```

---

## 7. ENDPOINTS DA API

### api/v1/diagnostic.py

```python
"""Endpoints de diagnóstico."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.services.diagnostic_service import DiagnosticService
from app.models.diagnostic import (
    DiagnosticStartRequest,
    DiagnosticStartResponse,
    AnswerSubmitRequest,
    AnswerSubmitResponse,
    EligibilityResponse,
    DiagnosticResultResponse,
    NextQuestionsResponse
)
from app.api.deps import get_current_user_optional

router = APIRouter(prefix="/diagnostic", tags=["Diagnostic"])
service = DiagnosticService()


@router.post("/start", response_model=DiagnosticStartResponse)
async def start_diagnostic(request: DiagnosticStartRequest):
    """
    Inicia um novo diagnóstico.
    
    - Requer email e consentimento de privacidade
    - Retorna as 15 perguntas da Fase 1 (Baseline)
    - Retorna token único para acesso ao resultado
    """
    if not request.consent_privacy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consentimento de privacidade é obrigatório"
        )
    
    result = await service.start_diagnostic(
        email=request.email,
        full_name=request.full_name,
        session_id=request.session_id,
        consent_privacy=request.consent_privacy,
        consent_marketing=request.consent_marketing,
        device_info=request.device_info,
        utm_source=request.utm_source
    )
    
    return result


@router.post("/{diagnostic_id}/answer", response_model=AnswerSubmitResponse)
async def submit_answer(
    diagnostic_id: str,
    request: AnswerSubmitRequest
):
    """
    Submete uma resposta para uma pergunta.
    
    - Atualiza contadores e scores parciais
    - Retorna progresso e status de elegibilidade
    """
    result = await service.submit_answer(
        diagnostic_id=diagnostic_id,
        question_id=request.question_id,
        question_text=request.question_text,
        question_area=request.question_area,
        answer_text=request.answer_text,
        answer_scale=request.answer_scale,
        response_time_seconds=request.response_time_seconds
    )
    
    return result


@router.get("/{diagnostic_id}/next-questions", response_model=NextQuestionsResponse)
async def get_next_questions(diagnostic_id: str):
    """
    Gera perguntas para a próxima fase.
    
    - Usa RAG + LLM para personalização
    - Tempo de geração: 3-5 segundos
    """
    result = await service.get_next_questions(diagnostic_id)
    return result


@router.get("/{diagnostic_id}/eligibility", response_model=EligibilityResponse)
async def check_eligibility(diagnostic_id: str):
    """
    Verifica se o diagnóstico pode ser finalizado.
    
    Critérios:
    - ≥40 perguntas OU ≥3500 palavras
    - ≥1 resposta em cada uma das 12 áreas
    """
    result = await service.check_eligibility(diagnostic_id)
    return result


@router.post("/{diagnostic_id}/finish", response_model=DiagnosticResultResponse)
async def finish_diagnostic(diagnostic_id: str):
    """
    Finaliza o diagnóstico e gera o relatório.
    
    - Valida elegibilidade antes de prosseguir
    - Gera relatório via RAG + LLM (5-10 segundos)
    - Envia email com resultado
    """
    # Verificar elegibilidade primeiro
    eligibility = await service.check_eligibility(diagnostic_id)
    if not eligibility["can_finish"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Diagnóstico não atende aos critérios. Progresso: {eligibility['overall_progress']:.1f}%"
        )
    
    result = await service.finish_diagnostic(diagnostic_id)
    return result


@router.get("/{diagnostic_id}/result", response_model=DiagnosticResultResponse)
async def get_result(diagnostic_id: str):
    """
    Obtém o resultado de um diagnóstico finalizado.
    """
    result = await service.get_result(diagnostic_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultado não encontrado. Diagnóstico pode não ter sido finalizado."
        )
    
    return result


@router.get("/result/{token}", response_model=DiagnosticResultResponse)
async def get_result_by_token(token: str):
    """
    Obtém resultado pelo token público.
    
    - Permite visualização sem autenticação
    - Token é único por diagnóstico
    """
    result = await service.get_result_by_token(token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultado não encontrado ou token inválido."
        )
    
    return result
```

---

## 8. MODELOS DE DADOS (PYDANTIC)

### models/diagnostic.py

```python
"""Modelos Pydantic para diagnóstico."""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# ===== REQUESTS =====

class DiagnosticStartRequest(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    session_id: Optional[str] = None
    consent_privacy: bool = Field(..., description="Consentimento obrigatório")
    consent_marketing: bool = False
    device_info: Optional[Dict[str, Any]] = None
    utm_source: Optional[str] = None


class AnswerSubmitRequest(BaseModel):
    question_id: int
    question_text: str
    question_area: str
    answer_text: Optional[str] = Field(None, max_length=10000)
    answer_scale: Optional[int] = Field(None, ge=1, le=5)  # LEGACY V1: Sempre null em V2 (perguntas 100% narrativas)
    response_time_seconds: Optional[int] = Field(None, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "question_id": 1,
                "question_text": "De 1 a 5, como você avalia sua energia física?",
                "question_area": "Saúde Física",
                "answer_scale": 4
            }
        }


# ===== RESPONSES =====

class QuestionResponse(BaseModel):
    id: int
    area: str
    type: str = Field(..., pattern="^(scale|open_long|open_short)$")
    text: str
    scale_labels: Optional[List[str]] = None
    follow_up_hint: Optional[str] = None


class ProgressResponse(BaseModel):
    overall: float = Field(..., ge=0, le=100)
    questions: float = Field(..., ge=0, le=100)
    words: float = Field(..., ge=0, le=100)
    coverage: float = Field(..., ge=0, le=100)


class DiagnosticStartResponse(BaseModel):
    diagnostic_id: str
    status: str
    phase: int
    questions: List[QuestionResponse]
    total_questions: int
    result_token: str


class AnswerSubmitResponse(BaseModel):
    status: str
    can_finish: bool
    phase_complete: bool
    progress: ProgressResponse
    total_answers: int
    total_words: int
    areas_covered: int


class NextQuestionsResponse(BaseModel):
    phase: int
    questions: List[QuestionResponse]
    total_questions: int


class CriteriaDetail(BaseModel):
    current: int
    required: int
    percentage: float
    met: bool
    missing_areas: Optional[List[str]] = None


class EligibilityResponse(BaseModel):
    can_finish: bool
    criteria: Dict[str, CriteriaDetail]
    overall_progress: float


class AreaAnalysis(BaseModel):
    area_name: str
    score: float
    status: str
    analysis: str
    key_insight: str


class Recommendation(BaseModel):
    action: str
    timeframe: str
    area_related: Optional[str] = None


class DiagnosticResultResponse(BaseModel):
    overall_score: float
    phase_identified: str
    motor_dominante: str
    motor_secundario: Optional[str] = None
    crise_raiz: str
    ponto_entrada_ideal: str
    executive_summary: str
    area_analysis: List[AreaAnalysis]
    patterns: Dict[str, List[str]]
    strengths: List[str]
    development_areas: List[Dict[str, Any]]
    recommendations: List[Recommendation]
```

---

## 9. CONTRATOS DA API (OPENAPI)

### Resumo dos Endpoints

| Método | Endpoint | Descrição | Auth |
|----|----|----|----|
| `POST` | `/api/v1/diagnostic/start` | Inicia diagnóstico | Não |
| `POST` | `/api/v1/diagnostic/{id}/answer` | Submete resposta | Não |
| `GET` | `/api/v1/diagnostic/{id}/next-questions` | Gera próximas perguntas | Não |
| `GET` | `/api/v1/diagnostic/{id}/eligibility` | Verifica elegibilidade | Não |
| `POST` | `/api/v1/diagnostic/{id}/finish` | Finaliza e gera relatório | Não |
| `GET` | `/api/v1/diagnostic/{id}/result` | Obtém resultado | Não |
| `GET` | `/api/v1/diagnostic/result/{token}` | Obtém resultado por token | Não |
| `POST` | `/api/v1/feedback` | Submete feedback NPS | Não |
| `POST` | `/api/v1/waitlist` | Adiciona à lista de espera | Não |
| `GET` | `/health` | Health check | Não |
| `GET` | `/health/detailed` | Health check detalhado | Não |

### Códigos de Status

| Código | Significado |
|----|----|
| `200` | Sucesso |
| `201` | Recurso criado |
| `400` | Requisição inválida / Critérios não atendidos |
| `404` | Não encontrado |
| `422` | Erro de validação |
| `500` | Erro interno |

### Fluxo Típico de Uso

```
1. POST /diagnostic/start
   ↓ Retorna diagnostic_id + 15 perguntas
   
2. POST /diagnostic/{id}/answer (x15)
   ↓ Respostas da Fase 1
   
3. GET /diagnostic/{id}/next-questions
   ↓ Gera 15 perguntas adaptativas (3-5s)
   
4. POST /diagnostic/{id}/answer (x15)
   ↓ Respostas da Fase 2
   
5. GET /diagnostic/{id}/eligibility
   ↓ Verifica se pode finalizar
   
6. POST /diagnostic/{id}/finish
   ↓ Gera relatório (5-10s)
   
7. GET /diagnostic/result/{token}
   ↓ Visualiza resultado
```

---