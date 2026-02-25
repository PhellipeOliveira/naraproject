-- Migration: Diagnostic Results V2 - Vetor de Estado Qualitativo
-- Data: 2026-02-17
-- Descrição: Substitui scoring numérico por análise qualitativa via vetor de estado

-- Adicionar novos campos para análise qualitativa
ALTER TABLE diagnostic_results
  ADD COLUMN IF NOT EXISTS vetor_estado JSONB,
  ADD COLUMN IF NOT EXISTS memorias_vermelhas TEXT[],
  ADD COLUMN IF NOT EXISTS areas_silenciadas SMALLINT[],
  ADD COLUMN IF NOT EXISTS ancoras_sugeridas TEXT[];

-- Adicionar comentários para documentação
COMMENT ON COLUMN diagnostic_results.vetor_estado IS 'Vetor de estado qualitativo com motor_dominante, estagio_jornada, crise_raiz, etc.';
COMMENT ON COLUMN diagnostic_results.memorias_vermelhas IS 'Citações literais do usuário que revelam conflitos não dominados';
COMMENT ON COLUMN diagnostic_results.areas_silenciadas IS 'IDs das áreas (1-12) não respondidas ou respondidas vagamente';
COMMENT ON COLUMN diagnostic_results.ancoras_sugeridas IS 'Âncoras Práticas sugeridas (das 19 disponíveis)';

-- Manter overall_score e area_scores por compatibilidade temporária
-- Podem ser removidos em migração futura após validação completa
COMMENT ON COLUMN diagnostic_results.overall_score IS '[LEGACY] Score numérico - usar vetor_estado.estagio_jornada';
COMMENT ON COLUMN diagnostic_results.area_scores IS '[LEGACY] Scores por área - usar area_analysis detalhado';

-- Criar índice para queries por motor dominante
CREATE INDEX IF NOT EXISTS idx_diagnostic_results_motor_dominante 
  ON diagnostic_results((vetor_estado->>'motor_dominante'));

-- Criar índice para queries por fase da jornada
CREATE INDEX IF NOT EXISTS idx_diagnostic_results_estagio_jornada 
  ON diagnostic_results((vetor_estado->>'estagio_jornada'));

-- Criar índice para queries por crise raiz
CREATE INDEX IF NOT EXISTS idx_diagnostic_results_crise_raiz 
  ON diagnostic_results((vetor_estado->>'crise_raiz'));
