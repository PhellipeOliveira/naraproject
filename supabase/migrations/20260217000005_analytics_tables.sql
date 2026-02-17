-- =====================================================
-- ANALYTICS E MÉTRICAS - NARA V2
-- Criado em: 2026-02-17
-- Propósito: Tracking de eventos e métricas do sistema
-- =====================================================

-- Tabela de Eventos (tracking granular)
CREATE TABLE IF NOT EXISTS public.analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Identificação
    event_name TEXT NOT NULL,
    event_category TEXT NOT NULL,  -- 'diagnostic', 'user', 'system', etc.
    
    -- Contexto
    diagnostic_id UUID REFERENCES public.diagnostics(id) ON DELETE SET NULL,
    user_id UUID,  -- Se tiver auth no futuro
    session_id TEXT,
    
    -- Dados do evento
    event_data JSONB DEFAULT '{}'::jsonb,
    
    -- Metadata
    user_agent TEXT,
    ip_address INET,
    referrer TEXT,
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT,
    
    -- Performance
    page_load_time_ms INT,
    
    -- Índices para queries
    CONSTRAINT valid_category CHECK (event_category IN ('diagnostic', 'user', 'navigation', 'error', 'conversion'))
);

-- Índices para performance
CREATE INDEX idx_analytics_events_created_at ON public.analytics_events(created_at DESC);
CREATE INDEX idx_analytics_events_event_name ON public.analytics_events(event_name);
CREATE INDEX idx_analytics_events_category ON public.analytics_events(event_category);
CREATE INDEX idx_analytics_events_diagnostic_id ON public.analytics_events(diagnostic_id) WHERE diagnostic_id IS NOT NULL;
CREATE INDEX idx_analytics_events_session_id ON public.analytics_events(session_id) WHERE session_id IS NOT NULL;

COMMENT ON TABLE public.analytics_events IS 'Tracking granular de eventos do sistema NARA';


-- =====================================================
-- Tabela de Métricas Agregadas (pré-computadas)
-- =====================================================

CREATE TABLE IF NOT EXISTS public.analytics_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Período da métrica
    date DATE NOT NULL,
    metric_type TEXT NOT NULL,  -- 'daily', 'weekly', 'monthly'
    
    -- Métricas de Diagnóstico
    diagnostics_started INT DEFAULT 0,
    diagnostics_completed INT DEFAULT 0,
    diagnostics_abandoned INT DEFAULT 0,
    completion_rate DECIMAL(5,2),  -- %
    
    avg_completion_time_minutes INT,
    avg_answers_count DECIMAL(6,2),
    avg_words_count DECIMAL(8,2),
    
    -- Distribuição de Motores
    motor_necessidade_count INT DEFAULT 0,
    motor_valor_count INT DEFAULT 0,
    motor_desejo_count INT DEFAULT 0,
    motor_proposito_count INT DEFAULT 0,
    
    -- Distribuição de Crises
    crise_identidade_count INT DEFAULT 0,
    crise_sentido_count INT DEFAULT 0,
    crise_execucao_count INT DEFAULT 0,
    crise_conexao_count INT DEFAULT 0,
    crise_incongruencia_count INT DEFAULT 0,
    crise_transformacao_count INT DEFAULT 0,
    
    -- Distribuição de Estágios
    estagio_germinar_count INT DEFAULT 0,
    estagio_enraizar_count INT DEFAULT 0,
    estagio_desenvolver_count INT DEFAULT 0,
    estagio_florescer_count INT DEFAULT 0,
    estagio_frutificar_count INT DEFAULT 0,
    estagio_realizar_count INT DEFAULT 0,
    
    -- Áreas Silenciadas (JSONB para flexibilidade)
    areas_silenciadas_stats JSONB DEFAULT '{}'::jsonb,
    
    -- Métricas de Engajamento
    nps_responses_count INT DEFAULT 0,
    nps_average DECIMAL(4,2),
    waitlist_signups INT DEFAULT 0,
    
    CONSTRAINT unique_metric_date_type UNIQUE(date, metric_type)
);

CREATE INDEX idx_analytics_metrics_date ON public.analytics_metrics(date DESC);
CREATE INDEX idx_analytics_metrics_type ON public.analytics_metrics(metric_type);

COMMENT ON TABLE public.analytics_metrics IS 'Métricas agregadas diárias/semanais/mensais do NARA';


-- =====================================================
-- View: Métricas em Tempo Real (últimos 7 dias)
-- =====================================================

