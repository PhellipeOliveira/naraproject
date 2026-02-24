"""
Constantes e dados estáticos do sistema NARA.
Conforme documento 01_FUNDAMENTOS — Metodologia de Transformação Narrativa,
12 Áreas Estruturantes do Círculo Narrativo, Motores Motivacionais e Fases da Jornada.
"""

# As 12 áreas estruturantes (Círculo Narrativo) — 01_FUNDAMENTOS § 2.1
AREAS = [
    "Saúde Física",
    "Saúde Mental",
    "Saúde Espiritual",
    "Vida Pessoal",
    "Vida Amorosa",
    "Vida Familiar",
    "Vida Social",
    "Vida Profissional",
    "Finanças",
    "Educação",
    "Inovação",
    "Lazer",
]

# Perguntas baseline (15) — 100% Narrativas — 01_BASE_METODOLOGICA § VI.1
# Baseadas em escuta ativa e sinais de conflito (M1)
BASELINE_QUESTIONS = [
    {
        "id": 1,
        "area": "Vida Pessoal",
        "type": "open_long",
        "text": "Se você tivesse que dar um título para o momento que está vivendo agora, qual seria? Você sente que está escrevendo sua própria história ou apenas seguindo o que os outros esperam de você?",
    },
    {
        "id": 2,
        "area": "Saúde Física",
        "type": "open_long",
        "text": "Como seu corpo tem se sentido para dar conta de tudo o que você precisa fazer no dia a dia? O que ele está tentando te dizer através do seu nível de cansaço ou disposição?",
    },
    {
        "id": 3,
        "area": "Saúde Mental",
        "type": "open_long",
        "text": "Quando as coisas ficam difíceis, que tipo de pensamentos negativos ou críticas sobre você mesmo costumam aparecer na sua cabeça? Como isso trava o seu dia?",
    },
    {
        "id": 4,
        "area": "Saúde Espiritual",
        "type": "open_long",
        "text": "No fundo, o que faz você sentir que sua vida realmente vale a pena? O que te dá forças para continuar quando tudo parece sem sentido ou direção?",
    },
    {
        "id": 5,
        "area": "Vida Familiar",
        "type": "open_long",
        "text": "Olhando para a sua família, quais hábitos ou jeitos de ser você sente que \"carrega\" sem ter escolhido? O que você gostaria de fazer diferente do que aprendeu com eles?",
    },
    {
        "id": 6,
        "area": "Vida Amorosa",
        "type": "open_long",
        "text": "Como você se sente em relação à pessoa que está ao seu lado (ou à falta dela)? Essa relação te ajuda a ser quem você quer se tornar ou você sente que precisa se anular para estar nela?",
    },
    {
        "id": 7,
        "area": "Vida Social",
        "type": "open_long",
        "text": "As pessoas com quem você convive hoje te incentivam a crescer ou você sente que precisa \"diminuir o seu brilho\" para ser aceito por elas?",
    },
    {
        "id": 8,
        "area": "Vida Profissional",
        "type": "open_long",
        "text": "No seu trabalho, você sente que pode ser você mesmo ou parece que está apenas \"fingindo\" ser alguém para dar conta do recado e ser respeitado?",
    },
    {
        "id": 9,
        "area": "Finanças",
        "type": "open_long",
        "text": "Como você se sente quando pensa no seu dinheiro hoje? Ele tem sido uma ferramenta para realizar seus planos ou uma fonte constante de medo e preocupação?",
    },
    {
        "id": 10,
        "area": "Educação",
        "type": "open_long",
        "text": "O que você tem aprendido de novo ultimamente que realmente muda o seu jeito de agir? Ou você sente que parou no tempo e está apenas repetindo o que já sabe?",
    },
    {
        "id": 11,
        "area": "Inovação",
        "type": "open_long",
        "text": "Quando surge um problema, você costuma tentar caminhos novos ou sempre faz do mesmo jeito? Onde você gostaria de ser mais criativo e ousado na sua vida?",
    },
    {
        "id": 12,
        "area": "Lazer",
        "type": "open_long",
        "text": "O que você faz para realmente \"desligar\" e recuperar suas energias? Você consegue aproveitar o seu tempo livre sem sentir que deveria estar sendo produtivo?",
    },
    {
        "id": 13,
        "area": "Geral",
        "type": "open_short",
        "text": "O que mais te empurra para a mudança hoje: o cansaço de uma dor que não aguenta mais, a vontade de ser fiel ao que acredita, o sonho de conquistar algo novo ou o desejo de ajudar e impactar as pessoas?",
    },
    {
        "id": 14,
        "area": "Geral",
        "type": "open_long",
        "text": "Se existisse uma única barreira que, se removida hoje, mudaria tudo na sua vida, que barreira seria essa?",
    },
    {
        "id": 15,
        "area": "Geral",
        "type": "open_long",
        "text": "Imagine-se daqui a um ano vivendo sua melhor versão. O que essa pessoa faz no dia a dia que você, hoje, ainda não consegue realizar?",
    },
]

