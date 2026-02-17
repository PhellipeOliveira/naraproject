# Changelog - Reformulação Base Metodológica NARA

**Data**: 17 de Fevereiro de 2026  
**Versão**: 2.0.0  
**Documento Base**: `01_BASE_METODOLOGICA_NARA.md`

---

## 📋 Visão Geral

Esta reformulação representa uma evolução significativa do sistema NARA, migrando de uma abordagem baseada em scores numéricos para uma análise qualitativa profunda através de **Vetor de Estado**, com perguntas 100% narrativas e metadados metodológicos enriquecidos.

---

## ⚠️ BREAKING CHANGES

### 1. Perguntas Baseline

**ANTES (V1)**:
- Mix de perguntas: escalas numéricas (1-5) + perguntas abertas
- 15 perguntas com 7 do tipo `scale` e 8 abertas

**AGORA (V2)**:
- **100% perguntas narrativas e abertas** (`open_long` ou `open_short`)
- Todas as 15 perguntas baseiam-se em escuta ativa
- Foco em permitir que o usuário narre sua história sem restrições numéricas

**Impacto**:
- Frontend: Componente `QuestionCard` simplificado (sem lógica de escala)
- Backend: Perguntas adaptativas também são 100% narrativas
- Diagnósticos antigos (V1) não são comparáveis com novos (V2)

---

### 2. Sistema de Scoring

**ANTES (V1)**:
- `overall_score` (0-10): Score numérico geral
- `area_scores`: Scores por área baseados em médias de escalas
- Foco quantitativo

**AGORA (V2)**:
- **Vetor de Estado Qualitativo**: Estrutura multidimensional
```json
{
  "motor_dominante": "Valor",
  "motor_secundario": "Propósito",
  "estagio_jornada": "Enraizar",
  "crise_raiz": "Identidade Herdada",
  "crises_derivadas": ["Paralisia decisória", "Falta de direção"],
  "ponto_entrada_ideal": "Simbólico",
  "dominios_alavanca": ["D1", "D3"],
  "tom_emocional": "Indignação silenciosa",
  "risco_principal": "Autotraição prolongada",
  "necessidade_atual": "Reescrita identitária + rito de passagem"
}
```

**Impacto**:
- API: Campo `vetor_estado` adicionado ao response
- Campos legacy (`overall_score`, `area_scores`) mantidos por compatibilidade temporária
- Frontend: UI redesenhada para exibir vetor de estado em vez de score numérico

---

### 3. Estrutura da API de Resultados

**Novos campos adicionados**:
- `vetor_estado` (JSONB): Diagnóstico qualitativo completo
- `memorias_vermelhas` (TEXT[]): Citações literais do usuário revelando conflitos
- `areas_silenciadas` (SMALLINT[]): Áreas não respondidas ou vagas (IDs 1-12)
- `ancoras_sugeridas` (TEXT[]): Das 19 Âncoras Práticas da metodologia

**Campos deprecados** (mantidos por compatibilidade):
- `overall_score`: Substituído por `vetor_estado.estagio_jornada`
- `area_scores`: Substituído por análise qualitativa em `area_analysis`

---

## ✨ Novas Features

### 1. Memórias Vermelhas

Sistema de extração automática de **frases literais** do usuário que revelam:
- Conflitos não dominados
- Padrões de autossabotagem
- Crenças limitantes
- Traumas ou vergonhas não ressignificadas

**Exemplo**:
```json
"memorias_vermelhas": [
  "Não consigo me apresentar em público sem sentir que vou falhar",
  "Sempre fui o filho que não deu certo",
  "Nunca serei bom o suficiente para estar nessa posição"
]
```

**Uso**: Citadas no diagnóstico final para validar hipóteses e gerar reconhecimento

---

### 2. Tratamento de Silêncios

Detecção automática de **áreas não respondidas ou respondidas vagamente**:
- Indica bloqueios emocionais ou cognitivos
- Revela onde o usuário tem resistência em explorar
- Identifica "pontos cegos" narrativos

**Exemplo**:
```json
"areas_silenciadas": [5, 6]  // Vida Amorosa, Vida Familiar
```

---

### 3. As 19 Âncoras Práticas

Sistema de **intervenções concretas** baseado na metodologia:

**Ambiente e Contexto**:
- Referências, Objetos, Ambientes, Grupo

**Comunicação e Expressão**:
- Tom, Vocabulário, Postura, Vestimenta

**Rotina e Estrutura**:
- Rituais Matinais, Rituais Noturnos, Limites, Marcos

**Emoção e Energia**:
- Emoção Projetada, Gestão de Energia, Práticas de Recarga

**Ação e Entrega**:
- Tarefas Identitárias, Microentregas, Exposição Gradual, Testemunhas

