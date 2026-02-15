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
8. [Prompts do Sistema](#8-prompts-do-sistema)
9. [Perguntas Baseline](#9-perguntas-baseline)
10. [Knowledge Base](#10-knowledge-base)

**Referência no código:** As 12 áreas, perguntas baseline, motores, fases e tipos de crise estão implementados em `nara-backend/app/core/constants.py`. O pipeline de diagnóstico (`nara-backend/app/rag/pipeline.py`) e o frontend (`nara-frontend/src/data/areas.ts`) usam essa base. A tabela `areas` no Supabase segue a mesma ordem (migrations).

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

#### Dinâmica Temporal nas Crises

| Tempo | Eixo de Intervenção | Foco |
|----|----|----|
| **Passado** | Narrativa | Ressignificar memórias vermelhas |
| **Presente** | Identidade | Estabilizar valores e limites |
| **Futuro** | Hábitos | Materializar a visão MX |

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

#### Detalhamento dos Clusters

**A. Crises de Identidade (A Raiz)**
- **Identidades Herdadas:** Viver sob rótulos impostos por pais, escola ou cultura, atuando papéis que não foram escolhidos.
- **Vergonha e Indignidade:** Capítulos do passado que o indivíduo tenta esconder ou que o fazem sentir-se indigno do "papel principal" em sua própria história.
- **Autoimagem Desatualizada:** Quando a pessoa já evoluiu internamente, mas sua identidade simbólica ainda está presa a uma versão antiga.

**B. Crises de Sentido e Direção**
- **Vazio e Fragmentação:** Sensação de viver episódios desconexos, sem uma linha condutora que una passado, presente e futuro.
- **Falta de Visão de Futuro:** A paralisia que ocorre quando o futuro é opaco ou nebuloso, impedindo que o presente tenha tração.
- **Urgência Tóxica:** O sentimento de estar "atrasado" ou de que o tempo foi desperdiçado.

**C. Crises de Ação e Estrutura (Execução)**
- **Paralisia Decisória:** A "espera por permissão" e o medo de tomar o protagonismo, muitas vezes disfarçados de procrastinação ou planejamento excessivo.
- **Ausência de Ritos:** A vida no "automático", onde faltam marcos simbólicos, limites claros e rotinas que protejam a energia e a história do indivíduo.

**D. Crises de Conexão e Expressão**
- **Invisibilidade Simbólica:** Medo de brilhar, de incomodar ou de ser julgado, o que leva o indivíduo a sabotar sua própria presença e voz em espaços de poder.
- **Incongruência com o Ambiente:** O desgaste de tentar manter uma nova identidade em contextos antigos que insistem em tratar a pessoa como sua versão anterior.
- **Solidão Existencial:** A falta de "testemunhas significativas" que validem a jornada e a história vivida.

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

---

## 3. INTELIGÊNCIA CONTEXTUAL VIA RAG

### Princípio Fundamental

> O RAG não serve para responder perguntas do usuário. Ele serve para **revelar o usuário para si mesmo**.

Os documentos no sistema RAG não devem ser tratados como conteúdo, mas como **lentes interpretativas**. Não estamos buscando "o texto certo" — estamos buscando o **enquadramento simbólico mais adequado** ao estado atual da pessoa.

### 🎯 Construção de Inteligência Contextual

#### O que captar relativo ao Público-Alvo

Para entender o contexto desse público, é preciso olhar além dos dados demográficos tradicionais (como a faixa de 30 a 55 anos e a predominância feminina de 60%). A inteligência contextual deve focar em:

- **Motores de Motivação:** Identificar qual impulso move o indivíduo no momento: a Necessidade (busca alívio de falta interna), o Valor (busca coerência interna), o Desejo (busca realização externa) ou o Propósito (busca impacto no mundo).
- **Estágios da Jornada (Maturação):** Captar em que fase do ciclo o indivíduo se encontra: se está apenas reconhecendo a insatisfação (Germinar), buscando valores sólidos (Enraizar), praticando novos hábitos (Desenvolver), expressando sua singularidade (Florescer), entregando resultados (Frutificar) ou buscando impacto coletivo (Realizar).
- **Perfil Cognitivo e Demandas:** Reconhecer que são aprendizes contínuos que rejeitam fórmulas prontas e buscam metodologias que unam profundidade simbólica com aplicabilidade prática.
- **A "Fome" de Nutrição:** O público busca referências que transbordem originalidade, espiritualidade e grandeza, além de uma comunidade que ofereça apoio, inspiração e exemplos reais.
- **O Dilema Central:** Captar o sentimento de incoerência entre o que eles acreditam/desejam e os resultados que estão vivendo, o que gera uma sensação de "traição a si mesmo".

#### O que explorar em relação às Crises Vividas

As crises devem ser exploradas não como problemas isolados, mas como **rupturas no fluxo narrativo** e chamados para a ressignificação. A distância entre a expectativa e o resultado real (o gap MX) manifesta-se nas quatro camadas já descritas.

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

**👉 Isso é o que transforma RAG em Inteligência Contextual.**

### Processo de Determinação do Usuário

#### ETAPA 1 — Coleta Bruta (o que o usuário diz)

**Fontes:**
- Respostas textuais
- Notas numéricas  
- Palavras recorrentes
- Silêncios (áreas não respondidas ou vagas)

Aqui não há diagnóstico, apenas matéria-prima.

#### ETAPA 2 — Análise Interna (Pré-RAG)

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

#### ETAPA 3 — Construção da Query RAG (momento crítico)

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

#### ETAPA 4 — O RAG devolve hipóteses, não respostas

O retriever retorna documentos que representam:
- possíveis motores dominantes
- possíveis estágios da jornada
- possíveis tipos de crise
- possíveis pontos de entrada (emocional, simbólico, comportamental)

**Você não usa tudo. Você cruza recorrência + coerência.**

#### ETAPA 5 — Síntese Diagnóstica

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

### Síntese Absoluta

> Seu RAG não deve responder "o que fazer", mas revelar **"quem o usuário está sendo agora"** — e qual estrutura interna precisa ser reorganizada primeiro.

---

## 4. STACK TÉCNICO DEFINITIVO

### Arquitetura Geral

```
┌────────────────────────────────────────────────┐
│                    FRONTEND                    │
│  React 18 + TypeScript + Vite                  │
│  ├── Tailwind CSS (estilização)                │
│  ├── shadcn/ui (componentes)                   │
│  ├── Zustand (state management)                │
│  ├── React Hook Form + Zod (formulários)       │
│  ├── TanStack Query (data fetching)            │
│  ├── Framer Motion (animações)                 │
│  └── Recharts (gráfico radar)                  │
│                    │                            │
│                    │ HTTP/REST (axios)          │
│                    ▼                            │
└────────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────┐
│               BACKEND (FastAPI + Python)       │
│  ├── POST /api/diagnostic/start                │
│  ├── GET  /api/diagnostic/{id}/questions       │
│  ├── POST /api/diagnostic/{id}/answer          │
│  ├── GET  /api/diagnostic/{id}/eligibility     │
│  ├── POST /api/diagnostic/{id}/finish          │
│  └── GET  /api/diagnostic/{id}/result          │
└────────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────┐
│            DATABASE (Supabase/PostgreSQL)      │
│  ├── profiles, diagnostics, answers            │
│  ├── knowledge_chunks (pgvector)               │
│  ├── feedback, waitlist, email_logs            │
│  └── RLS (Row Level Security)                  │
└────────────────────────────────────────────────┘
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

### 4.1 Problemas Específicos Identificados

#### Estrutura de Implementação LangChain

**Problemas Identificados:**

1. **Número de fases:** Menciona "Fase Baseline + Fases Adaptativas" genericamente, sem especificar que são 4 fases (60 perguntas total)

2. **Critério de elegibilidade NÃO implementado:**
   - Não há lógica para verificar: 40 respostas mínimas **OU** 3.500 palavras mínimas
   - Deve ser adicionado no método `process_diagnostic_completion()`

**Ajustes Necessários:**
- Implementar lógica de elegibilidade
- Adicionar validação para máximo de 4 fases (60 perguntas)
- Revisar código conforme nota do autor
- Adicionar tratamento de erros mais robusto
- Implementar retry logic para chamadas à OpenAI

### 4.2 Documentação Didática

**Tipo:** Documentação didática completa

**Estrutura do Conteúdo:**
1. O que o sistema é (visão geral)
2. O nascimento do sistema (`__init__`)
3. Perguntas fixas (baseline)
4. Geração de perguntas personalizadas (RAG)
5. Análise do contexto das respostas
6. Geração da próxima fase
7. Construção da query RAG
8. Análise final do diagnóstico
9. Cálculo de pontuações
10. FastAPI (porta de entrada)
11. Visão geral do sistema (diagrama)
12. Fluxo completo passo a passo

**Destaques:**
- Excelente material de **onboarding** para desenvolvedores
- Diagramas ASCII do fluxo de dados
- Tradução "humana" de cada componente técnico
- Explica conceitos de RAG de forma acessível

**Uso Recomendado:** Leitura obrigatória antes de mexer no código.

---

## 5. MODELO RAG COM BATCH GENERATION

### Por que RAG + Batch Generation?

✅ **Personalização Máxima:** Perguntas adaptadas ao perfil único de cada usuário  
✅ **Qualidade Garantida:** RAG reduz alucinações (contexto fundamentado)  
✅ **UX Otimizada:** Latência concentrada (3-5s entre fases), navegação fluida  
✅ **Escalabilidade:** pgvector suporta milhões de chunks, custo previsível

### Fluxo de Geração

```
┌────────────────────────────────────────────────┐
│              FASE 1: BASELINE (15 perguntas fixas)              │
│  • Idênticas para todos os usuários                    │
│  • Custo: R$ 0,00                    │
└────┬───────────────────────────────────────────┘
                    │ Completa 15 respostas
                    ▼
┌────────────────────────────────────────────────┐
│           TRIGGER: GERAÇÃO FASE 2 (RAG + LLM)                   │
│  1. Analisar respostas → identificar áreas críticas             │
│  2. Construir query diagnóstica                    │
│  3. Buscar chunks relevantes (pgvector - top 10)                │
│  4. GPT-4o mini gera 15 perguntas personalizadas                │
│  5. Tempo: 3-5 segundos | Custo: R$ 0,004                    │
└────┬───────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────┐
│              FASE 2-4: ADAPTIVE PROBING                    │
│  • 15 perguntas por fase (geradas via RAG)                    │
│  • Progressive Disclosure (uma por vez)                    │
│  • Latência percebida: ZERO após geração                    │
└────┬───────────────────────────────────────────┘
                    │ Critério de parada atingido
                    ▼
┌────────────────────────────────────────────────┐
│              PROCESSAMENTO FINAL (GPT-4o)                    │
│  • Buscar contexto RAG para áreas críticas                    │
│  • Gera relatório detalhado (~2.500 tokens)                    │
│  • Tempo: 5-10 segundos | Custo: R$ 0,17                    │
└────────────────────────────────────────────────┘
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

CAMINHO DE OTIMIZAÇÃO DO PROJETO

🎯 **Estratégia de Três Fases**

#### **FASE 1: MVP Beta (Atual) - Qualidade Máxima**

**Configuração:**
- RAG + GPT-4o para geração de perguntas
- GPT-4o para relatório final
- **Custo:** R$ 0,182/diagnóstico

**Objetivo:**
- Validar qualidade máxima do sistema
- Coletar feedback qualitativo detalhado
- Estabelecer baseline de "wow factor"

**Duração:** 4-8 semanas (20-50 usuários beta)

---

#### **FASE 2: Otimização Pós-Beta - Redução de Custos**

**Configuração:**
- **A/B Test:** 50% GPT-4o vs. 50% GPT-4o mini (geração de perguntas)
- Manter GPT-4o para relatório final
- **Custo:** menor (grupo otimizado)

**Objetivo:**
- Comparar qualidade percebida (NPS, feedback)
- Validar se GPT-4o mini mantém qualidade aceitável
- Decisão data-driven: custo vs. qualidade

**Métricas de Sucesso:**
- Se diferença de NPS < 5 pontos: Migrar para GPT-4o mini
- Se feedback qualitativo similar: Adotar otimização
- Redução de custo: 50% (mais economia por diagnóstico)

**Duração:** 2-4 semanas (100-200 diagnósticos)

---

#### **FASE 3: Escala - Otimizações Avançadas**

**Implementar progressivamente:**

1. **Cache de Perguntas Similares**
   - Armazenar perguntas geradas para perfis similares
   - Reutilizar quando padrões se repetem
   - Economia estimada: 20-30% em diagnósticos similares

2. **Fine-Tuning de Modelo Próprio**
   - Treinar GPT-4o mini com dados reais (após 1.000+ diagnósticos)
   - Especializar em geração de perguntas metodológicas
   - Redução potencial: 80-90% do custo de geração

3. **Hybrid Approach**
   - Perguntas frequentes: Biblioteca pré-gerada
   - Perguntas específicas: RAG + LLM
   - Custo variável baseado em complexidade

**Projeção de Custo em Escala (Fase 3):**
- Custo estimado: menor/diagnóstico
- Manter qualidade com 70-85% de economia

---

### 4.6. DECISÃO FINAL

🎯 **INÍCIO COM GPT-4O, MIGRAÇÃO PROGRESSIVA PARA GPT-4O MINI**

**Justificativa:**

1. **Validação de Qualidade Primeiro**
   - MVP beta com GPT-4o garante melhor impressão inicial
   - Custo adicional é negligível em validação (< R$ 20 total)
   - "Wow factor" maximizado nos primeiros 20-30 usuários críticos

2. **Otimização Data-Driven**
   - A/B test pós-beta com dados reais
   - Decisão baseada em métricas (NPS, feedback, qualidade percebida)
   - Migração gradual sem risco

3. **Caminho de Escala Claro**
   - Redução de 50% (Fase 2) + 80-90% (Fase 3)
   - Custo final em escala: bem menor
   - Margens excelentes para modelo de negócio futuro

**Custo Esperado por Fase:**
- Beta (50 usuários): R$ x
- Pós-Beta (500 usuários): R$ y
- Escala (5.000 usuários): R$ z

**Conclusão:** Custo de IA é **irrelevante** para viabilidade do negócio, mas otimizações progressivas aumentam margens futuras.

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

### Termos de Negócio

| Termo | Definição |
|----|----|
| **Progressive Disclosure** | Padrão UX de revelar informação gradualmente |
| **Batch Generation** | Gerar múltiplos itens em uma única chamada |
| **Magic Link** | Link de acesso único enviado por e-mail |
| **NPS** | Net Promoter Score — métrica de satisfação (-100 a +100) |
| **CTR** | Click-Through Rate — taxa de cliques |

---

## 8. PROMPTS DO SISTEMA

### 8.1 Prompt para Geração de Insights (Análise Final)

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

### 8.2 Prompt para Geração de Perguntas (Escuta Ativa)

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

### 8.3 Prompt para Análise Final (Diagnóstico Narrativo)

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

### 8.4 Prompts Auxiliares (Classificação e RAG)

```python
ANSWER_ANALYSIS_PROMPT = """
Analise as respostas e classifique sob a ótica da Engenharia de Mindset:
1. MEMÓRIAS VERMELHAS (M1): Conflitos e fatos não dominados.
2. BARREIRAS (PONTOS DE PROVA): Autossabotagem, procrastinação ou ambiente hostil.
3. CAPITAL SIMBÓLICO: Recursos sociais ou culturais que o usuário já possui.
4. FCU (Forma, Conteúdo e Uso): Como o usuário expressa sua atual posição.
"""

RAG_QUERY_TEMPLATE = """
Com base na Metodologia de Phellipe Oliveira, busque estratégias para:
ÁREA DO CÍRCULO NARRATIVO: {areas}
DOMÍNIO TEMÁTICO: {temas}
FASE DA JORNADA: {fase}
CONTEXTO DE CONFLITO: {contexto}
"""
```

---

## 9. PERGUNTAS BASELINE

As perguntas de baseline são estruturadas para realizar uma sondagem profunda e "abrir as verdades" sobre o indivíduo, ancoradas na **Metodologia de Transformação Narrativa**. As 15 perguntas iniciais para o diagnóstico de **M1 (Estado de Crise)** são:

### Perguntas para as 12 Áreas da Vida:

1. **Vida Pessoal:** Se sua vida hoje fosse um livro, qual seria o título do capítulo atual? De 0 a 5, o quanto você se sente de fato o **protagonista** da sua própria história?

2. **Saúde Física:** Como você avalia sua constituição e disposição corporal para os desafios da sua jornada? (0 = exausto, 5 = plena vitalidade). Descreva como o seu corpo tem reagido ao seu ritmo atual.

3. **Saúde Mental:** Quais **"frases automáticas"** de autocrítica ou medo mais visitam sua mente hoje? (0 = mente caótica, 5 = equilíbrio total).

4. **Saúde Espiritual:** O que dá sentido e **convicção interior** à sua existência hoje? (0 = perdido/sem fé, 5 = convicção plena).

5. **Vida Familiar:** Você sente que vive sob **"identidades herdadas"** ou valores familiares que não escolheu conscientemente? (0 = prisioneiro de rótulos, 5 = autêntico).

6. **Vida Amorosa:** Existe parceria e alinhamento emocional para a construção do seu **Círculo Narrativo Futuro (CN+)**? (0 = insatisfeito, 5 = pleno).

7. **Vida Social:** Suas interações atuais funcionam como um **"campo gravitacional"** que te nutre ou que drena sua energia? (0 = ambiente tóxico, 5 = rede nutritiva).

8. **Vida Profissional:** Você sente que domina seu ofício ou que está apenas atuando um papel que não condiz com quem você realmente é? (0 = frustrado, 5 = realizado).

9. **Finanças:** Como está a gestão do seu capital para sustentar a estrutura de vida que você deseja? (0 = caos/preocupação, 5 = total controle).

10. **Educação:** Você está em um processo ativo de **modelagem** de novos padrões ou sente que seu aprendizado está estagnado? (0 = estagnado, 5 = aprendiz contínuo).

11. **Inovação:** Quanto espaço real você reserva para a **criatividade** e para testar novas formas de resolver seus problemas? (0 = nenhum espaço, 5 = fluxo constante).

12. **Lazer:** Como você utiliza seu tempo livre para recuperação de energia e **rituais de descompressão**? (0 = inexistente, 5 = equilibrado).

### Perguntas Generalistas de Apoio (Sondagem de Motor e Gap MX)

13. **Identificação do Motor:** O que mais te move hoje: o alívio de uma dor (**Necessidade**), a busca por coerência (**Valor**), a conquista de algo (**Desejo**) ou o impacto no mundo (**Propósito**)?

14. **Conflito Raiz (M1):** Se você pudesse transpor um **único conflito** central hoje para alcançar sua meta extraordinária, qual seria esse obstáculo?

15. **Visão de Clímax (MX/M2X):** Descreva sua versão extraordinária daqui a 12 meses. O que essa pessoa faz no dia a dia que você, na sua versão atual, ainda não consegue realizar?

### Lógica da Intervenção para a IA

Após essas respostas, a inteligência contextual deve analisar as **incongruências simbólicas** reveladas. Por exemplo, se o usuário pontua alto em "Vida Profissional", mas revela "frases automáticas" de falha na "Saúde Mental", a IA deve gerar perguntas que cruzem esses eixos para identificar a **Barreira** oculta. O objetivo é mapear o **Gap MX** — a distância entre a narrativa vivida e a narrativa escolhida.

---

## 10. KNOWLEDGE BASE

Base de conhecimento organizada pelas 12 Áreas Estruturantes Específicas do Círculo Narrativo, baseada na Metodologia de Transformação Narrativa de Phellipe Oliveira.

### 1. SAÚDE FÍSICA

#### Fundamentos Narrativos

A Saúde Física refere-se à manutenção da constituição física e disposição corporal necessária para executar as tarefas da jornada. Na metodologia, o corpo é o principal canal das mensagens e o codificador singular da nova identidade.

**Componentes de Domínio (M2):**
- Vitalidade e vigor para transpor obstáculos.
- Sincronia entre disposição física e metas (MX).
- Gestão de energia como recurso para a 'Força-Tarefa'.

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Exaustão crônica impedindo a ação (Volição).
- Falta de domínio sobre hábitos biológicos básicos.
- Incongruência entre a imagem física e a identidade pretendida.

#### Diagnóstico M1 e Projeção MX

**Perguntas para localizar o Ponto de Entrada:**
- De 0 a 5, quanto seu corpo suporta a velocidade da sua visão de futuro?
- Sua rotina física atual é uma âncora de progresso ou uma barreira de inércia?
- Se seu corpo fosse um personagem, ele seria o protagonista ou um figurante cansado?

**Conexão com Motores:**
- **Necessidade:** Busca por alívio de dores ou limitações.
- **Desejo:** Busca por performance e vitalidade extraordinária.

---

### 2. SAÚDE MENTAL

#### Fundamentos Narrativos

Foca no equilíbrio das funções cognitivas e na gestão das emoções para evitar sabotagens internas. É o campo onde se aplica a TCC (Terapia Cognitivo-Comportamental) para reestruturar a 'velha narrativa'.

**Técnicas de Domínio (M2):**
- Identificação de Pensamentos Automáticos e Distorções Cognitivas.
- Reestruturação Cognitiva: trocar a 'vítima' pelo 'autor'.
- Descatastrofização de cenários de medo.

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Narrativa interna caótica ou contraditória.
- Bloqueios narrativos por capítulos ocultos ou vergonha do passado.
- Ansiedade por falta de linearidade entre passado e futuro.

---

### 3. SAÚDE ESPIRITUAL

#### Fundamentos Narrativos

Relaciona-se à força da fé e à convicção interior que impulsionam a manifestação dos propósitos da alma. É a âncora que dá sentido à travessia.

**Componentes de Domínio (M2):**
- Convicção plena na visão de futuro (MX).
- Alinhamento existencial: saber 'por que tudo isso importa'.
- Paz interior baseada na integridade (falar, sentir e agir em harmonia).

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Vazio existencial ou falta de direção transcendental.
- Crise de indignidade perante a própria grandeza.
- Desconexão com os valores inegociáveis da alma.

---

### 4. VIDA PESSOAL

#### Fundamentos Narrativos

Concentra-se no autoconhecimento, na descoberta da própria essência e na organização dos interesses individuais. É o centro da 'Luz Total' da personagem.

**Componentes de Domínio (M2):**
- Identidade clara: saber 'quem sou' além dos rótulos.
- Autonomia: escrever o próprio enredo sem esperar permissão.
- Congruência entre o mundo interno e a autoimagem.

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Sensação de estar perdido em meio a narrativas alheias.
- Falta de enredo que conecte os momentos da vida.
- Vazio por falta de uma 'Fantasia Pessoal' estimulante.

---

### 5. VIDA AMOROSA

#### Fundamentos Narrativos

Abrange os relacionamentos íntimos e o convívio afetuoso. Na metodologia, busca-se parcerias que nutram a construção do Círculo Narrativo Futuro (CN+).

**Componentes de Domínio (M2):**
- Identidade preservada dentro da união.
- Atmosfera emocional de apoio mútuo e incentivo ao florescimento.
- Comunicação assertiva de necessidades e limites.

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Vínculos superficiais que não despertam a autenticidade.
- Incongruência entre os valores do parceiro e a própria trajetória.
- Medo de se perder ao crescer, gerando autossabotagem afetiva.

---

### 6. VIDA FAMILIAR

#### Fundamentos Narrativos

Trata dos vínculos de parentesco e dos valores morais inicialmente absorvidos. É onde muitas vezes se encontram as 'Identidades Herdadas' que precisam ser ressignificadas.

**Componentes de Domínio (M2):**
- Limites saudáveis entre o 'eu decidido' e as expectativas parentais.
- Ritos e rituais familiares que nutrem a identidade.
- Presença e cuidado sem perda da autonomia narrativa.

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Conflitos de valores inegociáveis com membros do grupo íntimo.
- Vergonha da origem ou de capítulos não resolvidos.
- Atuar papéis impostos por tradições obsoletas.

---

### 7. VIDA SOCIAL

#### Fundamentos Narrativos

Refere-se às interações com a comunidade e à seleção de redes de contato (Recurso Social). O crescimento ocorre ao orbitar ambientes nutritivos e pessoas 'condutoras'.

**Componentes de Domínio (M2):**
- Capital Social: rede de relações que potencializa o indivíduo.
- Habilidade de Relating: descobrir as histórias e motivações do outro.
- Influência Social: falar sobre o que interessa e motiva o público.

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Ambientes estagnados que puxam para a 'antiga versão'.
- Solidão existencial mesmo rodeado de pessoas.
- Medo do julgamento ou de brilhar em público.

---

### 8. VIDA PROFISSIONAL

#### Fundamentos Narrativos

Foca na atuação produtiva, no domínio de competências técnicas e no desenvolvimento da carreira e autoridade (Capital Simbólico). O objetivo é alcançar o Nível de Posição defendido e reconhecido.

**Componentes de Domínio (M2):**
- Maestria técnica e autoridade percebida.
- Alinhamento entre a tarefa diária (Missão) e o legado (Propósito).
- Comunicação clara do diferencial competitivo.

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Sentimento de estar atuando um papel que não condiz com quem se é.
- Invisibilidade em espaços de poder e decisão.
- Procrastinação por falta de clareza sobre o próximo 'clímax' profissional.

---

### 9. FINANÇAS

#### Fundamentos Narrativos

Envolve a gestão do capital econômico e recursos materiais necessários para sustentar a estrutura de vida e o Círculo Narrativo. O dinheiro é visto como um recurso para a liberdade de ser, fazer e saber.

**Componentes de Domínio (M2):**
- Gestão de capital alinhada aos valores assumidos.
- Capacidade de investimento na própria transformação e ambiente.
- Estabilidade financeira para suportar a 'travessia'.

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Ansiedade por desorganização material.
- Crenças limitantes de escassez herdadas da família.
- Falta de recursos para materializar a visão (MX).

---

### 10. EDUCAÇÃO

#### Fundamentos Narrativos

Diz respeito à busca contínua por conhecimento, aprendizagem sistemática e aperfeiçoamento intelectual. É o processo de 'Modelagem' ativa de novos padrões de sucesso.

**Componentes de Domínio (M2):**
- Aprendizagem de processos (M3) para acelerar a própria jornada.
- Domínio de novos códigos linguísticos e mentais.
- Mentalidade de crescimento (Growth Mindset).

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Estagnação intelectual e apego a crenças obsoletas.
- Excesso de preparação sem ir para a ação (Paralisia).
- Dificuldade em transformar informação em habilidade prática.

---

### 11. INOVAÇÃO

#### Fundamentos Narrativos

Capacidade de criar, pesquisar e desenvolver novas formas de resolver problemas ou expressar a identidade. É a ousadia de testar limites criativos.

**Componentes de Domínio (M2):**
- Prototipagem de novos caminhos e ideias (M2X).
- Flexibilidade e adaptabilidade diante de perdas ou rupturas.
- Curiosidade genuína por experiências históricas e subjetivas.

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Medo de recomeçar ou de construir uma nova identidade.
- Bloqueio criativo por excesso de autocrítica.
- Repetição de ciclos exaustivos sem renovação.

---

### 12. LAZER

#### Fundamentos Narrativos

Compreende as atividades de entretenimento e o uso do tempo livre para recuperação de energia e prazer. Serve como ritual de descompressão necessário para manter a constância.

**Componentes de Domínio (M2):**
- Rituais de sensibilidade e propósito que recarregam a volição.
- Hobbies que expressam a criatividade sem pressão de resultado.
- Equilíbrio entre esforço e descanso.

**Sinais de Conflito (M1 - Memórias Vermelhas):**
- Culpa por descansar ou automatização da vida.
- Lazer viciado que drena em vez de nutrir.
- Ausência de pausas para celebrar microvitórias.

---