# Motores motivacionais — 01_FUNDAMENTOS § 2.2
MOTORES = {
    "Necessidade": "Dor interna que precisa de alívio",
    "Valor": "Integridade e coerência com princípios",
    "Desejo": "Vontade de conquista e realização",
    "Propósito": "Impacto significativo no mundo",
}

# Fases da jornada — 01_FUNDAMENTOS § 2.3 (Germinar → Realizar)
FASES_JORNADA = [
    "Germinar",
    "Enraizar",
    "Desenvolver",
    "Florescer",
    "Frutificar",
    "Realizar",
]

# Tipos de crise (Clusters Operacionais M1) — 01_BASE_METODOLOGICA § II.1
TIPOS_CRISE = [
    "Identidade",
    "Sentido",
    "Execução",
    "Conexão",
    "Incongruência",
    "Transformação",
]

# Os 4 Níveis de Identidade (Luz Total) — 01_BASE_METODOLOGICA § I.5
NIVEIS_IDENTIDADE = [
    "Personalidade",
    "Cultura",
    "Realizações",
    "Posição",
]

# Os 4 Pontos de Entrada (Portas de Intervenção) — 01_BASE_METODOLOGICA § I.6
PONTOS_ENTRADA = {
    "Emocional": "Usuário relata estados afetivos",
    "Simbólico": "Falta de sentido ou traição de valores",
    "Comportamental": "Foco em hábitos e procrastinação",
    "Existencial": "Crise de papel de vida",
}

# As 19 Âncoras Práticas (Assunção Intencional) — 01_BASE_METODOLOGICA § II.5
ANCORAS_PRATICAS = [
    # Ambiente e Contexto
    "Referências",
    "Objetos",
    "Ambientes",
    "Grupo",
    # Comunicação e Expressão
    "Tom",
    "Vocabulário",
    "Postura",
    "Vestimenta",
    # Rotina e Estrutura
    "Rituais Matinais",
    "Rituais Noturnos",
    "Limites",
    "Marcos",
    # Emoção e Energia
    "Emoção Projetada",
    "Gestão de Energia",
    "Práticas de Recarga",
    # Ação e Entrega
    "Tarefas Identitárias",
    "Microentregas",
    "Exposição Gradual",
    "Testemunhas",
]

# Domínios Temáticos — 01_BASE_METODOLOGICA § I.3
# Ferramentas transversais às 6 Fases da Jornada (não são fases).
DOMINIOS_TEMATICOS = {
    "D1": "Motivações e Conflitos",
    "D2": "Crenças, Valores e Princípios",
    "D3": "Evolução e Desenvolvimento",
    "D4": "Congruência Identidade-Cultura",
    "D5": "Transformação de Identidade",
    "D6": "Papel na Sociedade",
}

