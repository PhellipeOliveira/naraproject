# Status do Supabase - Alinhamento com Backend

> **Última verificação:** 2026-02-17

---

## 📊 Resumo Executivo

### ❓ Preciso aplicar migrations?

**Resposta:** Depende de quais migrations você já aplicou no Supabase.

### ✅ O Supabase está alinhado com o backend?

**Resposta:** **SIM**, desde que as migrations necessárias estejam aplicadas.

---

## 🗂️ Migrations Disponíveis (Ordem Cronológica)

### ✅ Migrations Essenciais (Provavelmente já aplicadas)

| # | Arquivo | Descrição | Status Estimado |
|---|---------|-----------|-----------------|
| 1 | `20260213000001_nara_extensions.sql` | Habilita pgvector | ✅ Aplicada |
| 2 | `20260213000002_nara_tables.sql` | Cria todas as tabelas principais | ✅ Aplicada |
| 3 | `20260213000003_nara_rpc.sql` | Cria funções RPC (match_knowledge_chunks) | ✅ Aplicada |
| 4 | `20260213000004_nara_rls.sql` | Configura Row Level Security | ✅ Aplicada |
| 5 | `20260213000005_nara_chunks_vector_index.sql` | Índice vetorial para busca | ✅ Aplicada |
| 6 | `20260213000006_nara_views_metrics.sql` | Views básicas (completion, nps, funnel) | ✅ Aplicada |

### 🔄 Migrations Recentes (Fase 2 - V2)

| # | Arquivo | Descrição | Status | Ação |
|---|---------|-----------|--------|------|
| 7 | `20260216000001_match_knowledge_chunks_filter_chunk_strategy.sql` | Adiciona filtro `chunk_strategy` | ⚠️ Verificar | **Aplicar se ainda não** |
| 8 | `20260216000002_diagnostics_current_phase_questions_count.sql` | Campo `current_phase_questions_count` | ⚠️ Verificar | Verificar se existe |
| 9 | `20260216000003_diagnostics_current_phase_questions.sql` | Campo `current_phase_questions` | ⚠️ Verificar | Verificar se existe |
| 10 | `20260217000001_knowledge_chunks_v2.sql` | Schema V2: renomeia `sintomas` → `sintomas_comportamentais` | ⚠️ Verificar | **Aplicar se ainda não** |
| 11 | `20260217000002_diagnostic_results_v2.sql` | Campos V2: vetor_estado, memorias_vermelhas, etc | ⚠️ Verificar | **Aplicar se ainda não** |
| 12 | `20260217000003_diagnostics_adjust.sql` | Ajustes em diagnostics | ⚠️ Verificar | Verificar se existe |
| 13 | `20260217000004_metrics_views_extended.sql` | Views estendidas (tempo médio, áreas, abandono) | ⚠️ Opcional | **Aplicar para analytics completo** |
| 14 | `20260217000005_analytics_tables.sql` | Tabelas de analytics (events, metrics, views) | ⚠️ Verificar | **Aplicar se quiser dashboard** |

---

## 🎯 Migrations Críticas vs Opcionais

### 🔴 **CRÍTICAS** (Backend depende delas)

1. ✅ **20260213000001-000005**: Setup inicial (pgvector, tabelas, RPC, RLS)
2. ⚠️ **20260216000001**: Filtro `chunk_strategy` (usado pelo retriever atual)
3. ⚠️ **20260217000001**: Schema V2 de `knowledge_chunks` (backend usa `sintomas_comportamentais`)
4. ⚠️ **20260217000002_diagnostic_results_v2**: Campos V2 (vetor_estado, etc)

### 🟡 **IMPORTANTES** (Funcionalidades V2)

5. ⚠️ **20260217000002_analytics_tables**: Analytics e dashboard
6. ⚠️ **20260217000003_diagnostics_adjust**: Ajustes para V2

### 🟢 **OPCIONAIS** (Melhorias)

7. ⚠️ **20260213000006**: Views básicas de métricas (já aplicada provavelmente)
8. ⚠️ **20260217000004**: Views estendidas (opcional, para analytics)
9. ⚠️ **20260216000002-000003**: Campos auxiliares (current_phase_questions)

---

## 🔍 Como Verificar o que está Aplicado

### Opção 1: Via Supabase Dashboard

1. Acesse: https://supabase.com/dashboard/project/mxqzlqyioqdnoexvttys
2. Vá em: **Database** > **Migrations** (ou **SQL Editor**)
3. Verifique a lista de migrations aplicadas

### Opção 2: Via SQL

Execute no **SQL Editor** do Supabase:

