# 02 - BANCO DE DADOS

> **Propósito:** Esquema completo do banco de dados, modelo de dados normalizado e políticas de segurança (RLS) para o sistema NARA.

---

## 📋 ÍNDICE

1. [Visão Geral da Arquitetura](#1-visão-geral-da-arquitetura)
2. [Schema Completo (DDL)](#2-schema-completo-ddl)
3. [Descrição Detalhada das Tabelas](#3-descrição-detalhada-das-tabelas)
4. [Funções RPC para RAG](#4-funções-rpc-para-rag)
5. [Políticas RLS (Row Level Security)](#5-políticas-rls-row-level-security)
6. [Diagrama de Relacionamentos](#6-diagrama-de-relacionamentos)
7. [Normalização Formal (1FN→5FN)](#7-normalização-formal-1fn5fn)
8. [Estratégia de Chunks para RAG](#8-estratégia-de-chunks-para-rag)
9. [Volumetria e Performance](#9-volumetria-e-performance)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. VISÃO GERAL DA ARQUITETURA

### Tecnologias

| Componente | Tecnologia | Finalidade |
|----|----|----|
| Banco Principal | Supabase PostgreSQL 15+ | Dados transacionais |
| Extensão Vetorial | pgvector | Busca semântica para RAG |
| Autenticação | Supabase Auth | JWT, magic links |
| Segurança | Row Level Security | Isolamento por usuário |

### Princípios de Design

1. **Normalização adequada:** Cada entidade tem sua tabela, sem duplicação
2. **UUID everywhere:** Identificadores únicos universais para todas PKs
3. **Flexibilidade:** JSONB para dados semi-estruturados (scores, metadata)
4. **Auditoria completa:** Campos `created_at` e `updated_at` em todas as tabelas
5. **RLS obrigatório:** Políticas definidas para cada tabela com dados sensíveis
6. **Chunks com metadados:** Estrutura rica para inteligência contextual

---

## 2. SCHEMA COMPLETO (DDL)

### Extensões Necessárias

```sql
-- ====
-- SCHEMA COMPLETO - NARA (Diagnóstico de Transformação Narrativa)
-- ====
-- Database: Supabase (PostgreSQL 15+)
-- Versão: 1.0
-- ====

-- Habilitar extensões
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Para busca textual fuzzy
```

### Tabela: profiles

```sql
-- ====
-- TABELA: profiles
-- Extensão de auth.users do Supabase
-- ====
CREATE TABLE public.profiles (
    -- Identidade
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Dados básicos
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    phone TEXT,
    
    -- Consentimentos LGPD
    accepted_terms BOOLEAN DEFAULT FALSE,
    accepted_privacy BOOLEAN DEFAULT FALSE,
    marketing_consent BOOLEAN DEFAULT FALSE,
    
    -- Preferências
    preferences JSONB DEFAULT '{
        "emailNotifications": true,
        "shareData": true,
        "language": "pt-BR"
    }'::JSONB,
    
    -- Metadados de aquisição
    acquisition_channel TEXT DEFAULT 'organic',
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT,
    referrer_code TEXT,
    referred_by UUID REFERENCES profiles(id),
    
    -- Contadores
    total_diagnostics INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    
    -- Constraints
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Comentários
COMMENT ON TABLE profiles IS 'Perfis de usuário estendendo auth.users do Supabase';
COMMENT ON COLUMN profiles.preferences IS 'Preferências do usuário em formato JSON';
COMMENT ON COLUMN profiles.referrer_code IS 'Código único para programa de indicação';

-- Índices
CREATE INDEX idx_profiles_email ON profiles(email);
CREATE INDEX idx_profiles_created_at ON profiles(created_at);
CREATE INDEX idx_profiles_referrer ON profiles(referrer_code);
```

### Tabela: diagnostics

```sql
-- ====
-- TABELA: diagnostics
-- Sessões de diagnóstico
-- ====
CREATE TABLE public.diagnostics (
    -- Identidade
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    
    -- Sessão anônima (pré-login)
    anonymous_session_id TEXT,
    
    -- Dados de identificação
    email TEXT NOT NULL,
    full_name TEXT,
    
    -- Estado atual
    status TEXT NOT NULL DEFAULT 'in_progress'
        CHECK (status IN ('in_progress', 'eligible', 'processing', 'completed', 'abandoned', 'failed')),
    current_phase INTEGER DEFAULT 1 CHECK (current_phase BETWEEN 1 AND 4),
    current_question INTEGER DEFAULT 0,
    
    -- Contadores de progresso
    total_answers INTEGER DEFAULT 0,
    total_words INTEGER DEFAULT 0,
    areas_covered SMALLINT[] DEFAULT ARRAY[]::SMALLINT[],
    
    -- Token de acesso ao resultado
    result_token TEXT UNIQUE,
    
    -- Consentimentos
    consent_privacy BOOLEAN DEFAULT FALSE,
    consent_marketing BOOLEAN DEFAULT FALSE,
    
    -- Scores calculados (JSONB para flexibilidade)
    overall_score DECIMAL(3,1),
    scores_by_area JSONB DEFAULT '{}',
    crisis_areas JSONB DEFAULT '[]',
    insights TEXT,
    
    -- URLs de arquivos gerados
    radar_chart_url TEXT,
    pdf_url TEXT,
    
    -- Metadados de rastreamento
    ip_address INET,
    user_agent TEXT,
    referrer TEXT,
    utm_source TEXT,
    utm_campaign TEXT,
    device_info JSONB DEFAULT '{}',
    
    -- Timestamps de interação
    started_at TIMESTAMPTZ DEFAULT NOW(),
    last_activity_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_progress CHECK (
        total_answers >= 0 AND
        total_words >= 0 AND
        current_question >= 0
    ),
    CONSTRAINT session_or_user CHECK (
        user_id IS NOT NULL OR anonymous_session_id IS NOT NULL OR email IS NOT NULL
    )
);

-- Comentários
COMMENT ON TABLE diagnostics IS 'Sessões de diagnóstico de transformação narrativa';
COMMENT ON COLUMN diagnostics.result_token IS 'Token único para acesso público ao resultado';
COMMENT ON COLUMN diagnostics.scores_by_area IS 'Scores das 12 áreas em formato {area_id: {score, count}}';
COMMENT ON COLUMN diagnostics.crisis_areas IS 'Lista das áreas identificadas como críticas';

-- Índices
CREATE INDEX idx_diagnostics_user ON diagnostics(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_diagnostics_anonymous ON diagnostics(anonymous_session_id) WHERE anonymous_session_id IS NOT NULL;
CREATE INDEX idx_diagnostics_email ON diagnostics(email);
CREATE INDEX idx_diagnostics_status ON diagnostics(status);
CREATE INDEX idx_diagnostics_token ON diagnostics(result_token) WHERE result_token IS NOT NULL;
CREATE INDEX idx_diagnostics_created ON diagnostics(created_at);
CREATE INDEX idx_diagnostics_activity ON diagnostics(last_activity_at);
```

### Tabela: answers

```sql
-- ====
-- TABELA: answers
-- Respostas dos usuários
-- ====
CREATE TABLE public.answers (
    -- Identidade
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    diagnostic_id UUID NOT NULL REFERENCES diagnostics(id) ON DELETE CASCADE,
    
    -- Dados da pergunta (desnormalizado intencionalmente para perguntas RAG dinâmicas)
    question_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_area TEXT NOT NULL,
    question_phase INTEGER NOT NULL,
    
    -- Conteúdo da resposta
    answer_value JSONB NOT NULL,  -- {text: "...", scale: 0-5, words: count}
    word_count INTEGER DEFAULT 0,
    
    -- Metadados de qualidade
    response_time_seconds INTEGER,
    
    -- Análise automática (preenchido por LLM)
    sentiment_score DECIMAL(3,2),       -- -1 a 1
    key_themes TEXT[],                  -- Temas extraídos
    
    -- Timestamps
    answered_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT unique_answer_per_question UNIQUE (diagnostic_id, question_id)
);

-- Comentários
COMMENT ON TABLE answers IS 'Respostas do diagnóstico com dados da pergunta embutidos';
COMMENT ON COLUMN answers.answer_value IS 'Estrutura: {text: string, scale: number|null, words: number}';
COMMENT ON COLUMN answers.question_area IS 'Uma das 12 áreas estruturantes ou categorias especiais';

-- Índices
CREATE INDEX idx_answers_diagnostic ON answers(diagnostic_id);
CREATE INDEX idx_answers_area ON answers(question_area);
CREATE INDEX idx_answers_phase ON answers(question_phase);
CREATE INDEX idx_answers_answered ON answers(answered_at);

-- Trigger para word_count automático
CREATE OR REPLACE FUNCTION calculate_word_count()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.answer_value->>'text' IS NOT NULL THEN
        NEW.word_count := array_length(
            regexp_split_to_array(trim(NEW.answer_value->>'text'), '\s+'), 1
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calculate_answer_word_count
    BEFORE INSERT OR UPDATE ON answers
    FOR EACH ROW EXECUTE FUNCTION calculate_word_count();
```

### Tabela: knowledge_chunks

```sql
-- ====
-- TABELA: knowledge_chunks
-- Base de conhecimento para RAG com metadados ricos
-- ====
CREATE TABLE public.knowledge_chunks (
    -- Identidade
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Classificação principal
    chapter TEXT NOT NULL,              -- Ex: "Saúde Física", "Vida Profissional"
    section TEXT,                       -- Ex: "Fundamentos Narrativos", "Diagnóstico M1"
    
    -- Conteúdo
    content TEXT NOT NULL,
    
    -- Vetor de embedding
    embedding VECTOR(1536),             -- OpenAI text-embedding-3-small
    
    -- Metadados para Inteligência Contextual (estrutura rica)
    metadata JSONB DEFAULT '{}'::JSONB,
    
    -- Campos de metadados indexáveis
    motor_motivacional TEXT[],          -- ['Necessidade', 'Valor', 'Desejo', 'Propósito']
    estagio_jornada TEXT[],             -- ['Germinar', 'Enraizar', ...]
    tipo_crise TEXT[],                  -- ['Identidade', 'Sentido', 'Execução', ...]
    ponto_entrada TEXT,                 -- 'Simbólico', 'Cognitivo', 'Comportamental', ...
    sintomas TEXT[],                    -- ['autossabotagem', 'paralisia', ...]
    tom_emocional TEXT,                 -- 'vergonha', 'indignação', 'apatia', ...
    
    -- Métricas
    token_count INTEGER,
    
    -- Estado
    is_active BOOLEAN DEFAULT TRUE,
    version INTEGER DEFAULT 1,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Comentários
COMMENT ON TABLE knowledge_chunks IS 'Chunks de conhecimento para RAG com metadados de inteligência contextual';
COMMENT ON COLUMN knowledge_chunks.metadata IS 'Metadados completos: {motor, estagio, crise, sintomas, tom, nivel_maturidade}';
COMMENT ON COLUMN knowledge_chunks.embedding IS 'Vetor de 1536 dimensões do text-embedding-3-small';

-- Índice vetorial (IVF para performance)
CREATE INDEX idx_chunks_embedding ON knowledge_chunks 
    USING ivfflat (embedding vector_cosine_ops) 
    WITH (lists = 100);

-- Índices tradicionais
CREATE INDEX idx_chunks_chapter ON knowledge_chunks(chapter);
CREATE INDEX idx_chunks_active ON knowledge_chunks(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_chunks_motor ON knowledge_chunks USING GIN (motor_motivacional);
CREATE INDEX idx_chunks_estagio ON knowledge_chunks USING GIN (estagio_jornada);
CREATE INDEX idx_chunks_crise ON knowledge_chunks USING GIN (tipo_crise);
CREATE INDEX idx_chunks_metadata ON knowledge_chunks USING GIN (metadata);
```

### Tabela: diagnostic_results

```sql
-- ====
-- TABELA: diagnostic_results
-- Resultados finais dos diagnósticos
-- ====
CREATE TABLE public.diagnostic_results (
    -- Identidade
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    diagnostic_id UUID UNIQUE NOT NULL REFERENCES diagnostics(id) ON DELETE CASCADE,
    
    -- Scores finais normalizados (0-10)
    overall_score DECIMAL(3,1),
    area_scores JSONB NOT NULL DEFAULT '{}',     -- {area_id: score}
    motor_scores JSONB NOT NULL DEFAULT '{}',    -- {motor_id: score}
    phase_identified TEXT,                       -- Fase da jornada detectada
    
    -- Diagnóstico M1 identificado
    motor_dominante TEXT,
    motor_secundario TEXT,
    crise_raiz TEXT,
    crises_derivadas TEXT[],
    ponto_entrada_ideal TEXT,
    dominios_alavanca TEXT[],
    
    -- Conteúdo do relatório
    executive_summary TEXT NOT NULL,              -- Resumo executivo
    detailed_analysis JSONB NOT NULL DEFAULT '{}',-- Análise por área
    recommendations JSONB NOT NULL DEFAULT '[]',  -- Recomendações
    strengths TEXT[] DEFAULT '{}',               -- Pontos fortes
    opportunities TEXT[] DEFAULT '{}',           -- Oportunidades
    
    -- Metadados de geração
    model_used TEXT DEFAULT 'gpt-4o',
    tokens_used INTEGER,
    generation_time_ms INTEGER,
    
    -- Timestamps
    generated_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Comentários
COMMENT ON TABLE diagnostic_results IS 'Relatórios finais gerados pelo sistema';
COMMENT ON COLUMN diagnostic_results.motor_dominante IS 'Motor motivacional principal: Necessidade, Valor, Desejo ou Propósito';
COMMENT ON COLUMN diagnostic_results.phase_identified IS 'Fase da jornada: Germinar, Enraizar, Desenvolver, Florescer, Frutificar, Realizar';

-- Índices
CREATE INDEX idx_results_diagnostic ON diagnostic_results(diagnostic_id);
CREATE INDEX idx_results_generated ON diagnostic_results(generated_at);
```

### Tabela: feedback

```sql
-- ====
-- TABELA: feedback
-- Feedback NPS e qualitativo
-- ====
CREATE TABLE public.feedback (
    -- Identidade
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    diagnostic_id UUID REFERENCES diagnostics(id) ON DELETE CASCADE,
    user_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    
    -- NPS e ratings
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    nps_score INTEGER CHECK (nps_score BETWEEN 0 AND 10),
    
    -- Feedback qualitativo
    feedback_text TEXT,
    feedback_type TEXT CHECK (feedback_type IN ('public', 'private')),
    
    -- Feedback específico
    accuracy_rating INTEGER CHECK (accuracy_rating BETWEEN 1 AND 5),
    relevance_rating INTEGER CHECK (relevance_rating BETWEEN 1 AND 5),
    clarity_rating INTEGER CHECK (clarity_rating BETWEEN 1 AND 5),
    
    -- Tags automáticas
    tags TEXT[] DEFAULT '{}',
    is_published BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_feedback_diagnostic ON feedback(diagnostic_id);
CREATE INDEX idx_feedback_nps ON feedback(nps_score);
CREATE INDEX idx_feedback_created ON feedback(created_at);
```

### Tabela: waitlist

```sql
-- ====
-- TABELA: waitlist
-- Lista de espera para features futuras
-- ====
CREATE TABLE public.waitlist (
    -- Identidade
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Dados
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    
    -- Fonte
    diagnostic_id UUID REFERENCES diagnostics(id) ON DELETE SET NULL,
    source TEXT DEFAULT 'diagnostic',
    referrer TEXT,
    
    -- Estado
    status TEXT DEFAULT 'pending' 
        CHECK (status IN ('pending', 'invited', 'converted')),
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    invited_at TIMESTAMPTZ,
    converted_at TIMESTAMPTZ,
    
    -- UTMs
    utm_source TEXT,
    
    -- Constraints
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Índices
CREATE INDEX idx_waitlist_email ON waitlist(email);
CREATE INDEX idx_waitlist_status ON waitlist(status);
CREATE INDEX idx_waitlist_created ON waitlist(created_at);
```

### Tabela: email_logs

```sql
-- ====
-- TABELA: email_logs
-- Auditoria de emails enviados
-- ====
CREATE TABLE public.email_logs (
    -- Identidade
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Destinatário
    recipient_email TEXT NOT NULL,
    diagnostic_id UUID REFERENCES diagnostics(id) ON DELETE SET NULL,
    user_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    
    -- Conteúdo
    email_type TEXT NOT NULL,
    subject TEXT NOT NULL,
    template_id TEXT,
    
    -- Status
    status TEXT DEFAULT 'queued' 
        CHECK (status IN ('queued', 'sent', 'delivered', 'opened', 'clicked', 'bounced', 'failed')),
    
    -- Metadados do provedor
    provider TEXT DEFAULT 'resend',
    resend_id TEXT,
    
    -- Tracking
    sent_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    opened_at TIMESTAMPTZ,
    clicked_at TIMESTAMPTZ,
    
    -- Erros
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_email_logs_recipient ON email_logs(recipient_email);
CREATE INDEX idx_email_logs_diagnostic ON email_logs(diagnostic_id);
CREATE INDEX idx_email_logs_type ON email_logs(email_type);
CREATE INDEX idx_email_logs_status ON email_logs(status);
CREATE INDEX idx_email_logs_created ON email_logs(created_at);
```

### Tabela: areas (Referência)

```sql
-- ====
-- TABELA: areas
-- Referência das 12 áreas estruturantes
-- ====
CREATE TABLE public.areas (
    id SMALLINT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    color TEXT,
    display_order SMALLINT
);

-- Popular com as 12 áreas
INSERT INTO areas (id, name, description, icon, color, display_order) VALUES
(1, 'Saúde Física', 'Manutenção da constituição física e disposição corporal', '💪', '#22c55e', 1),
(2, 'Saúde Mental', 'Equilíbrio das funções cognitivas e gestão das emoções', '🧠', '#8b5cf6', 2),
(3, 'Saúde Espiritual', 'Força da fé e convicção interior', '✨', '#f59e0b', 3),
(4, 'Vida Pessoal', 'Autoconhecimento e descoberta da própria essência', '🪞', '#ec4899', 4),
(5, 'Vida Amorosa', 'Relacionamentos íntimos e dedicação entre parceiros', '❤️', '#ef4444', 5),
(6, 'Vida Familiar', 'Vínculos de parentesco e valores morais', '👨‍👩‍👧‍👦', '#06b6d4', 6),
(7, 'Vida Social', 'Interações comunitárias e prestígio social', '👥', '#3b82f6', 7),
(8, 'Vida Profissional', 'Atuação produtiva e desenvolvimento da carreira', '💼', '#6366f1', 8),
(9, 'Finanças', 'Gestão do capital econômico e recursos materiais', '💰', '#10b981', 9),
(10, 'Educação', 'Busca contínua por conhecimento e aperfeiçoamento', '📚', '#f97316', 10),
(11, 'Inovação', 'Criatividade e desenvolvimento de novas ideias', '💡', '#a855f7', 11),
(12, 'Lazer', 'Entretenimento, hobbies e recuperação de energia', '🎮', '#14b8a6', 12);
```

### Trigger para updated_at

```sql
-- ====
-- TRIGGER: Atualização automática de updated_at
-- ====
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar em todas as tabelas relevantes
CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_diagnostics_updated_at
    BEFORE UPDATE ON diagnostics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_knowledge_chunks_updated_at
    BEFORE UPDATE ON knowledge_chunks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_email_logs_updated_at
    BEFORE UPDATE ON email_logs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## 3. DESCRIÇÃO DETALHADA DAS TABELAS

### Resumo das Tabelas

| Tabela | Propósito | Registros Estimados |
|----|----|----|
| `profiles` | Dados de usuário e consentimento | 1 por usuário |
| `diagnostics` | Sessões de diagnóstico | 1-3 por usuário |
| `answers` | Respostas dos usuários | 40-60 por diagnóstico |
| `diagnostic_results` | Relatórios gerados | 1 por diagnóstico completo |
| `knowledge_chunks` | Base de conhecimento RAG | ~500 chunks |
| `feedback` | Feedback NPS/qualitativo | 1 por diagnóstico |
| `waitlist` | Lista de espera | Crescente |
| `email_logs` | Auditoria de emails | 2-5 por usuário |
| `areas` | Referência das 12 áreas | 12 (fixo) |

### Campos JSONB Detalhados

#### diagnostics.scores_by_area
```json
{
  "Saúde Física": {"score": 7.2, "questions_answered": 4, "avg_sentiment": 0.3},
  "Saúde Mental": {"score": 4.5, "questions_answered": 3, "avg_sentiment": -0.2},
  "Vida Profissional": {"score": 6.8, "questions_answered": 5, "avg_sentiment": 0.1}
}
```

#### answers.answer_value
```json
{
  "text": "Resposta textual do usuário...",
  "scale": 4,
  "words": 87
}
```

#### knowledge_chunks.metadata
```json
{
  "motor_motivacional": ["Necessidade", "Valor"],
  "estagio_jornada": ["Germinar", "Enraizar"],
  "tipo_crise": "Identidade",
  "subtipo_crise": "Identidade Herdada",
  "dominio": "D1",
  "ponto_entrada": "Simbólico",
  "sintomas_comportamentais": ["autossabotagem", "paralisia decisória"],
  "tom_emocional_base": "vergonha",
  "nivel_maturidade": "baixo",
  "source": "metodologia_phellipe_oliveira",
  "version": "1.0"
}
```

---

## 4. FUNÇÕES RPC PARA RAG

### Busca por Similaridade (match_knowledge_chunks)

```sql
-- ====
-- FUNCTION: match_knowledge_chunks
-- Busca semântica com filtros de metadados
-- ====
CREATE OR REPLACE FUNCTION match_knowledge_chunks(
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.5,
    match_count INT DEFAULT 10,
    filter_chapter TEXT DEFAULT NULL,
    filter_motor TEXT[] DEFAULT NULL,
    filter_estagio TEXT[] DEFAULT NULL,
    filter_crise TEXT[] DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    chapter TEXT,
    section TEXT,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        k.id,
        k.chapter,
        k.section,
        k.content,
        k.metadata,
        1 - (k.embedding <=> query_embedding) AS similarity
    FROM knowledge_chunks k
    WHERE k.is_active = TRUE
        AND 1 - (k.embedding <=> query_embedding) > match_threshold
        AND (filter_chapter IS NULL OR k.chapter = filter_chapter)
        AND (filter_motor IS NULL OR k.motor_motivacional && filter_motor)
        AND (filter_estagio IS NULL OR k.estagio_jornada && filter_estagio)
        AND (filter_crise IS NULL OR k.tipo_crise && filter_crise)
    ORDER BY k.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

COMMENT ON FUNCTION match_knowledge_chunks IS 'Busca chunks relevantes por similaridade semântica com filtros opcionais de metadados';
```

### Busca Avançada para Diagnóstico

```sql
-- ====
-- FUNCTION: search_knowledge_for_diagnosis
-- Busca otimizada para geração de perguntas e análise
-- ====
CREATE OR REPLACE FUNCTION search_knowledge_for_diagnosis(
    query_embedding VECTOR(1536),
    areas_criticas TEXT[] DEFAULT NULL,
    motor_identificado TEXT DEFAULT NULL,
    match_count INT DEFAULT 10
)
RETURNS TABLE (
    id UUID,
    chapter TEXT,
    section TEXT,
    content TEXT,
    metadata JSONB,
    similarity FLOAT,
    relevance_boost FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        k.id,
        k.chapter,
        k.section,
        k.content,
        k.metadata,
        1 - (k.embedding <=> query_embedding) AS similarity,
        -- Boost de relevância para áreas críticas e motor identificado
        CASE 
            WHEN k.chapter = ANY(areas_criticas) THEN 0.2
            WHEN motor_identificado = ANY(k.motor_motivacional) THEN 0.1
            ELSE 0.0
        END AS relevance_boost
    FROM knowledge_chunks k
    WHERE k.is_active = TRUE
    ORDER BY (1 - (k.embedding <=> query_embedding)) + 
             CASE 
                 WHEN k.chapter = ANY(areas_criticas) THEN 0.2
                 WHEN motor_identificado = ANY(k.motor_motivacional) THEN 0.1
                 ELSE 0.0
             END DESC
    LIMIT match_count;
END;
$$;
```

### Estatísticas de Diagnósticos (Admin)

```sql
-- ====
-- FUNCTION: admin_get_diagnostic_stats
-- Estatísticas para dashboard administrativo
-- ====
CREATE OR REPLACE FUNCTION admin_get_diagnostic_stats()
RETURNS TABLE (
    total_diagnostics BIGINT,
    completed_diagnostics BIGINT,
    avg_completion_rate DECIMAL,
    avg_questions_answered DECIMAL,
    avg_words_count DECIMAL,
    avg_nps DECIMAL
)
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(d.*)::BIGINT,
        COUNT(d.*) FILTER (WHERE d.status = 'completed')::BIGINT,
        ROUND(COUNT(*) FILTER (WHERE d.status = 'completed')::DECIMAL / NULLIF(COUNT(*), 0) * 100, 2),
        ROUND(AVG(d.total_answers)::DECIMAL, 1),
        ROUND(AVG(d.total_words)::DECIMAL, 1),
        ROUND(AVG(f.nps_score)::DECIMAL, 1)
    FROM diagnostics d
    LEFT JOIN feedback f ON f.diagnostic_id = d.id;
END;
$$ LANGUAGE plpgsql;
```

---

## 5. POLÍTICAS RLS (ROW LEVEL SECURITY)

### Habilitar RLS

```sql
-- Habilitar RLS em todas as tabelas com dados sensíveis
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE diagnostics ENABLE ROW LEVEL SECURITY;
ALTER TABLE answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE diagnostic_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_logs ENABLE ROW LEVEL SECURITY;
```

### Políticas para profiles

```sql
-- Usuário pode ver/editar apenas seu próprio perfil
CREATE POLICY "Users can view own profile"
    ON profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON profiles FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

CREATE POLICY "Service can insert profiles"
    ON profiles FOR INSERT
    WITH CHECK (TRUE);
```

### Políticas para diagnostics

```sql
-- Usuário pode ver seus diagnósticos
CREATE POLICY "Users can view own diagnostics"
    ON diagnostics FOR SELECT
    USING (
        auth.uid() = user_id OR
        (user_id IS NULL AND anonymous_session_id = current_setting('app.session_id', true))
    );

-- Usuário pode criar diagnósticos
CREATE POLICY "Users can create diagnostics"
    ON diagnostics FOR INSERT
    WITH CHECK (
        auth.uid() = user_id OR
        (auth.uid() IS NULL AND anonymous_session_id IS NOT NULL)
    );

-- Usuário pode atualizar seus diagnósticos
CREATE POLICY "Users can update own diagnostics"
    ON diagnostics FOR UPDATE
    USING (
        auth.uid() = user_id OR
        (user_id IS NULL AND anonymous_session_id = current_setting('app.session_id', true))
    );

-- Acesso público via token (para visualização de resultado)
CREATE POLICY "Public access via result token"
    ON diagnostics FOR SELECT
    USING (
        result_token IS NOT NULL AND
        result_token = current_setting('app.result_token', true)
    );
```

### Políticas para answers

```sql
-- Usuário pode ver respostas dos seus diagnósticos
CREATE POLICY "Users can view own answers"
    ON answers FOR SELECT
    USING (
        diagnostic_id IN (
            SELECT id FROM diagnostics
            WHERE user_id = auth.uid()
            OR (user_id IS NULL AND anonymous_session_id = current_setting('app.session_id', true))
        )
    );

-- Usuário pode criar respostas
CREATE POLICY "Users can create answers"
    ON answers FOR INSERT
    WITH CHECK (
        diagnostic_id IN (
            SELECT id FROM diagnostics
            WHERE user_id = auth.uid()
            OR (user_id IS NULL AND anonymous_session_id = current_setting('app.session_id', true))
        )
    );
```

---

## 6. DIAGRAMA DE RELACIONAMENTOS

```
┌─────────────────────────────────────────────────────────────────┐
│                    MODELO DE DADOS NARA                         │
└─────────────────────────────────────────────────────────────────┘

                    ┌───────────────┐
                    │  auth.users   │ (Supabase Auth)
                    │───────────────│
                    │ id (PK)       │
                    │ email         │
                    └───────┬───────┘
                            │ 1:1
                            ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   waitlist    │   │   profiles    │   │  email_logs   │
│───────────────│   │───────────────│   │───────────────│
│ id (PK)       │   │ id (PK/FK)    │◄──│ id (PK)       │
│ email         │   │ email         │1:N│ user_id (FK)  │
│ diagnostic_id │─┐ │ full_name     │   │ email_type    │
│ ...           │ │ │ preferences   │   │ status        │
└───────────────┘ │ └───────┬───────┘   └───────────────┘
                  │         │
                  │         │ 1:N
                  │         ▼
                  │ ┌───────────────┐   ┌───────────────┐
                  │ │  diagnostics  │   │   feedback    │
                  │ │───────────────│   │───────────────│
                  └►│ id (PK)       │◄──│ id (PK)       │
                    │ user_id (FK)  │1:1│ diagnostic_id │
                    │ status        │   │ nps_score     │
                    │ scores_by_area│   │ ...           │
                    └───────┬───────┘   └───────────────┘
                            │
                  ┌─────────┼─────────┐
                  │         │         │
                  │ 1:N     │ 1:1     │ 1:N
                  ▼         ▼         ▼
          ┌─────────────┐ ┌─────────────────┐
          │   answers   │ │ diag_results    │
          │─────────────│ │─────────────────│
          │ id (PK)     │ │ id (PK)         │
          │ diag_id (FK)│ │ diagnostic_id   │
          │ answer_value│ │ overall_score   │
          │ question_*  │ │ motor_dominante │
          └─────────────┘ └─────────────────┘

┌─────────────────────┐                 ┌───────────────┐
│  knowledge_chunks   │                 │    areas      │
│─────────────────────│                 │───────────────│
│ id (PK)             │                 │ id (PK)       │
│ chapter             │─────────────────│ name          │
│ content             │     N:1         │ description   │
│ embedding           │                 │ icon, color   │
│ metadata            │                 └───────────────┘
└─────────────────────┘
```

---

## 7. NORMALIZAÇÃO FORMAL (1FN→5FN)

### Estado Atual: BCNF Compliant

| Forma Normal | Status | Observação |
|----|----|----|
| **1FN** | ✅ | Atributos atômicos; arrays justificados para listas |
| **2FN** | ✅ | Sem dependências parciais (PKs simples UUID) |
| **3FN** | ⚠️ | Desnormalização intencional em `answers` |
| **BCNF** | ✅ | Todo determinante é superchave |
| **4FN** | ✅ | Sem dependências multivaloradas independentes |
| **5FN** | N/A | Não aplicável |

### Justificativa das Desnormalizações

| Tabela | Campo | Justificativa |
|----|----|----|
| `answers` | `question_text`, `question_area` | Perguntas RAG são dinâmicas, não existem em tabela fixa |
| `diagnostics` | `scores_by_area` | Dados agregados, sempre lidos/escritos juntos |
| `knowledge_chunks` | Arrays de metadados | Filtros de busca complexos, evita JOINs |

---

## 8. ESTRATÉGIA DE CHUNKS PARA RAG

### Tipos de Chunks

| Categoria | Propósito | Quantidade Estimada |
|----|----|----|----|
| **metodologia** | Fundamentos das 12 áreas | ~24 (2 por área) |
| **diagnostico** | Sinais de M1 e critérios | ~36 (3 por área) |
| **intervencao** | Estratégias de intervenção | ~24 (2 por área) |
| **perguntas** | Templates de perguntas | ~60 (5 por área) |
| **exemplos** | Casos e padrões | ~50 |

### Estrutura de um Chunk Completo

```json
{
  "id": "uuid",
  "chapter": "Saúde Física",
  "section": "Fundamentos Narrativos",
  "content": "A Saúde Física refere-se à manutenção da constituição física...",
  "embedding": [0.023, -0.041, ...],
  "metadata": {
    "motor_motivacional": ["Necessidade", "Desejo"],
    "estagio_jornada": ["Germinar", "Desenvolver"],
    "tipo_crise": ["Execução"],
    "subtipo_crise": "Falta de vitalidade",
    "dominio": "D3",
    "ponto_entrada": "Comportamental",
    "sintomas_comportamentais": ["exaustão", "procrastinação"],
    "tom_emocional_base": "apatia",
    "nivel_maturidade": "baixo",
    "source": "metodologia_phellipe_oliveira",
    "version": "1.0"
  },
  "motor_motivacional": ["Necessidade", "Desejo"],
  "estagio_jornada": ["Germinar", "Desenvolver"],
  "tipo_crise": ["Execução"],
  "ponto_entrada": "Comportamental",
  "sintomas": ["exaustão", "procrastinação"],
  "tom_emocional": "apatia",
  "token_count": 342,
  "is_active": true,
  "version": 1
}
```

---

## 9. VOLUMETRIA E PERFORMANCE

### Estimativas de Volume

| Período | Usuários | Diagnósticos | Respostas | Chunks |
|----|----|----|----|----|----|
| Beta (1 mês) | 30 | 30 | 1.500 | 200 |
| Validação (3 meses) | 500 | 700 | 35.000 | 500 |
| Escala (12 meses) | 10.000 | 15.000 | 750.000 | 500 |

### Índices Críticos para Performance

| Tabela | Índice | Tipo | Propósito |
|----|----|----|----|
| `knowledge_chunks` | `idx_chunks_embedding` | ivfflat | Busca vetorial |
| `diagnostics` | `idx_diagnostics_status` | btree | Filtro por status |
| `answers` | `idx_answers_diagnostic` | btree | JOINs frequentes |
| `knowledge_chunks` | `idx_chunks_metadata` | gin | Filtros JSONB |

### Configuração do Índice Vetorial

```sql
-- Para ~500 chunks, lists = 100 é adequado
-- Para >10.000 chunks, aumentar para lists = sqrt(n)
CREATE INDEX idx_chunks_embedding ON knowledge_chunks 
    USING ivfflat (embedding vector_cosine_ops) 
    WITH (lists = 100);

-- Após inserir dados, analisar para otimizar
ANALYZE knowledge_chunks;
```

---

## 10. TROUBLESHOOTING

### Erro: Extensão `vector` não encontrada

```sql
-- Verificar se a extensão está habilitada
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Se não existir, habilitar no Supabase Dashboard:
-- Database → Extensions → Procurar "vector" → Enable
```

### Erro: Índice ivfflat não funciona

```sql
-- Verificar se há dados
SELECT COUNT(*) FROM knowledge_chunks;

-- Verificar se embeddings estão populados
SELECT COUNT(*) FROM knowledge_chunks WHERE embedding IS NOT NULL;

-- Recriar índice (se necessário)
DROP INDEX IF EXISTS idx_chunks_embedding;
CREATE INDEX idx_chunks_embedding ON knowledge_chunks 
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Analisar tabela
ANALYZE knowledge_chunks;
```

### Erro: RLS bloqueia acesso legítimo

```sql
-- Verificar políticas ativas
SELECT * FROM pg_policies WHERE tablename = 'diagnostics';

-- Testar RLS manualmente
SET ROLE authenticated;
SET request.jwt.claim.sub = '123e4567-e89b-12d3-a456-426614174000';
SELECT * FROM diagnostics;

-- Resetar role
RESET ROLE;
```

### Verificação de Instalação

```sql
-- Verificar tabelas criadas
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Deve retornar: profiles, diagnostics, answers, knowledge_chunks, 
-- diagnostic_results, feedback, waitlist, email_logs, areas

-- Verificar extensões
SELECT * FROM pg_extension WHERE extname IN ('uuid-ossp', 'vector', 'pg_trgm');

-- Verificar funções
SELECT routine_name FROM information_schema.routines 
WHERE routine_schema = 'public' AND routine_type = 'FUNCTION';
```

---

**Referências Cruzadas:**
- Fundamentos metodológicos: [01_FUNDAMENTOS.md](./01_FUNDAMENTOS.md)
- Prompts que usam este schema: [03_PROMPTS_CONHECIMENTO.md](./03_PROMPTS_CONHECIMENTO.md)
- Endpoints que acessam estas tabelas: [04_BACKEND_API.md](./04_BACKEND_API.md)
