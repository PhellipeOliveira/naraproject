# 01 - BASE METODOLÓGICA DO PROJETO NARA

> **Propósito:** Base conceitual completa e metodologia do Diagnóstico de Transformação Narrativa baseado nas 12 Áreas Estruturantes do Círculo Narrativo.

---

## 📋 ÍNDICE COMPLETO

### PARTE I: FUNDAMENTOS CONCEITUAIS
- [1. As 12 Áreas Estruturantes](#1-as-12-áreas-estruturantes)
- [2. Motores Motivacionais](#2-motores-motivacionais)
- [3. Fases da Jornada](#3-fases-da-jornada)
- [4. Conceitos-Chave da Metodologia](#4-conceitos-chave-da-metodologia)
- [5. Os 4 Níveis de Identidade (Luz Total)](#5-os-4-níveis-de-identidade-luz-total)
- [6. Os 4 Pontos de Entrada (Portas de Intervenção)](#6-os-4-pontos-de-entrada-portas-de-intervenção)
- [7. Síntese Metodológica](#7-síntese-metodológica)
- [8. Glossário Metodológico Completo](#8-glossário-metodológico-completo)

### PARTE II: DIAGNÓSTICO E CLUSTERS
- [1. Clusters Operacionais de Crise](#clusters-1-clusters-operacionais-de-crise)
- [2. Protocolo de Diagnóstico Rápido](#clusters-2-protocolo-de-diagnóstico-rápido)
- [3. Mecanismo de Assunção Intencional](#clusters-3-mecanismo-de-assunção-intencional)
- [4. Ferramental da TCC para a IA](#clusters-4-ferramental-da-tcc-para-a-ia)
- [5. As 19 Âncoras Práticas (Assunção Intencional)](#clusters-5-as-19-âncoras-práticas-assunção-intencional)

### PARTE III: INTELIGÊNCIA CONTEXTUAL E RAG
- [1. Princípios Fundamentais](#rag-1-princípios-fundamentais)
- [2. Construção de Inteligência Contextual](#rag-2-construção-de-inteligência-contextual)
- [3. Estrutura do Chunk para RAG](#rag-3-estrutura-do-chunk-para-rag)
- [4. Processo de Determinação do Usuário](#rag-4-processo-de-determinação-do-usuário)
- [5. Templates de Query RAG](#rag-5-templates-de-query-rag)
- [6. Psicografia do Usuário](#rag-6-psicografia-do-usuário)
- [7. Refinamentos para RAG](#rag-7-refinamentos-para-rag)

### PARTE IV: PROMPTS DO SISTEMA
- [1. Prompt de Geração de Insights](#prompts-1-prompt-de-geração-de-insights)
- [2. Prompt de Geração de Perguntas](#prompts-2-prompt-de-geração-de-perguntas)
- [3. Prompt de Análise Final](#prompts-3-prompt-de-análise-final)
- [4. Prompts Auxiliares](#prompts-4-prompts-auxiliares)

### PARTE V: KNOWLEDGE BASE (CHUNKS RAG)
- [Knowledge Base Estruturada por Área](#knowledge-base-estruturada)

### PARTE VI: CATÁLOGO DE PERGUNTAS
- [1. Perguntas Baseline (Abertas e Narrativas)](#perguntas-1-perguntas-baseline)
- [2. Lógica de Intervenção da IA](#perguntas-2-lógica-de-intervenção-da-ia)
- [3. Templates para Fases Adaptativas](#perguntas-3-templates-para-fases-adaptativas)

### PARTE VII: OPERAÇÃO E VALIDAÇÃO
- [1. Critérios de Elegibilidade](#operacao-1-critérios-de-elegibilidade)
- [2. Síntese Metodológica para Implementação](#operacao-2-síntese-metodológica-para-implementação)

---

# PARTE I: FUNDAMENTOS CONCEITUAIS

---

## 1. As 12 Áreas Estruturantes

O diagnóstico analisa **12 dimensões fundamentais** da vida do usuário, conhecidas na metodologia como **Áreas Estruturantes Específicas**, utilizadas para organizar a memória, identificar conflitos e promover o balanceamento narrativo da personagem:

| # | Área | Descrição | Componentes de Domínio (M2) | Sinais de Conflito (M1) |
|---|----|----|----|----|
| 1 | **Saúde Física** | Manutenção da constituição física e disposição corporal necessária para executar as tarefas da jornada. O corpo é o principal canal das mensagens e o codificador singular da nova identidade. | Vitalidade e vigor para transpor obstáculos; Sincronia entre disposição física e metas (MX); Gestão de energia como recurso para a 'Força-Tarefa'. | Exaustão crônica impedindo a ação (Volição); Falta de domínio sobre hábitos biológicos básicos; Incongruência entre a imagem física e a identidade pretendida. |
| 2 | **Saúde Mental** | Equilíbrio das funções cognitivas e gestão das emoções para evitar sabotagens internas. Campo onde se aplica a TCC (Terapia Cognitivo-Comportamental) para reestruturar a 'velha narrativa'. | Identificação de Pensamentos Automáticos e Distorções Cognitivas; Reestruturação Cognitiva: trocar a 'vítima' pelo 'autor'; Descatastrofização de cenários de medo. | Narrativa interna caótica ou contraditória; Bloqueios narrativos por capítulos ocultos ou vergonha do passado; Ansiedade por falta de linearidade entre passado e futuro. |
| 3 | **Saúde Espiritual** | Força da fé e convicção interior que impulsionam a manifestação dos propósitos da alma. A âncora que dá sentido à travessia. | Convicção plena na visão de futuro (MX); Alinhamento existencial: saber 'por que tudo isso importa'; Paz interior baseada na integridade (falar, sentir e agir em harmonia). | Vazio existencial ou falta de direção transcendental; Crise de indignidade perante a própria grandeza; Desconexão com os valores inegociáveis da alma. |
| 4 | **Vida Pessoal** | Autoconhecimento, descoberta da própria essência e organização dos interesses individuais. Centro da 'Luz Total' da personagem. | Identidade clara: saber 'quem sou' além dos rótulos; Autonomia: escrever o próprio enredo sem esperar permissão; Congruência entre o mundo interno e a autoimagem. | Sensação de estar perdido em meio a narrativas alheias; Falta de enredo que conecte os momentos da vida; Vazio por falta de uma 'Fantasia Pessoal' estimulante. |
| 5 | **Vida Amorosa** | Relacionamentos íntimos, convívio afetuoso e dedicação entre parceiros. Busca-se parcerias que nutram a construção do Círculo Narrativo Futuro (CN+). | Identidade preservada dentro da união; Atmosfera emocional de apoio mútuo e incentivo ao florescimento; Comunicação assertiva de necessidades e limites. | Vínculos superficiais que não despertam a autenticidade; Incongruência entre os valores do parceiro e a própria trajetória; Medo de se perder ao crescer, gerando autossabotagem afetiva. |
| 6 | **Vida Familiar** | Vínculos de parentesco, valores morais e ritos inicialmente absorvidos no ambiente doméstico. Onde muitas vezes se encontram as 'Identidades Herdadas' que precisam ser ressignificadas. | Limites saudáveis entre o 'eu decidido' e as expectativas parentais; Ritos e rituais familiares que nutrem a identidade; Presença e cuidado sem perda da autonomia narrativa. | Conflitos de valores inegociáveis com membros do grupo íntimo; Vergonha da origem ou de capítulos não resolvidos; Atuar papéis impostos por tradições obsoletas. |
| 7 | **Vida Social** | Interações comunitárias, seleção de redes de contato e prestígio social alcançado no campo social. O crescimento ocorre ao orbitar ambientes nutritivos e pessoas 'condutoras'. | Capital Social: rede de relações que potencializa o indivíduo; Habilidade de Relating: descobrir as histórias e motivações do outro; Influência Social: falar sobre o que interessa e motiva o público. | Ambientes estagnados que puxam para a 'antiga versão'; Solidão existencial mesmo rodeado de pessoas; Medo do julgamento ou de brilhar em público. |
| 8 | **Vida Profissional** | Atuação produtiva, domínio de competências técnicas e desenvolvimento da carreira e autoridade (Capital Simbólico). Objetivo: alcançar o Nível de Posição defendido e reconhecido. | Maestria técnica e autoridade percebida; Alinhamento entre a tarefa diária (Missão) e o legado (Propósito); Comunicação clara do diferencial competitivo. | Sentimento de estar atuando um papel que não condiz com quem se é; Invisibilidade em espaços de poder e decisão; Procrastinação por falta de clareza sobre o próximo 'clímax' profissional. |
| 9 | **Finanças** | Gestão do capital econômico e recursos materiais necessários para sustentar a estrutura de vida e o Círculo Narrativo. O dinheiro é visto como um recurso para a liberdade de ser, fazer e saber. | Gestão de capital alinhada aos valores assumidos; Capacidade de investimento na própria transformação e ambiente; Estabilidade financeira para suportar a 'travessia'. | Ansiedade por desorganização material; Crenças limitantes de escassez herdadas da família; Falta de recursos para materializar a visão (MX). |
| 10 | **Educação** | Busca contínua por conhecimento, aprendizagem sistemática e aperfeiçoamento intelectual. Processo de 'Modelagem' ativa de novos padrões de sucesso. | Aprendizagem de processos (M3) para acelerar a própria jornada; Domínio de novos códigos linguísticos e mentais; Mentalidade de crescimento (Growth Mindset). | Estagnação intelectual e apego a crenças obsoletas; Excesso de preparação sem ir para a ação (Paralisia); Dificuldade em transformar informação em habilidade prática. |
| 11 | **Inovação** | Criatividade, pesquisa e desenvolvimento de novas ideias ou formas de resolver problemas. Ousadia de testar limites criativos. | Prototipagem de novos caminhos e ideias (M2X); Flexibilidade e adaptabilidade diante de perdas ou rupturas; Curiosidade genuína por experiências históricas e subjetivas. | Medo de recomeçar ou de construir uma nova identidade; Bloqueio criativo por excesso de autocrítica; Repetição de ciclos exaustivos sem renovação. |
| 12 | **Lazer** | Atividades de entretenimento, hobbies e uso do tempo livre para recuperação de energia e prazer. Serve como ritual de descompressão necessário para manter a constância. | Rituais de sensibilidade e propósito que recarregam a volição; Hobbies que expressam a criatividade sem pressão de resultado; Equilíbrio entre esforço e descanso. | Culpa por descansar ou automatização da vida; Lazer viciado que drena em vez de nutrir; Ausência de pausas para celebrar microvitórias. |

Essas áreas são fundamentais para que o indivíduo planeje o seu **Círculo Narrativo**.

---

## 2. Motores Motivacionais

Os **Motores Motivacionais** são os quatro impulsos fundamentais que movem o indivíduo em sua jornada de transformação. Identificar o motor dominante é crucial para direcionar a intervenção:

### 2.1 NECESSIDADE (Motor da Dor)

| Dimensão | Descrição |
|----------|-----------|
| **Movimento** | Afastar-se da dor |
| **Busca** | Alívio de falta interna |
| **Frase típica** | "Não aguento mais viver assim" |
| **Energia** | Reativa, urgente |
| **Risco** | Tomar decisões por desespero |
| **Sinal positivo** | Consciência do que não funciona |
| **Foco da Intervenção** | Identificar e aliviar a dor raiz |

### 2.2 VALOR (Motor da Coerência)

| Dimensão | Descrição |
|----------|-----------|
| **Movimento** | Alinhar-se com princípios |
| **Busca** | Integridade e coerência interna |
| **Frase típica** | "Isso vai contra quem eu quero ser" |
| **Energia** | Estável, reflexiva |
| **Risco** | Rigidez, dificuldade de adaptação |
| **Sinal positivo** | Bússola moral clara |
| **Foco da Intervenção** | Alinhar ações aos valores declarados |

### 2.3 DESEJO (Motor da Conquista)

| Dimensão | Descrição |
|----------|-----------|
| **Movimento** | Ir em direção ao objetivo |
| **Busca** | Realização externa, metas tangíveis |
| **Frase típica** | "Eu quero muito alcançar isso" |
| **Energia** | Proativa, ambiciosa |
| **Risco** | Vazio após conquista, burnout |
| **Sinal positivo** | Clareza de objetivos |
| **Foco da Intervenção** | Definir metas tangíveis e mensuráveis |

### 2.4 PROPÓSITO (Motor do Legado)

| Dimensão | Descrição |
|----------|-----------|
| **Movimento** | Transcender o eu |
| **Busca** | Impacto significativo, contribuição |
| **Frase típica** | "Quero deixar algo que importa" |
| **Energia** | Sustentável, inspiradora |
| **Risco** | Negligenciar necessidades pessoais |
| **Sinal positivo** | Visão além de si mesmo |
| **Foco da Intervenção** | Conectar ações ao impacto desejado |

---

## 3. Fases da Jornada

A evolução do indivíduo passa por **seis fases de maturação**, cada uma vinculada a um Domínio Temático e uma etapa de Assunção Intencional:

```
GERMINAR → ENRAIZAR → DESENVOLVER → FLORESCER → FRUTIFICAR → REALIZAR
```

| Fase | Domínio Temático | Etapa da Assunção | Foco da Ação | Sinais Característicos |
|----|----|----|----|----|
| **GERMINAR** | D1: Motivações e Conflitos | **Reconhecer** | Nomear o motor dominante | Inquietação difusa, "algo precisa mudar", reconhecendo a insatisfação |
| **ENRAIZAR** | D2: Crenças, Valores e Princípios | **Modelar** | Definir "quem escolho ser" | Questionamento de crenças herdadas, buscando valores sólidos |
| **DESENVOLVER** | D3: Evolução e Desenvolvimento | **Assumir** | Implementar ritos e limites | Experimentação de novas práticas, praticando novos hábitos |
| **FLORESCER** | D4: Congruência Identidade-Cultura | **Reforçar** | Validar nova voz e expressão | Reconhecimento externo da mudança, expressando singularidade |
| **FRUTIFICAR** | D5: Transformação de Identidade | **Reforçar** | Consolidar novos resultados | Consistência natural nos novos padrões, entregando resultados |
| **REALIZAR** | D6: Papel na Sociedade | **Reforçar** | Estabelecer legado | Desejo de contribuir e ensinar, buscando impacto coletivo |

---

## 4. Conceitos-Chave da Metodologia

| Termo | Definição |
|----|----|
| **M1** | Estado de Crise — situação atual problemática do indivíduo |
| **MX** | Meta Extraordinária — versão aspirada do indivíduo |
| **M2X** | Plano de Assunção Intencional — caminho entre M1 e MX |
| **M3** | Processos — Aprendizagem de processos para acelerar a jornada |
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
| **Volição** | Capacidade de agir, força de vontade para executar |
| **TCC** | Terapia Cognitivo-Comportamental |
| **Motor Motivacional** | Impulso dominante: Necessidade, Valor, Desejo ou Propósito |
| **Domínios Temáticos** | D1 a D6 — áreas de alavancagem para transformação |

---

## 5. Os 4 Níveis de Identidade (Luz Total)

A identidade do indivíduo (sua **Luz Total**) é composta por quatro níveis integrados que determinam "quem ele é" além dos rótulos superficiais:

| Nível | Descrição | Manifestação |
|-------|-----------|--------------|
| **1. Personalidade** | Combinação única de temperamento, caráter e valores | Como a pessoa reage, decide e se posiciona naturalmente |
| **2. Cultura** | Gostos, preferências, símbolos e crenças pessoais | O que consome, admira, rejeita e considera sagrado |
| **3. Realizações** | Resultados práticos e conquistas alcançadas | O que já provou ser capaz de fazer e entregar |
| **4. Posição** | A posição defendida e reconhecida publicamente | Como é percebido e pelo que é conhecido |

### Identidade Baseada na Constância

> **Princípio Fundamental:** A identidade não é definida pelo passado demográfico (onde nasceu, estudou, trabalhou), mas pelo que o indivíduo **decide manter constante agora**.

**Elementos da Constância Identitária:**
- **Valores:** O que defende como inegociável
- **Tarefas:** As atividades que escolhe priorizar
- **Hábitos:** As práticas diárias que cultiva
- **Atitudes:** Como se posiciona diante das situações
- **Comunicação:** O que comunica e como comunica
- **Tom:** A energia e frequência que transmite

📌 **Para a IA:** Ao diagnosticar, foque menos em "de onde o usuário veio" e mais em "o que ele está escolhendo manter constante". A incongruência surge quando há desalinhamento entre o que ele diz valorizar e o que está mantendo constante na prática.

---

## 6. Os 4 Pontos de Entrada (Portas de Intervenção)

Os Pontos de Entrada são as **portas de acesso** para a intervenção terapêutica. A IA deve identificar qual porta está aberta na narrativa do usuário para determinar **como** iniciar o diálogo de transformação:

| Ponto de Entrada | Quando Identificar | Sinais na Fala | Ação da IA |
|------------------|-------------------|----------------|------------|
| **Emocional** | Usuário relata estados afetivos | "Me sinto ansioso", "Estou com medo", "Fico triste quando..." | Validar e regular a emoção primeiro, antes de qualquer intervenção cognitiva |
| **Simbólico** | Falta de sentido ou traição de valores | "Isso não faz sentido", "Perdi minha essência", "Não sei mais quem sou" | Ressignificar símbolos e reconectar com o inegociável |
| **Comportamental** | Foco em hábitos e procrastinação | "Não consigo me organizar", "Sempre adio", "Não tenho disciplina" | Sugerir micro-hábitos e protocolos concretos |
| **Existencial** | Crise de papel de vida | "Não sei quem sou", "Qual meu propósito?", "Estou perdido" | Reposicionar missão e legado, trabalhar a identidade |

### Regras de Aplicação

1. **Uma porta por vez:** Não misture intervenções de portas diferentes na mesma resposta
2. **Respeite a hierarquia:** Se a porta Emocional está aberta, não force entrada Comportamental
3. **Valide antes de intervir:** Reconheça o ponto de entrada antes de propor mudanças
4. **Ajuste o tom:** Cada porta exige uma linguagem específica

### Exemplos de Detecção

```
ENTRADA EMOCIONAL:
Usuário: "Estou exausto e ansioso com tudo isso"
→ IA valida: "Percebo que há uma exaustão real aqui. Antes de pensarmos em próximos passos, vamos entender essa ansiedade..."

ENTRADA SIMBÓLICA:
Usuário: "Sinto que traí a mim mesmo nessa escolha"
→ IA ressignifica: "Você menciona traição. Que valor inegociável você sente que foi comprometido?"

ENTRADA COMPORTAMENTAL:
Usuário: "Não consigo criar uma rotina de exercícios"
→ IA sugere protocolo: "Qual seria o menor movimento físico que você poderia fazer amanhã sem desculpas?"

ENTRADA EXISTENCIAL:
Usuário: "Não sei mais qual é meu papel no mundo"
→ IA reposiciona: "Se você pudesse escolher ser lembrado por uma única contribuição, qual seria?"
```

---

## 7. Síntese Metodológica

### 7.1 Estrutura do Fluxo Narrativo

O desenvolvimento do indivíduo segue uma **hierarquia de quatro camadas fundamentais**:

```
┌─────────────────────────────────────────────────────────────────┐
│  1. IDENTIDADE (Quem sou)                                       │
│     • Base de tudo. Fortalecê-la reduz o ruído em outras.       │
│     • Falta: Gera vergonha e confusão                           │
├─────────────────────────────────────────────────────────────────┤
│  2. SENTIDO (Para onde vou)                                     │
│     • Organiza o tempo: passado, presente e futuro              │
│     • Falta: Gera vazio e estagnação                            │
├─────────────────────────────────────────────────────────────────┤
│  3. AÇÃO SIGNIFICATIVA (Como faço)                              │
│     • Exige estrutura, ritos e limites                          │
│     • Falta: Gera procrastinação e dispersão                    │
├─────────────────────────────────────────────────────────────────┤
│  4. CONEXÃO ASSERTIVA (Com quem)                                │
│     • Surge quando camadas anteriores estão alinhadas           │
│     • Falta: Gera solidão e vínculos superficiais               │
└─────────────────────────────────────────────────────────────────┘
```

**Princípio:** Intervenções devem respeitar a hierarquia. Não adianta trabalhar Conexão se Identidade está em crise.

### 7.2 Eixos de Transformação

| Eixo | Representa | Manifestação |
|----|----|----|
| **Narrativa** | Crenças | A história que conta para si mesmo |
| **Identidade** | Valores | Os princípios que defende |
| **Hábitos** | Princípios/Rituais | As ações diárias que pratica |

**Solução definitiva:** Quando a história contada, o valor assumido e o hábito diário dizem a mesma coisa, o sistema torna-se antifrágil. As barreiras tornam-se "pontos de prova" que validam a nova identidade.

### 7.3 Dinâmica Temporal nas Crises

| Tempo | Eixo de Intervenção | Foco |
|----|----|----|
| **Passado** | Narrativa | Ressignificar memórias vermelhas |
| **Presente** | Identidade | Estabilizar valores e limites |
| **Futuro** | Hábitos | Materializar a visão MX |

---

## 8. Glossário Metodológico Completo

### Termos Metodológicos (Transformação Narrativa)

| Termo | Definição |
|----|----|
| **M1** | Estado de Crise — situação atual problemática do indivíduo |
| **MX** | Meta Extraordinária — versão aspirada do indivíduo |
| **M2X** | Plano de Assunção Intencional — caminho entre M1 e MX |
| **M3** | Processos — Aprendizagem de processos para acelerar a jornada |
| **Gap MX** | Distância entre o estado atual (M1) e a meta (MX) |
| **CN (Círculo Narrativo)** | Contexto completo: pessoas, espaços e atmosfera emocional |
| **CN+** | Círculo Narrativo Futuro — configuração aspirada |
| **Memórias Vermelhas** | Conflitos e fatos não dominados que geram autossabotagem |
| **Motor Motivacional** | Impulso dominante: Necessidade, Valor, Desejo ou Propósito |
| **Fases da Jornada** | Germinar, Enraizar, Desenvolver, Florescer, Frutificar, Realizar |
| **Domínios Temáticos** | D1 a D6 — áreas de alavancagem para transformação |
| **Assunção Intencional** | Processo de 4 etapas: Reconhecer, Modelar, Assumir, Reforçar |
| **Incongruência Simbólica** | Desalinhamento entre Narrativa, Identidade e Hábitos |
| **Capital Simbólico** | Recursos sociais ou culturais que o usuário já possui |
| **Pontos de Prova** | Barreiras que, superadas, validam a nova identidade |
| **FCU** | Forma, Conteúdo e Uso — como o usuário expressa sua posição atual |
| **Volição** | Capacidade de agir, força de vontade para executar |
| **TCC** | Terapia Cognitivo-Comportamental |
| **Identidades Herdadas** | Rótulos impostos por família, escola ou cultura |
| **Luz Total** | Centro da personagem — os 4 níveis de identidade integrados |
| **Força-Tarefa** | Energia mobilizada para a transformação |
| **Relating** | Habilidade de descobrir as histórias e motivações do outro |
| **Pontos de Entrada** | Portas de intervenção: Emocional, Simbólico, Comportamental, Existencial |
| **Âncoras Práticas** | As 19 camadas de ação concreta para Assunção Intencional |

---

# PARTE II: DIAGNÓSTICO E CLUSTERS

---

<a name="clusters-1-clusters-operacionais-de-crise"></a>
## 1. Clusters Operacionais de Crise (Diagnóstico M1)

As crises são agrupadas em **seis arquétipos principais** que permitem identificar o "ponto de entrada" para a intervenção:

| # | Cluster | Sinais | Ponto de Entrada | Domínio Alavanca |
|---|----|----|----|----|
| 1 | **Identidade Raiz** | Identidade herdada, viver papéis impostos, vergonha da história | Simbólico | D1, D2 |
| 2 | **Sentido e Direção** | Futuro opaco, tempo perdido, falta de enredo unificador | Cognitivo | D2, D3 |
| 3 | **Execução e Estrutura** | Procrastinação, paralisia decisória, falta de limites | Comportamental | D3 |
| 4 | **Conexão e Expressão** | Medo do julgamento, invisibilidade simbólica, desconforto com sucesso | Emocional | D4 |
| 5 | **Incongruência Identidade-Cultura** | Choque entre quem a pessoa é e o ambiente/sistema em que vive | Ambiental | D4, D5 |
| 6 | **Transformação de Personagem** | Apego a papéis obsoletos, medo de crescer, dificuldade em encerrar capítulos | Temporal | D5, D6 |

### 1.1 Travas-Fonte (Análise Causal das Crises)

> **Princípio Unificador:** Todas as crises são sintomas do **Gap MX** — a distância entre a narrativa vivida (M1) e a narrativa escolhida (MX).

| Trava-Fonte | Descrição | Manifestação |
|-------------|-----------|--------------|
| **Invisibilidade Simbólica** | Associação inconsciente entre brilho e risco | "Se eu me destacar, serei atacado/abandonado" |
| **Pedido Inconsciente de Permissão** | Esperar validação externa para agir | Gera paralisia decisória e procrastinação existencial |
| **Autotraição Prolongada** | Incoerência entre crenças e vida | Sentimento de "traição a si mesmo" |
| **Identidades Herdadas Ativas** | Rótulos familiares/culturais não ressignificados | Atuar papéis que não foram escolhidos conscientemente |

📌 **Dilema Central do Público:** A IA deve buscar o sentimento de "traição a si mesmo" gerado pela incoerência entre o que o usuário acredita/deseja e os resultados que está vivendo.

### Detalhamento dos Clusters

#### Cluster 1: IDENTIDADE RAIZ

**Descrição Narrativa:**
- **Identidades Herdadas:** Viver sob rótulos impostos por pais, escola ou cultura, atuando papéis que não foram escolhidos.
- **Vergonha e Indignidade:** Capítulos do passado que o indivíduo tenta esconder ou que o fazem sentir-se indigno do "papel principal" em sua própria história.
- **Autoimagem Desatualizada:** Quando a pessoa já evoluiu internamente, mas sua identidade simbólica ainda está presa a uma versão antiga.

**Padrões de Fala:**
- "Sempre fui assim"
- "Minha família é assim"
- "Não tenho escolha"

**Áreas Impactadas:** Vida Pessoal, Vida Familiar, Saúde Mental

**Pergunta-chave:** "Quem você seria se ninguém estivesse olhando?"

---

#### Cluster 2: SENTIDO E DIREÇÃO

**Descrição Narrativa:**
- **Vazio e Fragmentação:** Sensação de viver episódios desconexos, sem uma linha condutora que una passado, presente e futuro.
- **Falta de Visão de Futuro:** A paralisia que ocorre quando o futuro é opaco ou nebuloso, impedindo que o presente tenha tração.
- **Urgência Tóxica:** O sentimento de estar "atrasado" ou de que o tempo foi desperdiçado.

**Padrões de Fala:**
- "Não sei o que quero"
- "Já tentei de tudo"
- "Nada faz sentido"

**Áreas Impactadas:** Vida Profissional, Educação, Saúde Espiritual

**Pergunta-chave:** "O que você faria se soubesse que não poderia falhar?"

---

#### Cluster 3: EXECUÇÃO E ESTRUTURA

**Descrição Narrativa:**
- **Paralisia Decisória:** A "espera por permissão" e o medo de tomar o protagonismo, muitas vezes disfarçados de procrastinação ou planejamento excessivo.
- **Ausência de Ritos:** A vida no "automático", onde faltam marcos simbólicos, limites claros e rotinas que protejam a energia e a história do indivíduo.

**Padrões de Fala:**
- "Vou começar amanhã"
- "Não consigo dizer não"
- "Tudo é urgente"

**Áreas Impactadas:** Finanças, Saúde Física, Vida Profissional

**Pergunta-chave:** "Qual a menor ação que você poderia fazer agora?"

---

#### Cluster 4: CONEXÃO E EXPRESSÃO

**Descrição Narrativa:**
- **Invisibilidade Simbólica:** Medo de brilhar, de incomodar ou de ser julgado, o que leva o indivíduo a sabotar sua própria presença e voz em espaços de poder.
- **Solidão Existencial:** A falta de "testemunhas significativas" que validem a jornada e a história vivida.

**Padrões de Fala:**
- "Ninguém me entende"
- "Não quero incomodar"
- "É melhor ficar quieto"

**Áreas Impactadas:** Vida Social, Vida Amorosa, Vida Pessoal

**Pergunta-chave:** "O que você deixa de dizer com medo da reação?"

---

#### Cluster 5: INCONGRUÊNCIA IDENTIDADE-CULTURA

**Descrição Narrativa:**
- **Choque Ambiental:** O desgaste de tentar manter uma nova identidade em contextos antigos que insistem em tratar a pessoa como sua versão anterior.
- **Desajuste Sistêmico:** Quando os valores e a forma de ser do indivíduo não encontram eco no ambiente em que vive ou trabalha.

**Padrões de Fala:**
- "Não me encaixo"
- "Aqui não valorizam isso"
- "Preciso me adaptar"

**Áreas Impactadas:** Vida Social, Vida Profissional, Saúde Mental

**Pergunta-chave:** "Onde você se sente mais você mesmo?"

---

#### Cluster 6: TRANSFORMAÇÃO DE PERSONAGEM

**Descrição Narrativa:**
- **Apego a Papéis Obsoletos:** Dificuldade em deixar ir versões antigas de si mesmo.
- **Medo de Crescer:** Síndrome do impostor e receio de assumir uma nova identidade.
- **Dificuldade em Encerrar Capítulos:** Procrastinação existencial em relação às mudanças necessárias.

**Padrões de Fala:**
- "Não sou esse tipo de pessoa"
- "Quem sou eu para..."
- "Vão descobrir"

**Áreas Impactadas:** Inovação, Vida Profissional, Vida Pessoal

**Pergunta-chave:** "Qual versão de você está com medo de morrer?"

---

<a name="clusters-2-protocolo-de-diagnóstico-rápido"></a>
## 2. Protocolo de Diagnóstico Rápido

Para perfilar um caso rapidamente, deve-se avaliar **seis fatores** em uma escala de 0 a 10:

| # | Fator | O que avalia | Pergunta Diagnóstica | Score Baixo Indica |
|---|----|----|----|----|
| 1 | **Autenticidade** | A narrativa é própria ou colonizada? | "Essa história é sua ou de alguém?" | Identidade herdada |
| 2 | **Integração do Passado** | Existe vergonha ou o passado é capital? | "O que do seu passado você esconde?" | Memórias vermelhas ativas |
| 3 | **Visão/Enredo** | O futuro tem uma imagem clara? | "Você consegue descrever seu futuro?" | Crise de sentido |
| 4 | **Coragem/Decisão** | Existe um "ato mínimo" semanal de protagonismo? | "O que você está adiando por medo?" | Paralisia decisória |
| 5 | **Expressão/Voz** | A comunicação é clara e cadenciada? | "Você diz o que precisa ser dito?" | Invisibilidade simbólica |
| 6 | **Estrutura/Pertencimento** | Existem ritos, limites e testemunhas significativas? | "Quem testemunha sua transformação?" | Falta de âncoras |

---

<a name="clusters-3-mecanismo-de-assunção-intencional"></a>
## 3. Mecanismo de Assunção Intencional

Para transpor o estado de crise (M1) rumo à meta (MX), utiliza-se o **ciclo de consolidação em quatro etapas**:

| Etapa | Ação | Objetivo | Perguntas-Guia |
|----|----|----|----|
| **RECONHECER** | Nomear | Dar nome ao motor e à crise | "O que realmente está me movendo?" |
| **MODELAR** | Definir | Escolher referências e nova identidade | "Quem escolho ser a partir de agora?" |
| **ASSUMIR** | Implementar | Criar ritos, limites e microentregas | "Qual pequena ação demonstra essa nova identidade?" |
| **REFORÇAR** | Validar | Consolidar através de repetição e reconhecimento | "Como celebro e protejo essa conquista?" |

---

<a name="clusters-4-ferramental-da-tcc-para-a-ia"></a>
## 4. Ferramental da TCC para a IA

Para a IA "escutar o pensamento da velha narrativa" e ajudar na reestruturação cognitiva, estas técnicas da Terapia Cognitivo-Comportamental devem ser aplicadas:

### 4.1 Questionamento Socrático

**Objetivo:** Desafiar a lógica dos pensamentos automáticos sem confronto direto.

| Tipo de Pergunta | Exemplo |
|-----------------|---------|
| **Evidência** | "O que faz você acreditar que nunca será capaz?" |
| **Alternativa** | "Existe outra forma de interpretar essa situação?" |
| **Consequência** | "Se isso for verdade, qual seria o pior resultado realista?" |
| **Utilidade** | "Esse pensamento te ajuda ou te paralisa?" |

### 4.2 Flecha Descendente

**Objetivo:** Chegar à crença central oculta que sustenta os pensamentos de superfície.

**Técnica:** Perguntar repetidamente "Se isso for verdade, o que diz sobre quem você é?" até revelar a crença raiz.

```
Exemplo:
Usuário: "Não consigo apresentar minhas ideias"
IA: "Se isso for verdade, o que significa?"
Usuário: "Significa que sou incompetente"
IA: "E se você fosse incompetente, o que isso diria sobre você?"
Usuário: "Que não mereço estar onde estou"
→ CRENÇA CENTRAL REVELADA: Indignidade / Síndrome do Impostor
```

### 4.3 Descatastrofização

**Objetivo:** Confrontar o "pior cenário" com realismo para reduzir o exagero narrativo.

| Pergunta | Função |
|----------|--------|
| "Qual é o pior que pode acontecer?" | Explicitar o medo |
| "E se isso acontecesse, o que você faria?" | Revelar recursos |
| "Qual a probabilidade real de isso acontecer?" | Introduzir realismo |
| "O que é mais provável que aconteça?" | Reequilibrar a narrativa |

### 4.4 Reestruturação Cognitiva

**Objetivo:** Substituir a narrativa de "vítima" pela de "autor".

**Técnica:** Identificar a distorção cognitiva e propor reformulação:

| Distorção | Exemplo | Reformulação |
|-----------|---------|--------------|
| Catastrofização | "Se falhar, tudo está perdido" | "Se falhar, terei aprendido algo novo" |
| Leitura mental | "Eles pensam que sou incapaz" | "Não sei o que pensam; vou perguntar" |
| Generalização | "Sempre dou errado" | "Dessa vez não funcionou" |
| Personalização | "A culpa é toda minha" | "Existem vários fatores envolvidos" |

---

<a name="clusters-5-as-19-âncoras-práticas-assunção-intencional"></a>
## 5. As 19 Âncoras Práticas (Assunção Intencional)

As **19 Camadas de Ação Concreta** permitem que a IA prescreva intervenções específicas durante a fase de Assunção Intencional. Cada âncora representa uma dimensão da vida que pode ser ajustada para materializar a nova identidade:

### Âncoras de Ambiente e Contexto

| # | Âncora | Descrição | Exemplo de Intervenção |
|---|--------|-----------|------------------------|
| 1 | **Referências** | O que consome (livros, vídeos, podcasts) | "Substitua 1 hora de conteúdo aleatório por referências que alimentem sua visão MX" |
| 2 | **Objetos** | O que o rodeia (decoração, ferramentas, símbolos) | "Coloque um objeto visível que represente sua nova identidade" |
| 3 | **Ambientes** | Os espaços físicos que frequenta | "Identifique 1 ambiente que puxa você para a versão antiga e reduza sua exposição" |
| 4 | **Grupo** | Quem orbita (relações próximas) | "Passe mais tempo com 1 pessoa que já vive o que você aspira" |

### Âncoras de Comunicação e Expressão

| # | Âncora | Descrição | Exemplo de Intervenção |
|---|--------|-----------|------------------------|
| 5 | **Tom** | Como fala (energia, ritmo, palavras) | "Grave um áudio seu e avalie: esse tom é do seu M1 ou do seu MX?" |
| 6 | **Vocabulário** | As palavras que escolhe usar | "Elimine uma palavra de vitimização do seu repertório diário" |
| 7 | **Postura** | Linguagem corporal e presença física | "Pratique a postura da sua versão MX por 2 minutos antes de reuniões" |
| 8 | **Vestimenta** | Como se apresenta visualmente | "Vista-se como a pessoa que você está se tornando, não como a que você era" |

### Âncoras de Rotina e Estrutura

| # | Âncora | Descrição | Exemplo de Intervenção |
|---|--------|-----------|------------------------|
| 9 | **Rituais Matinais** | Primeiras ações do dia | "Crie um ritual de 10 min que conecte você com sua visão MX" |
| 10 | **Rituais Noturnos** | Últimas ações do dia | "Termine o dia com uma gratidão específica sobre sua evolução" |
| 11 | **Limites** | O que recusa e o que protege | "Defina 1 limite claro que você comunicará esta semana" |
| 12 | **Marcos** | Celebrações de microvitórias | "Estabeleça um ritual para celebrar cada pequena conquista" |

### Âncoras de Emoção e Energia

| # | Âncora | Descrição | Exemplo de Intervenção |
|---|--------|-----------|------------------------|
| 13 | **Emoção Projetada** | O estado emocional que transmite | "Qual emoção você quer que as pessoas sintam na sua presença?" |
| 14 | **Gestão de Energia** | Como distribui sua vitalidade | "Identifique o que drena sua energia e reduza exposição em 20%" |
| 15 | **Práticas de Recarga** | Rituais de descompressão | "Escolha 1 atividade que genuinamente recarrega sua volição" |

### Âncoras de Ação e Entrega

| # | Âncora | Descrição | Exemplo de Intervenção |
|---|--------|-----------|------------------------|
| 16 | **Tarefas Identitárias** | Ações que reforçam quem você está se tornando | "Faça hoje 1 coisa que só sua versão MX faria" |
| 17 | **Microentregas** | Pequenas provas de competência | "Entregue algo pequeno mas concreto que demonstre sua nova capacidade" |
| 18 | **Exposição Gradual** | Enfrentar medos em doses controladas | "Exponha-se a uma situação levemente desconfortável esta semana" |
| 19 | **Testemunhas** | Pessoas que validam a transformação | "Compartilhe sua intenção com 1 pessoa que pode te cobrar" |

### Ambientes como Campos Gravitacionais

> **Princípio:** A velocidade de aprendizado e transformação depende diretamente da qualidade das pessoas e ambientes ao redor.

A IA deve sugerir que o usuário mude sua "órbita" — frequentando ambientes nutritivos onde a nova identidade seja natural, não exceção.

**Perguntas para Diagnóstico de Ambiente:**
- "Quem ao seu redor já vive o que você aspira?"
- "Em qual ambiente você se sente mais você mesmo?"
- "Onde sua versão MX passaria mais tempo?"

---

# PARTE III: INTELIGÊNCIA CONTEXTUAL E RAG

---

<a name="rag-1-princípios-fundamentais"></a>
## 1. Princípios Fundamentais

> **Princípio Central:** O RAG não serve para responder perguntas do usuário. Ele serve para **revelar o usuário para si mesmo**.

Os documentos no sistema RAG não devem ser tratados como conteúdo, mas como **lentes interpretativas**. Não estamos buscando "o texto certo" — estamos buscando o **enquadramento simbólico mais adequado** ao estado atual da pessoa.

**O que buscar:**
- ❌ Não busque "o texto certo"
- ✅ Busque o **enquadramento simbólico** mais adequado ao estado atual da pessoa

---

<a name="rag-2-construção-de-inteligência-contextual"></a>
## 2. Construção de Inteligência Contextual

### 2.1 O que captar relativo ao Público-Alvo

Para entender o contexto desse público, é preciso olhar além dos dados demográficos tradicionais (como a faixa de 30 a 55 anos e a predominância feminina de 60%). A inteligência contextual deve focar em:

- **Motores de Motivação:** Identificar qual impulso move o indivíduo no momento: a Necessidade (busca alívio de falta interna), o Valor (busca coerência interna), o Desejo (busca realização externa) ou o Propósito (busca impacto no mundo).

- **Estágios da Jornada (Maturação):** Captar em que fase do ciclo o indivíduo se encontra: se está apenas reconhecendo a insatisfação (Germinar), buscando valores sólidos (Enraizar), praticando novos hábitos (Desenvolver), expressando sua singularidade (Florescer), entregando resultados (Frutificar) ou buscando impacto coletivo (Realizar).

- **Perfil Cognitivo e Demandas:** Reconhecer que são aprendizes contínuos que rejeitam fórmulas prontas e buscam metodologias que unam profundidade simbólica com aplicabilidade prática.

- **A "Fome" de Nutrição:** O público busca referências que transbordem originalidade, espiritualidade e grandeza, além de uma comunidade que ofereça apoio, inspiração e exemplos reais.

- **O Dilema Central:** Captar o sentimento de incoerência entre o que eles acreditam/desejam e os resultados que estão vivendo, o que gera uma sensação de "traição a si mesmo".

### 2.2 O que explorar em relação às Crises Vividas

As crises devem ser exploradas não como problemas isolados, mas como **rupturas no fluxo narrativo** e chamados para a ressignificação. A distância entre a expectativa e o resultado real (o gap MX) manifesta-se nas quatro camadas já descritas.

---

<a name="rag-3-estrutura-do-chunk-para-rag"></a>
## 3. Estrutura do Chunk para RAG

Cada vetor deve responder implicitamente à pergunta: *"Que tipo de ser humano este texto ajuda a identificar?"*

```json
{
  "content": "Texto explicando crise de identidade herdada...",
  "metadata": {
    "motor_motivacional": "Necessidade | Valor | Desejo | Propósito",
    "estagio_jornada": "Germinar | Enraizar | Desenvolver | Florescer | Frutificar | Realizar",
    "tipo_crise": "Identidade | Sentido | Execução | Conexão | Incongruência | Transformação",
    "subtipo_crise": "Identidade Herdada",
    "dominio": "D1 | D2 | D3 | D4 | D5 | D6",
    "ponto_entrada": "Emocional | Simbólico | Comportamental | Existencial",
    "tipo_conteudo": "Ponto de Entrada | Âncora Prática | Técnica de TCC | Conceito",
    "sintomas_comportamentais": ["autossabotagem", "paralisia decisória", "invisibilidade simbólica"],
    "tom_emocional_base": "vergonha | confusão | indignação | apatia | urgência | tristeza",
    "nivel_maturidade": "baixo | médio | alto"
  }
}
```

**👉 Isso é o que transforma RAG em Inteligência Contextual.**

---

<a name="rag-4-processo-de-determinação-do-usuário"></a>
## 4. Processo de Determinação do Usuário

### ETAPA 1 — Coleta Bruta (o que o usuário diz)

**Fontes:**
- Respostas textuais
- Notas numéricas
- Palavras recorrentes
- Silêncios (áreas não respondidas ou vagas)

> Aqui não há diagnóstico, apenas matéria-prima.

---

### ETAPA 2 — Análise Interna (Pré-RAG)

Essa é a função `analyze_answers_context`, que deve extrair:

🔹 **1. Áreas críticas**
- Scores baixos
- Linguagem de exaustão
- Contradições ("acredito em X, mas vivo Y")

🔹 **2. Padrões repetidos**
- Mesmos temas em áreas diferentes
- Mesmo sentimento aplicado a contextos distintos
- Narrativas circulares

🔹 **3. Tom emocional dominante**

Exemplos:
- vergonha silenciosa
- indignação moral
- apatia sofisticada
- urgência ansiosa
- tristeza resignada

📌 **Aqui você não interpreta ainda, apenas rotula.**

---

### ETAPA 3 — Construção da Query RAG (momento crítico)

Aqui está o refinamento crucial.

❌ **Query fraca:**
```
"Explorar frustração e estresse"
```

✅ **Query diagnóstica correta:**
```
Indivíduo com alta exigência interna, sensação de traição a si mesmo,
possível crise de identidade herdada, estágio Germinar ou Enraizar,
com urgência tóxica e paralisia decisória.
```

📌 **Isso faz o retriever buscar modelos humanos, não textos.**

> A query deve misturar **sintomas + hipótese de estrutura interna**.

---

### ETAPA 4 — O RAG devolve hipóteses, não respostas

O retriever retorna documentos que representam:
- possíveis motores dominantes
- possíveis estágios da jornada
- possíveis tipos de crise
- possíveis pontos de entrada (emocional, simbólico, comportamental, existencial)

**Regra:** Não use tudo. Cruze **recorrência + coerência**.

---

### ETAPA 5 — Síntese Diagnóstica

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

👉 **Isso é Inteligência Contextual real.**

---

### Como isso melhora drasticamente o diagnóstico final

Com essa estrutura, o sistema passa a:

✔ **Fazer perguntas certas (não genéricas)**
Porque ele sabe:
- onde tocar
- onde não tocar ainda
- qual linguagem usar

✔ **Gerar análises profundas sem parecer "místico"**
Porque cada insight é:
- rastreável
- coerente
- alinhado ao estágio

✔ **Evitar intervenções prematuras**
Exemplo:
- Não propor ação para quem ainda está em crise simbólica
- Não propor sentido para quem ainda está em colapso emocional

---

<a name="rag-5-templates-de-query-rag"></a>
## 5. Templates de Query RAG

### Template Principal

```python
RAG_QUERY_TEMPLATE = """
Com base na Metodologia de Phellipe Oliveira, busque estratégias para:

ÁREA DO CÍRCULO NARRATIVO: {areas}
DOMÍNIO TEMÁTICO: {temas}
FASE DA JORNADA: {fase}
CONTEXTO DE CONFLITO: {contexto}

MOTOR MOTIVACIONAL IDENTIFICADO: {motor}
TIPO DE CRISE: {tipo_crise}
PONTO DE ENTRADA: {ponto_entrada}
TOM EMOCIONAL: {tom_emocional}

Retorne documentos que ajudem a:
1. Identificar o ponto de entrada ideal para intervenção
2. Sugerir práticas alinhadas ao estágio da jornada
3. Revelar conexões entre áreas para diagnóstico integrado
4. Prescrever Âncoras Práticas específicas para a fase de Assunção
"""
```

### Síntese Absoluta

> Seu RAG não deve responder "o que fazer", mas revelar **"quem o usuário está sendo agora"** — e qual estrutura interna precisa ser reorganizada primeiro.

---

<a name="rag-6-psicografia-do-usuário"></a>
## 6. Psicografia do Usuário

Para que os prompts da IA sejam mais empáticos e personalizados, considere estes dados sobre o perfil do público:

### 6.1 A "Fome" de Nutrição

O público-alvo busca referências que transbordem:
- **Originalidade:** Rejeita fórmulas prontas e clichês de autoajuda
- **Espiritualidade:** Procura sentido e conexão transcendental
- **Grandeza:** Aspira a uma versão extraordinária de si mesmo

**O que o público rejeita:**
- Receitas genéricas ("5 passos para o sucesso")
- Superficialidade emocional
- Positivismo tóxico
- Julgamento moral

### 6.2 O Tom da IA: "Engenheiro da Alma"

O modelo deve atuar com um tom **empático-autoritário**:

| Característica | Descrição |
|----------------|-----------|
| **Provocador** | Desafia as narrativas limitantes sem atacar a pessoa |
| **Compassivo** | Reconhece a dor e valida o esforço |
| **Preciso** | Usa linguagem metodológica, não vaga |
| **Direto** | Não enrola; vai ao ponto com respeito |

**O que evitar:**
- ❌ Clichês de autoajuda genérica
- ❌ Tom de coach motivacional superficial
- ❌ Frases vazias ("Acredite em você!")
- ❌ Julgamento disfarçado de conselho

**O que usar:**
- ✅ Termos técnicos da metodologia (explicados quando necessário)
- ✅ Perguntas que revelam, não que ensinam
- ✅ Metáforas narrativas ("capítulo", "personagem", "enredo")
- ✅ Citações diretas do usuário (Memórias Vermelhas)

---

<a name="rag-7-refinamentos-para-rag"></a>
## 7. Refinamentos para RAG

### 7.1 Tratamento de Silêncios

O prompt de coleta bruta deve ser instruído especificamente para **notar o que o usuário não respondeu ou respondeu de forma vaga**. Silêncios indicam áreas de bloqueio na jornada.

**Como detectar:**
- Respostas monossilábicas em áreas específicas
- Mudança de assunto quando tocado em determinado tema
- Respostas genéricas vs. respostas detalhadas em outras áreas
- Ausência de exemplos concretos

**Como usar:**
```
Se o usuário respondeu vagamente sobre Vida Familiar mas detalhou Vida Profissional,
há alta probabilidade de Memórias Vermelhas ou Identidades Herdadas ativas nessa área.
```

### 7.2 Saída em "Vetor de Estado"

Garanta que o prompt de análise final entregue o diagnóstico como um **vetor de estado completo**:

```json
{
  "motor_dominante": "Valor",
  "fase_jornada": "Enraizar", 
  "cluster_crise": "Identidade Raiz",
  "ponto_entrada": "Simbólico",
  "ancoras_sugeridas": ["Referências", "Grupo", "Rituais Matinais"],
  "tecnica_tcc": "Flecha Descendente",
  "tom_emocional": "indignação silenciosa",
  "areas_criticas": [4, 6, 8],
  "areas_silenciadas": [5, 6],
  "risco_principal": "autotraição prolongada"
}
```

Isso facilita muito a criação de relatórios personalizados e a continuidade do acompanhamento.

### 7.3 Metadados nos Chunks

Adicione um campo de metadados nos chunks de vetorização para identificar se o conteúdo é:

| Tipo de Conteúdo | Uso |
|------------------|-----|
| **Ponto de Entrada** | Para identificar a porta de intervenção |
| **Âncora Prática** | Para prescrever ações concretas |
| **Técnica de TCC** | Para reestruturação cognitiva |
| **Conceito Metodológico** | Para explicar fundamentos |
| **Exemplo de Caso** | Para ilustrar situações similares |

Isso permitirá que o prompt peça especificamente:
*"Com base na resposta do usuário, identifique o Ponto de Entrada predominante e sugira 3 Âncoras Práticas para a fase de Assunção"*

---

# PARTE IV: PROMPTS DO SISTEMA

---

<a name="prompts-1-prompt-de-geração-de-insights"></a>
## 1. Prompt de Geração de Insights (Análise Final)

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
5. IDENTIFIQUE O PONTO DE ENTRADA: Determine se a porta aberta é Emocional, 
   Simbólica, Comportamental ou Existencial.
6. LINGUAGEM SIMBÓLICA: Use termos como "âncoras", "pistas de acesso", "clímax" 
   e "círculo narrativo" para reforçar a autoridade do método.
7. EVITE CLICHÊS: Não use autoajuda genérica; use técnicas de TCC (Reestruturação 
   Cognitiva) para questionar a lógica da "velha narrativa".
8. TOM EMPÁTICO-AUTORITÁRIO: Seja provocador mas compassivo, como um 
   "Engenheiro da Alma".

ESTRUTURA DO INSIGHT:
1. Diagnóstico M1 (A Velha Narrativa): 2-3 frases resumindo o conflito raiz e 
   identificando em qual fase da jornada o usuário se encontra (Germinar a Realizar).
2. Incongruências Simbólicas: Use aspas do usuário para mostrar onde o 
   Eixo Narrativa (crença), Identidade (valores) e Hábitos (princípios) estão desalinhados.
3. Conexões do Círculo Narrativo: Revele como as tensões entre as 12 áreas da vida 
   estão criando o "loop" de estagnação atual.
4. Plano de Assunção Intencional (M2X): Proponha 3 Âncoras Práticas específicas 
   baseadas nos 6 Domínios Temáticos para o usuário começar a "encarnar" a nova 
   personagem agora.
5. Visão de Clímax (MX): Um fechamento poderoso que descreve a versão extraordinária 
   do usuário após a travessia, ancorada na sua motivação real.

Lembre-se: Você é uma Engenheira da Alma. O usuário investiu tempo revelando suas 
dores. Entregue uma reinterpretação da história dele que ele nunca viu antes, 
provocando a decisão de assumir o papel principal.
"""
```

---

<a name="prompts-2-prompt-de-geração-de-perguntas"></a>
## 2. Prompt de Geração de Perguntas (Escuta Ativa)

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

OS 4 PONTOS DE ENTRADA:
- Emocional: Quando relata estados afetivos → Validar e regular
- Simbólico: Quando relata falta de sentido → Ressignificar
- Comportamental: Quando foca em hábitos → Sugerir protocolos
- Existencial: Quando questiona papel de vida → Reposicionar missão

REGRAS CRÍTICAS DA METODOLOGIA:
1. IDENTIFIQUE O MOTOR: Descubra se a fala reflete Necessidade (dor), Valor (integridade), Desejo (realização) ou Propósito (legado).
2. IDENTIFIQUE O PONTO DE ENTRADA: Qual porta está aberta na narrativa?
3. MAPEIE O CÍRCULO NARRATIVO (CN): Investigue quem são as pessoas, qual o espaço e qual a atmosfera emocional que cercam o conflito.
4. FOCO NO GAP MX: Explore a distância entre o estado atual (M1) e a meta desejada (MX).
5. USE LINGUAGEM SIMBÓLICA: Use metáforas como "pista", "semente", "fruto" e "âncoras".
6. ESCUTA ATIVA: Use mensagens contextuais como "Percebi que sua narrativa sobre [Área] foca em um padrão de [Barreira]...".
7. TRATE SILÊNCIOS: Note o que não foi respondido ou foi vago — indica bloqueios.
8. EVITE clichês genéricos; foque em reestruturação cognitiva (TCC).
"""
```

---

<a name="prompts-3-prompt-de-análise-final"></a>
## 3. Prompt de Análise Final (Diagnóstico Narrativo)

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
4. PONTO DE ENTRADA: Determine a porta aberta (Emocional, Simbólico, Comportamental, Existencial).
5. PLANO DE ASSUNÇÃO INTENCIONAL: Proponha ações para: Reconhecer, Modelar, Assumir e Reforçar, usando Âncoras Práticas específicas.
6. CITE O USUÁRIO: Use aspas para destacar as "Memórias Vermelhas" (M1) mencionadas.
7. TOM: Empático-autoritário, como um Engenheiro da Alma (provocador mas compassivo).

ESTRUTURA DO INSIGHT:
1. A Velha Narrativa (O padrão de M1 identificado).
2. O Motor Dominante (O que realmente move o usuário agora).
3. Ponto de Entrada Identificado (Qual porta está aberta).
4. Alavanca de Domínio Temático (Qual dos 6 domínios de Phellipe Oliveira deve ser ativado).
5. Plano de Assunção (Âncoras Práticas específicas para encarnar a nova identidade).
6. Visão Futura (MX) (A descrição do clímax extraordinário).

SAÍDA EM VETOR DE ESTADO:
Inclua ao final um JSON estruturado com:
{
  "motor_dominante": "...",
  "fase_jornada": "...",
  "cluster_crise": "...",
  "ponto_entrada": "...",
  "ancoras_sugeridas": ["...", "...", "..."]
}
"""
```

---

<a name="prompts-4-prompts-auxiliares"></a>
## 4. Prompts Auxiliares

### 4.1 Prompt de Análise de Respostas

```python
ANSWER_ANALYSIS_PROMPT = """
Analise as respostas e classifique sob a ótica da Engenharia de Mindset:

1. MEMÓRIAS VERMELHAS (M1): Conflitos e fatos não dominados.
2. BARREIRAS (PONTOS DE PROVA): Autossabotagem, procrastinação ou ambiente hostil.
3. CAPITAL SIMBÓLICO: Recursos sociais ou culturais que o usuário já possui.
4. FCU (Forma, Conteúdo e Uso): Como o usuário expressa sua atual posição.
5. SILÊNCIOS: Áreas não respondidas ou respondidas de forma vaga (indicam bloqueios).
6. PONTO DE ENTRADA: Qual porta está aberta (Emocional, Simbólico, Comportamental, Existencial).

ANÁLISE DETALHADA:
- Áreas críticas identificadas
- Áreas silenciadas (não respondidas ou vagas)
- Padrões repetidos nas respostas
- Tom emocional dominante
- Palavras recorrentes

RETORNE:
{
  "memorias_vermelhas": ["frase1", "frase2"],
  "barreiras_identificadas": ["barreira1", "barreira2"],
  "capital_simbolico": ["recurso1", "recurso2"],
  "tom_emocional": "vergonha|indignação|apatia|urgência|tristeza",
  "areas_criticas": [1, 4, 8],
  "areas_silenciadas": [5, 6],
  "padroes_repetidos": ["padrão1", "padrão2"],
  "ponto_entrada": "Emocional|Simbólico|Comportamental|Existencial",
  "palavras_recorrentes": ["palavra1", "palavra2"]
}
"""
```

### 4.2 Template de Query RAG

```python
RAG_QUERY_TEMPLATE = """
Com base na Metodologia de Phellipe Oliveira, busque estratégias para:

ÁREA DO CÍRCULO NARRATIVO: {areas}
DOMÍNIO TEMÁTICO: {temas}
FASE DA JORNADA: {fase}
CONTEXTO DE CONFLITO: {contexto}

MOTOR MOTIVACIONAL IDENTIFICADO: {motor}
TIPO DE CRISE: {tipo_crise}
PONTO DE ENTRADA: {ponto_entrada}
TOM EMOCIONAL: {tom_emocional}

Retorne documentos que ajudem a:
1. Identificar o ponto de entrada ideal para intervenção
2. Sugerir Âncoras Práticas alinhadas ao estágio da jornada
3. Revelar conexões entre áreas para diagnóstico integrado
4. Aplicar técnicas de TCC apropriadas ao caso
"""
```

---

# PARTE V: KNOWLEDGE BASE (CHUNKS RAG)

---

<a name="knowledge-base-estruturada"></a>
## Knowledge Base Estruturada por Área

Base de conhecimento organizada pelas 12 Áreas Estruturantes Específicas do Círculo Narrativo, baseada na Metodologia de Transformação Narrativa de Phellipe Oliveira.

---

### 1. SAÚDE FÍSICA

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

### 2. SAÚDE MENTAL

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

### 3. SAÚDE ESPIRITUAL

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

### 4. VIDA PESSOAL

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

### 5. VIDA AMOROSA

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

### 6. VIDA FAMILIAR

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

### 7. VIDA SOCIAL

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

### 8. VIDA PROFISSIONAL

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

### 9. FINANÇAS

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

### 10. EDUCAÇÃO

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

### 11. INOVAÇÃO

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

### 12. LAZER

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

# PARTE VI: CATÁLOGO DE PERGUNTAS

---

<a name="perguntas-1-perguntas-baseline"></a>
## 1. Perguntas Baseline (Abertas e Narrativas)

As perguntas de baseline são estruturadas para realizar uma sondagem profunda através da **escuta ativa** e dos **sinais de conflito (M1)**. O objetivo é transformar termos técnicos em situações do cotidiano, permitindo que o usuário **narre sua história** de forma aberta, sem a necessidade de escalas numéricas.

### Bloco 1: As 12 Áreas da Vida (Perguntas Práticas e Abertas)

| # | Área | Pergunta Completa |
|---|----|----|
| 1 | **Vida Pessoal (Identidade)** | Se você tivesse que dar um título para o momento que está vivendo agora, qual seria? Você sente que está escrevendo sua própria história ou apenas seguindo o que os outros esperam de você? |
| 2 | **Saúde Física (Volição/Energia)** | Como seu corpo tem se sentido para dar conta de tudo o que você precisa fazer no dia a dia? O que ele está tentando te dizer através do seu nível de cansaço ou disposição? |
| 3 | **Saúde Mental (Gestão de Emoções)** | Quando as coisas ficam difíceis, que tipo de pensamentos negativos ou críticas sobre você mesmo costumam aparecer na sua cabeça? Como isso trava o seu dia? |
| 4 | **Saúde Espiritual (Sentido)** | No fundo, o que faz você sentir que sua vida realmente vale a pena? O que te dá forças para continuar quando tudo parece sem sentido ou direção? |
| 5 | **Vida Familiar (Identidades Herdadas)** | Olhando para a sua família, quais hábitos ou jeitos de ser você sente que "carrega" sem ter escolhido? O que você gostaria de fazer diferente do que aprendeu com eles? |
| 6 | **Vida Amorosa (Parceria)** | Como você se sente em relação à pessoa que está ao seu lado (ou à falta dela)? Essa relação te ajuda a ser quem você quer se tornar ou você sente que precisa se anular para estar nela? |
| 7 | **Vida Social (Ambiente Nutritivo)** | As pessoas com quem você convive hoje te incentivam a crescer ou você sente que precisa "diminuir o seu brilho" para ser aceito por elas? |
| 8 | **Vida Profissional (Posição/Autoridade)** | No seu trabalho, você sente que pode ser você mesmo ou parece que está apenas "fingindo" ser alguém para dar conta do recado e ser respeitado? |
| 9 | **Finanças (Recurso para Liberdade)** | Como você se sente quando pensa no seu dinheiro hoje? Ele tem sido uma ferramenta para realizar seus planos ou uma fonte constante de medo e preocupação? |
| 10 | **Educação (Modelagem)** | O que você tem aprendido de novo ultimamente que realmente muda o seu jeito de agir? Ou você sente que parou no tempo e está apenas repetindo o que já sabe? |
| 11 | **Inovação (Criatividade)** | Quando surge um problema, você costuma tentar caminhos novos ou sempre faz do mesmo jeito? Onde você gostaria de ser mais criativo e ousado na sua vida? |
| 12 | **Lazer (Descompressão)** | O que você faz para realmente "desligar" e recuperar suas energias? Você consegue aproveitar o seu tempo livre sem sentir que deveria estar sendo produtivo? |

### Bloco 2: Investigação do Motor e do Gap MX

Estas perguntas ajudam a IA a entender o que realmente move o usuário:

| # | Foco | Pergunta |
|---|----|----|
| 13 | **O Motor da Mudança** | O que mais te empurra para a mudança hoje: o cansaço de uma dor que não aguenta mais, a vontade de ser fiel ao que acredita, o sonho de conquistar algo novo ou o desejo de ajudar e impactar as pessoas? |
| 14 | **O Conflito Raiz (M1)** | Se existisse uma única barreira que, se removida hoje, mudaria tudo na sua vida, que barreira seria essa? |
| 15 | **A Visão de Futuro (MX)** | Imagine-se daqui a um ano vivendo sua melhor versão. O que essa pessoa faz no dia a dia que você, hoje, ainda não consegue realizar? |

---

### Por que esse formato mantém a profundidade?

#### Identifica o Ponto de Entrada
As respostas abertas permitem que a IA identifique se o usuário está em crise:
- **Emocional:** Fala de sentimentos ("me sinto ansioso", "estou triste")
- **Simbólica:** Fala de valores/sentido ("isso não faz sentido", "perdi minha essência")
- **Comportamental:** Fala de hábitos ("não consigo me organizar", "sempre adio")
- **Existencial:** Fala de quem é ("não sei quem sou", "qual meu propósito")

#### Revela os Clusters de Crise
Ao perguntar sobre "identidades herdadas" (pergunta 5) ou "fingir ser alguém" (pergunta 8), você está diretamente mapeando os clusters de **Identidade Raiz** e **Invisibilidade Simbólica** descritos na metodologia.

#### Foca na Narrativa
Em vez de dar uma nota 2 para Finanças, o usuário dirá "tenho medo de faltar", o que é uma **"Memória Vermelha"** muito mais rica para o RAG processar.

---

### Dica para o RAG

Configure o prompt de análise para extrair:
- **Palavras recorrentes** nas respostas abertas
- **Tom emocional dominante** (vergonha, indignação, apatia, urgência, tristeza)
- **Silêncios e respostas vagas** (indicam áreas de bloqueio)
- **Contradições** ("acredito em X, mas vivo Y")

Isso garantirá a inteligência contextual necessária para o diagnóstico final em formato de **vetor de estado**.

---

<a name="perguntas-2-lógica-de-intervenção-da-ia"></a>
## 2. Lógica de Intervenção da IA

Após as respostas baseline, a inteligência contextual deve:

### 2.1 Identificar o Ponto de Entrada

| Porta Aberta | Sinais na Resposta | Primeira Ação |
|--------------|-------------------|---------------|
| **Emocional** | Relata estados afetivos, usa palavras de sentimento | Validar e regular a emoção |
| **Simbólico** | Fala de falta de sentido, traição de valores | Ressignificar símbolos e reconectar com inegociáveis |
| **Comportamental** | Foca em hábitos, procrastinação, rotina | Sugerir micro-hábitos e protocolos concretos |
| **Existencial** | Questiona papel de vida, propósito, identidade | Reposicionar missão e legado |

### 2.2 Analisar Incongruências Simbólicas

Exemplo: Usuário pontua alto em "Vida Profissional" mas revela "frases automáticas" de falha na "Saúde Mental"

### 2.3 Gerar Perguntas que Cruzem Eixos

Identificar a **Barreira** oculta entre áreas correlacionadas

### 2.4 Mapear o Gap MX

Distância entre a narrativa vivida e a narrativa escolhida

### 2.5 Prescrever Âncoras Práticas

Com base no Ponto de Entrada e na Fase da Jornada, sugerir 3 Âncoras Práticas específicas das 19 disponíveis.

---

<a name="perguntas-3-templates-para-fases-adaptativas"></a>
## 3. Templates para Fases Adaptativas

### Template: Alta Autocrítica Identificada

```json
{
  "trigger_pattern": "autocritica_alta",
  "ponto_entrada": "Emocional",
  "tecnica_tcc": "Flecha Descendente",
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
  ],
  "ancoras_sugeridas": ["Tom", "Rituais Matinais", "Gestão de Energia"]
}
```

### Template: Conflito Trabalho-Família

```json
{
  "trigger_pattern": "conflito_trabalho_familia",
  "ponto_entrada": "Simbólico",
  "tecnica_tcc": "Questionamento Socrático",
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
  ],
  "ancoras_sugeridas": ["Limites", "Rituais Noturnos", "Testemunhas"]
}
```

### Template: Falta de Propósito

```json
{
  "trigger_pattern": "falta_proposito",
  "ponto_entrada": "Existencial",
  "tecnica_tcc": "Descatastrofização",
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
  ],
  "ancoras_sugeridas": ["Referências", "Tarefas Identitárias", "Grupo"]
}
```

### Template: Área com Baixa Cobertura (< 2 respostas)

**Saúde Espiritual:**
```json
{
  "area_id": 3,
  "ponto_entrada": "Existencial",
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
  "ponto_entrada": "Comportamental",
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

# PARTE VII: OPERAÇÃO E VALIDAÇÃO

---

<a name="operacao-1-critérios-de-elegibilidade"></a>
## 1. Critérios de Elegibilidade

### Critérios para Finalização do Diagnóstico

O diagnóstico pode ser finalizado quando **UMA** das condições for atendida:

| Critério | Valor Mínimo |
|----|----|
| **Número de respostas** | Mínimo 40 respostas |
| **Volume textual** | Mínimo 3.500 palavras |
| **Cobertura** | Todas as 12 áreas estruturantes abordadas |

### Validação de Cobertura

Para cada área, verificar:
- Pelo menos 1 resposta direta sobre a área
- Conteúdo qualitativo suficiente para análise
- Identificação de possíveis Memórias Vermelhas

---

<a name="operacao-2-síntese-metodológica-para-implementação"></a>
## 2. Síntese Metodológica para Implementação

### 2.1 Fluxo de Processamento

```
1. ENTRADA
   └── Respostas do usuário (texto narrativo aberto)

2. PRÉ-PROCESSAMENTO
   ├── Extração de palavras-chave e recorrentes
   ├── Identificação de padrões emocionais e tom dominante
   ├── Mapeamento para áreas estruturantes
   ├── Detecção de silêncios e respostas vagas
   └── Identificação do Ponto de Entrada predominante

3. ANÁLISE RAG
   ├── Construção de query diagnóstica (sintomas + hipótese)
   ├── Recuperação de chunks relevantes (por tipo de conteúdo)
   └── Cruzamento de recorrência + coerência

4. SÍNTESE DIAGNÓSTICA
   ├── Determinação do motor dominante
   ├── Identificação da fase da jornada
   ├── Mapeamento de crises (raiz + derivadas)
   ├── Definição do ponto de entrada ideal
   └── Seleção de Âncoras Práticas apropriadas

5. GERAÇÃO DE SAÍDA
   ├── Diagnóstico narrativo estruturado
   ├── Plano de Assunção Intencional com Âncoras específicas
   ├── Técnica de TCC recomendada
   ├── Visão de Clímax (MX)
   └── Vetor de Estado em JSON
```

### 2.2 Orientações Técnicas

1. **Preservar Citações:** Sempre usar aspas para destacar frases reais do usuário (Memórias Vermelhas)

2. **Respeitar Hierarquia:** Não propor ações de camadas superiores se as inferiores estão em crise
   - Identidade → Sentido → Ação → Conexão

3. **Respeitar o Ponto de Entrada:** Não force uma porta que não está aberta
   - Se é Emocional, não comece com Comportamental
   - Se é Simbólico, não pule para ação

4. **Linguagem Metodológica:** Usar consistentemente os termos da metodologia (M1, MX, CN+, etc.), explicando quando necessário

5. **Tom Empático-Autoritário:** Como um "Engenheiro da Alma" - provocador mas compassivo

6. **Evitar Clichês:** Substituir autoajuda genérica por técnicas específicas de TCC e reestruturação cognitiva

7. **Prescrever Âncoras Específicas:** Sempre incluir 3 Âncoras Práticas concretas das 19 disponíveis

### 2.3 Checklist de Qualidade do Diagnóstico

- [ ] Motor dominante claramente identificado
- [ ] Fase da jornada definida
- [ ] Cluster de crise mapeado
- [ ] Ponto de Entrada identificado
- [ ] Pelo menos 3 citações do usuário (Memórias Vermelhas)
- [ ] Conexões entre áreas reveladas
- [ ] Áreas silenciadas identificadas (se houver)
- [ ] Técnica de TCC apropriada indicada
- [ ] Plano de Assunção com 3 Âncoras Práticas específicas
- [ ] Visão de Clímax inspiradora e personalizada
- [ ] Vetor de Estado em JSON incluído

---

## REFERÊNCIAS METODOLÓGICAS

Este documento consolida a metodologia de **Transformação Narrativa** desenvolvida por **Phellipe Oliveira**, integrando:

- As 12 Áreas Estruturantes do Círculo Narrativo
- Os 4 Motores Motivacionais
- As 6 Fases da Jornada de Maturação
- Os 4 Níveis de Identidade (Luz Total)
- Os 4 Pontos de Entrada (Portas de Intervenção)
- Os 6 Clusters Operacionais de Crise
- As Travas-Fonte e Análise Causal
- O Mecanismo de Assunção Intencional
- O Ferramental da TCC para a IA
- As 19 Âncoras Práticas
- A Estrutura do Fluxo Narrativo
- Os Eixos de Transformação (Narrativa, Identidade, Hábitos)
- A Psicografia do Usuário
- Os Refinamentos para RAG

---