**Uso**: Selecionadas automaticamente pelo sistema baseado no diagnóstico

---

### 4. Os 4 Pontos de Entrada

Identificação automática da **porta de intervenção** predominante:
- **Emocional**: Usuário relata estados afetivos → Validar e regular emoção
- **Simbólico**: Falta de sentido ou traição de valores → Ressignificar
- **Comportamental**: Foco em hábitos → Sugerir protocolos concretos
- **Existencial**: Crise de papel de vida → Reposicionar missão

**Impacto**: Determina a linguagem e abordagem da intervenção

---

### 5. Os 4 Níveis de Identidade (Luz Total)

Framework para análise integral da identidade:
1. **Personalidade**: Temperamento, caráter, valores
2. **Cultura**: Gostos, símbolos, crenças pessoais
3. **Realizações**: Resultados e conquistas
4. **Posição**: Como é percebido publicamente

---

### 6. Domínios Temáticos (D1-D6)

Organização das Fases da Jornada em domínios de alavancagem:
- **D1**: Motivações e Conflitos
- **D2**: Crenças, Valores e Princípios
- **D3**: Evolução e Desenvolvimento
- **D4**: Congruência Identidade-Cultura
- **D5**: Transformação de Identidade
- **D6**: Papel na Sociedade

---

### 7. Análise Contextual Enriquecida

Novo módulo `analyzer.py` que processa respostas e extrai:
- Memórias Vermelhas
- Barreiras de autossabotagem
- Capital Simbólico (recursos do usuário)
- Tom emocional dominante (vergonha, indignação, apatia, urgência, tristeza)
- Áreas críticas vs. silenciadas
- Padrões repetidos entre áreas
- Ponto de Entrada predominante
- Palavras recorrentes

---

## 🗄️ Banco de Dados

### Migrações Criadas

1. **`20260217000001_knowledge_chunks_v2.sql`**
   - Adiciona campos: `nivel_maturidade`, `subtipo_crise`, `tipo_conteudo`, `dominio[]`
   - Renomeia: `sintomas` → `sintomas_comportamentais`
   - Índices para performance (tipo_conteudo, dominio, version)

2. **`20260217000002_diagnostic_results_v2.sql`**
   - Adiciona: `vetor_estado`, `memorias_vermelhas`, `areas_silenciadas`, `ancoras_sugeridas`
   - Mantém campos legacy (`overall_score`, `area_scores`) por compatibilidade

3. **`20260217000003_diagnostics_adjust.sql`**
   - Adiciona: `analise_intermediaria` (para armazenar análise do analyzer)
   - Marca `scores_by_area` como legacy

---

### Knowledge Base V2

**Estrutura dos Chunks**:
```json
{
  "content": "...",
  "version": 2,
  "metadata": {
    "motor_motivacional": ["Valor", "Propósito"],
    "estagio_jornada": ["Enraizar", "Desenvolver"],
    "tipo_crise": ["Identidade", "Sentido"],
    "subtipo_crise": "Identidade Herdada",
    "ponto_entrada": "Simbólico",
    "tipo_conteudo": "Âncora Prática",
    "dominio": ["D1", "D2"],
    "sintomas_comportamentais": ["autossabotagem", "paralisia"],
    "tom_emocional": "vergonha",
    "nivel_maturidade": "baixo"
  }
}
```

**Novos tipos de conteúdo**:
- Ponto de Entrada
- Âncora Prática
- Técnica de TCC
- Conceito Metodológico
- Exemplo de Caso

**Total de chunks V2**: ~35 chunks estruturados (vs. ~15 V1)

---

## 🎨 Frontend

### Mudanças na UI

**QuestionCard**:
- Removida lógica de escala (1-5 buttons)
- Apenas textarea para respostas narrativas
- Contador de palavras mantido
- Suporte a `follow_up_hint`

**Result Page**:
Redesenhada completamente com novas seções:

1. **Vetor de Estado** (cards em grid)
   - Motor Dominante, Estágio da Jornada
   - Crise Raiz, Necessidade Atual

2. **Memórias Vermelhas** (citações destacadas)
   - Cards com borda vermelha
   - Frases entre aspas

3. **Âncoras Práticas Sugeridas** (lista numerada)
   - Ações concretas para assunção

4. **Capital Simbólico** (antes "Pontos Fortes")
   - Recursos identificados

5. **Análise do Círculo Narrativo** (expandida)
   - Status visual por área (crítico, atenção, estável, forte)
   - Análise + Key Insight

6. **Plano de Assunção Intencional** (antes "Recomendações")
   - Timeline (imediato, curto, médio prazo)
   - Área relacionada

---

## 🔧 Backend

### Novos Módulos

