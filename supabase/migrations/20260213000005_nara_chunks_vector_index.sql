-- NARA: Índice vetorial em knowledge_chunks (executar após popular a tabela)
-- Requer: 20260213000002_nara_tables.sql
-- O índice ivfflat precisa de linhas com embedding preenchido para ser útil.
-- Se a tabela estiver vazia, o índice não é criado (evita erro em fresh install).

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM public.knowledge_chunks WHERE embedding IS NOT NULL LIMIT 1) THEN
        CREATE INDEX IF NOT EXISTS idx_chunks_embedding
            ON public.knowledge_chunks
            USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100);
        ANALYZE public.knowledge_chunks;
    END IF;
END $$;
