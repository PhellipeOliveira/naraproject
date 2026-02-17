"""
Análise de contexto das respostas do usuário.
Extrai Memórias Vermelhas, silêncios, padrões e tom emocional.
"""
import logging
import re
from collections import Counter
from typing import Any

logger = logging.getLogger(__name__)

# Palavras-chave para identificação de padrões
PALAVRAS_AUTOSSABOTAGEM = [
    "sempre",
    "nunca",
    "não consigo",
    "impossível",
    "fracasso",
    "não sou capaz",
    "vou falhar",
    "não mereço",
    "não tenho",
    "não aguento",
]

PALAVRAS_EMOCAO = {
    "vergonha": [
        "vergonha",
        "envergonhado",
        "humilhado",
        "constrangido",
        "inadequado",
        "inferior",
    ],
    "indignação": [
        "injusto",
        "traído",
        "enganado",
        "usado",
        "desvalorizado",
        "desrespeitado",
        "ignorado",
    ],
    "apatia": [
        "vazio",
        "indiferente",
        "tanto faz",
        "sem sentido",
        "apático",
        "desanimado",
        "sem energia",
    ],
    "urgência": [
        "urgente",
        "ansioso",
        "preocupado",
        "estressado",
        "tenso",
        "pressionado",
        "correndo",
        "atrasado",
    ],
    "tristeza": [
        "triste",
        "deprimido",
        "melancólico",
        "sozinho",
        "abandonado",
        "perdido",
        "desesperançado",
    ],
}

PALAVRAS_CRISE = {
    "exaustão": ["cansado", "exausto", "esgotado", "sem energia", "fadiga"],
    "dor": ["dor", "sofrimento", "angústia", "aflição"],
    "conflito": ["conflito", "briga", "desentendimento", "tensão", "desacordo"],
}

# Áreas do Círculo Narrativo (índice 1-12)
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


