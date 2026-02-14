"""
Constantes e dados estáticos do sistema NARA.
Baseline conforme documento IDENTIDADE_NARA (Cap. 7) — Metodologia de Transformação Narrativa.
"""

# As 12 áreas estruturantes (Círculo Narrativo)
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

# Perguntas baseline (15) — M1 Estado de Crise — IDENTIDADE_NARA Cap. 7
BASELINE_QUESTIONS = [
    {
        "id": 1,
        "area": "Vida Pessoal",
        "type": "open_long",
        "text": "Se sua vida hoje fosse um livro, qual seria o título do capítulo atual? De 0 a 5, o quanto você se sente de fato o protagonista da sua própria história?",
    },
    {
        "id": 2,
        "area": "Saúde Física",
        "type": "open_long",
        "text": "Como você avalia sua constituição e disposição corporal para os desafios da sua jornada? (0 = exausto, 5 = plena vitalidade). Descreva como o seu corpo tem reagido ao seu ritmo atual.",
    },
    {
        "id": 3,
        "area": "Saúde Mental",
        "type": "open_long",
        "text": "Quais \"frases automáticas\" de autocrítica ou medo mais visitam sua mente hoje? (0 = mente caótica, 5 = equilíbrio total).",
    },
    {
        "id": 4,
        "area": "Saúde Espiritual",
        "type": "open_long",
        "text": "O que dá sentido e convicção interior à sua existência hoje? (0 = perdido/sem fé, 5 = convicção plena).",
    },
    {
        "id": 5,
        "area": "Vida Familiar",
        "type": "scale",
        "text": "Você sente que vive sob \"identidades herdadas\" ou valores familiares que não escolheu conscientemente?",
        "scale_labels": ["Prisioneiro de rótulos", "Pouco autêntico", "Em transição", "Autêntico", "Totalmente autêntico"],
    },
    {
        "id": 6,
        "area": "Vida Amorosa",
        "type": "scale",
        "text": "Existe parceria e alinhamento emocional para a construção do seu Círculo Narrativo Futuro (CN+)?",
        "scale_labels": ["Insatisfeito", "Pouco alinhado", "Regular", "Bem alinhado", "Pleno"],
    },
    {
        "id": 7,
        "area": "Vida Social",
        "type": "scale",
        "text": "Suas interações atuais funcionam como um \"campo gravitacional\" que te nutre ou que drena sua energia?",
        "scale_labels": ["Ambiente tóxico", "Mais drena", "Neutro", "Mais nutre", "Rede nutritiva"],
    },
    {
        "id": 8,
        "area": "Vida Profissional",
        "type": "scale",
        "text": "Você sente que domina seu ofício ou que está apenas atuando um papel que não condiz com quem você realmente é?",
        "scale_labels": ["Frustrado", "Pouco realizado", "Regular", "Realizado", "Muito realizado"],
    },
    {
        "id": 9,
        "area": "Finanças",
        "type": "scale",
        "text": "Como está a gestão do seu capital para sustentar a estrutura de vida que você deseja?",
        "scale_labels": ["Caos/preocupação", "Difícil", "Regular", "Boa", "Total controle"],
    },
    {
        "id": 10,
        "area": "Educação",
        "type": "scale",
        "text": "Você está em um processo ativo de modelagem de novos padrões ou sente que seu aprendizado está estagnado?",
        "scale_labels": ["Estagnado", "Pouco ativo", "Regular", "Ativo", "Aprendiz contínuo"],
    },
    {
        "id": 11,
        "area": "Inovação",
        "type": "scale",
        "text": "Quanto espaço real você reserva para a criatividade e para testar novas formas de resolver seus problemas?",
        "scale_labels": ["Nenhum espaço", "Pouco", "Regular", "Bom espaço", "Fluxo constante"],
    },
    {
        "id": 12,
        "area": "Lazer",
        "type": "scale",
        "text": "Como você utiliza seu tempo livre para recuperação de energia e rituais de descompressão?",
        "scale_labels": ["Inexistente", "Raro", "Regular", "Frequente", "Equilibrado"],
    },
    {
        "id": 13,
        "area": "Geral",
        "type": "open_short",
        "text": "O que mais te move hoje: o alívio de uma dor (Necessidade), a busca por coerência (Valor), a conquista de algo (Desejo) ou o impacto no mundo (Propósito)?",
    },
    {
        "id": 14,
        "area": "Geral",
        "type": "open_long",
        "text": "Se você pudesse transpor um único conflito central hoje para alcançar sua meta extraordinária, qual seria esse obstáculo?",
    },
    {
        "id": 15,
        "area": "Geral",
        "type": "open_long",
        "text": "Descreva sua versão extraordinária daqui a 12 meses. O que essa pessoa faz no dia a dia que você, na sua versão atual, ainda não consegue realizar?",
    },
]

# Motores motivacionais
MOTORES = {
    "Necessidade": "Dor interna que precisa de alívio",
    "Valor": "Integridade e coerência com princípios",
    "Desejo": "Vontade de conquista e realização",
    "Propósito": "Impacto significativo no mundo",
}

# Fases da jornada
FASES_JORNADA = [
    "Germinar",
    "Enraizar",
    "Desenvolver",
    "Florescer",
    "Frutificar",
    "Realizar",
]

# Tipos de crise
TIPOS_CRISE = [
    "Identidade",
    "Sentido",
    "Execução",
    "Conexão",
    "Incongruência",
    "Transformação",
]
