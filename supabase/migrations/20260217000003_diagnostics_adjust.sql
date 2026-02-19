-- Migration: Diagnostics Adjust - Análise Intermediária
-- Data: 2026-02-17
-- Descrição: Ajusta tabela diagnostics para armazenar análise intermediária

-- Adicionar campo para análise intermediária
ALTER TABLE diagnostics
  ADD COLUMN IF NOT EXISTS analise_intermediaria JSONB;

-- Adicionar comentário
COMMENT ON COLUMN diagnostics.analise_intermediaria IS 'Análise intermediária: padrões, tom emocional, áreas silenciadas, palavras recorrentes';

-- Marcar scores_by_area como legacy (manter por compatibilidade)
COMMENT ON COLUMN diagnostics.scores_by_area IS '[LEGACY] Scores calculados - usar apenas para diagnósticos antigos';

-- Criar índice para queries por status e phase
CREATE INDEX IF NOT EXISTS idx_diagnostics_status_phase 
  ON diagnostics(status, current_phase);

-- Criar índice para queries por email (para check-existing)
CREATE INDEX IF NOT EXISTS idx_diagnostics_email_status 
  ON diagnostics(email, status) 
  WHERE status IN ('in_progress', 'eligible');
