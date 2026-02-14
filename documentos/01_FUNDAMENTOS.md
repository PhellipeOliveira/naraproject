# 01 - FUNDAMENTOS DO PROJETO NARA

> **Propósito:** Base conceitual, metodologia e decisões técnicas do projeto NARA — o Diagnóstico de Transformação Narrativa baseado nas 12 Áreas Estruturantes do Círculo Narrativo.

---

## 📋 ÍNDICE

1. [Visão Geral e Objetivos](#1-visão-geral-e-objetivos)
2. [Metodologia de Transformação Narrativa](#2-metodologia-de-transformação-narrativa)
   - 2.1 As 12 Áreas Estruturantes
   - 2.2 Motores Motivacionais
   - 2.3 Fases da Jornada
   - 2.4 Conceitos-Chave da Metodologia
   - 2.5 Síntese Metodológica
   - 2.6 Clusters Operacionais de Crise
   - 2.7 Protocolo de Diagnóstico Rápido
3. [Inteligência Contextual via RAG](#3-inteligência-contextual-via-rag)
4. [Stack Técnico Definitivo](#4-stack-técnico-definitivo)
5. [Modelo RAG com Batch Generation](#5-modelo-rag-com-batch-generation)
6. [Análise de Custos com Tokens](#6-análise-de-custos-com-tokens)
7. [Glossário Técnico](#7-glossário-técnico)

---

## 1. VISÃO GERAL E OBJETIVOS

### 🎯 Contexto Crítico

O **Diagnóstico Inicial** é a funcionalidade mais importante do MVP. Ele precisa gerar o efeito "wow" com 20-30 usuários beta ANTES de desenvolver o restante da plataforma. Se o diagnóstico falhar em impressionar, o produto inteiro está em risco.

**Por que isso é crítico?**
- O diagnóstico é o **primeiro contato real** do usuário com o valor da plataforma Nara
- É o momento de **provar** que a metodologia das 12 Áreas da Vida funciona
- Determina se o usuário vai **engajar** suficientemente para criar uma conta
- Fornece **dados qualitativos** essenciais para validar premissas do produto
- É o "gancho" que converte visitantes em usuários pagantes futuros

### 📊 Métricas de Sucesso da Validação

| Métrica | Meta Mínima | Meta Ideal |
|----|----|----|
| Taxa de Conclusão | >50% | >70% |
| NPS do Diagnóstico | >50 | >70 |
| Conversão para Lista de Espera | >40% | >60% |
| Compartilhamento Espontâneo | >10% | >25% |
| Reação Qualitativa | "interessante" | "wow", "revelador" |

### 🎯 Decisões-Chave Tomadas

✅ **MODELO ESCOLHIDO:** RAG com Batch Generation + Progressive Disclosure  
✅ **STACK CONFIRMADO:** Backend Python (FastAPI + LangChain) + Frontend React/Vite  
✅ **VIABILIDADE:** Comprovada através de análise detalhada de custos

---

## 2. METODOLOGIA DE TRANSFORMAÇÃO NARRATIVA

### 2.1 As 12 Áreas Estruturantes (Círculo Narrativo)

O diagnóstico analisa **12 dimensões fundamentais** da vida do usuário, conhecidas na metodologia como **Áreas Estruturantes Específicas**, utilizadas para organizar a memória, identificar conflitos e promover o balanceamento narrativo da personagem:

| # | Área | Descrição | Componentes de Domínio (M2) | Sinais de Conflito (M1) |
|---|----|----|----|----|
| 1 | **Saúde Física** | Manutenção da constituição física e disposição corporal | Vitalidade, sincronia física-metas, gestão de energia | Exaustão crônica, falta de domínio, incongruência corpo-identidade |
| 2 | **Saúde Mental** | Equilíbrio das funções cognitivas e gestão das emoções | Identificação de distorções cognitivas, reestruturação cognitiva | Narrativa caótica, bloqueios por vergonha, ansiedade |
| 3 | **Saúde Espiritual** | Força da fé e convicção interior que impulsionam a manifestação dos propósitos | Convicção na visão MX, alinhamento existencial, paz interior | Vazio existencial, crise de indignidade, desconexão com valores |
| 4 | **Vida Pessoal** | Autoconhecimento, descoberta da própria essência e organização dos interesses | Identidade clara, autonomia, congruência interna | Perdido em narrativas alheias, falta de enredo, vazio |
| 5 | **Vida Amorosa** | Relacionamentos íntimos, convívio afetuoso e dedicação entre parceiros | Identidade preservada na união, atmosfera de apoio, comunicação assertiva | Vínculos superficiais, incongruência de valores, autossabotagem afetiva |
| 6 | **Vida Familiar** | Vínculos de parentesco, valores morais e ritos inicialmente absorvidos | Limites saudáveis, ritos familiares, presença com autonomia | Conflitos de valores, vergonha da origem, papéis impostos |
| 7 | **Vida Social** | Interações comunitárias, seleção de redes de contato e prestígio social | Capital Social, habilidade de Relating, Influência Social | Ambientes estagnados, solidão existencial, medo do julgamento |
| 8 | **Vida Profissional** | Atuação produtiva, domínio de competências técnicas e desenvolvimento da carreira | Maestria técnica, alinhamento missão-propósito, comunicação do diferencial | Atuando papel incongruente, invisibilidade, procrastinação |
| 9 | **Finanças** | Gestão do capital econômico e dos recursos materiais para sustentar a estrutura de vida | Gestão alinhada a valores, capacidade de investimento, estabilidade | Ansiedade, crenças de escassez, falta de recursos para MX |
| 10 | **Educação** | Busca contínua por conhecimento, aprendizagem sistemática e aperfeiçoamento intelectual | Aprendizagem de processos (M3), novos códigos mentais, Growth Mindset | Estagnação, excesso de preparação, dificuldade prática |
| 11 | **Inovação** | Criatividade, pesquisa e desenvolvimento de novas ideias ou formas de resolver problemas | Prototipagem de caminhos (M2X), flexibilidade, curiosidade genuína | Medo de recomeçar, bloqueio criativo, repetição de ciclos |
| 12 | **Lazer** | Atividades de entretenimento, hobbies e uso do tempo livre para recuperação de energia | Rituais de descompressão, hobbies criativos, equilíbrio esforço-descanso | Culpa por descansar, lazer viciado, ausência de pausas |

Essas áreas são fundamentais para que o indivíduo planeje o seu **Círculo Narrativo**.

### 2.2 Motores Motivacionais

Os quatro impulsos que movem o indivíduo — identificar o motor dominante é crucial para direcionar a intervenção:

| Motor | Descrição | Busca | Foco da Intervenção |
|----|----|----|----|
| **Necessidade** | Dor interna que precisa de alívio | Alívio de falta interna | Identificar e aliviar a dor raiz |
| **Valor** | Integridade e coerência com princípios | Coerência interna | Alinhar ações aos valores declarados |
| **Desejo** | Vontade de conquista e realização | Realização externa | Definir metas tangíveis e mensuráveis |
| **Propósito** | Impacto significativo no mundo | Legado e contribuição | Conectar ações ao impacto desejado |

### 2.3 Fases da Jornada

A evolução do indivíduo passa por seis fases de maturação, cada uma vinculada a um Domínio Temático e uma etapa de Assunção Intencional:

```
GERMINAR → ENRAIZAR → DESENVOLVER → FLORESCER → FRUTIFICAR → REALIZAR
```

| Fase | Domínio Temático | Etapa da Assunção | Foco da Ação | Características |
|----|----|----|----|----|
| **Germinar** | D1: Motivações e Conflitos | **Reconhecer** | Nomear o motor dominante | Reconhecendo a insatisfação |
| **Enraizar** | D2: Crenças, Valores e Princípios | **Modelar** | Definir "quem escolho ser" | Buscando valores sólidos |
| **Desenvolver** | D3: Evolução e Desenvolvimento | **Assumir** | Implementar ritos e limites | Praticando novos hábitos |
| **Florescer** | D4: Congruência Identidade-Cultura | **Reforçar** | Validar nova voz e expressão | Expressando singularidade |
| **Frutificar** | D5: Transformação de Identidade | **Reforçar** | Consolidar novos resultados | Entregando resultados |
| **Realizar** | D6: Papel na Sociedade | **Reforçar** | Estabelecer legado | Buscando impacto coletivo |

### 2.4 Conceitos-Chave da Metodologia

| Termo | Definição |
|----|----|
| **M1** | Estado de Crise — situação atual problemática do indivíduo |
| **MX** | Meta Extraordinária — versão aspirada do indivíduo |
| **M2X** | Plano de Assunção Intencional — caminho entre M1 e MX |
| **Gap MX** | Distância entre o estado atual (M1) e a meta (MX) — a medida da transformação necessária |
| **CN (Círculo Narrativo)** | Contexto completo: pessoas, espaços e atmosfera emocional |
| **CN+** | Círculo Narrativo Futuro — configuração aspirada |
| **Memórias Vermelhas** | Conflitos e fatos não dominados que geram autossabotagem |
| **Identidades Herdadas** | Rótulos impostos por família, escola ou cultura |
| **Incongruência Simbólica** | Desalinhamento entre Narrativa (crenças), Identidade (valores) e Hábitos (princípios) |
| **Assunção Intencional** | Processo de 4 etapas: Reconhecer, Modelar, Assumir, Reforçar |
| **Capital Simbólico** | Recursos sociais ou culturais que o usuário já possui |
| **Pontos de Prova** | Barreiras que, superadas, validam a nova identidade |
| **FCU** | Forma, Conteúdo e Uso — como o usuário expressa sua posição atual |

### 2.5 Síntese Metodológica

#### Estrutura do Fluxo Narrativo

O desenvolvimento do indivíduo segue uma hierarquia de quatro camadas fundamentais:

1. **Identidade (Quem sou)** — A base de tudo. Fortalecê-la reduz o ruído em todas as outras camadas. A falta de identidade gera vergonha e confusão.
2. **Sentido (Para onde vou)** — Organiza o tempo, integrando passado, presente e futuro. A falta de sentido gera vazio e estagnação.
3. **Ação Significativa (Como faço)** — Exige estrutura, ritos e limites para sustentar a coerência. A falta de ação gera procrastinação e dispersão.
4. **Conexão Assertiva (Com quem)** — Surge quando as camadas anteriores estão alinhadas, reduzindo o medo do julgamento. A falta de conexão gera solidão e vínculos superficiais.

#### Eixos de Transformação

| Eixo | Representa | Manifestação |
|----|----|----|
| **Narrativa** | Crenças | A história que conta para si mesmo |
| **Identidade** | Valores | Os princípios que defende |
| **Hábitos** | Princípios/Rituais | As ações diárias que pratica |

**Solução definitiva:** Quando a história contada, o valor assumido e o hábito diário dizem a mesma coisa, o sistema torna-se antifrágil. As barreiras tornam-se "pontos de prova" que validam a nova identidade.

### 2.6 Clusters Operacionais de Crise (Diagnóstico M1)

As crises são agrupadas em seis arquétipos principais que permitem identificar o "ponto de entrada" para a intervenção:

| # | Cluster | Sinais | Ponto de Entrada | Domínio Alavanca |
|---|----|----|----|----|
| 1 | **Identidade Raiz** | Identidade herdada, viver papéis impostos, vergonha da história | Simbólico | D1, D2 |
| 2 | **Sentido e Direção** | Futuro opaco, tempo perdido, falta de enredo unificador | Cognitivo | D2, D3 |
| 3 | **Execução e Estrutura** | Procrastinação, paralisia decisória, falta de limites | Comportamental | D3 |
| 4 | **Conexão e Expressão** | Medo do julgamento, invisibilidade simbólica, desconforto com sucesso | Emocional | D4 |
| 5 | **Incongruência Identidade-Cultura** | Choque entre quem a pessoa é e o ambiente/sistema em que vive | Ambiental | D4, D5 |
| 6 | **Transformação de Personagem** | Apego a papéis obsoletos, medo de crescer, dificuldade em encerrar capítulos | Temporal | D5, D6 |

### 2.7 Protocolo de Diagnóstico Rápido

Para perfilar um caso rapidamente, deve-se avaliar seis fatores em uma escala de 0 a 10:

| # | Fator | Pergunta-Chave | Score Baixo Indica |
|---|----|----|----|----|
| 1 | **Autenticidade** | A narrativa é própria ou colonizada? | Identidade herdada |
| 2 | **Integração do Passado** | Existe vergonha ou o passado é capital simbólico? | Memórias vermelhas ativas |
| 3 | **Visão/Enredo** | O futuro tem uma imagem clara? | Crise de sentido |
| 4 | **Coragem/Decisão** | Existe um "ato mínimo" semanal de protagonismo? | Paralisia decisória |
| 5 | **Expressão/Voz** | A comunicação é clara e cadenciada? | Invisibilidade simbólica |
| 6 | **Estrutura/Pertencimento** | Existem ritos, limites e testemunhas significativas? | Falta de âncoras |

#### Dinâmica Temporal nas Crises

| Tempo | Eixo de Intervenção | Foco |
|----|----|----|
| **Passado** | Narrativa | Ressignificar memórias vermelhas |
| **Presente** | Identidade | Estabilizar valores e limites |
| **Futuro** | Hábitos | Materializar a visão MX |

---

## 3. INTELIGÊNCIA CONTEXTUAL VIA RAG

### Princípio Fundamental

> O RAG não serve para responder perguntas do usuário. Ele serve para **revelar o usuário para si mesmo**.

Os documentos no sistema RAG não devem ser tratados como conteúdo, mas como **lentes interpretativas**. Não estamos buscando "o texto certo" — estamos buscando o **enquadramento simbólico mais adequado** ao estado atual da pessoa.

### Estrutura do Chunk para RAG

Cada vetor deve responder implicitamente à pergunta: *"Que tipo de ser humano este texto ajuda a identificar?"*

```json
{
  "content": "Texto explicando crise de identidade herdada...",
  "metadata": {
    "motor_motivacional": "Necessidade | Valor | Desejo | Propósito",
    "estagio_jornada": "Germinar | Enraizar | Desenvolver | Florescer | Frutificar | Realizar",
    "tipo_crise": "Identidade | Sentido | Execução | Conexão | Incongruência | Transformação",
    "subtipo_crise": "Identidade Herdada",
    "dominio": "D1",
    "ponto_entrada": "Simbólico | Cognitivo | Comportamental | Emocional | Ambiental | Temporal",
    "sintomas_comportamentais": ["autossabotagem", "paralisia decisória", "invisibilidade simbólica"],
    "tom_emocional_base": "vergonha | confusão | indignação | apatia | urgência",
    "nivel_maturidade": "baixo | médio | alto"
  }
}
```

### Processo de Determinação do Usuário

#### ETAPA 1 — Coleta Bruta
- Respostas textuais
- Notas numéricas  
- Palavras recorrentes
- Silêncios (áreas não respondidas ou vagas)

#### ETAPA 2 — Análise Pré-RAG
- **Áreas críticas:** Scores baixos, linguagem de exaustão, contradições
- **Padrões repetidos:** Mesmos temas em áreas diferentes, narrativas circulares
- **Tom emocional dominante:** vergonha, indignação, apatia, urgência, tristeza

#### ETAPA 3 — Construção da Query RAG

❌ Query fraca: `"Explorar frustração e estresse"`

✅ Query diagnóstica correta:
```
Indivíduo com alta exigência interna, sensação de traição a si mesmo,
possível crise de identidade herdada, estágio Germinar ou Enraizar,
com urgência tóxica e paralisia decisória.
```

#### ETAPA 4 — Síntese Diagnóstica

O diagnóstico final é um **vetor de estado**, não um rótulo único:

```json
{
  "motor_dominante": "Valor",
  "motor_secundario": "Propósito",
  "estagio_jornada": "Enraizar",
  "crise_raiz": "Identidade Herdada",
  "crises_derivadas": ["Falta de direção", "Paralisia decisória"],
  "ponto_entrada_ideal": "Simbólico",
  "dominios_alavanca": ["D1", "D3"],
  "tom_emocional": "Indignação silenciosa",
  "risco_principal": "Autotraição prolongada",
  "necessidade_atual": "Reescrita identitária + rito de passagem"
}
```

---

## 4. STACK TÉCNICO DEFINITIVO

### Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                          FRONTEND                               │
│  React 18 + TypeScript + Vite                                   │
│  ├── Tailwind CSS (estilização)                                 │
│  ├── shadcn/ui (componentes)                                    │
│  ├── Zustand (state management)                                 │
│  ├── React Hook Form + Zod (formulários)                        │
│  ├── TanStack Query (data fetching)                             │
│  ├── Framer Motion (animações)                                  │
│  └── Recharts (gráfico radar)                                   │
│                         │                                       │
│                         │ HTTP/REST (axios)                     │
│                         ▼                                       │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│               BACKEND (FastAPI + Python)                        │
│  ├── POST /api/diagnostic/start                                 │
│  ├── GET  /api/diagnostic/{id}/questions                        │
│  ├── POST /api/diagnostic/{id}/answer                           │
│  ├── GET  /api/diagnostic/{id}/eligibility                      │
│  ├── POST /api/diagnostic/{id}/finish                           │
│  └── GET  /api/diagnostic/{id}/result                           │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│            DATABASE (Supabase/PostgreSQL)                       │
│  ├── profiles, diagnostics, answers                             │
│  ├── knowledge_chunks (pgvector)                                │
│  ├── feedback, waitlist, email_logs                             │
│  └── RLS (Row Level Security)                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Tecnologias Confirmadas

| Camada | Tecnologia | Justificativa |
|----|----|----|
| **Frontend** | React + Vite | Hot reload rápido, bundle pequeno, simplicidade |
| **UI Library** | shadcn/ui + Tailwind | Componentes customizáveis, design system consistente |
| **State** | Zustand | Simples, sem boilerplate, persistência fácil |
| **Backend** | FastAPI + Python | Async, auto-docs, integração LangChain nativa |
| **RAG/LLM** | LangChain + OpenAI | Framework maduro para RAG, GPT-4o para qualidade |
| **Database** | Supabase + pgvector | PostgreSQL completo, busca vetorial integrada |
| **Email** | Resend | API moderna, templates React Email, alta entrega |
| **Deploy Frontend** | Vercel | Deploy trivial, edge functions, CDN global |
| **Deploy Backend** | Railway/Render | Deploy Python simples, escalável |

### Modelos de IA Utilizados

| Uso | Modelo | Custo (por 1M tokens) |
|----|----|----|
| Geração de perguntas | GPT-4o mini | $0.15 input / $0.60 output |
| Análise final | GPT-4o | $2.50 input / $10.00 output |
| Embeddings | text-embedding-3-small | $0.02 |

---

## 5. MODELO RAG COM BATCH GENERATION

### Por que RAG + Batch Generation?

✅ **Personalização Máxima:** Perguntas adaptadas ao perfil único de cada usuário  
✅ **Qualidade Garantida:** RAG reduz alucinações (contexto fundamentado)  
✅ **UX Otimizada:** Latência concentrada (3-5s entre fases), navegação fluida  
✅ **Escalabilidade:** pgvector suporta milhões de chunks, custo previsível

### Fluxo de Geração

```
┌─────────────────────────────────────────────────────────────────┐
│              FASE 1: BASELINE (15 perguntas fixas)              │
│  • Idênticas para todos os usuários                             │
│  • Custo: R$ 0,00                                               │
└─────────────────────────┬───────────────────────────────────────┘
                          │ Completa 15 respostas
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│           TRIGGER: GERAÇÃO FASE 2 (RAG + LLM)                   │
│  1. Analisar respostas → identificar áreas críticas             │
│  2. Construir query diagnóstica                                 │
│  3. Buscar chunks relevantes (pgvector - top 10)                │
│  4. GPT-4o mini gera 15 perguntas personalizadas                │
│  5. Tempo: 3-5 segundos | Custo: R$ 0,004                       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              FASE 2-4: ADAPTIVE PROBING                         │
│  • 15 perguntas por fase (geradas via RAG)                      │
│  • Progressive Disclosure (uma por vez)                         │
│  • Latência percebida: ZERO após geração                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │ Critério de parada atingido
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              PROCESSAMENTO FINAL (GPT-4o)                       │
│  • Buscar contexto RAG para áreas críticas                      │
│  • Gera relatório detalhado (~2.500 tokens)                     │
│  • Tempo: 5-10 segundos | Custo: R$ 0,17                        │
└─────────────────────────────────────────────────────────────────┘
```

### Critério de Elegibilidade para Finalização

O usuário pode finalizar quando:
- **Mínimo de respostas:** ≥ 40 perguntas respondidas
- **OU Mínimo de palavras:** ≥ 3.500 palavras em respostas textuais
- **E:** Pelo menos 1 resposta em cada uma das 12 áreas (cobertura completa)

---

## 6. ANÁLISE DE CUSTOS COM TOKENS

### Custo por Diagnóstico Completo

| Componente | Tokens | Modelo | Custo (R$) |
|----|----|----|----|
| Fase 1 (Baseline) | 0 | - | R$ 0,00 |
| Fases 2-4 (3×) | ~2.800/fase | GPT-4o mini | R$ 0,012 |
| Relatório Final | ~6.000 | GPT-4o | R$ 0,17 |
| Embeddings (queries) | ~200 | embedding-3-small | ~R$ 0,00 |
| **TOTAL** | | | **R$ 0,182** |

### Projeções

| Cenário | Diagnósticos | Custo Total |
|----|----|----|
| Beta (30 usuários) | 30 | R$ 5,46 |
| Validação (100 usuários) | 100 | R$ 18,20 |
| Escala inicial (1.000) | 1.000 | R$ 182,00 |

### Caminho de Otimização (Futuro)

| Fase | Estratégia | Custo Estimado | Redução |
|----|----|----|----|
| MVP (atual) | GPT-4o mini + GPT-4o | R$ 0,18 | - |
| Otimização | Llama 3.1 8B + GPT-4o mini | R$ 0,05 | -72% |
| Escala | Llama 3.1 70B fine-tuned | R$ 0,01 | -94% |

---

## 7. GLOSSÁRIO TÉCNICO

### Termos de Banco de Dados

| Termo | Definição |
|----|----|
| **UUID** | Universally Unique Identifier — identificador único de 128 bits |
| **PK (Primary Key)** | Chave Primária — identificador único de um registro |
| **FK (Foreign Key)** | Chave Estrangeira — referência a PK de outra tabela |
| **JSONB** | JSON Binary — tipo de dados JSON com armazenamento binário otimizado |
| **VECTOR** | Tipo de dados para armazenar vetores numéricos (pgvector) |
| **RLS** | Row Level Security — segurança em nível de linha |
| **ivfflat** | Inverted File with Flat quantization — tipo de índice para vetores |

### Termos de Normalização

| Termo | Definição |
|----|----|
| **1FN** | Primeira Forma Normal — atributos atômicos, sem grupos repetitivos |
| **2FN** | Segunda Forma Normal — sem dependências parciais |
| **3FN** | Terceira Forma Normal — sem dependências transitivas |
| **BCNF** | Forma Normal de Boyce-Codd — todo determinante é superchave |
| **4FN** | Quarta Forma Normal — sem dependências multivaloradas |
| **5FN** | Quinta Forma Normal — sem dependências de junção |

### Termos de RAG

| Termo | Definição |
|----|----|
| **RAG** | Retrieval-Augmented Generation — geração aumentada por recuperação |
| **Embedding** | Representação vetorial de texto em espaço n-dimensional |
| **Similarity Search** | Busca por similaridade usando distância entre vetores |
| **Cosine Distance** | Distância cosseno — métrica de similaridade entre vetores |
| **Chunk** | Fragmento semântico de texto para processamento |
| **Context Window** | Janela de contexto — limite de tokens do modelo |

### Termos Metodológicos (Transformação Narrativa)

| Termo | Definição |
|----|----|
| **M1** | Estado de Crise — situação atual problemática do indivíduo |
| **MX** | Meta Extraordinária — versão aspirada do indivíduo |
| **M2X** | Plano de Assunção Intencional — caminho entre M1 e MX |
| **Gap MX** | Distância entre o estado atual (M1) e a meta (MX) |
| **CN (Círculo Narrativo)** | Contexto completo: pessoas, espaços e atmosfera emocional |
| **Memórias Vermelhas** | Conflitos e fatos não dominados que geram autossabotagem |
| **Motor Motivacional** | Impulso dominante: Necessidade, Valor, Desejo ou Propósito |
| **Fases da Jornada** | Germinar, Enraizar, Desenvolver, Florescer, Frutificar, Realizar |
| **Domínios Temáticos** | D1 a D6 — áreas de alavancagem para transformação |
| **Assunção Intencional** | Processo de 4 etapas: Reconhecer, Modelar, Assumir, Reforçar |
| **Incongruência Simbólica** | Desalinhamento entre Narrativa, Identidade e Hábitos |

### Termos de Negócio

| Termo | Definição |
|----|----|
| **Progressive Disclosure** | Padrão UX de revelar informação gradualmente |
| **Batch Generation** | Gerar múltiplos itens em uma única chamada |
| **Magic Link** | Link de acesso único enviado por e-mail |
| **NPS** | Net Promoter Score — métrica de satisfação (-100 a +100) |
| **CTR** | Click-Through Rate — taxa de cliques |

---

**Referências Cruzadas:**
- Schema completo do banco: [02_BANCO_DADOS.md](./02_BANCO_DADOS.md)
- Prompts do sistema: [03_PROMPTS_CONHECIMENTO.md](./03_PROMPTS_CONHECIMENTO.md)
- Implementação backend: [04_BACKEND_API.md](./04_BACKEND_API.md)
