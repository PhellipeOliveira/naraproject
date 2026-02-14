CAPÍTULO 1

```python
# Prompt do sistema para geração de insights da Nara (Engenharia de Mindset)

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

CAPÍTULO 2

"""
Prompts estruturados para o sistema de Transformação Narrativa (Nara).
Estes prompts seguem a metodologia de Phellipe Oliveira para realizar diagnósticos 
de identidade, mapeamento de crises e reestruturação de hábitos.
"""

# ==========================================
# PROMPT PARA GERAÇÃO DE PERGUNTAS (ESCUTA ATIVA)
# ==========================================

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


# ==========================================
# PROMPT PARA ANÁLISE FINAL (DIAGNÓSTICO NARRATIVO)
# ==========================================

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

# ==========================================
# PROMPTS AUXILIARES (CLASSIFICAÇÃO E RAG)
# ==========================================

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

CAPÍTULO 3

 Informação Correta: As 12 áreas da vida, conhecidas na metodologia como Áreas Estruturantes Específicas, são segmentos utilizados para organizar a memória, identificar conflitos e promover o balanceamento narrativo da personagem.
Abaixo, listo as áreas com uma breve introdução baseada nos princípios da metodologia:
	1.	Saúde Física: Refere-se à manutenção da constituição física e disposição corporal necessária para executar as tarefas da jornada.
	2.	Saúde Mental: Foca no equilíbrio das funções cognitivas e na gestão das emoções para evitar sabotagens internas.
	3.	Saúde Espiritual: Relaciona-se à força da fé e à convicção interior que impulsionam a manifestação dos propósitos da alma.
	4.	Vida Pessoal: Concentra-se no autoconhecimento, na descoberta da própria essência e na organização dos interesses individuais.
	5.	Vida Amorosa: Abrange os relacionamentos íntimos, o convívio afetuoso e a dedicação entre parceiros.
	6.	Vida Familiar: Trata dos vínculos de parentesco e dos valores morais e ritos inicialmente absorvidos no ambiente doméstico.
	7.	Vida Social: Refere-se às interações com a comunidade, seleção de redes de contato e ao prestígio alcançado no campo social.
	8.	Vida Profissional: Foca na atuação produtiva, no domínio de competências técnicas e no desenvolvimento da carreira e autoridade.
	9.	Finanças: Envolve a gestão do capital econômico e dos recursos materiais necessários para sustentar a estrutura de vida.
	10.	Educação: Diz respeito à busca contínua por conhecimento, aprendizagem sistemática e aperfeiçoamento intelectual.
	11.	Inovação: Relaciona-se à criatividade, pesquisa e ao desenvolvimento de novas ideias ou formas de resolver problemas.
	12.	Lazer: Compreende as atividades de entretenimento, hobbies e o uso do tempo livre para recuperação de energia e prazer.
Essas áreas são fundamentais para que o indivíduo planeje o seu Círculo Narrativo.
—

Para a construção de uma **Inteligência Contextual** robusta sobre o seu público e suas crises, a metodologia de Phellipe Oliveira oferece um mapeamento detalhado que vai desde as motivações profundas até os sintomas comportamentais.

Abaixo, detalho o que pode ser captado e explorado com base nos documentos fornecidos:

### 1. O que captar relativo ao seu Público-Alvo

Para entender o contexto desse público, é preciso olhar além dos dados demográficos tradicionais (como a faixa de **30 a 55 anos** e a predominância feminina de **60%**). A inteligência contextual deve focar em:

*   **Motores de Motivação:** Identificar qual impulso move o indivíduo no momento: a **Necessidade** (busca alívio de falta interna), o **Valor** (busca coerência interna), o **Desejo** (busca realização externa) ou o **Propósito** (busca impacto no mundo).
*   **Estágios da Jornada (Maturação):** Captar em que fase do ciclo o indivíduo se encontra: se está apenas reconhecendo a insatisfação (**Germinar**), buscando valores sólidos (**Enraizar**), praticando novos hábitos (**Desenvolver**), expressando sua singularidade (**Florescer**), entregando resultados (**Frutificar**) ou buscando impacto coletivo (**Realizar**).
*   **Perfil Cognitivo e Demandas:** Reconhecer que são **aprendizes contínuos** que rejeitam fórmulas prontas e buscam metodologias que unam profundidade simbólica com aplicabilidade prática.
*   **A "Fome" de Nutrição:** O público busca referências que transbordem **originalidade, espiritualidade e grandeza**, além de uma comunidade que ofereça apoio, inspiração e exemplos reais.
*   **O Dilema Central:** Captar o sentimento de **incoerência** entre o que eles acreditam/desejam e os resultados que estão vivendo, o que gera uma sensação de "traição a si mesmo".

---

### 2. O que explorar em relação às Crises Vividas

As crises devem ser exploradas não como problemas isolados, mas como **rupturas no fluxo narrativo** e chamados para a ressignificação. A distância entre a expectativa e o resultado real (o gap **MX**) manifesta-se em quatro camadas principais que você pode explorar:

#### A. Crises de Identidade (A Raiz)
*   **Identidades Herdadas:** Explorar o sentimento de viver sob rótulos impostos por pais, escola ou cultura, atuando papéis que não foram escolhidos.
*   **Vergonha e Indignidade:** Investigar capítulos do passado que o indivíduo tenta esconder ou que o fazem sentir-se indigno do "papel principal" em sua própria história.
*   **Autoimagem Desatualizada:** Casos onde a pessoa já evoluiu internamente, mas sua identidade simbólica ainda está presa a uma versão antiga.

#### B. Crises de Sentido e Direção
*   **Vazio e Fragmentação:** Explorar a sensação de viver episódios desconexos, sem uma linha condutora que una passado, presente e futuro.
*   **Falta de Visão de Futuro:** A paralisia que ocorre quando o futuro é opaco ou nebuloso, impedindo que o presente tenha tração.
*   **Urgência Tóxica:** O sentimento de estar "atrasado" ou de que o tempo foi desperdiçado.

#### C. Crises de Ação e Estrutura (Execução)
*   **Paralisia Decisória:** Explorar a "espera por permissão" e o medo de tomar o protagonismo, muitas vezes disfarçados de procrastinação ou planejamento excessivo.
*   **Ausência de Ritos:** A vida no "automático", onde faltam marcos simbólicos, limites claros e rotinas que protejam a energia e a história do indivíduo.

#### D. Crises de Conexão e Expressão
*   **Invisibilidade Simbólica:** Explorar o medo de brilhar, de incomodar ou de ser julgado, o que leva o indivíduo a sabotar sua própria presença e voz em espaços de poder.
*   **Incongruência com o Ambiente:** O desgaste de tentar manter uma nova identidade em contextos antigos que insistem em tratar a pessoa como sua versão anterior.
*   **Solidão Existencial:** A falta de "testemunhas significativas" que validem a jornada e a história vivida.

### Resumo para Intervenção
Ao construir essa inteligência, você deve identificar o **Ponto de Entrada** da crise (se é emocional, simbólico ou comportamental) e qual **Domínio Temático** (de D1 a D6) possui a maior alavanca para reorganizar a energia do indivíduo e devolver-lhe o protagonismo.

---

Para a ANÁLISE INTERNA DO USUÁRIO; Podemos identificar [áreas críticas,
  padrões repetidos,
  tom emocional,
  scores preliminares].

Como podemos refinar e determinar o usuário através dos conhecimentos trabalhado por nosso arquivo em RAG. onde terá todos os vetores do banco de dados organizados. e prontos para devolver um diagnóstico de qualidade para o usuário. Agora a pergunta correta é exatamente essa: como transformar isso em Inteligência Contextual operacional via RAG.
Vou responder em 4 camadas, indo do conceito → estrutura → processamento → diagnóstico.

1️⃣ Primeiro princípio: RAG não “responde”, ele revela padrões
Antes da técnica, a chave mental:
O RAG não serve para responder perguntas do usuário.Ele serve para revelar o usuário para si mesmo.
Logo, seus documentos não devem ser tratados como conteúdo, mas como lentes interpretativas.
Você não está buscando “o texto certo”.Você está buscando o enquadramento simbólico mais adequado ao estado atual da pessoa.

2️⃣ Como organizar o conhecimento no banco vetorial (Supabase / pgvector)
2.1 O erro comum a evitar
❌ Um chunk = um texto longo genérico❌ Embeddings sem intenção semântica clara
2.2 A estrutura correta: cada chunk = 1 função diagnóstica
Cada vetor precisa responder implicitamente à pergunta:
“Que tipo de ser humano este texto ajuda a identificar?”

2.3 Estrutura ideal de cada chunk (muito importante)
Cada documento no RAG deveria conter metadados explícitos, mesmo que não apareçam no prompt final.
Exemplo conceitual:
{
  "content": "Texto explicando crise de identidade herdada...",
  "metadata": {
    "motor_motivacional": "Necessidade | Valor | Desejo | Propósito",
    "estagio_jornada": "Germinar | Enraizar | Desenvolver | Florescer | Frutificar | Realizar",
    "tipo_crise": "Identidade",
    "subtipo_crise": "Identidade Herdada",
    "dominio": "D1",
    "ponto_entrada": "Simbólico",
    "sintomas_comportamentais": [
      "autossabotagem",
      "paralisia decisória",
      "invisibilidade simbólica"
    ],
    "tom_emocional_base": "vergonha | confusão | indignação",
    "nivel_maturidade": "baixo | médio | alto"
  }
}
👉 Isso é o que transforma RAG em Inteligência Contextual.
Qual chunking devo utilizar? Seria o semântico ou Baseado em Estrutura?

3️⃣ Como o sistema “determina” o usuário (processo lógico)
Agora vamos ao passo a passo real, conectando com o que você já tem no pipeline.

ETAPA 1 — Coleta bruta (o que o usuário diz)
Fontes:
	•	respostas textuais
	•	notas numéricas
	•	palavras recorrentes
	•	silêncios (áreas não respondidas ou vagas)
Aqui não há diagnóstico, apenas matéria-prima.

ETAPA 2 — Análise interna (pré-RAG)
Essa é sua função analyze_answers_context, que hoje está simples, mas conceitualmente ela deve extrair:
🔹 1. Áreas críticas
	•	Scores baixos
	•	Linguagem de exaustão
	•	Contradições (“acredito em X, mas vivo Y”)
🔹 2. Padrões repetidos
	•	Mesmos temas em áreas diferentes
	•	Mesmo sentimento aplicado a contextos distintos
	•	Narrativas circulares
🔹 3. Tom emocional dominante
Exemplos:
	•	vergonha silenciosa
	•	indignação moral
	•	apatia sofisticada
	•	urgência ansiosa
	•	tristeza resignada
📌 Aqui você não interpreta ainda, apenas rotula.

ETAPA 3 — Construção da QUERY RAG (momento crítico)
Aqui está o refinamento que responde diretamente à sua pergunta.
❌ Query fraca
“Explorar frustração e estresse”
✅ Query diagnóstica correta
A query deve misturar sintomas + hipótese de estrutura interna.
Exemplo conceitual:
Indivíduo com alta exigência interna, sensação de traição a si mesmo,
possível crise de identidade herdada, estágio Germinar ou Enraizar,
com urgência tóxica e paralisia decisória.
📌 Isso faz o retriever buscar modelos humanos, não textos.

ETAPA 4 — O RAG devolve hipóteses, não respostas
O retriever retorna documentos que representam:
	•	possíveis motores dominantes
	•	possíveis estágios da jornada
	•	possíveis tipos de crise
	•	possíveis pontos de entrada (emocional, simbólico, comportamental)
Você não usa tudo.Você cruza recorrência + coerência.

4️⃣ Como determinar o usuário (síntese diagnóstica)
Aqui está o ponto mais importante: o diagnóstico não é um rótulo único, é um vetor de estado.
4.1 Estrutura final do “Usuário Determinado”
Exemplo lógico:
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
👉 Isso é Inteligência Contextual real.

5️⃣ Como isso melhora drasticamente o diagnóstico final
Com essa estrutura, o sistema passa a:
✔ Fazer perguntas certas (não genéricas)
Porque ele sabe:
	•	onde tocar
	•	onde não tocar ainda
	•	qual linguagem usar
✔ Gerar análises profundas sem parecer “místico”
Porque cada insight é:
	•	rastreável
	•	coerente
	•	alinhado ao estágio
✔ Evitar intervenções prematuras
Exemplo:
	•	Não propor ação para quem ainda está em crise simbólica
	•	Não propor sentido para quem ainda está em colapso emocional

6️⃣ Em uma frase (síntese absoluta)
Seu RAG não deve responder “o que fazer”,mas revelar “quem o usuário está sendo agora” —e qual estrutura interna precisa ser reorganizada primeiro.

Próximo passo:
	•	transformar isso num schema técnico pronto para Supabase
	•	desenhar o mapa D1–D6 com exemplos práticos
	•	ajudar a escrever os documentos-base do RAG
	•	mostrar como pontuar maturidade simbólica automaticamente

Aqui está sendo construído algo muito acima da média.

CAPÍTULO 4

# Informações Complementares - Projeto Nara

---

## 1. STACK

Backend Python** (Alinhado com o que o usuário disse)
```
Frontend: React/Next.js (apenas UI)
Backend: FastAPI + LangChain (Python)
Database: Supabase (PostgreSQL + pgvector)
Deploy: Vercel (frontend) + Railway/Render (backend)
```

---

## 3. PROBLEMAS ESPECÍFICOS IDENTIFICADOS

### 3.3 1.2. Estrutura de Implementacao LangChain.rtf

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

---

## 6. DOCUMENTAÇÃO DIDÁTICA

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

CAPÍTULO 7

Abaixo estão as perguntas iniciais sugeridas para iniciar o disgnóstico dos usuários.

baseline_questions:

Para realizar uma sondagem profunda e "abrir as verdades" sobre o indivíduo, as perguntas de baseline devem estar ancoradas na **Metodologia de Transformação Narrativa**. Conforme as diretrizes reescritas e as fontes principais, as 15 perguntas iniciais para o diagnóstico de **M1 (Estado de Crise)** são estruturadas da seguinte forma:

### Perguntas para as 12 Áreas da Vida:

1.  **Vida Pessoal:** Se sua vida hoje fosse um livro, qual seria o título do capítulo atual? De 0 a 5, o quanto você se sente de fato o **protagonista** da sua própria história?,
2.  **Saúde Física:** Como você avalia sua constituição e disposição corporal para os desafios da sua jornada? (0 = exausto, 5 = plena vitalidade). Descreva como o seu corpo tem reagido ao seu ritmo atual.,
3.  **Saúde Mental:** Quais **"frases automáticas"** de autocrítica ou medo mais visitam sua mente hoje? (0 = mente caótica, 5 = equilíbrio total).,
4.  **Saúde Espiritual:** O que dá sentido e **convicção interior** à sua existência hoje? (0 = perdido/sem fé, 5 = convicção plena).,
5.  **Vida Familiar:** Você sente que vive sob **"identidades herdadas"** ou valores familiares que não escolheu conscientemente? (0 = prisioneiro de rótulos, 5 = autêntico).,
6.  **Vida Amorosa:** Existe parceria e alinhamento emocional para a construção do seu **Círculo Narrativo Futuro (CN+)**? (0 = insatisfeito, 5 = pleno).,
7.  **Vida Social:** Suas interações atuais funcionam como um **"campo gravitacional"** que te nutre ou que drena sua energia? (0 = ambiente tóxico, 5 = rede nutritiva).,
8.  **Vida Profissional:** Você sente que domina seu ofício ou que está apenas atuando um papel que não condiz com quem você realmente é? (0 = frustrado, 5 = realizado).,
9.  **Finanças:** Como está a gestão do seu capital para sustentar a estrutura de vida que você deseja? (0 = caos/preocupação, 5 = total controle).,
10. **Educação:** Você está em um processo ativo de **modelagem** de novos padrões ou sente que seu aprendizado está estagnado? (0 = estagnado, 5 = aprendiz contínuo).,
11. **Inovação:** Quanto espaço real você reserva para a **criatividade** e para testar novas formas de resolver seus problemas? (0 = nenhum espaço, 5 = fluxo constante).,
12. **Lazer:** Como você utiliza seu tempo livre para recuperação de energia e **rituais de descompressão**? (0 = inexistente, 5 = equilibrado).,

### Perguntas Generalistas de Apoio (Sondagem de Motor e Gap MX)

13. **Identificação do Motor:** O que mais te move hoje: o alívio de uma dor (**Necessidade**), a busca por coerência (**Valor**), a conquista de algo (**Desejo**) ou o impacto no mundo (**Propósito**)?,
14. **Conflito Raiz (M1):** Se você pudesse transpor um **único conflito** central hoje para alcançar sua meta extraordinária, qual seria esse obstáculo?,
15. **Visão de Clímax (MX/M2X):** Descreva sua versão extraordinária daqui a 12 meses. O que essa pessoa faz no dia a dia que você, na sua versão atual, ainda não consegue realizar?,

### Lógica da Intervenção para a IA
Após essas respostas, a inteligência contextual deve analisar as **incongruências simbólicas** reveladas. Por exemplo, se o usuário pontua alto em "Vida Profissional", mas revela "frases automáticas" de falha na "Saúde Mental", a IA deve gerar perguntas que cruzem esses eixos para identificar a **Barreira** oculta. O objetivo é mapear o **Gap MX** — a distância entre a narrativa vivida e a narrativa escolhida.

CAPÍTULO 6

KNOWLEDGE_BASE:

```python
"""
KNOWLEDGE_BASE - Nara (Engenharia de Mindset)
Baseada na Metodologia de Transformação Narrativa de Phellipe Oliveira.
Organizada pelas 12 Áreas Estruturantes Específicas do Círculo Narrativo.
"""

