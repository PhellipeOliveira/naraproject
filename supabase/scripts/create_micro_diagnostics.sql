-- Tabela micro_diagnostics para o fluxo 5Q -> 5Q (micro-diagnóstico por área).
-- Execute este script no SQL Editor do Supabase (Dashboard > SQL Editor).
--
-- Se a tabela diagnostics usar id como BIGINT em vez de UUID, altere
-- diagnostic_id para: diagnostic_id BIGINT NOT NULL REFERENCES diagnostics(id) ON DELETE CASCADE

CREATE TABLE IF NOT EXISTS micro_diagnostics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  diagnostic_id UUID NOT NULL REFERENCES diagnostics(id) ON DELETE CASCADE,
  area TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'completed')),
  phase SMALLINT NOT NULL DEFAULT 1 CHECK (phase IN (1, 2)),
  questions_phase1 JSONB NOT NULL DEFAULT '[]'::jsonb,
  answers_phase1 JSONB NOT NULL DEFAULT '[]'::jsonb,
  questions_phase2 JSONB NOT NULL DEFAULT '[]'::jsonb,
  answers_phase2 JSONB NOT NULL DEFAULT '[]'::jsonb,
  result JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Índices para consultas por diagnóstico e status
CREATE INDEX IF NOT EXISTS idx_micro_diagnostics_diagnostic_id
  ON micro_diagnostics(diagnostic_id);
CREATE INDEX IF NOT EXISTS idx_micro_diagnostics_status
  ON micro_diagnostics(status);

-- Comentário na tabela (opcional)
COMMENT ON TABLE micro_diagnostics IS 'Micro-diagnósticos 5Q->5Q por área; um concluído por diagnóstico.';
