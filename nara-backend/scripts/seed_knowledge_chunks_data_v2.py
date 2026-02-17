"""
Knowledge chunks V2 baseados no documento 01_BASE_METODOLOGICA_NARA.md
Com metadados enriquecidos conforme a metodologia refinada.
"""

CHUNKS_V2 = [
    # =============================================================================
    # PARTE I: FUNDAMENTOS CONCEITUAIS
    # =============================================================================
    
    # 1. SAÚDE FÍSICA
    {
        "chapter": "Saúde Física",
        "section": "Fundamentos Narrativos",
        "content": """A Saúde Física refere-se à manutenção da constituição física e disposição corporal necessária para executar as tarefas da jornada. Na metodologia, o corpo é o principal canal das mensagens e o codificador singular da nova identidade.

Componentes de Domínio (M2):
- Vitalidade e vigor para transpor obstáculos
- Sincronia entre disposição física e metas (MX)
- Gestão de energia como recurso para a 'Força-Tarefa'

Sinais de Conflito (M1):
- Exaustão crônica impedindo a ação (Volição)
- Falta de domínio sobre hábitos biológicos básicos
- Incongruência entre a imagem física e a identidade pretendida

Padrões de Autossabotagem:
- "Não tenho tempo para cuidar de mim"
- "Quando as coisas acalmarem, vou começar"
- "Meu corpo sempre foi assim"
- Cuidar dos outros em detrimento de si""",
        "motor_motivacional": ["Necessidade", "Desejo"],
        "estagio_jornada": ["Germinar", "Enraizar"],
        "tipo_crise": ["Execução", "Identidade"],
        "subtipo_crise": "Falta de domínio sobre hábitos biológicos",
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Conceito",
        "dominio": ["D1", "D3"],
        "sintomas_comportamentais": [
            "exaustão crônica",
            "sedentarismo",
            "alimentação desordenada",
            "insônia",
            "fadiga",
        ],
        "tom_emocional": "urgência",
        "nivel_maturidade": "baixo",
    },
    
    # 2. SAÚDE MENTAL
    {
        "chapter": "Saúde Mental",
        "section": "Fundamentos Narrativos",
        "content": """Foca no equilíbrio das funções cognitivas e na gestão das emoções para evitar sabotagens internas. É o campo onde se aplica a TCC (Terapia Cognitivo-Comportamental) para reestruturar a 'velha narrativa'.

Técnicas de Domínio (M2):
- Identificação de Pensamentos Automáticos e Distorções Cognitivas
- Reestruturação Cognitiva: trocar a 'vítima' pelo 'autor'
- Descatastrofização de cenários de medo

Sinais de Conflito (M1):
- Narrativa interna caótica ou contraditória
- Bloqueios narrativos por capítulos ocultos ou vergonha do passado
- Ansiedade por falta de linearidade entre passado e futuro

Padrões de Autossabotagem:
- "Sou forte, não preciso de ajuda"
- "É frescura, todo mundo tem problemas"
- Intelectualizar emoções sem senti-las
- Manter-se ocupado para não sentir""",
        "motor_motivacional": ["Necessidade", "Valor"],
        "estagio_jornada": ["Germinar", "Enraizar", "Desenvolver"],
        "tipo_crise": ["Identidade", "Sentido"],
        "subtipo_crise": "Narrativa interna caótica",
        "ponto_entrada": "Emocional",
        "tipo_conteudo": "Conceito",
        "dominio": ["D1", "D2"],
        "sintomas_comportamentais": [
            "ansiedade persistente",
            "pensamentos ruminativos",
            "autocrítica destrutiva",
            "dificuldade de concentração",
        ],
        "tom_emocional": "vergonha",
        "nivel_maturidade": "baixo",
    },
    
    # 3. SAÚDE ESPIRITUAL
    {
        "chapter": "Saúde Espiritual",
        "section": "Fundamentos Narrativos",
        "content": """Relaciona-se à força da fé e à convicção interior que impulsionam a manifestação dos propósitos da alma. É a âncora que dá sentido à travessia.

Componentes de Domínio (M2):
- Convicção plena na visão de futuro (MX)
- Alinhamento existencial: saber 'por que tudo isso importa'
- Paz interior baseada na integridade (falar, sentir e agir em harmonia)

Sinais de Conflito (M1):
- Vazio existencial ou falta de direção transcendental
- Crise de indignidade perante a própria grandeza
- Desconexão com os valores inegociáveis da alma""",
        "motor_motivacional": ["Valor", "Propósito"],
        "estagio_jornada": ["Enraizar", "Florescer", "Realizar"],
        "tipo_crise": ["Sentido", "Identidade"],
        "subtipo_crise": "Vazio existencial",
        "ponto_entrada": "Existencial",
        "tipo_conteudo": "Conceito",
        "dominio": ["D2", "D6"],
        "sintomas_comportamentais": [
            "vazio existencial",
            "falta de direção",
            "desconexão com valores",
        ],
        "tom_emocional": "apatia",
        "nivel_maturidade": "médio",
    },
    
    # 4. VIDA PESSOAL
    {
        "chapter": "Vida Pessoal",
        "section": "Fundamentos Narrativos",
        "content": """Concentra-se no autoconhecimento, na descoberta da própria essência e na organização dos interesses individuais. É o centro da 'Luz Total' da personagem.

Componentes de Domínio (M2):
- Identidade clara: saber 'quem sou' além dos rótulos
- Autonomia: escrever o próprio enredo sem esperar permissão
- Congruência entre o mundo interno e a autoimagem

Sinais de Conflito (M1):
- Sensação de estar perdido em meio a narrativas alheias
- Falta de enredo que conecte os momentos da vida
- Vazio por falta de uma 'Fantasia Pessoal' estimulante""",
        "motor_motivacional": ["Valor", "Desejo"],
        "estagio_jornada": ["Germinar", "Enraizar", "Desenvolver"],
        "tipo_crise": ["Identidade", "Sentido"],
        "subtipo_crise": "Identidade Herdada",
        "ponto_entrada": "Simbólico",
        "tipo_conteudo": "Conceito",
        "dominio": ["D1", "D2"],
        "sintomas_comportamentais": [
            "sensação de perda",
            "falta de direção",
            "autossabotagem",
        ],
        "tom_emocional": "confusão",
        "nivel_maturidade": "baixo",
    },
    
    # 5. VIDA AMOROSA
    {
        "chapter": "Vida Amorosa",
        "section": "Fundamentos Narrativos",
        "content": """Abrange os relacionamentos íntimos e o convívio afetuoso. Na metodologia, busca-se parcerias que nutram a construção do Círculo Narrativo Futuro (CN+).

Componentes de Domínio (M2):
- Identidade preservada dentro da união
- Atmosfera emocional de apoio mútuo e incentivo ao florescimento
- Comunicação assertiva de necessidades e limites

Sinais de Conflito (M1):
- Vínculos superficiais que não despertam a autenticidade
- Incongruência entre os valores do parceiro e a própria trajetória
- Medo de se perder ao crescer, gerando autossabotagem afetiva""",
        "motor_motivacional": ["Valor", "Necessidade"],
        "estagio_jornada": ["Enraizar", "Desenvolver", "Florescer"],
        "tipo_crise": ["Conexão", "Identidade"],
        "subtipo_crise": "Vínculos superficiais",
        "ponto_entrada": "Emocional",
        "tipo_conteudo": "Conceito",
        "dominio": ["D4"],
        "sintomas_comportamentais": [
            "vínculos superficiais",
            "medo de crescer",
            "autossabotagem afetiva",
        ],
        "tom_emocional": "tristeza",
        "nivel_maturidade": "médio",
    },
    
    # 6. VIDA FAMILIAR
    {
        "chapter": "Vida Familiar",
        "section": "Fundamentos Narrativos",
        "content": """Trata dos vínculos de parentesco e dos valores morais inicialmente absorvidos. É onde muitas vezes se encontram as 'Identidades Herdadas' que precisam ser ressignificadas.

Componentes de Domínio (M2):
- Limites saudáveis entre o 'eu decidido' e as expectativas parentais
- Ritos e rituais familiares que nutrem a identidade
- Presença e cuidado sem perda da autonomia narrativa

Sinais de Conflito (M1):
- Conflitos de valores inegociáveis com membros do grupo íntimo
- Vergonha da origem ou de capítulos não resolvidos
- Atuar papéis impostos por tradições obsoletas""",
        "motor_motivacional": ["Valor", "Necessidade"],
        "estagio_jornada": ["Germinar", "Enraizar"],
        "tipo_crise": ["Identidade", "Incongruência"],
        "subtipo_crise": "Identidades Herdadas",
        "ponto_entrada": "Simbólico",
        "tipo_conteudo": "Conceito",
        "dominio": ["D1", "D2"],
        "sintomas_comportamentais": [
            "conflitos de valores",
            "vergonha da origem",
            "atuação de papéis impostos",
        ],
        "tom_emocional": "vergonha",
        "nivel_maturidade": "baixo",
    },
    
    # 7. VIDA SOCIAL
    {
        "chapter": "Vida Social",
        "section": "Fundamentos Narrativos",
        "content": """Refere-se às interações com a comunidade e à seleção de redes de contato (Recurso Social). O crescimento ocorre ao orbitar ambientes nutritivos e pessoas 'condutoras'.

Componentes de Domínio (M2):
- Capital Social: rede de relações que potencializa o indivíduo
- Habilidade de Relating: descobrir as histórias e motivações do outro
- Influência Social: falar sobre o que interessa e motiva o público

Sinais de Conflito (M1):
- Ambientes estagnados que puxam para a 'antiga versão'
- Solidão existencial mesmo rodeado de pessoas
- Medo do julgamento ou de brilhar em público""",
        "motor_motivacional": ["Desejo", "Propósito"],
        "estagio_jornada": ["Desenvolver", "Florescer", "Frutificar"],
        "tipo_crise": ["Conexão", "Incongruência"],
        "subtipo_crise": "Invisibilidade Simbólica",
        "ponto_entrada": "Emocional",
        "tipo_conteudo": "Conceito",
        "dominio": ["D4", "D5"],
        "sintomas_comportamentais": [
            "solidão existencial",
            "medo de julgamento",
            "autossabotagem social",
        ],
        "tom_emocional": "indignação",
        "nivel_maturidade": "médio",
    },
    
    # 8. VIDA PROFISSIONAL
    {
        "chapter": "Vida Profissional",
        "section": "Fundamentos Narrativos",
        "content": """Foca na atuação produtiva, no domínio de competências técnicas e no desenvolvimento da carreira e autoridade (Capital Simbólico). O objetivo é alcançar o Nível de Posição defendido e reconhecido.

Componentes de Domínio (M2):
- Maestria técnica e autoridade percebida
- Alinhamento entre a tarefa diária (Missão) e o legado (Propósito)
- Comunicação clara do diferencial competitivo

Sinais de Conflito (M1):
- Sentimento de estar atuando um papel que não condiz com quem se é
- Invisibilidade em espaços de poder e decisão
- Procrastinação por falta de clareza sobre o próximo 'clímax' profissional

Padrões de Autossabotagem:
- "Trabalho é trabalho, não precisa ter significado"
- "Não tenho escolha, preciso do dinheiro"
- Síndrome do impostor: "Vão descobrir que não sou tão bom"
- Workaholism como fuga de outras áreas""",
        "motor_motivacional": ["Desejo", "Propósito"],
        "estagio_jornada": ["Desenvolver", "Florescer", "Frutificar", "Realizar"],
        "tipo_crise": ["Identidade", "Sentido", "Conexão"],
        "subtipo_crise": "Invisibilidade Simbólica",
        "ponto_entrada": "Simbólico",
        "tipo_conteudo": "Conceito",
        "dominio": ["D3", "D4", "D5", "D6"],
        "sintomas_comportamentais": [
            "síndrome do impostor",
            "procrastinação",
            "invisibilidade",
            "workaholism",
        ],
        "tom_emocional": "indignação",
        "nivel_maturidade": "médio",
    },
    
    # 9. FINANÇAS
    {
        "chapter": "Finanças",
        "section": "Fundamentos Narrativos",
        "content": """Envolve a gestão do capital econômico e recursos materiais necessários para sustentar a estrutura de vida e o Círculo Narrativo. O dinheiro é visto como um recurso para a liberdade de ser, fazer e saber.

Componentes de Domínio (M2):
- Gestão de capital alinhada aos valores assumidos
- Capacidade de investimento na própria transformação e ambiente
- Estabilidade financeira para suportar a 'travessia'

Sinais de Conflito (M1):
- Ansiedade por desorganização material
- Crenças limitantes de escassez herdadas da família
- Falta de recursos para materializar a visão (MX)""",
        "motor_motivacional": ["Necessidade", "Desejo"],
        "estagio_jornada": ["Enraizar", "Desenvolver"],
        "tipo_crise": ["Execução", "Identidade"],
        "subtipo_crise": "Crenças limitantes de escassez",
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Conceito",
        "dominio": ["D3"],
        "sintomas_comportamentais": [
            "ansiedade financeira",
            "desorganização",
            "crenças de escassez",
        ],
        "tom_emocional": "urgência",
        "nivel_maturidade": "baixo",
    },
    
    # 10. EDUCAÇÃO
    {
        "chapter": "Educação",
        "section": "Fundamentos Narrativos",
        "content": """Diz respeito à busca contínua por conhecimento, aprendizagem sistemática e aperfeiçoamento intelectual. É o processo de 'Modelagem' ativa de novos padrões de sucesso.

Componentes de Domínio (M2):
- Aprendizagem de processos (M3) para acelerar a própria jornada
- Domínio de novos códigos linguísticos e mentais
- Mentalidade de crescimento (Growth Mindset)

Sinais de Conflito (M1):
- Estagnação intelectual e apego a crenças obsoletas
- Excesso de preparação sem ir para a ação (Paralisia)
- Dificuldade em transformar informação em habilidade prática""",
        "motor_motivacional": ["Desejo", "Valor"],
        "estagio_jornada": ["Enraizar", "Desenvolver", "Florescer"],
        "tipo_crise": ["Execução", "Transformação"],
        "subtipo_crise": "Paralisia decisória",
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Conceito",
        "dominio": ["D2", "D3"],
        "sintomas_comportamentais": [
            "estagnação intelectual",
            "paralisia por excesso de preparação",
            "dificuldade prática",
        ],
        "tom_emocional": "apatia",
        "nivel_maturidade": "médio",
    },
    
    # 11. INOVAÇÃO
    {
        "chapter": "Inovação",
        "section": "Fundamentos Narrativos",
        "content": """Capacidade de criar, pesquisar e desenvolver novas formas de resolver problemas ou expressar a identidade. É a ousadia de testar limites criativos.

Componentes de Domínio (M2):
- Prototipagem de novos caminhos e ideias (M2X)
- Flexibilidade e adaptabilidade diante de perdas ou rupturas
- Curiosidade genuína por experiências históricas e subjetivas

Sinais de Conflito (M1):
- Medo de recomeçar ou de construir uma nova identidade
- Bloqueio criativo por excesso de autocrítica
- Repetição de ciclos exaustivos sem renovação""",
        "motor_motivacional": ["Desejo", "Propósito"],
        "estagio_jornada": ["Desenvolver", "Florescer", "Frutificar"],
        "tipo_crise": ["Transformação", "Identidade"],
        "subtipo_crise": "Medo de recomeçar",
        "ponto_entrada": "Simbólico",
        "tipo_conteudo": "Conceito",
        "dominio": ["D3", "D5"],
        "sintomas_comportamentais": [
            "bloqueio criativo",
            "medo de recomeçar",
            "repetição de ciclos",
        ],
        "tom_emocional": "apatia",
        "nivel_maturidade": "médio",
    },
    
    # 12. LAZER
    {
        "chapter": "Lazer",
        "section": "Fundamentos Narrativos",
        "content": """Compreende as atividades de entretenimento e o uso do tempo livre para recuperação de energia e prazer. Serve como ritual de descompressão necessário para manter a constância.

Componentes de Domínio (M2):
- Rituais de sensibilidade e propósito que recarregam a volição
- Hobbies que expressam a criatividade sem pressão de resultado
- Equilíbrio entre esforço e descanso

Sinais de Conflito (M1):
- Culpa por descansar ou automatização da vida
- Lazer viciado que drena em vez de nutrir
- Ausência de pausas para celebrar microvitórias""",
        "motor_motivacional": ["Necessidade"],
        "estagio_jornada": ["Enraizar", "Desenvolver"],
        "tipo_crise": ["Execução"],
        "subtipo_crise": "Culpa por descansar",
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Conceito",
        "dominio": ["D3"],
        "sintomas_comportamentais": [
            "culpa por descansar",
            "automatização da vida",
            "lazer que drena",
        ],
        "tom_emocional": "urgência",
        "nivel_maturidade": "baixo",
    },
    
    # =============================================================================
    # PARTE II: TÉCNICAS DE TCC
    # =============================================================================
    
    {
        "chapter": "Ferramental TCC",
        "section": "Questionamento Socrático",
        "content": """Técnica para desafiar a lógica dos pensamentos automáticos sem confronto direto.

Tipos de Perguntas:
- Evidência: "O que faz você acreditar que nunca será capaz?"
- Alternativa: "Existe outra forma de interpretar essa situação?"
- Consequência: "Se isso for verdade, qual seria o pior resultado realista?"
- Utilidade: "Esse pensamento te ajuda ou te paralisa?"

Objetivo: Revelar crenças irracionais e promover reestruturação cognitiva.""",
        "motor_motivacional": ["Valor", "Necessidade"],
        "estagio_jornada": ["Germinar", "Enraizar"],
        "tipo_crise": ["Identidade", "Saúde Mental"],
        "subtipo_crise": "Pensamentos automáticos negativos",
        "ponto_entrada": "Emocional",
        "tipo_conteudo": "Técnica de TCC",
        "dominio": ["D1", "D2"],
        "sintomas_comportamentais": [
            "pensamentos automáticos",
            "autocrítica",
            "distorções cognitivas",
        ],
        "tom_emocional": "vergonha",
        "nivel_maturidade": "baixo",
    },
    
    {
        "chapter": "Ferramental TCC",
        "section": "Flecha Descendente",
        "content": """Técnica para chegar à crença central oculta que sustenta os pensamentos de superfície.

Método: Perguntar repetidamente "Se isso for verdade, o que diz sobre quem você é?" até revelar a crença raiz.

Exemplo:
Usuário: "Não consigo apresentar minhas ideias"
IA: "Se isso for verdade, o que significa?"
Usuário: "Significa que sou incompetente"
IA: "E se você fosse incompetente, o que isso diria sobre você?"
Usuário: "Que não mereço estar onde estou"
→ CRENÇA CENTRAL REVELADA: Indignidade / Síndrome do Impostor""",
        "motor_motivacional": ["Valor"],
        "estagio_jornada": ["Germinar", "Enraizar"],
        "tipo_crise": ["Identidade"],
        "subtipo_crise": "Síndrome do Impostor",
        "ponto_entrada": "Simbólico",
        "tipo_conteudo": "Técnica de TCC",
        "dominio": ["D1"],
        "sintomas_comportamentais": [
            "síndrome do impostor",
            "autocrítica",
            "indignidade",
        ],
        "tom_emocional": "vergonha",
        "nivel_maturidade": "baixo",
    },
    
    {
        "chapter": "Ferramental TCC",
        "section": "Descatastrofização",
        "content": """Técnica para confrontar o "pior cenário" com realismo e reduzir o exagero narrativo.

Perguntas:
- "Qual é o pior que pode acontecer?" → Explicitar o medo
- "E se isso acontecesse, o que você faria?" → Revelar recursos
- "Qual a probabilidade real de isso acontecer?" → Introduzir realismo
- "O que é mais provável que aconteça?" → Reequilibrar a narrativa

Objetivo: Reduzir ansiedade antecipatória e catastrofização.""",
        "motor_motivacional": ["Necessidade"],
        "estagio_jornada": ["Germinar"],
        "tipo_crise": ["Saúde Mental", "Execução"],
        "subtipo_crise": "Catastrofização",
        "ponto_entrada": "Emocional",
        "tipo_conteudo": "Técnica de TCC",
        "dominio": ["D1"],
        "sintomas_comportamentais": [
            "ansiedade antecipatória",
            "catastrofização",
            "paralisia por medo",
        ],
        "tom_emocional": "urgência",
        "nivel_maturidade": "baixo",
    },
    
    {
        "chapter": "Ferramental TCC",
        "section": "Reestruturação Cognitiva",
        "content": """Técnica para substituir a narrativa de "vítima" pela de "autor".

Identificar distorção → Propor reformulação:

- Catastrofização: "Se falhar, tudo está perdido" → "Se falhar, terei aprendido algo novo"
- Leitura mental: "Eles pensam que sou incapaz" → "Não sei o que pensam; vou perguntar"
- Generalização: "Sempre dou errado" → "Dessa vez não funcionou"
- Personalização: "A culpa é toda minha" → "Existem vários fatores envolvidos"

Objetivo: Trocar narrativa limitante por narrativa potencializadora.""",
        "motor_motivacional": ["Valor"],
        "estagio_jornada": ["Enraizar", "Desenvolver"],
        "tipo_crise": ["Identidade", "Saúde Mental"],
        "subtipo_crise": "Distorções cognitivas",
        "ponto_entrada": "Simbólico",
        "tipo_conteudo": "Técnica de TCC",
        "dominio": ["D2"],
        "sintomas_comportamentais": [
            "distorções cognitivas",
            "narrativa de vítima",
            "pensamentos limitantes",
        ],
        "tom_emocional": "indignação",
        "nivel_maturidade": "médio",
    },
    
    # =============================================================================
    # PARTE III: ÂNCORAS PRÁTICAS (Seleção de 10 âncoras mais importantes)
    # =============================================================================
    
    {
        "chapter": "Âncoras Práticas",
        "section": "Referências",
        "content": """Âncora de Ambiente e Contexto: O que você consome (livros, vídeos, podcasts).

Intervenção: "Substitua 1 hora de conteúdo aleatório por referências que alimentem sua visão MX"

Objetivo: Nutrir a mente com exemplos alinhados à nova identidade aspirada.""",
        "motor_motivacional": ["Desejo", "Propósito"],
        "estagio_jornada": ["Enraizar", "Desenvolver"],
        "tipo_crise": ["Sentido", "Transformação"],
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Âncora Prática",
        "dominio": ["D2", "D3"],
        "sintomas_comportamentais": ["estagnação", "falta de inspiração"],
        "tom_emocional": "apatia",
        "nivel_maturidade": "médio",
    },
    
    {
        "chapter": "Âncoras Práticas",
        "section": "Grupo",
        "content": """Âncora de Ambiente e Contexto: Quem orbita (relações próximas).

Intervenção: "Passe mais tempo com 1 pessoa que já vive o que você aspira"

Objetivo: Criar campo gravitacional nutritivo que acelere a transformação.""",
        "motor_motivacional": ["Desejo", "Propósito"],
        "estagio_jornada": ["Desenvolver", "Florescer"],
        "tipo_crise": ["Conexão", "Incongruência"],
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Âncora Prática",
        "dominio": ["D4"],
        "sintomas_comportamentais": ["solidão existencial", "ambiente estagnado"],
        "tom_emocional": "indignação",
        "nivel_maturidade": "médio",
    },
    
    {
        "chapter": "Âncoras Práticas",
        "section": "Tom",
        "content": """Âncora de Comunicação e Expressão: Como você fala (energia, ritmo, palavras).

Intervenção: "Grave um áudio seu e avalie: esse tom é do seu M1 ou do seu MX?"

Objetivo: Alinhar expressão verbal com a nova identidade.""",
        "motor_motivacional": ["Valor", "Desejo"],
        "estagio_jornada": ["Desenvolver", "Florescer"],
        "tipo_crise": ["Conexão", "Identidade"],
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Âncora Prática",
        "dominio": ["D4"],
        "sintomas_comportamentais": ["invisibilidade simbólica", "medo de expressão"],
        "tom_emocional": "indignação",
        "nivel_maturidade": "alto",
    },
    
    {
        "chapter": "Âncoras Práticas",
        "section": "Rituais Matinais",
        "content": """Âncora de Rotina e Estrutura: Primeiras ações do dia.

Intervenção: "Crie um ritual de 10 min que conecte você com sua visão MX"

Objetivo: Iniciar o dia alinhado com a meta extraordinária.""",
        "motor_motivacional": ["Desejo", "Propósito"],
        "estagio_jornada": ["Desenvolver", "Frutificar"],
        "tipo_crise": ["Execução"],
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Âncora Prática",
        "dominio": ["D3"],
        "sintomas_comportamentais": ["falta de estrutura", "dispersão"],
        "tom_emocional": "urgência",
        "nivel_maturidade": "médio",
    },
    
    {
        "chapter": "Âncoras Práticas",
        "section": "Limites",
        "content": """Âncora de Rotina e Estrutura: O que você recusa e o que protege.

Intervenção: "Defina 1 limite claro que você comunicará esta semana"

Objetivo: Proteger energia e identidade através de limites saudáveis.""",
        "motor_motivacional": ["Valor"],
        "estagio_jornada": ["Enraizar", "Desenvolver"],
        "tipo_crise": ["Execução", "Conexão"],
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Âncora Prática",
        "dominio": ["D3", "D4"],
        "sintomas_comportamentais": ["exaustão", "invasão de limites"],
        "tom_emocional": "urgência",
        "nivel_maturidade": "alto",
    },
    
    {
        "chapter": "Âncoras Práticas",
        "section": "Gestão de Energia",
        "content": """Âncora de Emoção e Energia: Como você distribui sua vitalidade.

Intervenção: "Identifique o que drena sua energia e reduza exposição em 20%"

Objetivo: Preservar volição para ações significativas.""",
        "motor_motivacional": ["Necessidade"],
        "estagio_jornada": ["Germinar", "Enraizar"],
        "tipo_crise": ["Execução", "Saúde Física"],
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Âncora Prática",
        "dominio": ["D1", "D3"],
        "sintomas_comportamentais": ["exaustão", "dispersão"],
        "tom_emocional": "urgência",
        "nivel_maturidade": "baixo",
    },
    
    {
        "chapter": "Âncoras Práticas",
        "section": "Tarefas Identitárias",
        "content": """Âncora de Ação e Entrega: Ações que reforçam quem você está se tornando.

Intervenção: "Faça hoje 1 coisa que só sua versão MX faria"

Objetivo: Encarnar a nova identidade através de ações concretas.""",
        "motor_motivacional": ["Desejo", "Valor"],
        "estagio_jornada": ["Desenvolver", "Florescer", "Frutificar"],
        "tipo_crise": ["Transformação", "Identidade"],
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Âncora Prática",
        "dominio": ["D5"],
        "sintomas_comportamentais": ["paralisia", "medo de crescer"],
        "tom_emocional": "indignação",
        "nivel_maturidade": "alto",
    },
    
    {
        "chapter": "Âncoras Práticas",
        "section": "Microentregas",
        "content": """Âncora de Ação e Entrega: Pequenas provas de competência.

Intervenção: "Entregue algo pequeno mas concreto que demonstre sua nova capacidade"

Objetivo: Validar competência através de entregas tangíveis.""",
        "motor_motivacional": ["Desejo"],
        "estagio_jornada": ["Desenvolver", "Florescer"],
        "tipo_crise": ["Execução", "Identidade"],
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Âncora Prática",
        "dominio": ["D3", "D5"],
        "sintomas_comportamentais": ["procrastinação", "síndrome do impostor"],
        "tom_emocional": "urgência",
        "nivel_maturidade": "médio",
    },
    
    {
        "chapter": "Âncoras Práticas",
        "section": "Exposição Gradual",
        "content": """Âncora de Ação e Entrega: Enfrentar medos em doses controladas.

Intervenção: "Exponha-se a uma situação levemente desconfortável esta semana"

Objetivo: Expandir zona de conforto através de exposição gradual.""",
        "motor_motivacional": ["Desejo", "Valor"],
        "estagio_jornada": ["Desenvolver", "Florescer"],
        "tipo_crise": ["Conexão", "Transformação"],
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Âncora Prática",
        "dominio": ["D3", "D4"],
        "sintomas_comportamentais": ["medo de exposição", "invisibilidade"],
        "tom_emocional": "urgência",
        "nivel_maturidade": "alto",
    },
    
    {
        "chapter": "Âncoras Práticas",
        "section": "Testemunhas",
        "content": """Âncora de Ação e Entrega: Pessoas que validam a transformação.

Intervenção: "Compartilhe sua intenção com 1 pessoa que pode te cobrar"

Objetivo: Criar accountability e validação externa da nova identidade.""",
        "motor_motivacional": ["Propósito", "Desejo"],
        "estagio_jornada": ["Florescer", "Frutificar", "Realizar"],
        "tipo_crise": ["Conexão", "Transformação"],
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Âncora Prática",
        "dominio": ["D4", "D5", "D6"],
        "sintomas_comportamentais": ["solidão existencial", "falta de accountability"],
        "tom_emocional": "indignação",
        "nivel_maturidade": "alto",
    },
    
    # =============================================================================
    # PARTE IV: PONTOS DE ENTRADA
    # =============================================================================
    
    {
        "chapter": "Pontos de Entrada",
        "section": "Emocional",
        "content": """Porta de acesso quando o usuário relata estados afetivos.

Sinais na Fala: "Me sinto ansioso", "Estou com medo", "Fico triste quando..."

Ação da IA: Validar e regular a emoção primeiro, antes de qualquer intervenção cognitiva.

Exemplo: "Percebo que há uma exaustão real aqui. Antes de pensarmos em próximos passos, vamos entender essa ansiedade..."

Regra: Não misture intervenções de portas diferentes na mesma resposta.""",
        "motor_motivacional": ["Necessidade"],
        "estagio_jornada": ["Germinar"],
        "tipo_crise": ["Saúde Mental", "Conexão"],
        "ponto_entrada": "Emocional",
        "tipo_conteudo": "Ponto de Entrada",
        "dominio": ["D1"],
        "sintomas_comportamentais": ["ansiedade", "tristeza", "medo"],
        "tom_emocional": "urgência",
        "nivel_maturidade": "baixo",
    },
    
    {
        "chapter": "Pontos de Entrada",
        "section": "Simbólico",
        "content": """Porta de acesso quando há falta de sentido ou traição de valores.

Sinais na Fala: "Isso não faz sentido", "Perdi minha essência", "Não sei mais quem sou"

Ação da IA: Ressignificar símbolos e reconectar com o inegociável.

Exemplo: "Você menciona traição. Que valor inegociável você sente que foi comprometido?"

Regra: Se a porta Simbólica está aberta, trabalhe na ressignificação antes de propor ações.""",
        "motor_motivacional": ["Valor"],
        "estagio_jornada": ["Enraizar"],
        "tipo_crise": ["Identidade", "Sentido"],
        "ponto_entrada": "Simbólico",
        "tipo_conteudo": "Ponto de Entrada",
        "dominio": ["D2"],
        "sintomas_comportamentais": ["vazio existencial", "traição de valores"],
        "tom_emocional": "indignação",
        "nivel_maturidade": "médio",
    },
    
    {
        "chapter": "Pontos de Entrada",
        "section": "Comportamental",
        "content": """Porta de acesso quando o foco está em hábitos e procrastinação.

Sinais na Fala: "Não consigo me organizar", "Sempre adio", "Não tenho disciplina"

Ação da IA: Sugerir micro-hábitos e protocolos concretos.

Exemplo: "Qual seria o menor movimento físico que você poderia fazer amanhã sem desculpas?"

Regra: Não force entrada Comportamental se a porta Emocional está aberta.""",
        "motor_motivacional": ["Desejo", "Necessidade"],
        "estagio_jornada": ["Desenvolver"],
        "tipo_crise": ["Execução"],
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Ponto de Entrada",
        "dominio": ["D3"],
        "sintomas_comportamentais": ["procrastinação", "falta de organização"],
        "tom_emocional": "urgência",
        "nivel_maturidade": "médio",
    },
    
    {
        "chapter": "Pontos de Entrada",
        "section": "Existencial",
        "content": """Porta de acesso quando há crise de papel de vida.

Sinais na Fala: "Não sei quem sou", "Qual meu propósito?", "Estou perdido"

Ação da IA: Reposicionar missão e legado, trabalhar a identidade.

Exemplo: "Se você pudesse escolher ser lembrado por uma única contribuição, qual seria?"

Regra: Respeite a hierarquia - não pule para ação se a identidade está em crise.""",
        "motor_motivacional": ["Propósito", "Valor"],
        "estagio_jornada": ["Germinar", "Enraizar"],
        "tipo_crise": ["Identidade", "Sentido"],
        "ponto_entrada": "Existencial",
        "tipo_conteudo": "Ponto de Entrada",
        "dominio": ["D1", "D6"],
        "sintomas_comportamentais": ["crise existencial", "falta de propósito"],
        "tom_emocional": "apatia",
        "nivel_maturidade": "baixo",
    },
    
    # =============================================================================
    # PARTE V: CLUSTERS DE CRISE (Conceitos Metodológicos)
    # =============================================================================
    
    {
        "chapter": "Clusters de Crise",
        "section": "Identidade Raiz",
        "content": """Crise caracterizada por identidades herdadas, viver papéis impostos e vergonha da história.

Descrição: Viver sob rótulos impostos por pais, escola ou cultura, atuando papéis que não foram escolhidos.

Padrões de Fala:
- "Sempre fui assim"
- "Minha família é assim"
- "Não tenho escolha"

Áreas Impactadas: Vida Pessoal, Vida Familiar, Saúde Mental

Ponto de Entrada: Simbólico
Domínio Alavanca: D1, D2

Pergunta-chave: "Quem você seria se ninguém estivesse olhando?" """,
        "motor_motivacional": ["Valor", "Necessidade"],
        "estagio_jornada": ["Germinar", "Enraizar"],
        "tipo_crise": ["Identidade"],
        "subtipo_crise": "Identidade Herdada",
        "ponto_entrada": "Simbólico",
        "tipo_conteudo": "Conceito",
        "dominio": ["D1", "D2"],
        "sintomas_comportamentais": [
            "autossabotagem",
            "vergonha da origem",
            "atuação de papéis",
        ],
        "tom_emocional": "vergonha",
        "nivel_maturidade": "baixo",
    },
    
    {
        "chapter": "Clusters de Crise",
        "section": "Sentido e Direção",
        "content": """Crise caracterizada por futuro opaco, tempo perdido e falta de enredo unificador.

Descrição: Sensação de viver episódios desconexos, sem uma linha condutora que una passado, presente e futuro.

Padrões de Fala:
- "Não sei o que quero"
- "Já tentei de tudo"
- "Nada faz sentido"

Áreas Impactadas: Vida Profissional, Educação, Saúde Espiritual

Ponto de Entrada: Cognitivo (Simbólico)
Domínio Alavanca: D2, D3

Pergunta-chave: "O que você faria se soubesse que não poderia falhar?" """,
        "motor_motivacional": ["Valor", "Propósito"],
        "estagio_jornada": ["Germinar", "Enraizar"],
        "tipo_crise": ["Sentido"],
        "subtipo_crise": "Vazio e Fragmentação",
        "ponto_entrada": "Simbólico",
        "tipo_conteudo": "Conceito",
        "dominio": ["D2", "D3"],
        "sintomas_comportamentais": [
            "vazio existencial",
            "fragmentação narrativa",
            "urgência tóxica",
        ],
        "tom_emocional": "apatia",
        "nivel_maturidade": "baixo",
    },
    
    {
        "chapter": "Clusters de Crise",
        "section": "Execução e Estrutura",
        "content": """Crise caracterizada por procrastinação, paralisia decisória e falta de limites.

Descrição: A "espera por permissão" e o medo de tomar o protagonismo, muitas vezes disfarçados de procrastinação ou planejamento excessivo.

Padrões de Fala:
- "Vou começar amanhã"
- "Não consigo dizer não"
- "Tudo é urgente"

Áreas Impactadas: Finanças, Saúde Física, Vida Profissional

Ponto de Entrada: Comportamental
Domínio Alavanca: D3

Pergunta-chave: "Qual a menor ação que você poderia fazer agora?" """,
        "motor_motivacional": ["Desejo", "Necessidade"],
        "estagio_jornada": ["Desenvolver"],
        "tipo_crise": ["Execução"],
        "subtipo_crise": "Paralisia Decisória",
        "ponto_entrada": "Comportamental",
        "tipo_conteudo": "Conceito",
        "dominio": ["D3"],
        "sintomas_comportamentais": [
            "procrastinação",
            "paralisia decisória",
            "ausência de limites",
        ],
        "tom_emocional": "urgência",
        "nivel_maturidade": "baixo",
    },
    
    {
        "chapter": "Clusters de Crise",
        "section": "Conexão e Expressão",
        "content": """Crise caracterizada por medo do julgamento, invisibilidade simbólica e desconforto com sucesso.

Descrição: Medo de brilhar, de incomodar ou de ser julgado, o que leva o indivíduo a sabotar sua própria presença e voz em espaços de poder.

Padrões de Fala:
- "Ninguém me entende"
- "Não quero incomodar"
- "É melhor ficar quieto"

Áreas Impactadas: Vida Social, Vida Amorosa, Vida Pessoal

Ponto de Entrada: Emocional
Domínio Alavanca: D4

Pergunta-chave: "O que você deixa de dizer com medo da reação?" """,
        "motor_motivacional": ["Desejo", "Valor"],
        "estagio_jornada": ["Desenvolver", "Florescer"],
        "tipo_crise": ["Conexão"],
        "subtipo_crise": "Invisibilidade Simbólica",
        "ponto_entrada": "Emocional",
        "tipo_conteudo": "Conceito",
        "dominio": ["D4"],
        "sintomas_comportamentais": [
            "invisibilidade simbólica",
            "medo de julgamento",
            "solidão existencial",
        ],
        "tom_emocional": "indignação",
        "nivel_maturidade": "médio",
    },
    
    {
        "chapter": "Clusters de Crise",
        "section": "Incongruência Identidade-Cultura",
        "content": """Crise caracterizada por choque entre quem a pessoa é e o ambiente/sistema em que vive.

Descrição: O desgaste de tentar manter uma nova identidade em contextos antigos que insistem em tratar a pessoa como sua versão anterior.

Padrões de Fala:
- "Não me encaixo"
- "Aqui não valorizam isso"
- "Preciso me adaptar"

Áreas Impactadas: Vida Social, Vida Profissional, Saúde Mental

Ponto de Entrada: Ambiental (Comportamental)
Domínio Alavanca: D4, D5

Pergunta-chave: "Onde você se sente mais você mesmo?" """,
        "motor_motivacional": ["Valor"],
        "estagio_jornada": ["Florescer", "Frutificar"],
        "tipo_crise": ["Incongruência"],
        "subtipo_crise": "Choque Ambiental",
        "ponto_entrada": "Simbólico",
        "tipo_conteudo": "Conceito",
        "dominio": ["D4", "D5"],
        "sintomas_comportamentais": [
            "choque ambiental",
            "desajuste sistêmico",
        ],
        "tom_emocional": "indignação",
        "nivel_maturidade": "alto",
    },
    
    {
        "chapter": "Clusters de Crise",
        "section": "Transformação de Personagem",
        "content": """Crise caracterizada por apego a papéis obsoletos, medo de crescer e dificuldade em encerrar capítulos.

Descrição: Dificuldade em deixar ir versões antigas de si mesmo e assumir uma nova identidade.

Padrões de Fala:
- "Não sou esse tipo de pessoa"
- "Quem sou eu para..."
- "Vão descobrir"

Áreas Impactadas: Inovação, Vida Profissional, Vida Pessoal

Ponto de Entrada: Temporal (Existencial)
Domínio Alavanca: D5, D6

Pergunta-chave: "Qual versão de você está com medo de morrer?" """,
        "motor_motivacional": ["Desejo", "Propósito"],
        "estagio_jornada": ["Frutificar", "Realizar"],
        "tipo_crise": ["Transformação"],
        "subtipo_crise": "Apego a Papéis Obsoletos",
        "ponto_entrada": "Existencial",
        "tipo_conteudo": "Conceito",
        "dominio": ["D5", "D6"],
        "sintomas_comportamentais": [
            "apego a papéis obsoletos",
            "medo de crescer",
            "síndrome do impostor",
        ],
        "tom_emocional": "indignação",
        "nivel_maturidade": "alto",
    },
]
