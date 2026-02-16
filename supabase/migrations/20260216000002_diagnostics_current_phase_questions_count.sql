-- Armazena quantas perguntas tem a fase atual (15 na Fase 1; variável nas fases 2+).
-- Usado para marcar phase_complete ao responder a última pergunta da fase.
ALTER TABLE public.diagnostics
ADD COLUMN IF NOT EXISTS current_phase_questions_count INTEGER DEFAULT 15
CHECK (current_phase_questions_count > 0);

COMMENT ON COLUMN public.diagnostics.current_phase_questions_count IS 'Número de perguntas da fase atual (15 na Fase 1; definido ao gerar fases 2+)';