# Eixos de Transformação — síntese operacional da metodologia
EIXOS_TRANSFORMACAO = {
    "Narrativa": {
        "essencia": "A lente da Crença — a história que o indivíduo conta sobre si e o mundo",
        "ferramenta_principal": "TCC (reestruturação cognitiva)",
        "objetivo": "Ressignificar eventos-chave, reformular padrões repetitivos, criar narrativa futura",
    },
    "Identidade": {
        "essencia": "O espelho dos Valores — quem o indivíduo é",
        "ferramenta_principal": "Assunção Intencional",
        "objetivo": "Reposicionar o 'quem sou eu', dissolver rótulos herdados, reconstruir autoimagem",
    },
    "Habitos": {
        "essencia": "A manifestação dos Princípios — ações práticas diárias",
        "ferramenta_principal": "Assunção Intencional",
        "objetivo": "Implantar microações coerentes, criar rotinas de sustentação, remover automatismos limitantes",
    },
}

# Motores com semântica de diagnóstico e peso de Gap MX
MOTORES_DETALHADOS = {
    "Necessidade": {
        "discurso_praticado": "Percepção de falta interna ou dor",
        "busca": "Alívio e estabilidade emocional",
        "pergunta_acesso": "O que está faltando na sua vida hoje que te traria paz?",
        "peso_gap": 1.0,
    },
    "Valor": {
        "discurso_praticado": "Indivíduo quer estar alinhado internamente (crenças, valores e princípios)",
        "busca": "Integridade e alinhamento interno",
        "pergunta_acesso": "Qual valor seu está sendo desrespeitado?",
        "peso_gap": 0.8,
    },
    "Desejo": {
        "discurso_praticado": "Identificação de falta externa ou aspiração",
        "busca": "Conquista, realização e prazer",
        "pergunta_acesso": "Se tudo fosse possível, o que você gostaria de viver nos próximos 12 meses?",
        "peso_gap": 0.6,
    },
    "Proposito": {
        "discurso_praticado": "Indivíduo quer estar alinhado externamente (impacto e contribuição)",
        "busca": "Impacto e legado",
        "pergunta_acesso": "Que marca você quer deixar no mundo?",
        "peso_gap": 0.4,
    },
}

# Domínios Temáticos completos com pergunta-chave e fase de maior potência
# (correlação de intervenção, não equivalência Domínio = Fase).
DOMINIOS_TEMATICOS_COMPLETOS = {
    "D1": {
        "nome": "Motivações e Conflitos",
        "pergunta_chave": "O que está te movendo — e o que está te travando?",
        "impacto": "Mapear motivações (desejo, valor, necessidade, propósito) e conflitos que impedem avanço",
        "fase_potencia_maxima": "Germinar",
    },
    "D2": {
        "nome": "Crenças, Valores e Princípios",
        "pergunta_chave": "O que é inegociável para você?",
        "impacto": "Alinhar pensamento, fala e ação com autenticidade e integridade narrativa",
        "fase_potencia_maxima": "Enraizar",
    },
    "D3": {
        "nome": "Evolução e Desenvolvimento Pessoal",
        "pergunta_chave": "Você está se tornando quem deseja ser?",
        "impacto": "Aplicar disciplina, mentalidade de crescimento e modelagem comportamental",
        "fase_potencia_maxima": "Desenvolver",
    },
    "D4": {
        "nome": "Congruência entre Identidade e Cultura",
        "pergunta_chave": "Sua expressão é fiel à sua essência ou moldada pelo ambiente?",
        "impacto": "Ajustar comunicação interna e externa para coerência entre ser e ambiente",
        "fase_potencia_maxima": "Florescer",
    },
    "D5": {
        "nome": "Transformação de Identidade e Personagens",
        "pergunta_chave": "Quem você está sendo nesta fase da vida?",
        "impacto": "Reescrever narrativas pessoais, soltar padrões limitantes, incorporar novos personagens internos",
        "fase_potencia_maxima": "Frutificar",
    },
    "D6": {
        "nome": "Papel dos Indivíduos na Sociedade",
        "pergunta_chave": "Como sua história contribui para o mundo?",
        "impacto": "Despertar senso de impacto, liderança e pertencimento",
        "fase_potencia_maxima": "Realizar",
    },
}