```sql
-- Verificar se pgvector está instalado
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Verificar se tabelas principais existem
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN (
    'diagnostics', 
    'diagnostic_results', 
    'knowledge_chunks', 
    'answers', 
    'analytics_events',
    'analytics_metrics'
  )
ORDER BY table_name;

-- Verificar se função RPC existe (crítica!)
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_schema = 'public' 
  AND routine_name = 'match_knowledge_chunks';

-- Verificar se campo V2 existe em knowledge_chunks
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'knowledge_chunks' 
  AND column_name IN ('sintomas', 'sintomas_comportamentais', 'nivel_maturidade', 'subtipo_crise');

-- Verificar se views de métricas existem
SELECT table_name 
FROM information_schema.views 
WHERE table_schema = 'public' 
  AND table_name LIKE 'v_%'
ORDER BY table_name;
```

---

## 🚀 Plano de Ação Recomendado

### 1️⃣ **Verificar Estado Atual**

```sql
-- Copiar e executar no SQL Editor do Supabase
-- (queries acima)
```

### 2️⃣ **Aplicar Migrations Faltantes (se necessário)**

Se a verificação mostrar que falta algo, aplicar na ordem:

#### A. Migrations Críticas V2

```sql
-- 1. Filtro chunk_strategy (se ainda não aplicado)
-- Copiar e executar: supabase/migrations/20260216000001_match_knowledge_chunks_filter_chunk_strategy.sql

-- 2. Schema V2 knowledge_chunks
-- Copiar e executar: supabase/migrations/20260217000001_knowledge_chunks_v2.sql

-- 3. Schema V2 diagnostic_results
-- Copiar e executar: supabase/migrations/20260217000002_diagnostic_results_v2.sql
```

#### B. Analytics (se quiser dashboard)

```sql
-- Tabelas de analytics
-- Copiar e executar: supabase/migrations/20260217000002_analytics_tables.sql

-- Views estendidas (opcional)
-- Copiar e executar: supabase/migrations/20260217000004_metrics_views_extended.sql
```

### 3️⃣ **Validar Alinhamento Backend ↔ Supabase**

Execute este teste no backend:

```bash
cd nara-backend
source .venv/bin/activate

# Teste 1: Health check detalhado
curl http://localhost:8000/health/detailed

# Teste 2: Verificar retriever
python -c "
from app.rag.retriever import retrieve_relevant_chunks
import asyncio

async def test():
    chunks = await retrieve_relevant_chunks(
        query='Qual meu propósito?',
        top_k=3,
        filter_chunk_strategy='semantic'
    )
    print(f'Chunks encontrados: {len(chunks)}')

asyncio.run(test())
"

# Teste 3: Verificar ingest
python -m scripts.ingest_docs_rag --strategy semantic --dry-run
```

---

## 📝 Checklist de Validação

Use este checklist para confirmar que está tudo alinhado:

- [ ] Extension `vector` instalada (pgvector)
- [ ] Tabela `diagnostics` existe
- [ ] Tabela `diagnostic_results` existe com campos V2 (`vetor_estado`, etc)
- [ ] Tabela `knowledge_chunks` existe com `sintomas_comportamentais` (não `sintomas`)
- [ ] Tabela `answers` existe
- [ ] Função `match_knowledge_chunks` existe e aceita `filter_chunk_strategy`
- [ ] Tabelas de analytics existem (`analytics_events`, `analytics_metrics`)
- [ ] Views de métricas existem (`v_completion_rate`, `v_diagnostic_funnel`)
- [ ] Chunks populados (`SELECT COUNT(*) FROM knowledge_chunks WHERE is_active = true`)
- [ ] Backend conecta sem erros (`/health/detailed` retorna "healthy")
- [ ] Retriever funciona (`retrieve_relevant_chunks` retorna resultados)

---

## ⚠️ Problemas Conhecidos

### Problema 1: Conflito de Timestamps

**Status:** ✅ **RESOLVIDO**

Havia migrations duplicadas com mesmo timestamp:
- `20260217000003_diagnostics_adjust.sql`
- `20260217000003_metrics_views.sql` ❌

**Solução:** Renomeada para `20260217000004_metrics_views_extended.sql` ✅

### Problema 2: Migrations Duplicadas

**Status:** ⚠️ **ATENÇÃO**

Há 2 migrations com timestamp `20260217000002`:
- `20260217000002_analytics_tables.sql` (15:33)
- `20260217000002_diagnostic_results_v2.sql` (10:32)

Ambas são **válidas e necessárias**, mas podem causar problemas de ordem.

**Recomendação:** Aplicar na ordem correta:
1. Primeiro: `diagnostic_results_v2.sql` (schema)
2. Depois: `analytics_tables.sql` (tabelas novas)

---

## 🎯 Conclusão

### Para sua pergunta: "Preciso aplicar?"

**Responda:**

1. Execute a query de verificação (Seção 2, Opção 2)
2. Se faltar algo do checklist → **SIM, aplicar**
3. Se tudo existir → **NÃO precisa**

### Para sua pergunta: "Supabase está alinhado?"

**SIM**, o código do backend está alinhado com as migrations disponíveis.

Porém, você precisa **aplicar as migrations que ainda não estão no seu Supabase**.

---

**Próximo passo:** Execute a query de verificação e me informe o resultado! 🚀
