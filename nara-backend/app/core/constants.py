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

# Domínios Temáticos — 01_BASE_METODOLOGICA § I.3 (Fases da Jornada)
DOMINIOS_TEMATICOS = {
    "D1": "Motivações e Conflitos",
    "D2": "Crenças, Valores e Princípios",
    "D3": "Evolução e Desenvolvimento",
    "D4": "Congruência Identidade-Cultura",
    "D5": "Transformação de Identidade",
    "D6": "Papel na Sociedade",
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
