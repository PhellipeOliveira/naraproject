-- NARA: Funções RPC para RAG e admin
-- Requer: 20260213000002_nara_tables.sql

CREATE OR REPLACE FUNCTION public.match_knowledge_chunks(
    query_embedding vector(1536),
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
        1 - (k.embedding <=> query_embedding)::FLOAT AS similarity
    FROM public.knowledge_chunks k
    WHERE k.is_active = TRUE
        AND k.embedding IS NOT NULL
        AND 1 - (k.embedding <=> query_embedding) > match_threshold
        AND (filter_chapter IS NULL OR k.chapter = filter_chapter)
        AND (filter_motor IS NULL OR k.motor_motivacional && filter_motor)
        AND (filter_estagio IS NULL OR k.estagio_jornada && filter_estagio)
        AND (filter_crise IS NULL OR k.tipo_crise && filter_crise)
    ORDER BY k.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

CREATE OR REPLACE FUNCTION public.search_knowledge_for_diagnosis(
    query_embedding vector(1536),
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
        1 - (k.embedding <=> query_embedding)::FLOAT AS similarity,
        CASE
            WHEN areas_criticas IS NOT NULL AND k.chapter = ANY(areas_criticas) THEN 0.2
            WHEN motor_identificado IS NOT NULL AND k.motor_motivacional IS NOT NULL AND motor_identificado = ANY(k.motor_motivacional) THEN 0.1
            ELSE 0.0
        END::FLOAT AS relevance_boost
    FROM public.knowledge_chunks k
    WHERE k.is_active = TRUE AND k.embedding IS NOT NULL
    ORDER BY (1 - (k.embedding <=> query_embedding)) +
             CASE
                 WHEN areas_criticas IS NOT NULL AND k.chapter = ANY(areas_criticas) THEN 0.2
                 WHEN motor_identificado IS NOT NULL AND k.motor_motivacional IS NOT NULL AND motor_identificado = ANY(k.motor_motivacional) THEN 0.1
                 ELSE 0.0
             END DESC
    LIMIT match_count;
END;
$$;

CREATE OR REPLACE FUNCTION public.admin_get_diagnostic_stats()
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
LANGUAGE plpgsql
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
    FROM public.diagnostics d
    LEFT JOIN public.feedback f ON f.diagnostic_id = d.id;
END;
$$;