1. **`app/rag/analyzer.py`**
   - Análise contextual das respostas
   - Extração de Memórias Vermelhas
   - Detecção de silêncios e padrões
   - Identificação de tom emocional e Ponto de Entrada

2. **Prompts Refinados** (`app/rag/generator.py`)
   - Baseados na metodologia refinada
   - Tom "Engenheiro da Alma" (empático-autoritário)
   - Linguagem simbólica: "âncoras", "clímax", "travessia"
   - Foco em TCC e reestruturação cognitiva

3. **RAG Query Template** (`app/rag/retriever.py`)
   - Template estruturado para queries
   - Filtro `version=2` para chunks refinados
   - Busca por tipo de conteúdo (Âncora, TCC, Conceito)

---

### Alterações em Constantes

**`app/core/constants.py`** - Novos conceitos:
- `NIVEIS_IDENTIDADE` (4 níveis)
- `PONTOS_ENTRADA` (4 portas)
- `ANCORAS_PRATICAS` (19 âncoras)
- `DOMINIOS_TEMATICOS` (D1-D6)
- `FATORES_DIAGNOSTICO` (6 fatores do protocolo)
- `CLUSTERS_CRISE` (6 clusters com detalhamento)

---

## 🧪 Testes

Criado `tests/test_reformulacao.py` com cobertura para:
- Estrutura do vetor de estado
- Extração de Memórias Vermelhas
- Detecção de silêncios
- Identificação de tom emocional
- Identificação de Ponto de Entrada
- Barreiras de autossabotagem
- Filtro de version=2 no retrieval
- Estrutura completa do analyzer
- Validação de Âncoras Práticas
- Validação de Pontos de Entrada e Domínios

**Comando**: `pytest tests/test_reformulacao.py -v`

---

## 📦 Deployment

### Variáveis de Ambiente

**Nenhuma nova variável necessária** ✅

As existentes são suficientes:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `OPENAI_API_KEY`
- `RESEND_API_KEY`
- `FRONTEND_URL`

### Passos para Deploy

1. **Aplicar Migrações** (Supabase)
```bash
# Executar na ordem:
supabase/migrations/20260217000001_knowledge_chunks_v2.sql
supabase/migrations/20260217000002_diagnostic_results_v2.sql
supabase/migrations/20260217000003_diagnostics_adjust.sql
```

2. **Seed Knowledge Base V2**
```bash
cd nara-backend
python -m scripts.seed_knowledge_chunks
```

3. **Deploy Backend** (Render)
```bash
# Redeploy automático via Git push
git push origin main
```

4. **Deploy Frontend**
```bash
# Build e deploy
cd nara-frontend
npm run build
# Deploy para seu serviço (Vercel, Netlify, etc.)
```

---

## 🔄 Migração de Dados

### Diagnósticos Antigos

**Estratégia**: Manter diagnósticos V1 como estão, novos diagnósticos usam V2.

**Compatibilidade**:
- Campos legacy (`overall_score`, `area_scores`) mantidos em V2
- Frontend detecta presença de `vetor_estado` para renderizar UI apropriada
- API continua retornando campos legacy para clientes antigos

**Rollback**:
- Flag `USE_LEGACY_SCORING` pode ser adicionada ao config se necessário

---

## 🎯 Próximos Passos

### Curto Prazo
- [ ] Validar chunks V2 com seed completo
- [ ] Testar pipeline end-to-end com diagnóstico real
- [ ] Ajustar prompts baseado em feedback dos primeiros diagnósticos
- [ ] Adicionar visualizações (gráficos) para área_analysis

### Médio Prazo
- [ ] Deprecar campos legacy após validação
- [ ] Criar migration para converter diagnósticos V1 → V2
- [ ] Adicionar exportação PDF com novo layout
- [ ] Implementar sistema de follow-up baseado em âncoras

### Longo Prazo
- [ ] Sistema de acompanhamento (tracking de âncoras)
- [ ] IA conversacional para aprofundar Memórias Vermelhas
- [ ] Suporte a áudio/vídeo para respostas narrativas
- [ ] Dashboard para visualizar evolução temporal

---

## 📚 Referências

- **Documento Base**: `documentos/01_BASE_METODOLOGICA_NARA.md`
- **Metodologia**: Transformação Narrativa (Phellipe Oliveira)
- **Conceitos-chave**: M1, MX, M2X, CN+, Gap MX, Assunção Intencional

---

## 🙏 Créditos

**Metodologia**: Phellipe Oliveira  
**Desenvolvimento**: Equipe NARA  
**Data**: 17 de Fevereiro de 2026

---

## 📞 Suporte

Para dúvidas sobre a reformulação:
- Documentação técnica: `documentos/01_BASE_METODOLOGICA_NARA.md`
- Testes: `nara-backend/tests/test_reformulacao.py`
- Issues: GitHub Issues do projeto
