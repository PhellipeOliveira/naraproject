# API V2 - Documentação Técnica Completa

> **Versão:** 2.0 (Base Metodológica NARA - Transformação Narrativa)  
> **Data:** Fevereiro 2026  
> **Autor:** Phellipe Oliveira

---

## 📋 Índice

1. [Visão Geral das Mudanças V2](#visão-geral-das-mudanças-v2)
2. [Vetor de Estado Qualitativo](#vetor-de-estado-qualitativo)
3. [Novos Campos do Resultado](#novos-campos-do-resultado)
4. [Schemas Completos](#schemas-completos)
5. [Exemplos de Payloads](#exemplos-de-payloads)
6. [Migração V1 → V2](#migração-v1--v2)
7. [Boas Práticas de Implementação](#boas-práticas-de-implementação)

---

## Visão Geral das Mudanças V2

### Filosofia da V2

A versão 2 da API representa uma **mudança paradigmática** no diagnóstico NARA, saindo de uma abordagem quantitativa (scores numéricos) para uma abordagem **qualitativa e narrativa** baseada na Base Metodológica.

### Principais Diferenças

| Aspecto | V1 (Legacy) | V2 (Atual) |
|---------|-------------|------------|
| **Resultado Principal** | `overall_score` (número 0-10) | `vetor_estado` (objeto qualitativo) |
| **Análise de Áreas** | Scores numéricos por área | Status qualitativo (crítico/atenção/estável/forte) |
| **Tipo de Perguntas** | Misto (escala + texto) | 100% narrativas (open_long/open_short) |
| **Identificação de Crise** | Áreas com score < 5 | Clusters operacionais M1 (6 tipos) |
| **Recomendações** | Genéricas por área | Âncoras Práticas específicas (19 tipos) |
| **Motor Motivacional** | Apenas nome | Score detalhado dos 4 motores |

### Retrocompatibilidade

**IMPORTANTE:** A API V2 **mantém campos legacy da V1** para garantir que frontends antigos continuem funcionando. Todos os campos V1 são calculados a partir dos dados V2.

---

## Vetor de Estado Qualitativo

### Conceito

O **Vetor de Estado** é o núcleo do diagnóstico V2. Ele substitui o `overall_score` numérico por um **snapshot multidimensional** do estado atual do usuário na jornada de transformação.

### Estrutura Completa

```typescript
interface VetorEstado {
  // === MOTORES MOTIVACIONAIS (O QUE MOVE) ===
  motor_dominante: "Necessidade" | "Valor" | "Desejo" | "Propósito";
  motor_secundario: "Necessidade" | "Valor" | "Desejo" | "Propósito";
  
  // === JORNADA (ONDE ESTÁ) ===
  estagio_jornada: "Germinar" | "Enraizar" | "Desenvolver" | "Florescer" | "Frutificar" | "Realizar";
  
  // === CRISES (O QUE BLOQUEIA) ===
  crise_raiz: "Identidade Raiz" | "Sentido e Direção" | "Execução e Estrutura" | 
              "Conexão e Expressão" | "Incongruência Identidade-Cultura" | 
              "Transformação de Personagem";
  crises_derivadas: string[];  // Crises secundárias relacionadas
  
  // === INTERVENÇÃO (COMO AGIR) ===
  ponto_entrada_ideal: "Emocional" | "Simbólico" | "Comportamental" | "Existencial";
  dominios_alavanca: string[];  // Ex: ["D1", "D2"] - Domínios Temáticos prioritários
  
  // === CONTEXTO (COMO ESTÁ) ===
  tom_emocional: string;  // Ex: "frustração e confusão", "esperança e determinação"
  risco_principal: string;  // Descrição do principal risco identificado
  necessidade_atual: string;  // O que o usuário precisa fazer agora
}
```

### Descrição Detalhada dos Campos

#### 1. `motor_dominante` e `motor_secundario`

**O que são:** Os 4 Motores Motivacionais da Base Metodológica.

| Motor | Descrição | Quando aparece |
|-------|-----------|----------------|
| **Necessidade** | Afastar-se da dor, alívio de sofrimento interno | Usuário relata cansaço, esgotamento, "não aguento mais" |
| **Valor** | Coerência com princípios, integridade | Usuário menciona traição de valores, incongruência moral |
| **Desejo** | Conquista, realização, reconhecimento | Usuário fala de sonhos, metas, "quero alcançar" |
| **Propósito** | Legado, impacto, contribuição | Usuário busca sentido maior, "fazer diferença" |

**Como usar no frontend:**
- Exiba o motor dominante em destaque (card principal)
- Use cores diferentes para cada motor
- Mostre o score detalhado em `motors_scores` (0-10) na análise intermediária

#### 2. `estagio_jornada`

**O que é:** A fase atual do usuário na jornada de transformação (6 estágios).

| Estágio | Descrição | Características |
|---------|-----------|----------------|
| **Germinar** | Início do despertar | Questionamento inicial, desconforto |
| **Enraizar** | Busca de fundamentos | Revisão de crenças, valores |
| **Desenvolver** | Construção ativa | Testando novas identidades |
| **Florescer** | Expressão autêntica | Vivendo a nova narrativa |
| **Frutificar** | Resultados tangíveis | Colhendo frutos da mudança |
| **Realizar** | Plenitude e maestria | Domínio da nova identidade |

**Como usar no frontend:**
- Exiba como progressão visual (timeline)
- Use metáforas da natureza (ícones de planta crescendo)
- Mostre próximo estágio como motivação

#### 3. `crise_raiz` e `crises_derivadas`

**O que são:** Os 6 Clusters Operacionais de Crise (M1 - Estado de Conflito).

| Cluster | Descrição | Sinais |
|---------|-----------|--------|
| **Identidade Raiz** | Crise de "quem eu sou" | Identidades herdadas, vergonha, autoimagem desatualizada |
| **Sentido e Direção** | Crise de "para onde vou" | Vazio existencial, falta de visão, fragmentação |
| **Execução e Estrutura** | Crise de "como faço" | Paralisia decisória, ausência de ritos, desorganização |
| **Conexão e Expressão** | Crise de "como me relaciono" | Invisibilidade simbólica, solidão existencial |
| **Incongruência Identidade-Cultura** | Crise de "não pertenço" | Choque ambiental, desajuste sistêmico |
| **Transformação de Personagem** | Crise de "medo de mudar" | Apego a papéis obsoletos, medo de crescer |

**Como usar no frontend:**
- Destaque a crise raiz em vermelho/destrutivo
- Liste crises derivadas como "também presente"
- Mostre áreas impactadas por cada cluster

#### 4. `ponto_entrada_ideal`

**O que é:** A "porta" mais efetiva para iniciar a intervenção.

| Ponto de Entrada | Quando usar | Estratégia |
|------------------|-------------|------------|
| **Emocional** | Usuário relata estados afetivos intensos | Validar emoções, regular antes de agir |
| **Simbólico** | Falta de sentido ou traição de valores | Ressignificar narrativa, reescrever história |
| **Comportamental** | Foco em hábitos e procrastinação | Protocolos práticos, âncoras de ação |
| **Existencial** | Crise de papel de vida | Reposicionar missão, redefinir identidade |

**Como usar no frontend:**
- Exiba como primeiro passo do plano de ação
- Use ícones que representem cada porta (coração, estrela, ação, pensamento)

#### 5. `dominios_alavanca`

**O que são:** Os Domínios Temáticos prioritários (D1-D6).

| Domínio | Descrição |
|---------|-----------|
| **D1** | Motivações e Conflitos |
| **D2** | Crenças, Valores e Princípios |
| **D3** | Evolução e Desenvolvimento |
| **D4** | Congruência Identidade-Cultura |
| **D5** | Transformação de Identidade |
| **D6** | Papel na Sociedade |

**Como usar no frontend:**
- Mostre como "alavancas de mudança"
- Relacione com as áreas do círculo narrativo

#### 6. `tom_emocional`

**O que é:** Análise do estado afetivo predominante nas respostas.

**Exemplos:**
- "frustração e confusão"
- "esperança misturada com medo"
- "determinação nascente"
- "apatia e resignação"

**Como usar no frontend:**
- Exiba de forma empática no sumário executivo
- Use para contextualizar recomendações

#### 7. `risco_principal`

**O que é:** O principal risco identificado se nada for feito.

**Exemplos:**
- "Burnout por esgotamento do papel atual"
- "Paralisia decisória que impede qualquer ação"
- "Isolamento social progressivo"

**Como usar no frontend:**
- Destaque em banner de atenção (não alarmista)
- Use tom de urgência compassiva

#### 8. `necessidade_atual`

**O que é:** A ação mais importante agora (frase direta e prática).

**Exemplos:**
- "Criar espaços de descompressão diária para evitar colapso"
- "Iniciar conversa honesta sobre expectativas herdadas"
- "Definir um projeto pequeno que expresse a nova identidade"

**Como usar no frontend:**
- Destaque como call-to-action principal
- Torne clicável para expandir detalhes

---

## Novos Campos do Resultado

### `memorias_vermelhas`

**O que são:** Frases literais do usuário que revelam conflitos não dominados (M1).

**Tipo:** `string[]`

**Exemplos:**
```json
{
  "memorias_vermelhas": [
    "Não aguento mais viver essa vida que não é minha",
    "Sempre penso que não sou bom o suficiente",
    "Sinto que estou fingindo ser alguém que não sou"
  ]
}
```

**Como usar no frontend:**
- Exiba como citações destacadas (border-left vermelho)
- Use aspas e estilo itálico
- Background destructive/5 (vermelho suave)
- Máximo 5-7 memórias (as mais significativas)

**Propósito:**
- Confrontar o usuário com suas próprias palavras
- Criar momento de tomada de consciência
- Validar que a IA realmente "ouviu" o que foi dito

---

### `ancoras_sugeridas`

**O que são:** Das 19 Âncoras Práticas da Base Metodológica, as 3-5 mais relevantes para este usuário.

**Tipo:** `string[]`

**19 Âncoras Possíveis:**

#### Ambiente e Contexto
1. **Referências** - Pessoas/histórias que inspiram a nova identidade
2. **Objetos** - Itens simbólicos da nova narrativa
3. **Ambientes** - Espaços físicos que reforçam mudança
4. **Grupo** - Comunidade que valida a transformação

#### Comunicação e Expressão
5. **Tom** - Como falar (assertivo, compassivo, autoritário)
6. **Vocabulário** - Palavras da nova identidade
7. **Postura** - Linguagem corporal assumida
8. **Vestimenta** - Visual que expressa transformação

#### Rotina e Estrutura
9. **Rituais Matinais** - Protocolo de início do dia
10. **Rituais Noturnos** - Protocolo de encerramento
11. **Limites** - Não-negociáveis da nova identidade
12. **Marcos** - Celebrações de microvitórias

#### Emoção e Energia
13. **Emoção Projetada** - Estado afetivo intencional
14. **Gestão de Energia** - Preservação da volição
15. **Práticas de Recarga** - Rituais de recuperação

#### Ação e Entrega
16. **Tarefas Identitárias** - Ações que definem quem você é
17. **Microentregas** - Pequenas vitórias consistentes
18. **Exposição Gradual** - Testes progressivos da nova identidade
19. **Testemunhas** - Pessoas que testemunham a mudança

**Exemplo de resposta:**
```json
{
  "ancoras_sugeridas": [
    "Rituais Matinais",
    "Gestão de Energia",
    "Limites",
    "Testemunhas",
    "Vocabulário"
  ]
}
```

**Como usar no frontend:**
- Lista numerada com ícones
- Cards clicáveis que expandem detalhes
- Checkbox para usuário marcar "implementadas"
- Link para guia detalhado de cada âncora

---

### `areas_silenciadas`

**O que são:** IDs das áreas (1-12) que o usuário evitou responder ou respondeu de forma vaga.

**Tipo:** `number[]`

**Mapeamento das Áreas:**
```
1  = Saúde Física
2  = Saúde Mental
3  = Saúde Espiritual
4  = Vida Pessoal
5  = Vida Amorosa
6  = Vida Familiar
7  = Vida Social
8  = Vida Profissional
9  = Finanças
10 = Educação
11 = Inovação
12 = Lazer
```

**Exemplo:**
```json
{
  "areas_silenciadas": [5, 6],  // Vida Amorosa e Familiar
}
```

**Como usar no frontend:**
- Mostre como "Áreas não exploradas"
- Ofereça botão para "Aprofundar nesta área"
- Use tom de curiosidade, não julgamento
- Explique que silêncios revelam bloqueios

**Propósito:**
- Revelar padrões de esquiva
- Identificar tabus pessoais
- Sugerir áreas para exploração futura

---

## Schemas Completos

### POST `/api/v1/diagnostic/start`

**Request:**
```typescript
interface StartDiagnosticRequest {
  email: string;
  full_name?: string;
  consent_privacy: boolean;
  consent_marketing?: boolean;
}
```

**Response:**
```typescript
interface StartDiagnosticResponse {
  diagnostic_id: string;
  status: "in_progress";
  phase: 1;
  questions: Question[];
  total_questions: 15;
  result_token: string;
}

interface Question {
  id: number;
  area: string;  // Ex: "Vida Pessoal", "Saúde Mental"
  type: "open_long" | "open_short";
  text: string;
  follow_up_hint?: string;  // V2: Contexto adicional
}
```

---

### POST `/api/v1/diagnostic/{diagnostic_id}/answer`

**Request:**
```typescript
interface SubmitAnswerRequest {
  question_id: number;
  question_text: string;
  question_area: string;
  answer_text: string;  // V2: Campo obrigatório (perguntas 100% narrativas)
  response_time_seconds?: number;
}
```

**Response:**
```typescript
interface SubmitAnswerResponse {
  status: "in_progress" | "eligible";
  can_finish: boolean;
  phase_complete: boolean;
  progress: {
    overall: number;      // 0-100
    questions: number;    // % de perguntas respondidas
    words: number;        // % de palavras (meta: 3500)
    coverage: number;     // % de áreas cobertas (12)
  };
  total_answers: number;
  total_words: number;
  areas_covered: number;
}
```

---

### POST `/api/v1/diagnostic/{diagnostic_id}/finish`

**Response V2 (Completo):**
```typescript
interface DiagnosticResultResponse {
  // === CAMPOS V2 (PRINCIPAIS) ===
  vetor_estado: VetorEstado;
  memorias_vermelhas: string[];
  areas_silenciadas: number[];
  ancoras_sugeridas: string[];
  
  // === ANÁLISE DETALHADA ===
  executive_summary: string;
  area_analysis: AreaAnalysis[];
  patterns: {
    correlations?: string[];
    contradictions?: string[];
    self_sabotage_cycles?: string[];
  };
  strengths: string[];
  development_areas: DevelopmentArea[];
  recommendations: Recommendation[];
  
  // === CAMPOS LEGACY V1 (mantidos por compatibilidade) ===
  overall_score?: number;  // Calculado a partir do vetor_estado
  phase_identified: string;
  motor_dominante: string;
  motor_secundario?: string;
  crise_raiz: string;
  ponto_entrada_ideal: string;
}

interface AreaAnalysis {
  area_name: string;
  area_id: number;
  status: "crítico" | "atenção" | "estável" | "forte";
  analysis: string;
  key_insight: string;
}

interface DevelopmentArea {
  area_name: string;
  priority: "alta" | "média" | "baixa";
  reasoning: string;
}

interface Recommendation {
  action: string;
  timeframe: "imediato" | "curto_prazo" | "medio_prazo";
  area_related?: string;
  ancor_type?: string;  // V2: Referência a uma das 19 âncoras
}
```

---

## Exemplos de Payloads

### Exemplo 1: Usuário em Crise de Identidade Raiz

**Respostas típicas:**
- "Não sei mais quem eu sou de verdade"
- "Sempre fiz o que os outros esperavam de mim"
- "Carrego crenças da minha família que me sufocam"

**Resultado V2:**
```json
{
  "vetor_estado": {
    "motor_dominante": "Necessidade",
    "motor_secundario": "Valor",
    "estagio_jornada": "Germinar",
    "crise_raiz": "Identidade Raiz",
    "crises_derivadas": [
      "Incongruência Identidade-Cultura",
      "Transformação de Personagem"
    ],
    "ponto_entrada_ideal": "Existencial",
    "dominios_alavanca": ["D1", "D5"],
    "tom_emocional": "confusão misturada com frustração crescente",
    "risco_principal": "Colapso identitário por sustentação prolongada de papel inautêntico",
    "necessidade_atual": "Criar espaço de experimentação segura para testar nova identidade"
  },
  "memorias_vermelhas": [
    "Não sei mais quem eu sou de verdade",
    "Sempre fiz o que os outros esperavam de mim",
    "Carrego crenças da minha família que me sufocam"
  ],
  "areas_silenciadas": [4, 5],
  "ancoras_sugeridas": [
    "Referências",
    "Limites",
    "Vocabulário",
    "Testemunhas",
    "Rituais Matinais"
  ],
  "executive_summary": "Você está no início de um despertar profundo (Germinar), movido pela necessidade urgente de alívio do desconforto de viver uma vida que não é sua. A crise central é de Identidade Raiz: você carrega papéis e crenças herdadas que não escolheu conscientemente. Suas palavras revelam o peso de expectativas externas que sufocam sua essência. O caminho exige coragem para questionar 'quem eu sou quando ninguém está olhando' e criar espaços seguros de experimentação da nova identidade."
}
```

---

### Exemplo 2: Usuário em Crise de Sentido e Direção

**Respostas típicas:**
- "Perdi o sentido do que faço"
- "Não vejo mais para onde estou indo"
- "Tudo virou obrigação, nada tem propósito"

**Resultado V2:**
```json
{
  "vetor_estado": {
    "motor_dominante": "Propósito",
    "motor_secundario": "Desejo",
    "estagio_jornada": "Enraizar",
    "crise_raiz": "Sentido e Direção",
    "crises_derivadas": [
      "Execução e Estrutura"
    ],
    "ponto_entrada_ideal": "Simbólico",
    "dominios_alavanca": ["D2", "D6"],
    "tom_emocional": "vazio existencial misturado com busca ativa de significado",
    "risco_principal": "Fragmentação identitária por falta de narrativa coerente",
    "necessidade_atual": "Ressignificar o trabalho atual conectando-o a um propósito maior"
  },
  "memorias_vermelhas": [
    "Perdi o sentido do que faço",
    "Não vejo mais para onde estou indo",
    "Tudo virou obrigação, nada tem propósito"
  ],
  "areas_silenciadas": [3, 11],
  "ancoras_sugeridas": [
    "Referências",
    "Tarefas Identitárias",
    "Marcos",
    "Vocabulário",
    "Emoção Projetada"
  ]
}
```

---

## Migração V1 → V2

### Checklist de Migração

#### Backend
- [x] Criar `app/rag/analyzer.py` com análise contextual
- [x] Atualizar `app/rag/generator.py` com prompts V2
- [x] Integrar analyzer no pipeline de finalização
- [x] Adicionar campos V2 no schema de `diagnostic_results`
- [x] Manter campos V1 por retrocompatibilidade

#### Frontend
- [x] Adicionar interface `VetorEstado` em types
- [x] Atualizar `DiagnosticResultResponse` com campos V2
- [x] Redesenhar página de resultado com seções V2
- [x] Remover componentes de escala (perguntas 100% narrativas)
- [ ] Adicionar componentes visuais avançados (opcional)

### Estratégia de Transição

1. **Fase 1 (Concluída):** Backend gera ambos os formatos (V1 + V2)
2. **Fase 2 (Atual):** Frontend lê V2 mas suporta V1
3. **Fase 3 (Futuro):** Deprecar campos V1 após 6 meses

---

## Boas Práticas de Implementação

### Frontend

#### 1. **Detecção de Versão**
```typescript
function isV2Result(result: DiagnosticResultResponse): boolean {
  return result.vetor_estado !== undefined;
}
```

#### 2. **Fallback Gracioso**
```typescript
const motorDominante = data.vetor_estado?.motor_dominante 
  || data.motor_dominante  // fallback V1
  || "Não identificado";
```

#### 3. **Renderização Condicional**
```tsx
{data.vetor_estado ? (
  <VetorEstadoCard vetor={data.vetor_estado} />
) : (
  <LegacyScoreDisplay score={data.overall_score} />
)}
```

### Backend

#### 1. **Validação de Dados**
```python
from pydantic import BaseModel, validator

class VetorEstadoSchema(BaseModel):
    motor_dominante: str
    
    @validator('motor_dominante')
    def validate_motor(cls, v):
        valid = ["Necessidade", "Valor", "Desejo", "Propósito"]
        if v not in valid:
            raise ValueError(f"Motor inválido: {v}")
        return v
```

#### 2. **Logging Estruturado**
```python
logger.info(
    "Diagnóstico finalizado",
    extra={
        "diagnostic_id": diagnostic_id,
        "motor_dominante": vetor.motor_dominante,
        "crise_raiz": vetor.crise_raiz,
        "num_memorias": len(memorias_vermelhas)
    }
)
```

#### 3. **Testes de Regressão**
```python
def test_resultado_v2_tem_todos_campos_obrigatorios():
    result = await finish_diagnostic(diagnostic_id)
    assert "vetor_estado" in result
    assert "memorias_vermelhas" in result
    assert "ancoras_sugeridas" in result
```

---

## Referências

- [01_BASE_METODOLOGICA_NARA.md](../documentos/01_BASE_METODOLOGICA_NARA.md) - Base conceitual completa
- [04_BACKEND_API.md](../documentos/04_BACKEND_API.md) - Implementação backend
- [05_FRONTEND_UX.md](../documentos/05_FRONTEND_UX.md) - Implementação frontend

---

**Última atualização:** Fevereiro 2026  
**Autor:** Phellipe Oliveira  
**Versão do documento:** 1.0
