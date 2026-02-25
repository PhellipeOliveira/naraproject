-- Add canonical source identifier for file-level upsert/reindex flows.
ALTER TABLE public.knowledge_chunks
ADD COLUMN IF NOT EXISTS source TEXT;

CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_source
ON public.knowledge_chunks (source);
