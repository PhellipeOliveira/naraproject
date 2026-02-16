-- Armazena as perguntas da fase atual (fases 2+), para permitir retomada.
-- Fase 1 usa BASELINE_QUESTIONS no código; fases 2+ são geradas e precisam ser persistidas.
ALTER TABLE public.diagnostics
ADD COLUMN IF NOT EXISTS current_phase_questions JSONB DEFAULT '[]';

COMMENT ON COLUMN public.diagnostics.current_phase_questions IS 'Perguntas da fase atual (fases 2+). Permite retomar diagnóstico sem perder as perguntas geradas.';