# Assunção Intencional — 4 movimentos de consolidação
ASSUNCAO_INTENCIONAL = {
    "Reconhecer": {
        "fase_jornada": "Germinar",
        "foco": "Tomar consciência do padrão atual",
        "acao": "Identificar histórias, crenças e padrões limitantes através de auto-observação e diagnóstico narrativo",
    },
    "Modelar": {
        "fase_jornada": "Enraizar",
        "foco": "Criar imagem clara da identidade ideal",
        "acao": "Mapear nova narrativa, crenças, valores, princípios e hábitos; visualizar o novo eu",
    },
    "Assumir": {
        "fase_jornada": "Desenvolver",
        "foco": "Viver simbolicamente a nova identidade no presente",
        "acao": "Declarar a nova identidade com afirmações, adotar rituais simbólicos e agir como se já fosse real",
    },
    "Reforcar": {
        "fase_jornada": "Florescer|Frutificar|Realizar",
        "foco": "Consolidar a nova identidade",
        "acao": "Manter microvitórias diárias, praticar storytelling com evidências, ancorar emoções em valores",
    },
}

# Técnicas TCC com gatilho e pergunta metodológica padrão
TECNICAS_TCC_NARA = {
    "Identificacao de Pensamentos Automaticos": {
        "sinal_ativacao": "Frases internas repetitivas: 'vou falhar', 'nunca consigo'",
        "pergunta_nara": "Essa frase te visita com frequência? Ela parece um reflexo ou um roteiro automático?",
        "ponto_entrada_ideal": "Emocional",
    },
    "Questionamento Socratico": {
        "sinal_ativacao": "Crenças absolutas: 'nunca serei capaz', 'não tenho saída'",
        "pergunta_nara": "O que faz você acreditar nisso? Você já conseguiu em algum momento?",
        "ponto_entrada_ideal": "Existencial",
    },
    "Reestruturacao Cognitiva Escrita": {
        "sinal_ativacao": "Loop mental repetido, narrativa punitiva sobre erros",
        "pergunta_nara": "Escreva essa narrativa. Agora reescreva uma versão que honre a verdade sem te atacar.",
        "ponto_entrada_ideal": "Simbolico",
    },
    "Descatastrofizacao": {
        "sinal_ativacao": "Pensamentos catastróficos: 'tudo vai desmoronar', 'será um desastre'",
        "pergunta_nara": "O que de pior pode acontecer? E se isso acontecer, o que você faria?",
        "ponto_entrada_ideal": "Existencial",
    },
    "Redefinicao Cognitiva Assistida": {
        "sinal_ativacao": "Leitura punitiva de eventos: 'isso prova que não sou bom'",
        "pergunta_nara": "E se esse evento fosse um convite ao seu próximo nível?",
        "ponto_entrada_ideal": "Simbolico",
    },
    "Substituicao de Pensamentos Distorcidos": {
        "sinal_ativacao": "Generalizações: 'sempre', 'nunca', 'eu nunca consigo'",
        "pergunta_nara": "Qual frase-âncora mais verdadeira pode substituir esse roteiro?",
        "ponto_entrada_ideal": "Comportamental",
    },
    "Imaginacao Guiada": {
        "sinal_ativacao": "Bloqueio identitário, dificuldade de visualizar nova versão de si",
        "pergunta_nara": "Feche os olhos. Como é a sua postura, fala e ação como a identidade que você escolheu?",
        "ponto_entrada_ideal": "Emocional",
    },
    "Flecha Descendente": {
        "sinal_ativacao": "Padrão de autossabotagem repetido, autocrítica persistente",
        "pergunta_nara": "Se isso for verdade... o que isso diz sobre quem você é? E o que isso significaria?",
        "ponto_entrada_ideal": "Emocional",
    },
}

