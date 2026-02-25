# Supabase: Chunks e RAG

Este doc descreve a arquitetura atual dos chunks de conhecimento e como gerenciá-los.

---

## Tabela e RPC

| Nome | Uso |
|------|-----|
| **`knowledge_chunks`** | Tabela no Supabase com o conteúdo + embedding de cada chunk. |
| **`match_knowledge_chunks`** | Função RPC (pgvector) que busca chunks por similaridade semântica. |

As migrations (criação da tabela, coluna `embedding`, RPC, índice vetorial) são aplicadas diretamente no Supabase via editor SQL.

---

## Princípio atual: uma versão ativa, sem filtro no retriever

O banco deve conter apenas os chunks da **versão ativa**. Quando os chunks são recriados (novo conteúdo, novo seed), os antigos devem ser apagados antes de inserir os novos.

Não há mais filtragem de versão no retriever — todos os chunks presentes e ativos (`is_active = true`) são consultados. Isso simplifica o código e elimina o risco de receber "0 chunks" por filtro desalinhado.

---

## Versão ativa: `RAG_CHUNK_VERSION` em `config.py`

```python
# app/config.py
RAG_CHUNK_VERSION: int = 2      # altere aqui ao migrar para novos chunks
RAG_CHUNK_STRATEGY: str = "semantic"  # estratégia do seed ativo
```

Esses valores são usados por:
- **`scripts/seed_knowledge_chunks.py`** — grava `version` e `chunk_strategy` no metadata.
- **`app/rag/ingest.py` — `chunks_to_knowledge_rows()`** — usa `settings.RAG_CHUNK_VERSION`.

---

## Como popular o banco

### Opção 1 — Seed da base metodológica (dados hardcoded)

```bash
cd nara-backend
python -m scripts.seed_knowledge_chunks
```

Insere os chunks de `scripts/seed_knowledge_chunks_data_v2.py` com embeddings gerados via OpenAI.

### Opção 2 — Ingestão de arquivos `.md` (pasta `docs-rag/`)

```bash
cd nara-backend
python -m scripts.ingest_docs_rag
# flags úteis:
#   --strategy semantic   (padrão: size)
#   --dry-run             (conta chunks sem inserir)
#   --no-fundamentos      (pula 01_FUNDAMENTOS.md)
```

Ambos os scripts respeitam `RAG_CHUNK_VERSION` de `config.py`.

---

## Colunas relevantes da tabela

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `content` | text | Texto do chunk |
| `embedding` | vector | Embedding OpenAI |
| `chapter` | text | Área (ex.: "Saúde Física") |
| `section` | text | Subseção do documento |
| `version` | int | Versão do chunk (= `RAG_CHUNK_VERSION`) |
| `is_active` | bool | `true` para chunks em uso |
| `metadata` | jsonb | `chunk_strategy`, `source`, etc. |
| `motor_motivacional` | text[] | Motores associados |
| `estagio_jornada` | text[] | Estágios associados |
| `tipo_crise` | text[] | Tipos de crise associados |

---

## Rotação de chunks (apagar e recriar)

Ao atualizar o conteúdo da base de conhecimento:

1. No Supabase, apague os chunks antigos:
   ```sql
   DELETE FROM knowledge_chunks WHERE is_active = true;
   ```
2. Atualize `RAG_CHUNK_VERSION` em `config.py` se necessário.
3. Execute o script de seed adequado.

Não é necessário alterar nenhum código do retriever ou da pipeline.

---

## Verificar chunks no banco

```bash
python -m scripts.check_knowledge_chunks
```

Ou pelo health check detalhado da API: `GET /health/detailed` → campo `knowledge_base`.
