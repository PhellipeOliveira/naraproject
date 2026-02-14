-- Views para métricas (taxa de conclusão, NPS, funil) conforme 07_DEPLOY_QUALIDADE.md

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
