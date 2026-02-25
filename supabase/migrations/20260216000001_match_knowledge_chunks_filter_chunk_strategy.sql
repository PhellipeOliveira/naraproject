-- NARA: Adiciona filtro opcional por chunk_strategy em match_knowledge_chunks.
-- Requer: 20260213000003_nara_rpc.sql (ou schema já existente).
-- Retrocompatível: filter_chunk_strategy DEFAULT NULL = comportamento igual ao anterior.

CREATE OR REPLACE FUNCTION public.match_knowledge_chunks(
    query_embedding vector(1536),
    match_threshold FLOAT DEFAULT 0.5,
    match_count INT DEFAULT 10,
    filter_chapter TEXT DEFAULT NULL,
    filter_motor TEXT[] DEFAULT NULL,
    filter_estagio TEXT[] DEFAULT NULL,
    filter_crise TEXT[] DEFAULT NULL,
    filter_chunk_strategy TEXT DEFAULT NULL
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
        AND (filter_chunk_strategy IS NULL OR (k.metadata->>'chunk_strategy') = filter_chunk_strategy)
    ORDER BY k.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
