# NARA Backend

API FastAPI do diagnóstico narrativo NARA.

## Requisitos

- **Python 3.11 ou 3.12** (não use 3.14: Pydantic/pydantic-core falha ao compilar no 3.14)

## Setup

```bash
# 1. Garantir Python 3.12 (macOS: brew install python@3.12)
python3.12 --version   # deve ser 3.12.x

# 2. Criar venv com 3.12 (não use só "python3" se for 3.14)
python3.12 -m venv .venv
source .venv/bin/activate   # no Windows: .venv\Scripts\activate

# 3. Instalar dependências e rodar testes
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edite .env com SUPABASE_URL, SUPABASE_SERVICE_KEY e OPENAI_API_KEY
python -m pytest --tb=short -q
```

**Se `pip install` falhar com erro em `pydantic-core`:** você está usando Python 3.14. Remova o venv (`rm -rf venv` ou `rm -rf .venv`), instale Python 3.12 (`brew install python@3.12`) e crie o venv de novo com `python3.12 -m venv .venv`.

## Rodar

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
# ou: python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs (se DEBUG=true)

## RAG (perguntas adaptativas e relatório)

A geração de perguntas da **fase 2+** e o relatório final usam chunks em `knowledge_chunks` (pgvector).

**Para funcionar:**
1. Migrações aplicadas (incluindo `match_knowledge_chunks` em `supabase/migrations/20260213000003_nara_rpc.sql`).
2. Tabela populada e com embeddings:
   - **Seed mínimo:** `python -m scripts.seed_knowledge_chunks`
   - **Documentos completos (docs-rag + 01_FUNDAMENTOS):** `python -m scripts.ingest_docs_rag`  
     Lê a pasta `docs-rag/` na raiz do repositório e, opcionalmente, `documentos/01_FUNDAMENTOS.md` como guia. Gera chunks por seções markdown, embeddings e insere em `knowledge_chunks`. Ver `documentos/01_FUNDAMENTOS.md` § 3 (Estrutura do Chunk para RAG).
3. Índice vetorial: migration `20260213000005_nara_chunks_vector_index.sql` (cria ivfflat quando houver dados).

**Como conferir:** Ao concluir as 15 perguntas da fase 1 e pedir as próximas, o backend chama `retrieve_for_question_generation` → RPC `match_knowledge_chunks`. Nos logs deve aparecer `RAG retrieved N chunks`. Se aparecer `RAG context empty`, não há chunks com embedding ou o threshold de similaridade não está sendo atingido.

**Versões de chunks (v1 vs v2):** Se você apagou chunks antigos e recriou apenas a base metodológica refinada, o código usa **version=2** por padrão. Detalhes em [docs/SUPABASE_CHUNKS_E_VERSOES.md](docs/SUPABASE_CHUNKS_E_VERSOES.md).
