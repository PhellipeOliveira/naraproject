# 07 - DEPLOY E QUALIDADE

> **Propósito:** LGPD, métricas de sucesso, testes, deploy, monitoramento e checklist completo para o sistema NARA.

---

## 📋 ÍNDICE

1. [Conformidade LGPD](#1-conformidade-lgpd)
2. [Métricas de Sucesso](#2-métricas-de-sucesso)
3. [Testes e Qualidade](#3-testes-e-qualidade)
4. [Deploy e Infraestrutura](#4-deploy-e-infraestrutura)
5. [Monitoramento](#5-monitoramento)
6. [Checklist de Lançamento](#6-checklist-de-lançamento)
7. [Volumetria e Escalabilidade](#7-volumetria-e-escalabilidade)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. CONFORMIDADE LGPD

### Dados Coletados e Finalidades

| Dado | Finalidade | Base Legal | Retenção |
|------|------------|------------|----------|
| Email | Autenticação, envio de resultados | Consentimento | Até cancelamento |
| Nome | Personalização de comunicação | Consentimento | Até cancelamento |
| Respostas do diagnóstico | Geração de relatório personalizado | Execução de contrato | 2 anos ou até exclusão |
| IP / Device info | Segurança, prevenção de fraude | Legítimo interesse | 90 dias |
| Cookies analíticos | Melhoria do serviço | Consentimento | 1 ano |
| UTM Parameters | Análise de marketing | Legítimo interesse | 90 dias |

### Endpoints de Direitos do Titular (LGPD)

```python
# api/v1/privacy.py
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.database import supabase
from datetime import datetime

router = APIRouter(prefix="/privacy", tags=["Privacy"])


@router.get("/my-data")
async def export_my_data(current_user: dict = Depends(get_current_user)):
    """
    Exporta todos os dados do usuário (LGPD Art. 18 - Portabilidade).
    """
    user_id = current_user["id"]
    email = current_user["email"]
    
    # Coletar todos os dados
    profile = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    diagnostics = supabase.table("diagnostics").select("*").eq("email", email).execute()
    
    diagnostic_ids = [d["id"] for d in diagnostics.data]
    
    answers = []
    results = []
    if diagnostic_ids:
        answers = supabase.table("answers").select("*").in_("diagnostic_id", diagnostic_ids).execute().data
        results = supabase.table("diagnostic_results").select("*").in_("diagnostic_id", diagnostic_ids).execute().data
    
    return {
        "export_date": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "data": {
            "profile": profile.data,
            "diagnostics": diagnostics.data,
            "answers": answers,
            "results": results
        }
    }


@router.delete("/my-data")
async def delete_my_data(confirm: bool = False, current_user: dict = Depends(get_current_user)):
    """
    Exclui todos os dados do usuário (LGPD Art. 18 - Eliminação).
    """
    if not confirm:
        raise HTTPException(status_code=400, detail="Confirmação necessária. Envie confirm=true.")
    
    user_id = current_user["id"]
    email = current_user["email"]
    
    # Buscar e deletar diagnósticos
    diagnostics = supabase.table("diagnostics").select("id").eq("email", email).execute()
    diagnostic_ids = [d["id"] for d in diagnostics.data]
    
    if diagnostic_ids:
        supabase.table("answers").delete().in_("diagnostic_id", diagnostic_ids).execute()
        supabase.table("diagnostic_results").delete().in_("diagnostic_id", diagnostic_ids).execute()
        supabase.table("diagnostics").delete().in_("id", diagnostic_ids).execute()
    
    # Deletar perfil
    supabase.table("profiles").delete().eq("id", user_id).execute()
    
    return {"status": "deleted", "deleted_at": datetime.utcnow().isoformat()}
```

### Consentimentos Pré-Diagnóstico

O usuário deve aceitar obrigatoriamente:
- **Termos de Uso** - Regras de utilização da plataforma
- **Política de Privacidade** - Como os dados serão tratados

E opcionalmente:
- **Comunicações de Marketing** - Receber novidades por email

---

## 2. MÉTRICAS DE SUCESSO

### KPIs do MVP

| Métrica | Definição | Meta Beta | Meta Lançamento | Prioridade |
|---------|-----------|-----------|-----------------|------------|
| **Taxa de Conclusão** | Diagnósticos finalizados / iniciados | >50% | >70% | P0 |
| **NPS** | Net Promoter Score | >50 | >70 | P0 |
| **Conversão Waitlist** | Inscritos / Diagnósticos completos | >40% | >60% | P1 |
| **Tempo Médio** | Minutos para completar | 15-25min | 12-20min | P1 |
| **Compartilhamento** | % que compartilha resultado | >10% | >25% | P2 |
| **Retenção D7** | Volta em 7 dias | >20% | >40% | P2 |
| **Reação Qualitativa** | Feedback textual | "interessante" | "wow", "revelador" | P0 |

### Views SQL para Métricas

```sql
-- Taxa de conclusão por período
CREATE OR REPLACE VIEW v_completion_rate AS
SELECT
    date_trunc('day', created_at) AS date,
    COUNT(*) AS total_started,
    COUNT(*) FILTER (WHERE status = 'completed') AS total_completed,
    ROUND(
        COUNT(*) FILTER (WHERE status = 'completed')::NUMERIC / 
        NULLIF(COUNT(*), 0) * 100, 2
    ) AS completion_rate_pct
FROM diagnostics
GROUP BY date_trunc('day', created_at)
ORDER BY date DESC;


-- NPS semanal
CREATE OR REPLACE VIEW v_weekly_nps AS
SELECT
    date_trunc('week', created_at) AS week,
    COUNT(*) AS total_responses,
    ROUND(AVG(nps_score)::NUMERIC, 1) AS avg_nps,
    ROUND(
        (COUNT(*) FILTER (WHERE nps_score >= 9)::NUMERIC - 
         COUNT(*) FILTER (WHERE nps_score <= 6)::NUMERIC) /
        NULLIF(COUNT(*), 0) * 100, 1
    ) AS nps_score
FROM feedback
WHERE nps_score IS NOT NULL
GROUP BY date_trunc('week', created_at)
ORDER BY week DESC;


-- Funil do diagnóstico
CREATE OR REPLACE VIEW v_diagnostic_funnel AS
WITH stages AS (
    SELECT
        id,
        CASE
            WHEN total_answers = 0 THEN '1_started'
            WHEN total_answers < 15 THEN '2_phase_1'
            WHEN total_answers < 30 THEN '3_phase_2'
            WHEN status = 'completed' THEN '4_completed'
            ELSE '3_in_progress'
        END AS stage
    FROM diagnostics
    WHERE created_at > NOW() - INTERVAL '30 days'
)
SELECT stage, COUNT(*) AS count
FROM stages
GROUP BY stage
ORDER BY stage;
```

---

## 3. TESTES E QUALIDADE

### Estrutura de Testes

```
tests/
├── unit/
│   ├── test_eligibility.py
│   ├── test_scoring.py
│   └── test_validators.py
├── integration/
│   ├── test_diagnostic_flow.py
│   └── test_rag_pipeline.py
├── e2e/
│   └── test_complete_diagnostic.py
└── conftest.py
```

### Testes Unitários

```python
# tests/unit/test_eligibility.py
import pytest
from app.rag.pipeline import NaraDiagnosticPipeline


class TestEligibility:
    def setup_method(self):
        self.pipeline = NaraDiagnosticPipeline()
    
    def test_not_eligible_with_few_answers(self):
        result = self.pipeline._check_eligibility(
            total_answers=30,
            total_words=2000,
            areas_covered=list(self.pipeline.AREAS)
        )
        assert result.can_finish is False
    
    def test_eligible_with_40_answers(self):
        result = self.pipeline._check_eligibility(
            total_answers=40,
            total_words=2000,
            areas_covered=list(self.pipeline.AREAS)
        )
        assert result.can_finish is True
    
    def test_eligible_with_3500_words(self):
        result = self.pipeline._check_eligibility(
            total_answers=35,
            total_words=3500,
            areas_covered=list(self.pipeline.AREAS)
        )
        assert result.can_finish is True
    
    def test_not_eligible_missing_areas(self):
        result = self.pipeline._check_eligibility(
            total_answers=40,
            total_words=4000,
            areas_covered=self.pipeline.AREAS[:10]
        )
        assert result.can_finish is False
        assert len(result.missing_areas) == 2
```

### Testes de Integração

```python
# tests/integration/test_diagnostic_flow.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestDiagnosticFlow:
    
    async def test_start_diagnostic(self, async_client: AsyncClient):
        response = await async_client.post(
            "/api/v1/diagnostic/start",
            json={
                "email": "test@example.com",
                "consent_privacy": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "diagnostic_id" in data
        assert len(data["questions"]) == 15
    
    async def test_submit_answer(self, async_client: AsyncClient, diagnostic_id: str):
        response = await async_client.post(
            f"/api/v1/diagnostic/{diagnostic_id}/answer",
            json={
                "question_id": 1,
                "question_text": "De 1 a 5, como você avalia sua energia?",
                "question_area": "Saúde Física",
                "answer_scale": 4
            }
        )
        
        assert response.status_code == 200
        assert response.json()["total_answers"] == 1
```

---

## 4. DEPLOY E INFRAESTRUTURA

### Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET                                │
└─────────────────────────────┬───────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│      VERCEL (CDN)       │     │     RAILWAY/RENDER      │
│    Frontend React       │────▶│    Backend FastAPI      │
└─────────────────────────┘     └───────────┬─────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                         SUPABASE                                │
│    PostgreSQL + pgvector    │    Auth    │    RLS               │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│       OPENAI API        │     │       RESEND API        │
└─────────────────────────┘     └─────────────────────────┘
```

### Dockerfile Backend

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

ENV PYTHONUNBUFFERED=1

RUN useradd -m appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variáveis de Ambiente

```bash
# .env.example

# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...

# OpenAI
OPENAI_API_KEY=sk-...

# Resend
RESEND_API_KEY=re_...
EMAIL_FROM=nara@seudominio.com

# App
APP_NAME=NARA
ENV=production
DEBUG=false
FRONTEND_URL=https://nara.app

# Diagnóstico
MIN_QUESTIONS_TO_FINISH=40
MIN_WORDS_TO_FINISH=3500
MIN_AREAS_COVERED=12

# CORS
CORS_ORIGINS=["https://nara.app"]
```

---

## 5. MONITORAMENTO

### Health Checks

```python
# app/api/health.py
from fastapi import APIRouter
from app.database import supabase
from app.config import settings
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


@router.get("/health/detailed")
async def health_detailed():
    checks = {}
    
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

### Alertas Críticos

| Alerta | Condição | Severidade | Ação |
|--------|----------|------------|------|
| Taxa de erro alta | >5% de 5xx em 5min | P1 | Notificar Slack |
| Latência alta | p95 > 5s por 10min | P2 | Notificar Slack |
| Taxa de conclusão baixa | <30% em 24h | P3 | Notificar email |
| Custo OpenAI alto | >$50/dia | P3 | Notificar email |

---

## 6. CHECKLIST DE LANÇAMENTO

### ✅ Pré-Lançamento

#### Código
- [ ] Todos os testes passando
- [ ] Code review completo
- [ ] Sem secrets hardcoded
- [ ] Linting sem erros

#### Infraestrutura
- [ ] SSL configurado (HTTPS)
- [ ] DNS propagado
- [ ] Backups configurados
- [ ] Rate limiting ativo

#### Segurança
- [ ] RLS testado em todas as tabelas
- [ ] CORS configurado
- [ ] Headers de segurança ativos

#### LGPD
- [ ] Banner de cookies implementado
- [ ] Política de privacidade publicada
- [ ] Termos de uso publicados
- [ ] Endpoints de direitos funcionando

#### Monitoramento
- [ ] Logs estruturados configurados
- [ ] Alertas configurados
- [ ] Health checks funcionando

#### Conteúdo
- [ ] Perguntas baseline revisadas
- [ ] Chunks de conhecimento populados
- [ ] Prompts de LLM testados
- [ ] Templates de email testados

### ✅ Lançamento

- [ ] Deploy frontend (Vercel)
- [ ] Deploy backend (Railway)
- [ ] Verificar health checks
- [ ] Teste de fumaça manual
- [ ] Verificar envio de emails
- [ ] Verificar geração de relatório

### ✅ Pós-Lançamento

- [ ] Monitorar métricas (1h)
- [ ] Verificar logs por erros
- [ ] Coletar primeiros feedbacks
- [ ] Verificar custos OpenAI

---

## 7. VOLUMETRIA E ESCALABILIDADE

### Estimativas de Volume

| Período | Usuários | Diagnósticos | Respostas | Custo OpenAI |
|---------|----------|--------------|-----------|--------------|
| Beta (1 mês) | 30 | 30 | 1.500 | R$ 6 |
| Validação (3 meses) | 500 | 700 | 35.000 | R$ 130 |
| Escala (12 meses) | 10.000 | 15.000 | 750.000 | R$ 2.700 |

### Limites e Quotas

| Recurso | Limite Free | Limite Pago |
|---------|-------------|-------------|
| Supabase DB | 500MB | 8GB+ |
| Supabase Auth | 50k MAU | Unlimited |
| Vercel Bandwidth | 100GB | 1TB+ |
| OpenAI RPM | 3 | 3500+ |
| Resend Emails | 100/dia | 50k/mês |

---

## 8. TROUBLESHOOTING

### Problema: Diagnóstico não finaliza

**Sintomas:** Botão "Finalizar" não aparece ou retorna erro.

**Checklist:**
1. Verificar total de respostas (≥40 ou ≥3500 palavras)
2. Verificar cobertura das 12 áreas
3. Verificar status do diagnóstico no banco
4. Verificar logs do backend por erros

**SQL de diagnóstico:**
```sql
SELECT id, status, total_answers, total_words, array_length(areas_covered, 1) as areas
FROM diagnostics WHERE id = 'xxx';
```

### Problema: Perguntas não são geradas

**Sintomas:** Fase 2+ não carrega perguntas.

**Checklist:**
1. Verificar conexão com OpenAI (health check)
2. Verificar se há chunks no banco de conhecimento
3. Verificar logs por erros de timeout
4. Verificar rate limits da OpenAI

### Problema: Email não chega

**Sintomas:** Usuário não recebe email com resultado.

**Checklist:**
1. Verificar tabela `email_logs` por status
2. Verificar configuração do Resend
3. Verificar se email está em spam
4. Verificar domínio de envio (SPF, DKIM)

**SQL de diagnóstico:**
```sql
SELECT * FROM email_logs 
WHERE recipient_email = 'xxx@email.com' 
ORDER BY created_at DESC;
```

### Problema: RAG retorna chunks irrelevantes

**Sintomas:** Perguntas ou relatório não fazem sentido.

**Checklist:**
1. Verificar qualidade dos embeddings
2. Verificar threshold de similaridade
3. Verificar se chunks têm metadados corretos
4. Testar query manualmente

**SQL para testar RAG:**
```sql
SELECT content, 1 - (embedding <=> '[vetor]') as similarity
FROM knowledge_chunks
WHERE is_active = true
ORDER BY embedding <=> '[vetor]'
LIMIT 5;
```

---

**Referências Cruzadas:**
- Schema do banco: [02_BANCO_DADOS.md](./02_BANCO_DADOS.md)
- Backend e API: [04_BACKEND_API.md](./04_BACKEND_API.md)
- Sistema de email: [06_OPERACOES_EMAIL.md](./06_OPERACOES_EMAIL.md)