KNOWLEDGE_BASE = [
    # ==========================================
    # 1. SAÚDE FÍSICA
    # ==========================================
    {
        "chapter": "Saúde Física",
        "section": "Fundamentos Narrativos",
        "content": """
A Saúde Física refere-se à manutenção da constituição física e disposição corporal necessária para executar as tarefas da jornada. Na metodologia, o corpo é o principal canal das mensagens e o codificador singular da nova identidade.
Componentes de Domínio (M2):
- Vitalidade e vigor para transpor obstáculos.
- Sincronia entre disposição física e metas (MX).
- Gestão de energia como recurso para a 'Força-Tarefa'.
Sinais de Conflito (M1 - Memórias Vermelhas):
- Exaustão crônica impedindo a ação (Volição).
- Falta de domínio sobre hábitos biológicos básicos.
- Incongruência entre a imagem física e a identidade pretendida.
"""
    },
    {
        "chapter": "Saúde Física",
        "section": "Diagnóstico M1 e Projeção MX",
        "content": """
Perguntas para localizar o Ponto de Entrada:
- De 0 a 5, quanto seu corpo suporta a velocidade da sua visão de futuro?
- Sua rotina física atual é uma âncora de progresso ou uma barreira de inércia?
- Se seu corpo fosse um personagem, ele seria o protagonista ou um figurante cansado?
Conexão com Motores:
- Necessidade: Busca por alívio de dores ou limitações.
- Desejo: Busca por performance e vitalidade extraordinária.
"""
    },

    # ==========================================
    # 2. SAÚDE MENTAL
    # ==========================================
    {
        "chapter": "Saúde Mental",
        "section": "Fundamentos Narrativos",
        "content": """
Foca no equilíbrio das funções cognitivas e na gestão das emoções para evitar sabotagens internas. É o campo onde se aplica a TCC (Terapia Cognitivo-Comportamental) para reestruturar a 'velha narrativa'.
Técnicas de Domínio (M2):
- Identificação de Pensamentos Automáticos e Distorções Cognitivas.
- Reestruturação Cognitiva: trocar a 'vítima' pelo 'autor'.
- Descatastrofização de cenários de medo.
Sinais de Conflito (M1 - Memórias Vermelhas):
- Narrativa interna caótica ou contraditória.
- Bloqueios narrativos por capítulos ocultos ou vergonha do passado.
- Ansiedade por falta de linearidade entre passado e futuro.
"""
    },

    # ==========================================
    # 3. VIDA PROFISSIONAL
    # ==========================================
    {
        "chapter": "Vida Profissional",
        "section": "Fundamentos Narrativos",
        "content": """
Foca na atuação produtiva, no domínio de competências técnicas e no desenvolvimento da carreira e autoridade (Capital Simbólico). O objetivo é alcançar o Nível de Posição defendido e reconhecido.
Componentes de Domínio (M2):
- Maestria técnica e autoridade percebida.
- Alinhamento entre a tarefa diária (Missão) e o legado (Propósito).
- Comunicação clara do diferencial competitivo.
Sinais de Conflito (M1 - Memórias Vermelhas):
- Sentimento de estar atuando um papel que não condiz com quem se é.
- Invisibilidade em espaços de poder e decisão.
- Procrastinação por falta de clareza sobre o próximo 'clímax' profissional.
"""
    },

    # ==========================================
    # 4. FINANÇAS
    # ==========================================
    {
        "chapter": "Finanças",
        "section": "Fundamentos Narrativos",
        "content": """
Envolve a gestão do capital econômico e recursos materiais necessários para sustentar a estrutura de vida e o Círculo Narrativo. O dinheiro é visto como um recurso para a liberdade de ser, fazer e saber.
Componentes de Domínio (M2):
- Gestão de capital alinhada aos valores assumidos.
- Capacidade de investimento na própria transformação e ambiente.
- Estabilidade financeira para suportar a 'travessia'.
Sinais de Conflito (M1 - Memórias Vermelhas):
- Ansiedade por desorganização material.
- Crenças limitantes de escassez herdadas da família.
- Falta de recursos para materializar a visão (MX).
"""
    },

    # ==========================================
    # 5. VIDA FAMILIAR
    # ==========================================
    {
        "chapter": "Vida Familiar",
        "section": "Fundamentos Narrativos",
        "content": """
Trata dos vínculos de parentesco e dos valores morais inicialmente absorvidos. É onde muitas vezes se encontram as 'Identidades Herdadas' que precisam ser ressignificadas.
Componentes de Domínio (M2):
- Limites saudáveis entre o 'eu decidido' e as expectativas parentais.
- Ritos e rituais familiares que nutrem a identidade.
- Presença e cuidado sem perda da autonomia narrativa.
Sinais de Conflito (M1 - Memórias Vermelhas):
- Conflitos de valores inegociáveis com membros do grupo íntimo.
- Vergonha da origem ou de capítulos não resolvidos.
- Atuar papéis impostos por tradições obsoletas.
"""
    },

    # ==========================================
    # 6. VIDA SOCIAL
    # ==========================================
    {
        "chapter": "Vida Social",
        "section": "Fundamentos Narrativos",
        "content": """
Refere-se às interações com a comunidade e à seleção de redes de contato (Recurso Social). O crescimento ocorre ao orbitar ambientes nutritivos e pessoas 'condutoras'.
Componentes de Domínio (M2):
- Capital Social: rede de relações que potencializa o indivíduo.
- Habilidade de Relating: descobrir as histórias e motivações do outro.
- Influência Social: falar sobre o que interessa e motiva o público.
Sinais de Conflito (M1 - Memórias Vermelhas):
- Ambientes estagnados que puxam para a 'antiga versão'.
- Solidão existencial mesmo rodeado de pessoas.
- Medo do julgamento ou de brilhar em público.
"""
    },

    # ==========================================
    # 7. VIDA PESSOAL
    # ==========================================
    {
        "chapter": "Vida Pessoal",
        "section": "Fundamentos Narrativos",
        "content": """
Concentra-se no autoconhecimento, na descoberta da própria essência e na organização dos interesses individuais. É o centro da 'Luz Total' da personagem.
Componentes de Domínio (M2):
- Identidade clara: saber 'quem sou' além dos rótulos.
- Autonomia: escrever o próprio enredo sem esperar permissão.
- Congruência entre o mundo interno e a autoimagem.
Sinais de Conflito (M1 - Memórias Vermelhas):
- Sensação de estar perdido em meio a narrativas alheias.
- Falta de enredo que conecte os momentos da vida.
- Vazio por falta de uma 'Fantasia Pessoal' estimulante.
"""
    },

    # ==========================================
    # 8. LAZER
    # ==========================================
    {
        "chapter": "Lazer",
        "section": "Fundamentos Narrativos",
        "content": """
Compreende as atividades de entretenimento e o uso do tempo livre para recuperação de energia e prazer. Serve como ritual de descompressão necessário para manter a constância.
Componentes de Domínio (M2):
- Rituais de sensibilidade e propósito que recarregam a volição.
- Hobbies que expressam a criatividade sem pressão de resultado.
- Equilíbrio entre esforço e descanso.
Sinais de Conflito (M1 - Memórias Vermelhas):
- Culpa por descansar ou automatização da vida.
- Lazer viciado que drena em vez de nutrir.
- Ausência de pausas para celebrar microvitórias.
"""
    },

    # ==========================================
    # 9. EDUCAÇÃO
    # ==========================================
    {
        "chapter": "Educação",
        "section": "Fundamentos Narrativos",
        "content": """
Diz respeito à busca contínua por conhecimento, aprendizagem sistemática e aperfeiçoamento intelectual. É o processo de 'Modelagem' ativa de novos padrões de sucesso.
Componentes de Domínio (M2):
- Aprendizagem de processos (M3) para acelerar a própria jornada.
- Domínio de novos códigos linguísticos e mentais.
- Mentalidade de crescimento (Growth Mindset).
Sinais de Conflito (M1 - Memórias Vermelhas):
- Estagnação intelectual e apego a crenças obsoletas.
- Excesso de preparação sem ir para a ação (Paralisia).
- Dificuldade em transformar informação em habilidade prática.
"""
    },

    # ==========================================
    # 10. VIDA ESPIRITUAL
    # ==========================================
    {
        "chapter": "Vida Espiritual",
        "section": "Fundamentos Narrativos",
        "content": """
Relaciona-se à força da fé e à convicção interior que impulsionam a manifestação dos propósitos da alma. É a âncora que dá sentido à travessia.
Componentes de Domínio (M2):
- Convicção plena na visão de futuro (MX).
- Alinhamento existencial: saber 'por que tudo isso importa'.
- Paz interior baseada na integridade (falar, sentir e agir em harmonia).
Sinais de Conflito (M1 - Memórias Vermelhas):
- Vazio existencial ou falta de direção transcendental.
- Crise de indignidade perante a própria grandeza.
- Desconexão com os valores inegociáveis da alma.
"""
    },

    # ==========================================
    # 11. INOVAÇÃO
    # ==========================================
    {
        "chapter": "Inovação",
        "section": "Fundamentos Narrativos",
        "content": """
Capacidade de criar, pesquisar e desenvolver novas formas de resolver problemas ou expressar a identidade. É a ousadia de testar limites criativos.
Componentes de Domínio (M2):
- Prototipagem de novos caminhos e ideias (M2X).
- Flexibilidade e adaptabilidade diante de perdas ou rupturas.
- Curiosidade genuína por experiências históricas e subjetivas.
Sinais de Conflito (M1 - Memórias Vermelhas):
- Medo de recomeçar ou de construir uma nova identidade.
- Bloqueio criativo por excesso de autocrítica.
- Repetição de ciclos exaustivos sem renovação.
"""
    },

    # ==========================================
    # 12. VIDA AMOROSA
    # ==========================================
    {
        "chapter": "Vida Amorosa",
        "section": "Fundamentos Narrativos",
        "content": """
Abrange os relacionamentos íntimos e o convívio afetuoso. Na metodologia, busca-se parcerias que nutram a construção do Círculo Narrativo Futuro (CN+).
Componentes de Domínio (M2):
- Identidade preservada dentro da união.
- Atmosfera emocional de apoio mútuo e incentivo ao florescimento.
- Comunicação assertiva de necessidades e limites.
Sinais de Conflito (M1 - Memórias Vermelhas):
- Vínculos superficiais que não despertam a autenticidade.
- Incongruência entre os valores do parceiro e a própria trajetória.
- Medo de se perder ao crescer, gerando autossabotagem afetiva.
"""
    }
]
```

----

Esta síntese foi estruturada para servir como uma base de conhecimento (Knowledge Base) robusta para sistemas de RAG, organizando a **Metodologia de Transformação Narrativa** em camadas lógicas, clusters de diagnóstico e protocolos de intervenção.

---

# Síntese Metodológica: Engenharia de Mindset e Mapa das Crises

A essência desta metodologia reside na compreensão de que toda crise é um sintoma da **distância entre a narrativa vivida e a narrativa escolhida**, manifestada como um **Gap MX** (expectativa vs. resultado). A transformação ocorre através do alinhamento entre **Narrativa** (crenças), **Identidade** (valores) e **Hábitos** (princípios/rituais).

### 1. A Estrutura do Fluxo Narrativo
O desenvolvimento do indivíduo segue uma hierarquia de quatro camadas fundamentais:
*   **Identidade (Quem sou):** A base de tudo. Fortalecê-la reduz o ruído em todas as outras camadas. A falta de identidade gera vergonha e confusão.
*   **Sentido (Para onde vou):** Organiza o tempo, integrando passado, presente e futuro. A falta de sentido gera vazio e estagnação.
*   **Ação Significativa (Como faço):** Exige estrutura, ritos e limites para sustentar a coerência. A falta de ação gera procrastinação e dispersão.
*   **Conexão Assertiva (Com quem):** Surge quando as camadas anteriores estão alinhadas, reduzindo o medo do julgamento. A falta de conexão gera solidão e vínculos superficiais.

### 2. Clusters Operacionais de Crise (Diagnóstico M1)
As crises são agrupadas em seis arquétipos principais que permitem identificar o "ponto de entrada" para a intervenção:

1.  **Identidade Raiz:** Falha na autoimagem e valores não assumidos. Sinais incluem "identidade herdada", viver papéis impostos e vergonha da própria história.
2.  **Sentido e Direção:** Ruptura na coerência temporal. Sinais incluem futuro opaco, sensação de tempo perdido e falta de um enredo unificador.
3.  **Execução e Estrutura:** Ausência de ritos e hábitos. Manifesta-se através de procrastinação, paralisia decisória e falta de limites.
4.  **Conexão e Expressão:** Dificuldade em comunicar a própria substância. Sinais incluem medo do julgamento, invisibilidade simbólica e desconforto com o sucesso.
5.  **Incongruência Identidade-Cultura:** Choque entre quem a pessoa escolheu ser e o ambiente/sistema em que vive.
6.  **Transformação de Personagem:** Dificuldade em encerrar capítulos antigos e "batizar" a nova fase. Sinais incluem apego a papéis obsoletos e medo de crescer.

### 3. O Mecanismo de Intervenção: Assunção Intencional
Para transpor o estado de crise (M1) rumo à meta (MX), utiliza-se o ciclo de consolidação em quatro etapas, vinculado às fases da jornada e aos domínios temáticos:

| Fase da Jornada | Domínio Temático (Alavanca) | Etapa da Assunção | Foco da Ação |
| :--- | :--- | :--- | :--- |
| **Germinar** | D1: Motivações e Conflitos | **Reconhecer** | Nomear o motor (Necessidade/Valor/Desejo/Propósito). |
| **Enraizar** | D2: Crenças, Valores e Princípios | **Modelar** | Definir o "quem escolho ser" e novas referências. |
| **Desenvolver** | D3: Evolução e Desenvolvimento | **Assumir** | Implementar ritos, limites e microentregas diárias. |
| **Florescer** | D4: Congruência Identidade-Cultura | **Reforçar** | Validar a nova voz e expressão pública. |
| **Frutificar** | D5: Transformação de Identidade | **Reforçar** | Consolidar os novos resultados e papéis. |
| **Realizar** | D6: Papel na Sociedade | **Reforçar** | Estabelecer legado e rede de apoio. |

### 4. Protocolo de Diagnóstico Rápido
Para perfilar um caso, deve-se avaliar seis fatores em uma escala de 0 a 10:
1.  **Autenticidade:** A narrativa é própria ou colonizada?
2.  **Integração do Passado:** Existe vergonha ou o passado é capital simbólico?
3.  **Visão/Enredo:** O futuro tem uma imagem clara?
4.  **Coragem/Decisão:** Existe um "ato mínimo" semanal de protagonismo?
5.  **Expressão/Voz:** A comunicação é clara e cadenciada?
6.  **Estrutura/Pertencimento:** Existem ritos, limites e testemunhas significativas?

### 5. Dinâmica Temporal e Solução Coringa
*   **O Tempo nas Crises:** O passado deve ser ressignificado na **Narrativa**; o presente deve ser estabilizado pela **Identidade**; e o futuro deve ser materializado pelos **Hábitos**.
*   **Alinhamento do Eixo:** A solução definitiva é a remoção da incongruência simbólica. Quando a história contada, o valor assumido e o hábito diário dizem a mesma coisa, o sistema torna-se antifrágil: as barreiras tornam-se "pontos de prova" que validam a nova identidade.