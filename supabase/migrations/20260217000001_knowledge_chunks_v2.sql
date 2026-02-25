-- Migration: Knowledge Chunks V2 - Metadados Enriquecidos
-- Data: 2026-02-17
-- Descrição: Adiciona novos campos metodológicos para a Base Metodológica NARA refinada

-- Adicionar novos campos à tabela knowledge_chunks
ALTER TABLE knowledge_chunks 
  ADD COLUMN IF NOT EXISTS nivel_maturidade TEXT,
  ADD COLUMN IF NOT EXISTS subtipo_crise TEXT,
  ADD COLUMN IF NOT EXISTS tipo_conteudo TEXT,
  ADD COLUMN IF NOT EXISTS dominio TEXT[];

-- Renomear coluna sintomas para sintomas_comportamentais
ALTER TABLE knowledge_chunks 
  RENAME COLUMN sintomas TO sintomas_comportamentais;

-- Adicionar comentários para documentação
COMMENT ON COLUMN knowledge_chunks.nivel_maturidade IS 'Nível de maturidade do usuário: baixo, médio, alto';
COMMENT ON COLUMN knowledge_chunks.subtipo_crise IS 'Subtipo específico da crise (ex: Identidade Herdada)';
COMMENT ON COLUMN knowledge_chunks.tipo_conteudo IS 'Tipo: Ponto de Entrada, Âncora Prática, Técnica de TCC, Conceito, Exemplo de Caso';
COMMENT ON COLUMN knowledge_chunks.dominio IS 'Domínios Temáticos: D1 a D6';
COMMENT ON COLUMN knowledge_chunks.sintomas_comportamentais IS 'Array de sintomas comportamentais observáveis';

-- Criar índice para melhorar performance de queries por tipo_conteudo
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_tipo_conteudo 
  ON knowledge_chunks(tipo_conteudo);

-- Criar índice para queries por dominio
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_dominio 
  ON knowledge_chunks USING GIN(dominio);

-- Criar índice para queries por version
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_version 
  ON knowledge_chunks(version);
