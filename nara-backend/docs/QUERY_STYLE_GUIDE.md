# Query Style Guide (RAG Coverage)

Este guia define o contrato para escrever queries no arquivo `nara-backend/scripts/rag_coverage_topics.json`.

## Contrato obrigatório

- `queries` deve continuar como `string[]`.
- Cada query deve ser atômica:
  - 1 intenção principal
  - 1 conceito central
  - combinação curta (heurística: 2 a 7 tokens úteis)
- Evitar listas de vários conceitos na mesma linha.

Exemplo ruim:

- `pontos de entrada emocional simbólico comportamental existencial`

Exemplo bom:

- `pontos de entrada`
- `pontos de entrada Emocional`
- `pontos de entrada Simbólico`
- `pontos de entrada Comportamental`
- `pontos de entrada Existencial`

## Taxonomia mínima

Use os três tipos abaixo para manter consistência:

- **Tópico**: query guarda-chuva de recall amplo.
  - Ex.: `pontos de entrada`
- **Tópico + conceito**: foco semântico por conceito.
  - Ex.: `pontos de entrada Emocional`
- **Técnica/Ação**: valida procedimento específico.
  - Ex.: `porta emocional validar regular emoção`

## Regra de atomização

- Se uma query tiver 2 ou mais itens do `concepts[]` do mesmo grupo, ela é considerada condensada.
- Queries condensadas devem ser desdobradas em:
  - 1 query guarda-chuva do tópico
  - 1 query por conceito detectado

## Regra de expansão por grupo

- Para grupos com `N` conceitos, buscar no mínimo `N + 1` queries:
  - 1 guarda-chuva
  - `N` atômicas de conceito
- Exceções são permitidas quando o corpus ainda não contém evidência textual para todos os conceitos.

## Regras de qualidade

- Evitar queries maiores que 10 tokens (heurística de legibilidade).
- Evitar duplicações semânticas dentro do mesmo grupo.
- Manter ordenação estável para diffs limpos:
  - guarda-chuva
  - tópico+conceito
  - técnica/ação

## Governança e não-regressão

- Rodar `python -m scripts.lint_queries` antes de abrir PR.
- Se necessário, rodar `python -m scripts.fix_queries --dry-run` para revisar sugestões.
- Aplicar somente após revisão: `python -m scripts.fix_queries --apply`.
- Medir impacto com:
  - `python -m scripts.coverage_report_rag --output ../docs/RAG_COVERAGE_REPORT_AFTER.md`
- Comparar com baseline e validar:
  - evolução de cobertura por grupo
  - ausência de regressões críticas (`gaps` em grupos prioritários)
