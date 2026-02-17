-- Views SQL ESTENDIDAS para métricas de sucesso
-- Conforme 07_DEPLOY_QUALIDADE.md - Seção 2
-- NOTA: Views básicas (v_completion_rate, v_weekly_nps, v_diagnostic_funnel) 
--       já existem em 20260213000006_nara_views_metrics.sql
-- Esta migration ESTENDE com views adicionais

-- ====================================================================
-- ATUALIZAÇÃO: Taxa de conclusão por período (adiciona percentage)
-- ====================================================================
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

COMMENT ON VIEW v_completion_rate IS 'Taxa de conclusão de diagnósticos por dia';


-- ====================================================================
-- 2. NPS semanal (se tabela feedback existir)
-- ====================================================================
DO $$
BEGIN
    IF EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'feedback'
    ) THEN
        EXECUTE '
        CREATE OR REPLACE VIEW v_weekly_nps AS
        SELECT
            date_trunc(''week'', created_at) AS week,
            COUNT(*) AS total_responses,
            ROUND(AVG(nps_score)::NUMERIC, 1) AS avg_nps,
            ROUND(
                (COUNT(*) FILTER (WHERE nps_score >= 9)::NUMERIC - 
                 COUNT(*) FILTER (WHERE nps_score <= 6)::NUMERIC) /
                NULLIF(COUNT(*), 0) * 100, 1
            ) AS nps_score
        FROM feedback
        WHERE nps_score IS NOT NULL
        GROUP BY date_trunc(''week'', created_at)
        ORDER BY week DESC;
        ';
        
        COMMENT ON VIEW v_weekly_nps IS 'NPS (Net Promoter Score) semanal';
    END IF;
END
$$;


-- ====================================================================
-- 3. Funil do diagnóstico
-- ====================================================================
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
SELECT 
    stage, 
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM stages
GROUP BY stage
ORDER BY stage;

COMMENT ON VIEW v_diagnostic_funnel IS 'Funil de conversão do diagnóstico (últimos 30 dias)';


-- ====================================================================
-- 4. Tempo médio de conclusão
-- ====================================================================
CREATE OR REPLACE VIEW v_average_completion_time AS
SELECT
    date_trunc('day', created_at) AS date,
    COUNT(*) AS diagnostics_completed,
    ROUND(
        AVG(EXTRACT(EPOCH FROM (updated_at - created_at)) / 60)::NUMERIC, 
        2
    ) AS avg_minutes,
    ROUND(
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (updated_at - created_at)) / 60)::NUMERIC,
        2
    ) AS median_minutes
FROM diagnostics
WHERE status = 'completed'
  AND updated_at IS NOT NULL
  AND created_at > NOW() - INTERVAL '30 days'
GROUP BY date_trunc('day', created_at)
ORDER BY date DESC;

COMMENT ON VIEW v_average_completion_time IS 'Tempo médio e mediano para concluir diagnóstico';


-- ====================================================================
-- 5. Áreas mais cobertas
-- ====================================================================
CREATE OR REPLACE VIEW v_most_covered_areas AS
SELECT
    unnest(areas_covered) AS area,
    COUNT(*) AS times_covered,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM diagnostics WHERE status = 'completed'), 2) as percentage
FROM diagnostics
WHERE status = 'completed'
  AND areas_covered IS NOT NULL
  AND created_at > NOW() - INTERVAL '30 days'
GROUP BY area
ORDER BY times_covered DESC;

COMMENT ON VIEW v_most_covered_areas IS 'Áreas mais frequentemente cobertas em diagnósticos (últimos 30 dias)';


-- ====================================================================
-- 6. Estatísticas de palavras e respostas
-- ====================================================================
CREATE OR REPLACE VIEW v_diagnostic_stats AS
SELECT
    date_trunc('day', created_at) AS date,
    COUNT(*) AS total_diagnostics,
    ROUND(AVG(total_answers)::NUMERIC, 1) AS avg_answers,
    ROUND(AVG(total_words)::NUMERIC, 0) AS avg_words,
    ROUND(AVG(array_length(areas_covered, 1))::NUMERIC, 1) AS avg_areas_covered,
    MIN(total_answers) AS min_answers,
    MAX(total_answers) AS max_answers
FROM diagnostics
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY date_trunc('day', created_at)
ORDER BY date DESC;

COMMENT ON VIEW v_diagnostic_stats IS 'Estatísticas diárias de diagnósticos (respostas, palavras, áreas)';


-- ====================================================================
-- 7. Taxa de abandono por fase
-- ====================================================================
CREATE OR REPLACE VIEW v_abandonment_by_phase AS
SELECT
    current_phase,
    COUNT(*) AS abandoned_count,
    ROUND(AVG(total_answers)::NUMERIC, 1) AS avg_answers_before_abandon
FROM diagnostics
WHERE status IN ('abandoned', 'in_progress')
  AND updated_at < NOW() - INTERVAL '7 days'  -- Inativo há mais de 7 dias
GROUP BY current_phase
ORDER BY current_phase;

COMMENT ON VIEW v_abandonment_by_phase IS 'Taxa de abandono por fase do diagnóstico';


-- ====================================================================
-- 8. Performance do RAG (chunks mais recuperados)
-- ====================================================================
-- Esta view requer que você registre qual chunk foi usado em cada resposta
-- Comentada por enquanto, pode implementar depois se necessário

/*
CREATE OR REPLACE VIEW v_most_used_chunks AS
SELECT
    k.chapter,
    k.section,
    COUNT(*) AS times_used,
    ROUND(AVG(similarity)::NUMERIC, 3) AS avg_similarity
FROM answer_chunks ac  -- Tabela hipotética que registra chunks usados
JOIN knowledge_chunks k ON k.id = ac.chunk_id
GROUP BY k.chapter, k.section
ORDER BY times_used DESC
LIMIT 20;
*/


-- ====================================================================
-- 9. Grants (permitir leitura pública das views - ajustar conforme RLS)
-- ====================================================================
-- GRANT SELECT ON v_completion_rate TO anon, authenticated;
-- GRANT SELECT ON v_diagnostic_funnel TO anon, authenticated;
-- GRANT SELECT ON v_average_completion_time TO anon, authenticated;
-- GRANT SELECT ON v_most_covered_areas TO anon, authenticated;
-- GRANT SELECT ON v_diagnostic_stats TO anon, authenticated;
-- GRANT SELECT ON v_abandonment_by_phase TO anon, authenticated;
-- (Descomentarndo se quiser acesso público)