# Protocolo de Diagnóstico Rápido (6 fatores) — 01_BASE_METODOLOGICA § II.2
FATORES_DIAGNOSTICO = [
    "Autenticidade",
    "Integração do Passado",
    "Visão/Enredo",
    "Coragem/Decisão",
    "Expressão/Voz",
    "Estrutura/Pertencimento",
]

# Clusters Operacionais de Crise (subtipos) — 01_BASE_METODOLOGICA § II.1
CLUSTERS_CRISE = {
    "Identidade Raiz": {
        "sinais": [
            "Identidades Herdadas",
            "Vergonha e Indignidade",
            "Autoimagem Desatualizada",
        ],
        "areas_impactadas": ["Vida Pessoal", "Vida Familiar", "Saúde Mental"],
    },
    "Sentido e Direção": {
        "sinais": [
            "Vazio e Fragmentação",
            "Falta de Visão de Futuro",
            "Urgência Tóxica",
        ],
        "areas_impactadas": ["Vida Profissional", "Educação", "Saúde Espiritual"],
    },
    "Execução e Estrutura": {
        "sinais": [
            "Paralisia Decisória",
            "Ausência de Ritos",
        ],
        "areas_impactadas": ["Finanças", "Saúde Física", "Vida Profissional"],
    },
    "Conexão e Expressão": {
        "sinais": [
            "Invisibilidade Simbólica",
            "Solidão Existencial",
        ],
        "areas_impactadas": ["Vida Social", "Vida Amorosa", "Vida Pessoal"],
    },
    "Incongruência Identidade-Cultura": {
        "sinais": [
            "Choque Ambiental",
            "Desajuste Sistêmico",
        ],
        "areas_impactadas": ["Vida Social", "Vida Profissional", "Saúde Mental"],
    },
    "Transformação de Personagem": {
        "sinais": [
            "Apego a Papéis Obsoletos",
            "Medo de Crescer",
            "Dificuldade em Encerrar Capítulos",
        ],
        "areas_impactadas": ["Inovação", "Vida Profissional", "Vida Pessoal"],
    },
}

# Sinais M1 por área (usado em prompts e ingestão)
SINAIS_M1_POR_AREA = {
    "Saúde Física": ["Fadiga crônica", "Corpo desconectado das metas", "Volição baixa"],
    "Saúde Mental": ["Autocrítica excessiva", "Pensamentos automáticos negativos", "Ruminação"],
    "Saúde Espiritual": ["Vazio existencial", "Falta de sentido", "Desconexão de propósito"],
    "Vida Pessoal": ["Identidade fragmentada", "Narrativa de autossabotagem", "Ausência de essência"],
    "Vida Amorosa": ["Anulação pelo parceiro", "Padrão de relacionamento repetido", "Solidão afetiva"],
    "Vida Familiar": ["Identidades herdadas não questionadas", "Conflito geracional", "Vergonha familiar"],
    "Vida Social": ["Invisibilidade simbólica", "Diminuição do brilho para aceitação", "Solidão existencial"],
    "Vida Profissional": ["Síndrome do impostor", "Atuação de papel falso", "Invisibilidade em espaços de poder"],
    "Finanças": ["Crenças de escassez herdadas", "Ansiedade por desorganização material", "Falta de recurso para MX"],
    "Educação": ["Estagnação intelectual", "Paralisia por excesso de preparação", "Informação sem ação"],
    "Inovação": ["Bloqueio criativo", "Medo de recomeçar", "Repetição de ciclos exaustivos"],
    "Lazer": ["Culpa por descansar", "Lazer viciado que drena", "Ausência de rituais de descompressão"],
}