CREATE OR REPLACE VIEW public.analytics_realtime AS
SELECT 
    DATE(d.created_at) as date,
    COUNT(DISTINCT d.id) as total_diagnostics,
    COUNT(DISTINCT CASE WHEN d.status = 'completed' THEN d.id END) as completed,
    COUNT(DISTINCT CASE WHEN d.status = 'in_progress' THEN d.id END) as in_progress,
    COUNT(DISTINCT CASE WHEN d.status = 'abandoned' THEN d.id END) as abandoned,
    
    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN d.status = 'completed' THEN d.id END)::DECIMAL 
        / NULLIF(COUNT(DISTINCT d.id), 0),
        2
    ) as completion_rate,
    
    AVG(d.total_answers)::INT as avg_answers,
    AVG(d.total_words)::INT as avg_words,
    
    -- Distribuição de motores (dos completados)
    COUNT(DISTINCT CASE WHEN dr.motor_dominante = 'Necessidade' THEN dr.diagnostic_id END) as motor_necessidade,
    COUNT(DISTINCT CASE WHEN dr.motor_dominante = 'Valor' THEN dr.diagnostic_id END) as motor_valor,
    COUNT(DISTINCT CASE WHEN dr.motor_dominante = 'Desejo' THEN dr.diagnostic_id END) as motor_desejo,
    COUNT(DISTINCT CASE WHEN dr.motor_dominante = 'Propósito' THEN dr.diagnostic_id END) as motor_proposito
    
FROM public.diagnostics d
LEFT JOIN public.diagnostic_results dr ON dr.diagnostic_id = d.id
WHERE d.created_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE(d.created_at)
ORDER BY date DESC;

COMMENT ON VIEW public.analytics_realtime IS 'Métricas em tempo real dos últimos 7 dias';


-- =====================================================
-- View: Heatmap de Áreas Silenciadas
-- =====================================================

CREATE OR REPLACE VIEW public.analytics_areas_silenciadas AS
WITH area_counts AS (
    SELECT 
        UNNEST(dr.areas_silenciadas) as area_id,
        COUNT(*) as silence_count
    FROM public.diagnostic_results dr
    WHERE dr.areas_silenciadas IS NOT NULL 
      AND ARRAY_LENGTH(dr.areas_silenciadas, 1) > 0
    GROUP BY area_id
)
SELECT 
    area_id,
    silence_count,
    ROUND(100.0 * silence_count / SUM(silence_count) OVER (), 2) as percentage,
    CASE area_id
        WHEN 1 THEN 'Saúde Física'
        WHEN 2 THEN 'Saúde Mental'
        WHEN 3 THEN 'Saúde Espiritual'
        WHEN 4 THEN 'Vida Pessoal'
        WHEN 5 THEN 'Vida Amorosa'
        WHEN 6 THEN 'Vida Familiar'
        WHEN 7 THEN 'Vida Social'
        WHEN 8 THEN 'Vida Profissional'
        WHEN 9 THEN 'Finanças'
        WHEN 10 THEN 'Educação'
        WHEN 11 THEN 'Inovação'
        WHEN 12 THEN 'Lazer'
    END as area_name
FROM area_counts
ORDER BY silence_count DESC;

COMMENT ON VIEW public.analytics_areas_silenciadas IS 'Ranking de áreas mais silenciadas pelos usuários';


-- =====================================================
-- View: Distribuição de Motores (Geral)
-- =====================================================

CREATE OR REPLACE VIEW public.analytics_motores_distribution AS
SELECT 
    motor_dominante,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
FROM public.diagnostic_results
WHERE motor_dominante IS NOT NULL
GROUP BY motor_dominante
ORDER BY count DESC;

COMMENT ON VIEW public.analytics_motores_distribution IS 'Distribuição geral de motores motivacionais';


-- =====================================================
-- View: Distribuição de Crises (Geral)
-- =====================================================

CREATE OR REPLACE VIEW public.analytics_crises_distribution AS
SELECT 
    vetor_estado->>'crise_raiz' as crise_raiz,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
FROM public.diagnostic_results
WHERE vetor_estado IS NOT NULL 
  AND vetor_estado->>'crise_raiz' IS NOT NULL
GROUP BY crise_raiz
ORDER BY count DESC;

COMMENT ON VIEW public.analytics_crises_distribution IS 'Distribuição geral de crises raiz';


-- =====================================================
-- Função: Agregar métricas diárias (executar via CRON)
-- =====================================================

CREATE OR REPLACE FUNCTION public.aggregate_daily_metrics(target_date DATE DEFAULT CURRENT_DATE - INTERVAL '1 day')
RETURNS VOID AS $$
DECLARE
    v_diagnostics_started INT;
    v_diagnostics_completed INT;
    v_diagnostics_abandoned INT;
    v_completion_rate DECIMAL(5,2);
    v_avg_time INT;
    v_avg_answers DECIMAL(6,2);
    v_avg_words DECIMAL(8,2);