def analyze_answers_context(responses: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Analisa o contexto das respostas do usuário.
    
    Args:
        responses: Lista de respostas com question_area, answer_value, etc.
    
    Returns:
        Dict com análise contextual:
        - memorias_vermelhas: Citações literais que revelam conflitos
        - barreiras_identificadas: Padrões de autossabotagem
        - capital_simbolico: Recursos e forças do usuário
        - tom_emocional: Tom dominante (vergonha, indignação, etc.)
        - areas_criticas: IDs das áreas com sinais de crise
        - areas_silenciadas: IDs das áreas não respondidas ou vagas
        - padroes_repetidos: Temas recorrentes em áreas diferentes
        - ponto_entrada: Porta de intervenção predominante
        - palavras_recorrentes: Palavras mais frequentes
    """
    logger.info("Analisando contexto de %d respostas...", len(responses))
    
    # Consolidar todos os textos
    all_texts = []
    areas_respondidas = {}  # area_id -> lista de textos
    areas_com_resposta = set()
    
    for r in responses:
        av = r.get("answer_value") or {}
        text = av.get("text", "").strip()
        area = r.get("question_area", "Geral")
        
        # Mapear área para ID (1-12)
        try:
            area_id = AREAS.index(area) + 1 if area in AREAS else 0
        except ValueError:
            area_id = 0
        
        if area_id > 0:
            areas_com_resposta.add(area_id)
            if area_id not in areas_respondidas:
                areas_respondidas[area_id] = []
            if text:
                areas_respondidas[area_id].append(text)
        
        if text:
            all_texts.append(text)
    
    full_text = " ".join(all_texts).lower()
    
    # 1. DETECTAR MEMÓRIAS VERMELHAS
    memorias_vermelhas = _extract_memorias_vermelhas(responses)
    
    # 2. IDENTIFICAR BARREIRAS (AUTOSSABOTAGEM)
    barreiras = _identify_barreiras(full_text)
    
    # 3. IDENTIFICAR CAPITAL SIMBÓLICO (RECURSOS)
    capital_simbolico = _identify_capital_simbolico(all_texts)
    
    # 4. DETECTAR TOM EMOCIONAL DOMINANTE
    tom_emocional = _detect_tom_emocional(full_text)
    
    # 5. IDENTIFICAR ÁREAS CRÍTICAS
    areas_criticas = _identify_areas_criticas(areas_respondidas)
    
    # 6. DETECTAR ÁREAS SILENCIADAS
    areas_silenciadas = _identify_areas_silenciadas(areas_com_resposta)
    
    # 7. IDENTIFICAR PADRÕES REPETIDOS
    padroes_repetidos = _identify_padroes_repetidos(areas_respondidas)
    
    # 8. DETERMINAR PONTO DE ENTRADA
    ponto_entrada = _determine_ponto_entrada(full_text, memorias_vermelhas)
    
    # 9. EXTRAIR PALAVRAS RECORRENTES
    palavras_recorrentes = _extract_palavras_recorrentes(full_text)
    
    result = {
        "memorias_vermelhas": memorias_vermelhas,
        "barreiras_identificadas": barreiras,
        "capital_simbolico": capital_simbolico,
        "tom_emocional": tom_emocional,
        "areas_criticas": areas_criticas,
        "areas_silenciadas": areas_silenciadas,
        "padroes_repetidos": padroes_repetidos,
        "ponto_entrada": ponto_entrada,
        "palavras_recorrentes": palavras_recorrentes,
    }
    
    logger.info(
        "Análise concluída: %d memórias vermelhas, %d áreas críticas, tom=%s, ponto_entrada=%s",
        len(memorias_vermelhas),
        len(areas_criticas),
        tom_emocional,
        ponto_entrada,
    )
    
    return result


def _extract_memorias_vermelhas(responses: list[dict]) -> list[str]:
    """Extrai frases que revelam conflitos não dominados."""
    memorias = []
    
    for r in responses:
        av = r.get("answer_value") or {}
        text = av.get("text", "").strip()
        
        if not text:
            continue
        
        # Buscar frases que indicam conflito
        # Frases com "não consigo", "sempre", "nunca", "sinto que"
        patterns = [
            r"não consigo [^.!?]{10,}[.!?]",
            r"sempre [^.!?]{10,}[.!?]",
            r"nunca [^.!?]{10,}[.!?]",
            r"sinto que [^.!?]{10,}[.!?]",
            r"tenho medo [^.!?]{10,}[.!?]",
            r"me sinto [^.!?]{10,}[.!?]",
            r"parece que [^.!?]{10,}[.!?]",
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                frase = match.strip()
                if len(frase) > 20 and frase not in memorias:  # Evitar duplicatas
                    memorias.append(frase)
    
    return memorias[:10]  # Limitar a 10 mais importantes


def _identify_barreiras(text: str) -> list[str]:
    """Identifica padrões de autossabotagem."""
    barreiras = []
    
    for palavra in PALAVRAS_AUTOSSABOTAGEM:
        if palavra in text:
            barreiras.append(f"Padrão de linguagem: '{palavra}'")
    
    # Buscar padrões específicos
    if "não tenho tempo" in text:
        barreiras.append("Falta de priorização (não tenho tempo)")
    if "quando" in text and ("acalmar" in text or "melhor" in text):
        barreiras.append("Adiamento condicional (quando as coisas...)")
    if "sempre foi assim" in text or "minha família" in text:
        barreiras.append("Identidades Herdadas")
    
    return list(set(barreiras))  # Remover duplicatas


def _identify_capital_simbolico(texts: list[str]) -> list[str]:
    """Identifica recursos e forças do usuário."""
    capital = []
    
    # Palavras positivas que indicam recursos
    palavras_positivas = [
        "consigo",
        "capaz",
        "conquista",
        "orgulho",
        "realização",
        "aprendizado",
        "crescimento",
        "superação",
        "força",
    ]
    
    for text in texts:
        text_lower = text.lower()
        for palavra in palavras_positivas:
            if palavra in text_lower:
                # Extrair sentença que contém a palavra
                sentences = text.split(".")
                for sentence in sentences:
                    if palavra in sentence.lower() and sentence.strip():
                        capital.append(sentence.strip()[:100])  # Limitar tamanho
                        break
    
    return list(set(capital))[:5]  # Top 5 recursos


def _detect_tom_emocional(text: str) -> str:
    """Detecta o tom emocional dominante."""
    scores = {}
    
    for emocao, palavras in PALAVRAS_EMOCAO.items():
        count = sum(1 for palavra in palavras if palavra in text)
        scores[emocao] = count
    
    if not scores or max(scores.values()) == 0:
        return "neutro"
    
    return max(scores, key=scores.get)


def _identify_areas_criticas(areas_respondidas: dict[int, list[str]]) -> list[int]:
    """Identifica áreas com sinais de crise."""
    criticas = []
    
    for area_id, texts in areas_respondidas.items():
        combined = " ".join(texts).lower()
        
        # Verificar presença de palavras de crise
        crisis_score = 0
        for categoria, palavras in PALAVRAS_CRISE.items():
            if any(palavra in combined for palavra in palavras):
                crisis_score += 1
        
        # Verificar autossabotagem
        if any(palavra in combined for palavra in PALAVRAS_AUTOSSABOTAGEM):
            crisis_score += 1
        
        # Se score >= 2, considerar crítica
        if crisis_score >= 2:
            criticas.append(area_id)
    
    return criticas


def _identify_areas_silenciadas(areas_com_resposta: set[int]) -> list[int]:
    """Identifica áreas não respondidas ou respondidas vagamente."""
    todas_areas = set(range(1, 13))  # 1 a 12
    silenciadas = list(todas_areas - areas_com_resposta)
    return sorted(silenciadas)


def _identify_padroes_repetidos(areas_respondidas: dict[int, list[str]]) -> list[str]:
    """Identifica temas que aparecem em múltiplas áreas."""
    # Extrair palavras-chave de cada área
    area_keywords = {}
    for area_id, texts in areas_respondidas.items():
        combined = " ".join(texts).lower()
        # Extrair substantivos e verbos importantes (simplificado)
        words = re.findall(r'\b\w{5,}\b', combined)  # Palavras com 5+ letras
        area_keywords[area_id] = Counter(words).most_common(10)
    
    # Buscar palavras que aparecem em 2+ áreas
    palavra_areas = {}
    for area_id, keywords in area_keywords.items():
        for palavra, _ in keywords:
            if palavra not in palavra_areas:
                palavra_areas[palavra] = []
            palavra_areas[palavra].append(area_id)
    
    padroes = []
    for palavra, areas in palavra_areas.items():
        if len(areas) >= 2:
            areas_nomes = [AREAS[a-1] for a in areas if a <= len(AREAS)]
            padroes.append(f"'{palavra}' aparece em {', '.join(areas_nomes)}")
    
    return padroes[:5]  # Top 5 padrões


def _determine_ponto_entrada(text: str, memorias: list[str]) -> str:
    """Determina o Ponto de Entrada predominante."""
    scores = {
        "Emocional": 0,
        "Simbólico": 0,
        "Comportamental": 0,
        "Existencial": 0,
    }
    
    # Emocional: menciona sentimentos
    palavras_emocional = ["sinto", "emoção", "ansioso", "triste", "medo", "angústia"]
    scores["Emocional"] = sum(1 for p in palavras_emocional if p in text)
    
    # Simbólico: menciona valores, sentido, traição
    palavras_simbolico = ["sentido", "valor", "essência", "traído", "incoerente", "identidade"]
    scores["Simbólico"] = sum(1 for p in palavras_simbolico if p in text)
    
    # Comportamental: menciona hábitos, procrastinação, rotina
    palavras_comportamental = ["hábito", "rotina", "organizar", "adio", "procrastino", "disciplina"]
    scores["Comportamental"] = sum(1 for p in palavras_comportamental if p in text)
    
    # Existencial: menciona propósito, quem sou, perdido
    palavras_existencial = ["propósito", "quem sou", "perdido", "missão", "legado", "papel"]
    scores["Existencial"] = sum(1 for p in palavras_existencial if p in text)
    
    # Se todas as scores forem 0, analisar memórias vermelhas
    if max(scores.values()) == 0 and memorias:
        combined_memorias = " ".join(memorias).lower()
        if "sinto" in combined_memorias or "medo" in combined_memorias:
            return "Emocional"
        if "sentido" in combined_memorias or "valor" in combined_memorias:
            return "Simbólico"
    
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "Emocional"


def _extract_palavras_recorrentes(text: str) -> list[str]:
    """Extrai as palavras mais recorrentes (substantivos e verbos)."""
    # Remover stopwords comuns
    stopwords = {
        "que", "para", "com", "uma", "mais", "como", "não", "quando",
        "muito", "sobre", "mas", "também", "isso", "ela", "ele",
        "meu", "minha", "seu", "sua", "está", "sido", "ser", "ter",
    }
    
    # Extrair palavras (5+ letras)
    words = re.findall(r'\b\w{5,}\b', text)
    words = [w for w in words if w not in stopwords]
    
    # Contar frequência
    counter = Counter(words)
    
    return [palavra for palavra, _ in counter.most_common(10)]
