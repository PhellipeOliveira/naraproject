# 03 - PROMPTS E BASE DE CONHECIMENTO COMPLETA

> **Propósito:** Documentação exaustiva de todos os prompts do sistema, base de conhecimento para RAG, metodologia completa, catálogo de perguntas e diretrizes de diagnóstico NARA.

---

## 📋 ÍNDICE NAVEGÁVEL

1. [System Prompts Completos](#1-system-prompts-completos)
   - 1.1 [Prompt de Geração de Insights](#11-prompt-geração-de-insights-insight_system_prompt)
   - 1.2 [Prompt de Geração de Perguntas](#12-prompt-geração-de-perguntas-question_generation_system_prompt)
   - 1.3 [Prompt de Análise Final](#13-prompt-análise-final-final_analysis_system_prompt)
   - 1.4 [Prompt de Análise de Respostas](#14-prompt-análise-de-respostas)
   - 1.5 [Template de Query RAG](#15-template-de-query-rag)

2. [Metodologia Completa](#2-metodologia-completa)
   - 2.1 [As 12 Áreas Estruturantes (Descrições Completas)](#21-as-12-áreas-estruturantes-descrições-completas)
   - 2.2 [Motores Motivacionais](#22-motores-motivacionais)
   - 2.3 [Fases da Jornada de Maturação](#23-fases-da-jornada-de-maturação)
   - 2.4 [Clusters de Crise (Diagnóstico M1)](#24-clusters-de-crise-diagnóstico-m1)
   - 2.5 [Estrutura do Fluxo Narrativo](#25-estrutura-do-fluxo-narrativo)
   - 2.6 [Mecanismo de Assunção Intencional](#26-mecanismo-de-assunção-intencional)
   - 2.7 [Protocolo de Diagnóstico Rápido](#27-protocolo-de-diagnóstico-rápido)

3. [Knowledge Base Completa (Chunks RAG)](#3-knowledge-base-completa-chunks-rag)
   - 3.1 [Saúde Física](#31-saúde-física)
   - 3.2 [Saúde Mental](#32-saúde-mental)
   - 3.3 [Saúde Espiritual](#33-saúde-espiritual)
   - 3.4 [Vida Pessoal](#34-vida-pessoal)
   - 3.5 [Vida Amorosa](#35-vida-amorosa)
   - 3.6 [Vida Familiar](#36-vida-familiar)
   - 3.7 [Vida Social](#37-vida-social)
   - 3.8 [Vida Profissional](#38-vida-profissional)
   - 3.9 [Finanças](#39-finanças)
   - 3.10 [Educação](#310-educação)
   - 3.11 [Inovação](#311-inovação)
   - 3.12 [Lazer](#312-lazer)

4. [Inteligência Contextual e RAG](#4-inteligência-contextual-e-rag)
   - 4.1 [Princípios Fundamentais do RAG](#41-princípios-fundamentais-do-rag)
   - 4.2 [Estrutura de Chunks com Metadados](#42-estrutura-de-chunks-com-metadados)
   - 4.3 [Processo de Análise em Etapas](#43-processo-de-análise-em-etapas)
   - 4.4 [Estrutura do Usuário Determinado](#44-estrutura-do-usuário-determinado)
   - 4.5 [Construção de Queries Diagnósticas](#45-construção-de-queries-diagnósticas)

5. [Catálogo de Perguntas](#5-catálogo-de-perguntas)
   - 5.1 [Perguntas Baseline (15 Fixas)](#51-perguntas-baseline-15-fixas)
   - 5.2 [Lógica de Intervenção da IA](#52-lógica-de-intervenção-da-ia)
   - 5.3 [Templates para Fases Adaptativas](#53-templates-para-fases-adaptativas)

6. [Critérios de Elegibilidade e Validação](#6-critérios-de-elegibilidade-e-validação)

7. [Síntese Metodológica para Implementação](#7-síntese-metodológica-para-implementação)

---

## 1. SYSTEM PROMPTS COMPLETOS

### 1.1 Prompt Geração de Insights (INSIGHT_SYSTEM_PROMPT)

```python
INSIGHT_SYSTEM_PROMPT = """
Você é Nara, Engenheira de Mindset e Especialista em Transformação Narrativa. 
Seu objetivo é realizar um Diagnóstico Narrativo profundo que revele a 
incongruência simbólica do usuário e aponte o caminho para a Nova Identidade.

REGRAS CRÍTICAS:
1. IDENTIFIQUE O MOTOR: Determine se a dor ou busca do usuário reflete uma 
   Necessidade (alívio), Valor (coerência), Desejo (conquista) ou Propósito (legado).
2. FOCO NO GAP MX: Identifique a distância real entre o estado atual de crise (M1) 
   e a meta extraordinária aspirada (MX).
3. USE "MEMÓRIAS VERMELHAS": Cite frases reais do usuário entre aspas para 
   expor conflitos não dominados e padrões de autossabotagem identificados.
4. MAPEIE AS 12 ÁREAS: Analise como o conflito em uma área estruturante (ex: Vida 
   Familiar) está gerando ruído em outra (ex: Vida Profissional ou Saúde Mental).
5. LINGUAGEM SIMBÓLICA: Use termos como "âncoras", "pistas de acesso", "clímax" 
   e "círculo narrativo" para reforçar a autoridade do método.
6. EVITE CLICHÊS: Não use autoajuda genérica; use técnicas de TCC (Reestruturação 
   Cognitiva) para questionar a lógica da "velha narrativa".

ESTRUTURA DO INSIGHT:
1. Diagnóstico M1 (A Velha Narrativa): 2-3 frases resumindo o conflito raiz e 
   identificando em qual fase da jornada o usuário se encontra (Germinar a Realizar).
2. Incongruências Simbólicas: Use aspas do usuário para mostrar onde o 
   Eixo Narrativa (crença), Identidade (valores) e Hábitos (princípios) estão desalinhados.
3. Conexões do Círculo Narrativo: Revele como as tensões entre as 12 áreas da vida 
   estão criando o "loop" de estagnação atual.
4. Plano de Assunção Intencional (M2X): Proponha 3 práticas concretas baseadas 
   nos 6 Domínios Temáticos para o usuário começar a "encarnar" a nova personagem agora.
5. Visão de Clímax (MX): Um fechamento poderoso que descreve a versão extraordinária 
   do usuário após a travessia, ancorada na sua motivação real.

Lembre-se: Você é uma Engenheira da Alma. O usuário investiu tempo revelando suas 
dores. Entregue uma reinterpretação da história dele que ele nunca viu antes, 
provocando a decisão de assumir o papel principal.
"""
```

---

### 1.2 Prompt Geração de Perguntas (QUESTION_GENERATION_SYSTEM_PROMPT)

```python
QUESTION_GENERATION_SYSTEM_PROMPT = """
Você é Nara, uma Engenheira de Mindset e Especialista em Transformação Narrativa. 
Sua missão é atuar como facilitadora de travessias internas, ajudando o usuário a 
reescrever a história que conta para si mesmo.

SUA MISSÃO:
Gerar perguntas CIRÚRGICAS e SIMBÓLICAS baseadas na escuta ativa das respostas 
anteriores para identificar a motivação real e o estágio da jornada do usuário.

AS 12 ÁREAS ESTRUTURANTES (CÍRCULO NARRATIVO):
1. Saúde Física - Constituição e disposição corporal.
2. Saúde Mental - Equilíbrio cognitivo e gestão de emoções.
3. Saúde Espiritual - Força da fé e convicção interior.
4. Vida Pessoal - Essência, autoconhecimento e interesses individuais.
5. Vida Amorosa - Relacionamentos íntimos e convívio afetuoso.
6. Vida Familiar - Vínculos de parentesco e valores morais herdados.
7. Vida Social - Interações comunitárias e prestígio social.
8. Vida Profissional - Domínio técnico, carreira e autoridade.
9. Finanças - Gestão de capital e recursos materiais.
10. Educação - Aprendizagem contínua e aperfeiçoamento intelectual.
11. Inovação - Criatividade e resolução de problemas.
12. Lazer - Recuperação de energia e entretenimento.

REGRAS CRÍTICAS DA METODOLOGIA:
1. IDENTIFIQUE O MOTOR: Descubra se a fala reflete Necessidade (dor), Valor (integridade), Desejo (realização) ou Propósito (legado).
2. MAPEIE O CÍRCULO NARRATIVO (CN): Investigue quem são as pessoas, qual o espaço e qual a atmosfera emocional que cercam o conflito.
3. FOCO NO GAP MX: Explore a distância entre o estado atual (M1) e a meta desejada (MX).
4. USE LINGUAGEM SIMBÓLICA: Use metáforas como "pista", "semente", "fruto" e "âncoras".
5. ESCUTA ATIVA: Use mensagens contextuais como "Percebi que sua narrativa sobre [Área] foca em um padrão de [Barreira]...".
6. EVITE clichês genéricos; foque em reestruturação cognitiva (TCC).
"""
```

---

### 1.3 Prompt Análise Final (FINAL_ANALYSIS_SYSTEM_PROMPT)

```python
FINAL_ANALYSIS_SYSTEM_PROMPT = """
Você é Nara, analista sênior em Engenharia de Mindset. Sua missão é entregar um 
Diagnóstico Narrativo que revele a Incongruência Simbólica do usuário e aponte 
o caminho para a Nova Identidade.

SUA MISSÃO:
Identificar onde o "fio narrativo" se rompeu (Identidade -> Sentido -> Ação -> Conexão) 
e propor o reposicionamento da personagem.

REGRAS CRÍTICAS:
1. DIAGNÓSTICO M1: Classifique a dor principal como Crise de Identidade, Sentido, Execução ou Conexão.
2. EIXOS DE TRANSFORMAÇÃO: Analise o desalinhamento entre Narrativa (crenças), Identidade (valores) e Hábitos (princípios).
3. FASE DA JORNADA: Identifique se o usuário está em: Germinar, Enraizar, Desenvolver, Florescer, Frutificar ou Realizar.
4. PLANO DE ASSUNÇÃO INTENCIONAL: Proponha ações para: Reconhecer, Modelar, Assumir e Reforçar.
5. CITE O USUÁRIO: Use aspas para destacar as "Memórias Vermelhas" (M1) mencionadas.
6. TOM: Autoritário mas empático, como um Engenheiro da Alma.

ESTRUTURA DO INSIGHT:
1. A Velha Narrativa (O padrão de M1 identificado).
2. O Motor Dominante (O que realmente move o usuário agora).
3. Alavanca de Domínio Temático (Qual dos 6 domínios de Phellipe Oliveira deve ser ativado).
4. Plano de Assunção (Práticas concretas/âncoras para encarnar a nova identidade).
5. Visão Futura (MX) (A descrição do clímax extraordinário).
"""
```

---

### 1.4 Prompt Análise de Respostas

```python
ANSWER_ANALYSIS_PROMPT = """
Analise as respostas e classifique sob a ótica da Engenharia de Mindset:

1. MEMÓRIAS VERMELHAS (M1): Conflitos e fatos não dominados.
2. BARREIRAS (PONTOS DE PROVA): Autossabotagem, procrastinação ou ambiente hostil.
3. CAPITAL SIMBÓLICO: Recursos sociais ou culturais que o usuário já possui.
4. FCU (Forma, Conteúdo e Uso): Como o usuário expressa sua atual posição.

ANÁLISE DETALHADA:
- Áreas críticas identificadas
- Padrões repetidos nas respostas
- Tom emocional dominante
- Scores preliminares por área

RETORNE:
{
  "memorias_vermelhas": ["frase1", "frase2"],
  "barreiras_identificadas": ["barreira1", "barreira2"],
  "capital_simbolico": ["recurso1", "recurso2"],
  "tom_emocional": "vergonha|indignação|apatia|urgência|tristeza",
  "areas_criticas": [1, 4, 8],
  "padroes_repetidos": ["padrão1", "padrão2"]
}
"""
```

---

### 1.5 Template de Query RAG

```python
RAG_QUERY_TEMPLATE = """
Com base na Metodologia de Phellipe Oliveira, busque estratégias para:

ÁREA DO CÍRCULO NARRATIVO: {areas}
DOMÍNIO TEMÁTICO: {temas}
FASE DA JORNADA: {fase}
CONTEXTO DE CONFLITO: {contexto}

MOTOR MOTIVACIONAL IDENTIFICADO: {motor}
TIPO DE CRISE: {tipo_crise}
TOM EMOCIONAL: {tom_emocional}

Retorne documentos que ajudem a:
1. Identificar o ponto de entrada ideal para intervenção
2. Sugerir práticas alinhadas ao estágio da jornada
3. Revelar conexões entre áreas para diagnóstico integrado
"""
```

---

## 2. METODOLOGIA COMPLETA

### 2.1 As 12 Áreas Estruturantes (Descrições Completas)

As **Áreas Estruturantes Específicas** são segmentos utilizados para organizar a memória, identificar conflitos e promover o balanceamento narrativo da personagem.

| # | Área | Descrição Completa |
|---|------|---------------------|
| 1 | **Saúde Física** | Manutenção da constituição física e disposição corporal necessária para executar as tarefas da jornada. Inclui alimentação, exercício, sono e energia vital. |
| 2 | **Saúde Mental** | Equilíbrio das funções cognitivas e gestão das emoções para evitar sabotagens internas. Abrange clareza mental, regulação emocional e resiliência psicológica. |
| 3 | **Saúde Espiritual** | Força da fé e convicção interior que impulsionam a manifestação dos propósitos da alma. Conexão com algo maior, sentido transcendente, práticas contemplativas. |
| 4 | **Vida Pessoal** | Autoconhecimento, descoberta da própria essência e organização dos interesses individuais. Centro da "Luz Total" da personagem. |
| 5 | **Vida Amorosa** | Relacionamentos íntimos, convívio afetuoso e dedicação entre parceiros. Parcerias que nutrem a construção do Círculo Narrativo Futuro (CN+). |
| 6 | **Vida Familiar** | Vínculos de parentesco, valores morais e ritos inicialmente absorvidos no ambiente doméstico. Onde se encontram as "Identidades Herdadas". |
| 7 | **Vida Social** | Interações comunitárias, seleção de redes de contato e prestígio social. Capital Social e habilidade de Relating. |
| 8 | **Vida Profissional** | Atuação produtiva, domínio de competências técnicas e desenvolvimento da carreira e autoridade (Capital Simbólico). |
| 9 | **Finanças** | Gestão do capital econômico e recursos materiais para sustentar a estrutura de vida e o Círculo Narrativo. |
| 10 | **Educação** | Busca contínua por conhecimento, aprendizagem sistemática e aperfeiçoamento intelectual. Processo de "Modelagem" ativa. |
| 11 | **Inovação** | Criatividade, pesquisa e desenvolvimento de novas ideias ou formas de resolver problemas. Ousadia de testar limites criativos. |
| 12 | **Lazer** | Atividades de entretenimento, hobbies e uso do tempo livre para recuperação de energia e prazer. Rituais de descompressão. |

---

### 2.2 Motores Motivacionais

Os **Motores Motivacionais** são os quatro impulsos fundamentais que movem o indivíduo em sua jornada de transformação:

#### 1. NECESSIDADE (Motor da Dor)
- **Movimento:** Afastar-se da dor
- **Busca:** Alívio de falta interna
- **Frase típica:** "Não aguento mais viver assim"
- **Energia:** Reativa, urgente
- **Risco:** Tomar decisões por desespero
- **Sinal positivo:** Consciência do que não funciona

#### 2. VALOR (Motor da Coerência)
- **Movimento:** Alinhar-se com princípios
- **Busca:** Integridade e coerência interna
- **Frase típica:** "Isso vai contra quem eu quero ser"
- **Energia:** Estável, reflexiva
- **Risco:** Rigidez, dificuldade de adaptação
- **Sinal positivo:** Bússola moral clara

#### 3. DESEJO (Motor da Conquista)
- **Movimento:** Ir em direção ao objetivo
- **Busca:** Realização externa, metas tangíveis
- **Frase típica:** "Eu quero muito alcançar isso"
- **Energia:** Proativa, ambiciosa
- **Risco:** Vazio após conquista, burnout
- **Sinal positivo:** Clareza de objetivos

#### 4. PROPÓSITO (Motor do Legado)
- **Movimento:** Transcender o eu
- **Busca:** Impacto significativo, contribuição
- **Frase típica:** "Quero deixar algo que importa"
- **Energia:** Sustentável, inspiradora
- **Risco:** Negligenciar necessidades pessoais
- **Sinal positivo:** Visão além de si mesmo

---

### 2.3 Fases da Jornada de Maturação

A jornada de transformação narrativa passa por **seis fases de maturação**:

| Fase | Domínio Temático | Etapa da Assunção | Foco da Ação | Sinais Característicos |
|------|------------------|-------------------|--------------|------------------------|
| **GERMINAR** | D1: Motivações e Conflitos | Reconhecer | Nomear o motor dominante | Inquietação difusa, "algo precisa mudar" |
| **ENRAIZAR** | D2: Crenças, Valores e Princípios | Modelar | Definir "quem escolho ser" | Questionamento de crenças herdadas |
| **DESENVOLVER** | D3: Evolução e Desenvolvimento | Assumir | Implementar ritos e limites | Experimentação de novas práticas |
| **FLORESCER** | D4: Congruência Identidade-Cultura | Reforçar | Validar nova voz e expressão | Reconhecimento externo da mudança |
| **FRUTIFICAR** | D5: Transformação de Identidade | Reforçar | Consolidar novos resultados | Consistência natural nos novos padrões |
| **REALIZAR** | D6: Papel na Sociedade | Reforçar | Estabelecer legado | Desejo de contribuir e ensinar |

---

### 2.4 Clusters de Crise (Diagnóstico M1)

As crises são agrupadas em **seis arquétipos principais**:

#### Cluster 1: IDENTIDADE RAIZ
- **Sinais:** Identidade herdada, viver papéis impostos, vergonha da própria história
- **Padrões de fala:** "Sempre fui assim", "Minha família é assim", "Não tenho escolha"
- **Áreas impactadas:** Vida Pessoal, Vida Familiar, Saúde Mental
- **Pergunta-chave:** "Quem você seria se ninguém estivesse olhando?"

#### Cluster 2: SENTIDO E DIREÇÃO
- **Sinais:** Futuro opaco, sensação de tempo perdido, falta de enredo unificador
- **Padrões de fala:** "Não sei o que quero", "Já tentei de tudo", "Nada faz sentido"
- **Áreas impactadas:** Vida Profissional, Educação, Saúde Espiritual
- **Pergunta-chave:** "O que você faria se soubesse que não poderia falhar?"

#### Cluster 3: EXECUÇÃO E ESTRUTURA
- **Sinais:** Procrastinação crônica, paralisia decisória, falta de limites
- **Padrões de fala:** "Vou começar amanhã", "Não consigo dizer não", "Tudo é urgente"
- **Áreas impactadas:** Finanças, Saúde Física, Vida Profissional
- **Pergunta-chave:** "Qual a menor ação que você poderia fazer agora?"

#### Cluster 4: CONEXÃO E EXPRESSÃO
- **Sinais:** Medo do julgamento, invisibilidade simbólica, solidão mesmo acompanhado
- **Padrões de fala:** "Ninguém me entende", "Não quero incomodar", "É melhor ficar quieto"
- **Áreas impactadas:** Vida Social, Vida Amorosa, Vida Pessoal
- **Pergunta-chave:** "O que você deixa de dizer com medo da reação?"

#### Cluster 5: INCONGRUÊNCIA IDENTIDADE-CULTURA
- **Sinais:** Choque entre quem a pessoa é e o ambiente que habita
- **Padrões de fala:** "Não me encaixo", "Aqui não valorizam isso", "Preciso me adaptar"
- **Áreas impactadas:** Vida Social, Vida Profissional, Saúde Mental
- **Pergunta-chave:** "Onde você se sente mais você mesmo?"

#### Cluster 6: TRANSFORMAÇÃO DE PERSONAGEM
- **Sinais:** Apego a papéis obsoletos, medo de crescer, síndrome do impostor
- **Padrões de fala:** "Não sou esse tipo de pessoa", "Quem sou eu para", "Vão descobrir"
- **Áreas impactadas:** Inovação, Vida Profissional, Vida Pessoal
- **Pergunta-chave:** "Qual versão de você está com medo de morrer?"

---

### 2.5 Estrutura do Fluxo Narrativo

O desenvolvimento do indivíduo segue uma **hierarquia de quatro camadas fundamentais**:

```
┌─────────────────────────────────────────────────────────────┐
│  1. IDENTIDADE (Quem sou)                                   │
│     • Base de tudo. Fortalecê-la reduz ruído em outras.     │
│     • Falta: Gera vergonha e confusão                       │
├─────────────────────────────────────────────────────────────┤
│  2. SENTIDO (Para onde vou)                                 │
│     • Organiza o tempo: passado, presente e futuro          │
│     • Falta: Gera vazio e estagnação                        │
├─────────────────────────────────────────────────────────────┤
│  3. AÇÃO SIGNIFICATIVA (Como faço)                          │
│     • Exige estrutura, ritos e limites                      │
│     • Falta: Gera procrastinação e dispersão                │
├─────────────────────────────────────────────────────────────┤
│  4. CONEXÃO ASSERTIVA (Com quem)                            │
│     • Surge quando camadas anteriores estão alinhadas       │
│     • Falta: Gera solidão e vínculos superficiais           │
└─────────────────────────────────────────────────────────────┘
```

**Princípio:** Intervenções devem respeitar a hierarquia. Não adianta trabalhar Conexão se Identidade está em crise.

---

### 2.6 Mecanismo de Assunção Intencional

Para transpor o estado de crise (M1) rumo à meta (MX), utiliza-se o **ciclo de consolidação em quatro etapas**:

| Etapa | Ação | Objetivo | Perguntas-Guia |
|-------|------|----------|----------------|
| **RECONHECER** | Nomear | Dar nome ao motor e à crise | "O que realmente está me movendo?" |
| **MODELAR** | Definir | Escolher referências e nova identidade | "Quem escolho ser a partir de agora?" |
| **ASSUMIR** | Implementar | Criar ritos, limites e microentregas | "Qual pequena ação demonstra essa nova identidade?" |
| **REFORÇAR** | Validar | Consolidar através de repetição e reconhecimento | "Como celebro e protejo essa conquista?" |

---

### 2.7 Protocolo de Diagnóstico Rápido

Para perfilar um caso rapidamente, avalie **seis fatores** em escala de 0 a 10:

| Fator | O que avalia | Pergunta diagnóstica |
|-------|--------------|----------------------|
| **Autenticidade** | A narrativa é própria ou colonizada? | "Essa história é sua ou de alguém?" |
| **Integração do Passado** | Existe vergonha ou o passado é capital? | "O que do seu passado você esconde?" |
| **Visão/Enredo** | O futuro tem imagem clara? | "Você consegue descrever seu futuro?" |
| **Coragem/Decisão** | Existe "ato mínimo" de protagonismo? | "O que você está adiando por medo?" |
| **Expressão/Voz** | A comunicação é clara e cadenciada? | "Você diz o que precisa ser dito?" |
| **Estrutura/Pertencimento** | Existem ritos e testemunhas? | "Quem testemunha sua transformação?" |

**Dinâmica Temporal:**
- **Passado** → Deve ser ressignificado na **Narrativa**
- **Presente** → Deve ser estabilizado pela **Identidade**
- **Futuro** → Deve ser materializado pelos **Hábitos**

---

## 3. KNOWLEDGE BASE COMPLETA (CHUNKS RAG)

### 3.1 Saúde Física

```json
{
  "chapter": "Saúde Física",
  "area_id": 1,
  "section": "Fundamentos Narrativos",
  "content": "A Saúde Física refere-se à manutenção da constituição física e disposição corporal necessária para executar as tarefas da jornada. Na metodologia, o corpo é o principal canal das mensagens e o codificador singular da nova identidade.",
  
  "componentes_dominio_m2": [
    "Vitalidade e vigor para transpor obstáculos",
    "Sincronia entre disposição física e metas (MX)",
    "Gestão de energia como recurso para a 'Força-Tarefa'"
  ],
  
  "sinais_conflito_m1": [
    "Exaustão crônica impedindo a ação (Volição)",
    "Falta de domínio sobre hábitos biológicos básicos",
    "Incongruência entre a imagem física e a identidade pretendida"
  ],
  
  "perguntas_diagnosticas": [
    "De 0 a 5, quanto seu corpo suporta a velocidade da sua visão de futuro?",
    "Sua rotina física atual é uma âncora de progresso ou uma barreira de inércia?",
    "Se seu corpo fosse um personagem, ele seria o protagonista ou um figurante cansado?"
  ],
  
  "conexao_motores": {
    "necessidade": "Busca por alívio de dores ou limitações",
    "desejo": "Busca por performance e vitalidade extraordinária"
  },
  
  "indicadores_positivos": [
    "Rotina de exercícios estabelecida (3+ vezes/semana)",
    "Consciência sobre alimentação e hidratação",
    "Qualidade de sono satisfatória (7-8h)",
    "Energia suficiente para atividades diárias",
    "Relação positiva com o corpo"
  ],
  
  "indicadores_negativos": [
    "Sedentarismo prolongado",
    "Alimentação desordenada",
    "Insônia ou sono de má qualidade",
    "Fadiga crônica inexplicada",
    "Desconexão ou vergonha corporal"
  ],
  
  "padroes_autossabotagem": [
    "Não tenho tempo para cuidar de mim",
    "Quando as coisas acalmarem, vou começar",
    "Meu corpo sempre foi assim",
    "Cuidar dos outros em detrimento de si"
  ]
}
```

---

### 3.2 Saúde Mental

```json
{
  "chapter": "Saúde Mental",
  "area_id": 2,
  "section": "Fundamentos Narrativos",
  "content": "Foca no equilíbrio das funções cognitivas e na gestão das emoções para evitar sabotagens internas. É o campo onde se aplica a TCC (Terapia Cognitivo-Comportamental) para reestruturar a 'velha narrativa'.",
  
  "tecnicas_dominio_m2": [
    "Identificação de Pensamentos Automáticos e Distorções Cognitivas",
    "Reestruturação Cognitiva: trocar a 'vítima' pelo 'autor'",
    "Descatastrofização de cenários de medo"
  ],
  
  "sinais_conflito_m1": [
    "Narrativa interna caótica ou contraditória",
    "Bloqueios narrativos por capítulos ocultos ou vergonha do passado",
    "Ansiedade por falta de linearidade entre passado e futuro"
  ],
  
  "indicadores_positivos": [
    "Capacidade de identificar e nomear emoções",
    "Estratégias saudáveis de regulação emocional",
    "Resiliência frente a adversidades",
    "Clareza mental para tomada de decisões",
    "Momentos de paz interior"
  ],
  
  "indicadores_negativos": [
    "Ansiedade persistente ou ataques de pânico",
    "Sintomas depressivos recorrentes",
    "Pensamentos ruminativos incontroláveis",
    "Dificuldade de concentração severa",
    "Autocrítica destrutiva constante"
  ],
  
  "padroes_autossabotagem": [
    "Sou forte, não preciso de ajuda",
    "É frescura, todo mundo tem problemas",
    "Intelectualizar emoções sem senti-las",
    "Manter-se ocupado para não sentir"
  ],
  
  "perguntas_diagnosticas": [
    "Quais 'frases automáticas' de autocrítica ou medo mais visitam sua mente hoje?",
    "O que você faz quando emoções difíceis aparecem?",
    "Com que frequência você se sente sobrecarregado?",
    "O que sua mente repete quando você está sozinho?"
  ]
}
```

---

### 3.3 Saúde Espiritual

```json
{
  "chapter": "Saúde Espiritual",
  "area_id": 3,
  "section": "Fundamentos Narrativos",
  "content": "Relaciona-se à força da fé e à convicção interior que impulsionam a manifestação dos propósitos da alma. É a âncora que dá sentido à travessia.",
  
  "componentes_dominio_m2": [
    "Convicção plena na visão de futuro (MX)",
    "Alinhamento existencial: saber 'por que tudo isso importa'",
    "Paz interior baseada na integridade (falar, sentir e agir em harmonia)"
  ],
  
  "sinais_conflito_m1": [
    "Vazio existencial ou falta de direção transcendental",
    "Crise de indignidade perante a própria grandeza",
    "Desconexão com os valores inegociáveis da alma"
  ],
  
  "perguntas_diagnosticas": [
    "O que dá sentido e convicção interior à sua existência hoje?",
    "O que você faz quando precisa de conforto em momentos difíceis?",
    "Com que frequência você dedica tempo a práticas que nutrem seu interior?"
  ]
}
```

---

### 3.4 Vida Pessoal

```json
{
  "chapter": "Vida Pessoal",
  "area_id": 4,
  "section": "Fundamentos Narrativos",
  "content": "Concentra-se no autoconhecimento, na descoberta da própria essência e na organização dos interesses individuais. É o centro da 'Luz Total' da personagem.",
  
  "componentes_dominio_m2": [
    "Identidade clara: saber 'quem sou' além dos rótulos",
    "Autonomia: escrever o próprio enredo sem esperar permissão",
    "Congruência entre o mundo interno e a autoimagem"
  ],
  
  "sinais_conflito_m1": [
    "Sensação de estar perdido em meio a narrativas alheias",
    "Falta de enredo que conecte os momentos da vida",
    "Vazio por falta de uma 'Fantasia Pessoal' estimulante"
  ],
  
  "perguntas_diagnosticas": [
    "Se sua vida hoje fosse um livro, qual seria o título do capítulo atual?",
    "De 0 a 5, o quanto você se sente o protagonista da sua própria história?",
    "O que está te impedindo de viver a vida que você realmente deseja?"
  ]
}
```

---

### 3.5 Vida Amorosa

```json
{
  "chapter": "Vida Amorosa",
  "area_id": 5,
  "section": "Fundamentos Narrativos",
  "content": "Abrange os relacionamentos íntimos e o convívio afetuoso. Na metodologia, busca-se parcerias que nutram a construção do Círculo Narrativo Futuro (CN+).",
  
  "componentes_dominio_m2": [
    "Identidade preservada dentro da união",
    "Atmosfera emocional de apoio mútuo e incentivo ao florescimento",
    "Comunicação assertiva de necessidades e limites"
  ],
  
  "sinais_conflito_m1": [
    "Vínculos superficiais que não despertam a autenticidade",
    "Incongruência entre os valores do parceiro e a própria trajetória",
    "Medo de se perder ao crescer, gerando autossabotagem afetiva"
  ],
  
  "perguntas_diagnosticas": [
    "Existe parceria e alinhamento emocional para a construção do seu Círculo Narrativo Futuro?",
    "Quão satisfeito(a) você está com sua vida amorosa/relacionamento atual?"
  ]
}
```

---

### 3.6 Vida Familiar

```json
{
  "chapter": "Vida Familiar",
  "area_id": 6,
  "section": "Fundamentos Narrativos",
  "content": "Trata dos vínculos de parentesco e dos valores morais inicialmente absorvidos. É onde muitas vezes se encontram as 'Identidades Herdadas' que precisam ser ressignificadas.",
  
  "componentes_dominio_m2": [
    "Limites saudáveis entre o 'eu decidido' e as expectativas parentais",
    "Ritos e rituais familiares que nutrem a identidade",
    "Presença e cuidado sem perda da autonomia narrativa"
  ],
  
  "sinais_conflito_m1": [
    "Conflitos de valores inegociáveis com membros do grupo íntimo",
    "Vergonha da origem ou de capítulos não resolvidos",
    "Atuar papéis impostos por tradições obsoletas"
  ],
  
  "perguntas_diagnosticas": [
    "Você sente que vive sob 'identidades herdadas' ou valores familiares que não escolheu conscientemente?",
    "Como é sua relação com sua família de origem e como isso influencia quem você é hoje?"
  ]
}
```

---

### 3.7 Vida Social

```json
{
  "chapter": "Vida Social",
  "area_id": 7,
  "section": "Fundamentos Narrativos",
  "content": "Refere-se às interações com a comunidade e à seleção de redes de contato (Recurso Social). O crescimento ocorre ao orbitar ambientes nutritivos e pessoas 'condutoras'.",
  
  "componentes_dominio_m2": [
    "Capital Social: rede de relações que potencializa o indivíduo",
    "Habilidade de Relating: descobrir as histórias e motivações do outro",
    "Influência Social: falar sobre o que interessa e motiva o público"
  ],
  
  "sinais_conflito_m1": [
    "Ambientes estagnados que puxam para a 'antiga versão'",
    "Solidão existencial mesmo rodeado de pessoas",
    "Medo do julgamento ou de brilhar em público"
  ],
  
  "perguntas_diagnosticas": [
    "Suas interações atuais funcionam como um 'campo gravitacional' que te nutre ou que drena sua energia?",
    "Descreva suas amizades mais significativas. O que elas trazem para sua vida?"
  ]
}
```

---

### 3.8 Vida Profissional

```json
{
  "chapter": "Vida Profissional",
  "area_id": 8,
  "section": "Fundamentos Narrativos",
  "content": "Foca na atuação produtiva, no domínio de competências técnicas e no desenvolvimento da carreira e autoridade (Capital Simbólico). O objetivo é alcançar o Nível de Posição defendido e reconhecido.",
  
  "componentes_dominio_m2": [
    "Maestria técnica e autoridade percebida",
    "Alinhamento entre a tarefa diária (Missão) e o legado (Propósito)",
    "Comunicação clara do diferencial competitivo"
  ],
  
  "sinais_conflito_m1": [
    "Sentimento de estar atuando um papel que não condiz com quem se é",
    "Invisibilidade em espaços de poder e decisão",
    "Procrastinação por falta de clareza sobre o próximo 'clímax' profissional"
  ],
  
  "perguntas_diagnosticas": [
    "Você sente que domina seu ofício ou que está apenas atuando um papel que não condiz com quem você realmente é?",
    "Se dinheiro não fosse questão, você continuaria nesse trabalho?",
    "O que você faz no trabalho que gostaria de fazer mais?"
  ],
  
  "padroes_autossabotagem": [
    "Trabalho é trabalho, não precisa ter significado",
    "Não tenho escolha, preciso do dinheiro",
    "Síndrome do impostor: 'Vão descobrir que não sou tão bom'",
    "Workaholism como fuga de outras áreas"
  ]
}
```

---

### 3.9 Finanças

```json
{
  "chapter": "Finanças",
  "area_id": 9,
  "section": "Fundamentos Narrativos",
  "content": "Envolve a gestão do capital econômico e recursos materiais necessários para sustentar a estrutura de vida e o Círculo Narrativo. O dinheiro é visto como um recurso para a liberdade de ser, fazer e saber.",
  
  "componentes_dominio_m2": [
    "Gestão de capital alinhada aos valores assumidos",
    "Capacidade de investimento na própria transformação e ambiente",
    "Estabilidade financeira para suportar a 'travessia'"
  ],
  
  "sinais_conflito_m1": [
    "Ansiedade por desorganização material",
    "Crenças limitantes de escassez herdadas da família",
    "Falta de recursos para materializar a visão (MX)"
  ],
  
  "perguntas_diagnosticas": [
    "Como está a gestão do seu capital para sustentar a estrutura de vida que você deseja?",
    "Qual é a sua maior preocupação financeira atual?",
    "Como você aprendeu a lidar com dinheiro? Essa educação te serve bem hoje?"
  ]
}
```

---

### 3.10 Educação

```json
{
  "chapter": "Educação",
  "area_id": 10,
  "section": "Fundamentos Narrativos",
  "content": "Diz respeito à busca contínua por conhecimento, aprendizagem sistemática e aperfeiçoamento intelectual. É o processo de 'Modelagem' ativa de novos padrões de sucesso.",
  
  "componentes_dominio_m2": [
    "Aprendizagem de processos (M3) para acelerar a própria jornada",
    "Domínio de novos códigos linguísticos e mentais",
    "Mentalidade de crescimento (Growth Mindset)"
  ],
  
  "sinais_conflito_m1": [
    "Estagnação intelectual e apego a crenças obsoletas",
    "Excesso de preparação sem ir para a ação (Paralisia)",
    "Dificuldade em transformar informação em habilidade prática"
  ],
  
  "perguntas_diagnosticas": [
    "Você está em um processo ativo de modelagem de novos padrões ou sente que seu aprendizado está estagnado?",
    "O que você gostaria de aprender ou desenvolver nos próximos anos? Por quê?"
  ]
}
```

---

### 3.11 Inovação

```json
{
  "chapter": "Inovação",
  "area_id": 11,
  "section": "Fundamentos Narrativos",
  "content": "Capacidade de criar, pesquisar e desenvolver novas formas de resolver problemas ou expressar a identidade. É a ousadia de testar limites criativos.",
  
  "componentes_dominio_m2": [
    "Prototipagem de novos caminhos e ideias (M2X)",
    "Flexibilidade e adaptabilidade diante de perdas ou rupturas",
    "Curiosidade genuína por experiências históricas e subjetivas"
  ],
  
  "sinais_conflito_m1": [
    "Medo de recomeçar ou de construir uma nova identidade",
    "Bloqueio criativo por excesso de autocrítica",
    "Repetição de ciclos exaustivos sem renovação"
  ],
  
  "perguntas_diagnosticas": [
    "Quanto espaço real você reserva para a criatividade e para testar novas formas de resolver seus problemas?",
    "Quando foi a última vez que você experimentou algo completamente novo? Como foi?"
  ]
}
```

---

### 3.12 Lazer

```json
{
  "chapter": "Lazer",
  "area_id": 12,
  "section": "Fundamentos Narrativos",
  "content": "Compreende as atividades de entretenimento e o uso do tempo livre para recuperação de energia e prazer. Serve como ritual de descompressão necessário para manter a constância.",
  
  "componentes_dominio_m2": [
    "Rituais de sensibilidade e propósito que recarregam a volição",
    "Hobbies que expressam a criatividade sem pressão de resultado",
    "Equilíbrio entre esforço e descanso"
  ],
  
  "sinais_conflito_m1": [
    "Culpa por descansar ou automatização da vida",
    "Lazer viciado que drena em vez de nutrir",
    "Ausência de pausas para celebrar microvitórias"
  ],
  
  "perguntas_diagnosticas": [
    "Como você utiliza seu tempo livre para recuperação de energia e rituais de descompressão?",
    "O que você faz para se divertir e recarregar energias? Isso é suficiente?"
  ]
}
```

---

## 4. INTELIGÊNCIA CONTEXTUAL E RAG

### 4.1 Princípios Fundamentais do RAG

> **Princípio Central:** RAG não "responde", ele **revela padrões**. O RAG não serve para responder perguntas do usuário. Ele serve para **revelar o usuário para si mesmo**.

Os documentos não devem ser tratados como conteúdo, mas como **lentes interpretativas**.

**O que buscar:**
- ❌ Não busque "o texto certo"
- ✅ Busque o **enquadramento simbólico** mais adequado ao estado atual da pessoa

---

### 4.2 Estrutura de Chunks com Metadados

Cada vetor no banco deve responder implicitamente à pergunta: **"Que tipo de ser humano este texto ajuda a identificar?"**

**Estrutura Ideal de Metadados:**

```json
{
  "content": "Texto explicando crise de identidade herdada...",
  "metadata": {
    "motor_motivacional": "Necessidade | Valor | Desejo | Propósito",
    "estagio_jornada": "Germinar | Enraizar | Desenvolver | Florescer | Frutificar | Realizar",
    "tipo_crise": "Identidade | Sentido | Execução | Conexão | Incongruência | Transformação",
    "subtipo_crise": "Identidade Herdada",
    "dominio": "D1 | D2 | D3 | D4 | D5 | D6",
    "ponto_entrada": "Emocional | Simbólico | Comportamental",
    "sintomas_comportamentais": [
      "autossabotagem",
      "paralisia decisória",
      "invisibilidade simbólica"
    ],
    "tom_emocional_base": "vergonha | confusão | indignação | apatia | urgência | tristeza",
    "nivel_maturidade": "baixo | médio | alto"
  }
}
```

---

### 4.3 Processo de Análise em Etapas

#### ETAPA 1 — Coleta Bruta (O que o usuário diz)

**Fontes:**
- Respostas textuais
- Notas numéricas
- Palavras recorrentes
- Silêncios (áreas não respondidas ou vagas)

> Aqui não há diagnóstico, apenas matéria-prima.

---

#### ETAPA 2 — Análise Interna (Pré-RAG)

**Extrair:**

1. **Áreas Críticas:**
   - Scores baixos
   - Linguagem de exaustão
   - Contradições ("acredito em X, mas vivo Y")

2. **Padrões Repetidos:**
   - Mesmos temas em áreas diferentes
   - Mesmo sentimento em contextos distintos
   - Narrativas circulares

3. **Tom Emocional Dominante:**
   - Vergonha silenciosa
   - Indignação moral
   - Apatia sofisticada
   - Urgência ansiosa
   - Tristeza resignada

> Aqui você não interpreta ainda, apenas rotula.

---

#### ETAPA 3 — Construção da Query RAG

**Query Fraca (❌):**
```
"Explorar frustração e estresse"
```

**Query Diagnóstica Correta (✅):**
```
Indivíduo com alta exigência interna, sensação de traição a si mesmo,
possível crise de identidade herdada, estágio Germinar ou Enraizar,
com urgência tóxica e paralisia decisória.
```

> A query deve misturar **sintomas + hipótese de estrutura interna**.

---

#### ETAPA 4 — O RAG Devolve Hipóteses

O retriever retorna documentos que representam:
- Possíveis motores dominantes
- Possíveis estágios da jornada
- Possíveis tipos de crise
- Possíveis pontos de entrada

**Regra:** Não use tudo. Cruze **recorrência + coerência**.

---

### 4.4 Estrutura do Usuário Determinado

O diagnóstico não é um rótulo único, é um **vetor de estado**:

```json
{
  "motor_dominante": "Valor",
  "motor_secundario": "Propósito",
  "estagio_jornada": "Enraizar",
  "crise_raiz": "Identidade Herdada",
  "crises_derivadas": [
    "Falta de direção",
    "Paralisia decisória"
  ],
  "ponto_entrada_ideal": "Simbólico",
  "dominios_alavanca": ["D1", "D3"],
  "tom_emocional": "Indignação silenciosa",
  "risco_principal": "Autotraição prolongada",
  "necessidade_atual": "Reescrita identitária + rito de passagem"
}
```

> Isso é **Inteligência Contextual real**.

---

### 4.5 Construção de Queries Diagnósticas

**Benefícios do sistema bem estruturado:**

✔ **Fazer perguntas certas** (não genéricas)
- Sabe onde tocar
- Sabe onde não tocar ainda
- Sabe qual linguagem usar

✔ **Gerar análises profundas** sem parecer "místico"
- Cada insight é rastreável
- Coerente com a metodologia
- Alinhado ao estágio

✔ **Evitar intervenções prematuras**
- Não propor ação para quem está em crise simbólica
- Não propor sentido para quem está em colapso emocional

---

## 5. CATÁLOGO DE PERGUNTAS

### 5.1 Perguntas Baseline (15 Fixas)

**Critério:** Estas perguntas são idênticas para todos os usuários na Fase 1.

#### Perguntas para as 12 Áreas da Vida

| # | Área | Pergunta Completa |
|---|------|-------------------|
| 1 | **Vida Pessoal** | Se sua vida hoje fosse um livro, qual seria o título do capítulo atual? De 0 a 5, o quanto você se sente de fato o **protagonista** da sua própria história? |
| 2 | **Saúde Física** | Como você avalia sua constituição e disposição corporal para os desafios da sua jornada? (0 = exausto, 5 = plena vitalidade). Descreva como o seu corpo tem reagido ao seu ritmo atual. |
| 3 | **Saúde Mental** | Quais **"frases automáticas"** de autocrítica ou medo mais visitam sua mente hoje? (0 = mente caótica, 5 = equilíbrio total). |
| 4 | **Saúde Espiritual** | O que dá sentido e **convicção interior** à sua existência hoje? (0 = perdido/sem fé, 5 = convicção plena). |
| 5 | **Vida Familiar** | Você sente que vive sob **"identidades herdadas"** ou valores familiares que não escolheu conscientemente? (0 = prisioneiro de rótulos, 5 = autêntico). |
| 6 | **Vida Amorosa** | Existe parceria e alinhamento emocional para a construção do seu **Círculo Narrativo Futuro (CN+)**? (0 = insatisfeito, 5 = pleno). |
| 7 | **Vida Social** | Suas interações atuais funcionam como um **"campo gravitacional"** que te nutre ou que drena sua energia? (0 = ambiente tóxico, 5 = rede nutritiva). |
| 8 | **Vida Profissional** | Você sente que domina seu ofício ou que está apenas atuando um papel que não condiz com quem você realmente é? (0 = frustrado, 5 = realizado). |
| 9 | **Finanças** | Como está a gestão do seu capital para sustentar a estrutura de vida que você deseja? (0 = caos/preocupação, 5 = total controle). |
| 10 | **Educação** | Você está em um processo ativo de **modelagem** de novos padrões ou sente que seu aprendizado está estagnado? (0 = estagnado, 5 = aprendiz contínuo). |
| 11 | **Inovação** | Quanto espaço real você reserva para a **criatividade** e para testar novas formas de resolver seus problemas? (0 = nenhum espaço, 5 = fluxo constante). |
| 12 | **Lazer** | Como você utiliza seu tempo livre para recuperação de energia e **rituais de descompressão**? (0 = inexistente, 5 = equilibrado). |

#### Perguntas Generalistas (Sondagem de Motor e Gap MX)

| # | Foco | Pergunta |
|---|------|----------|
| 13 | **Identificação do Motor** | O que mais te move hoje: o alívio de uma dor (**Necessidade**), a busca por coerência (**Valor**), a conquista de algo (**Desejo**) ou o impacto no mundo (**Propósito**)? |
| 14 | **Conflito Raiz (M1)** | Se você pudesse transpor um **único conflito** central hoje para alcançar sua meta extraordinária, qual seria esse obstáculo? |
| 15 | **Visão de Clímax (MX/M2X)** | Descreva sua versão extraordinária daqui a 12 meses. O que essa pessoa faz no dia a dia que você, na sua versão atual, ainda não consegue realizar? |

---

### 5.2 Lógica de Intervenção da IA

Após as respostas baseline, a inteligência contextual deve:

1. **Analisar Incongruências Simbólicas**
   - Exemplo: Usuário pontua alto em "Vida Profissional" mas revela "frases automáticas" de falha na "Saúde Mental"

2. **Gerar Perguntas que Cruzem Eixos**
   - Identificar a **Barreira** oculta entre áreas correlacionadas

3. **Mapear o Gap MX**
   - Distância entre a narrativa vivida e a narrativa escolhida

4. **Identificar Ponto de Entrada**
   - Emocional, Simbólico ou Comportamental

---

### 5.3 Templates para Fases Adaptativas

#### Template: Alta Autocrítica Identificada

```json
{
  "trigger_pattern": "autocritica_alta",
  "templates": [
    {
      "area_id": 4,
      "type": "open_ended",
      "text": "Você mencionou que {citação_resposta_anterior}. De onde vem essa voz crítica? Ela soa como alguém que você conhece?",
      "explanation": "Explorar origem da autocrítica para identificar introjeção"
    },
    {
      "area_id": 2,
      "type": "open_ended",
      "text": "Se você falasse consigo mesmo(a) como fala com alguém que ama, o que diria sobre essa situação?",
      "explanation": "Gerar compaixão autodirigida"
    }
  ]
}
```

#### Template: Conflito Trabalho-Família

```json
{
  "trigger_pattern": "conflito_trabalho_familia",
  "templates": [
    {
      "area_id": 6,
      "type": "open_ended",
      "text": "Você mencionou tensão entre demandas profissionais e familiares. Quando você prioriza trabalho, o que sente? E quando prioriza família?",
      "explanation": "Mapear culpa e valores conflitantes"
    },
    {
      "area_id": 8,
      "type": "multiple_choice",
      "text": "Se você tivesse que reduzir 20% da sua carga de trabalho, qual seria o primeiro impacto?",
      "options": ["Financeiro", "Reconhecimento", "Identidade", "Relacionamentos", "Outro"]
    }
  ]
}
```

#### Template: Falta de Propósito

```json
{
  "trigger_pattern": "falta_proposito",
  "templates": [
    {
      "area_id": 3,
      "type": "open_ended",
      "text": "Descreva um momento em que você sentiu que estava fazendo exatamente o que deveria fazer. O que tornava esse momento especial?",
      "explanation": "Buscar experiências de flow e significado"
    },
    {
      "area_id": 11,
      "type": "open_ended",
      "text": "Se você soubesse que teria sucesso garantido, que projeto ou causa você abraçaria?",
      "explanation": "Remover medo do fracasso para revelar desejo autêntico"
    }
  ]
}
```

#### Template: Área com Baixa Cobertura (< 2 respostas)

**Saúde Espiritual:**
```json
{
  "area_id": 3,
  "templates": [
    {
      "type": "multiple_choice",
      "text": "Com que frequência você dedica tempo a práticas que nutrem seu interior (meditação, oração, contemplação, contato com a natureza)?",
      "options": ["Diariamente", "Semanalmente", "Mensalmente", "Raramente", "Nunca"]
    },
    {
      "type": "open_ended",
      "text": "O que você faz quando precisa de conforto em momentos difíceis? Isso funciona?"
    }
  ]
}
```

**Finanças:**
```json
{
  "area_id": 9,
  "templates": [
    {
      "type": "open_ended",
      "text": "Qual é a sua maior preocupação financeira atual? O que você já tentou fazer a respeito?"
    },
    {
      "type": "open_ended",
      "text": "Como você aprendeu a lidar com dinheiro? Essa educação te serve bem hoje?"
    },
    {
      "type": "multiple_choice",
      "text": "Se você recebesse inesperadamente 3 meses de salário, qual seria sua primeira ação?",
      "options": ["Pagar dívidas", "Poupar/investir", "Realizar um desejo", "Ajudar alguém", "Não sei"]
    }
  ]
}
```

---

## 6. CRITÉRIOS DE ELEGIBILIDADE E VALIDAÇÃO

### Critérios para Finalização do Diagnóstico

O diagnóstico pode ser finalizado quando **UMA** das condições for atendida:

| Critério | Valor Mínimo |
|----------|--------------|
| **Número de respostas** | 40 respostas mínimas |
| **Volume textual** | 3.500 palavras mínimas |

### Limites do Sistema

| Parâmetro | Limite |
|-----------|--------|
| Total de fases | Máximo 4 fases |
| Perguntas por fase | 15 perguntas |
| Total máximo de perguntas | 60 perguntas |

### Validação de Elegibilidade

```python
def check_eligibility(total_responses, total_words):
    """
    Verifica se o diagnóstico pode ser finalizado.
    
    Returns:
        tuple: (is_eligible, reason)
    """
    if total_responses >= 40:
        return True, "Mínimo de 40 respostas atingido"
    
    if total_words >= 3500:
        return True, "Mínimo de 3.500 palavras atingido"
    
    return False, f"Necessário: 40 respostas (atual: {total_responses}) OU 3.500 palavras (atual: {total_words})"
```

---

## 7. SÍNTESE METODOLÓGICA PARA IMPLEMENTAÇÃO

### Essência da Metodologia

> Toda crise é um sintoma da **distância entre a narrativa vivida e a narrativa escolhida**, manifestada como um **Gap MX** (expectativa vs. resultado).

A transformação ocorre através do alinhamento entre:
- **Narrativa** (crenças)
- **Identidade** (valores)
- **Hábitos** (princípios/rituais)

### Solução Definitiva

**Alinhamento do Eixo:** A solução definitiva é a **remoção da incongruência simbólica**.

Quando a história contada, o valor assumido e o hábito diário dizem a mesma coisa, o sistema torna-se **antifrágil**: as barreiras tornam-se "pontos de prova" que validam a nova identidade.

### Resumo para Intervenção

1. **Identifique o Ponto de Entrada** da crise:
   - Emocional
   - Simbólico
   - Comportamental

2. **Determine qual Domínio Temático** (D1 a D6) possui a maior alavanca para reorganizar a energia

3. **Respeite a hierarquia** do fluxo narrativo:
   - Identidade → Sentido → Ação → Conexão

4. **Aplique o ciclo de Assunção Intencional**:
   - Reconhecer → Modelar → Assumir → Reforçar

5. **Use linguagem simbólica** da metodologia para reforçar autoridade

### Tabela de Referência Rápida

| Se identificar... | Foque em... | Domínio | Etapa |
|-------------------|-------------|---------|-------|
| Vergonha/Confusão | Identidade | D1-D2 | Reconhecer/Modelar |
| Vazio/Estagnação | Sentido | D2-D3 | Modelar/Assumir |
| Procrastinação/Dispersão | Ação | D3-D4 | Assumir/Reforçar |
| Solidão/Invisibilidade | Conexão | D4-D6 | Reforçar |

---

## 📚 REFERÊNCIAS CRUZADAS

- **Fundamentos metodológicos:** [01_FUNDAMENTOS.md](./01_FUNDAMENTOS.md)
- **Schema das tabelas:** [02_BANCO_DADOS.md](./02_BANCO_DADOS.md)
- **Implementação Backend:** [04_BACKEND_API.md](./04_BACKEND_API.md)
- **Fluxo do Diagnóstico:** [05_FLUXO_DIAGNOSTICO.md](./05_FLUXO_DIAGNOSTICO.md)

---

*Documento gerado com base na metodologia de Transformação Narrativa de Phellipe Oliveira.*
*Última atualização: Fevereiro 2026*