BEGIN
    -- Calcular métricas básicas
    SELECT 
        COUNT(*),
        COUNT(*) FILTER (WHERE status = 'completed'),
        COUNT(*) FILTER (WHERE status = 'abandoned'),
        ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'completed')::DECIMAL / NULLIF(COUNT(*), 0), 2),
        AVG(EXTRACT(EPOCH FROM (completed_at - created_at))/60)::INT,
        AVG(total_answers),
        AVG(total_words)
    INTO 
        v_diagnostics_started,
        v_diagnostics_completed,
        v_diagnostics_abandoned,
        v_completion_rate,
        v_avg_time,
        v_avg_answers,
        v_avg_words
    FROM public.diagnostics
    WHERE DATE(created_at) = target_date;
    
    -- Inserir ou atualizar métricas
    INSERT INTO public.analytics_metrics (
        date,
        metric_type,
        diagnostics_started,
        diagnostics_completed,
        diagnostics_abandoned,
        completion_rate,
        avg_completion_time_minutes,
        avg_answers_count,
        avg_words_count,
        
        -- Motores
        motor_necessidade_count,
        motor_valor_count,
        motor_desejo_count,
        motor_proposito_count,
        
        -- Crises
        crise_identidade_count,
        crise_sentido_count,
        crise_execucao_count,
        crise_conexao_count,
        crise_incongruencia_count,
        crise_transformacao_count,
        
        -- Estágios
        estagio_germinar_count,
        estagio_enraizar_count,
        estagio_desenvolver_count,
        estagio_florescer_count,
        estagio_frutificar_count,
        estagio_realizar_count
    )
    SELECT 
        target_date,
        'daily',
        v_diagnostics_started,
        v_diagnostics_completed,
        v_diagnostics_abandoned,
        v_completion_rate,
        v_avg_time,
        v_avg_answers,
        v_avg_words,
        
        -- Motores
        COUNT(*) FILTER (WHERE dr.motor_dominante = 'Necessidade'),
        COUNT(*) FILTER (WHERE dr.motor_dominante = 'Valor'),
        COUNT(*) FILTER (WHERE dr.motor_dominante = 'Desejo'),
        COUNT(*) FILTER (WHERE dr.motor_dominante = 'Propósito'),
        
        -- Crises
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'crise_raiz' LIKE '%Identidade%'),
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'crise_raiz' LIKE '%Sentido%'),
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'crise_raiz' LIKE '%Execução%'),
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'crise_raiz' LIKE '%Conexão%'),
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'crise_raiz' LIKE '%Incongruência%'),
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'crise_raiz' LIKE '%Transformação%'),
        
        -- Estágios
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'estagio_jornada' = 'Germinar'),
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'estagio_jornada' = 'Enraizar'),
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'estagio_jornada' = 'Desenvolver'),
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'estagio_jornada' = 'Florescer'),
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'estagio_jornada' = 'Frutificar'),
        COUNT(*) FILTER (WHERE dr.vetor_estado->>'estagio_jornada' = 'Realizar')
    FROM public.diagnostics d
    LEFT JOIN public.diagnostic_results dr ON dr.diagnostic_id = d.id
    WHERE DATE(d.created_at) = target_date
    ON CONFLICT (date, metric_type) 
    DO UPDATE SET
        updated_at = NOW(),
        diagnostics_started = EXCLUDED.diagnostics_started,
        diagnostics_completed = EXCLUDED.diagnostics_completed,
        diagnostics_abandoned = EXCLUDED.diagnostics_abandoned,
        completion_rate = EXCLUDED.completion_rate,
        avg_completion_time_minutes = EXCLUDED.avg_completion_time_minutes,
        avg_answers_count = EXCLUDED.avg_answers_count,
        avg_words_count = EXCLUDED.avg_words_count,
        motor_necessidade_count = EXCLUDED.motor_necessidade_count,
        motor_valor_count = EXCLUDED.motor_valor_count,
        motor_desejo_count = EXCLUDED.motor_desejo_count,
        motor_proposito_count = EXCLUDED.motor_proposito_count,
        crise_identidade_count = EXCLUDED.crise_identidade_count,
        crise_sentido_count = EXCLUDED.crise_sentido_count,
        crise_execucao_count = EXCLUDED.crise_execucao_count,
        crise_conexao_count = EXCLUDED.crise_conexao_count,
        crise_incongruencia_count = EXCLUDED.crise_incongruencia_count,
        crise_transformacao_count = EXCLUDED.crise_transformacao_count,
        estagio_germinar_count = EXCLUDED.estagio_germinar_count,
        estagio_enraizar_count = EXCLUDED.estagio_enraizar_count,
        estagio_desenvolver_count = EXCLUDED.estagio_desenvolver_count,
        estagio_florescer_count = EXCLUDED.estagio_florescer_count,
        estagio_frutificar_count = EXCLUDED.estagio_frutificar_count,
        estagio_realizar_count = EXCLUDED.estagio_realizar_count;
        
    RAISE NOTICE 'Métricas agregadas para %', target_date;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION public.aggregate_daily_metrics IS 'Agrega métricas diárias. Executar via CRON.';


-- =====================================================
-- Permissões (ajustar conforme necessidade)
-- =====================================================

-- Analytics events: insert apenas (logs)
-- Views: read-only para dashboard

GRANT SELECT ON public.analytics_realtime TO anon, authenticated;
GRANT SELECT ON public.analytics_areas_silenciadas TO anon, authenticated;
GRANT SELECT ON public.analytics_motores_distribution TO anon, authenticated;
GRANT SELECT ON public.analytics_crises_distribution TO anon, authenticated;
