# NARA Backend

API FastAPI do diagnóstico narrativo NARA.

## Requisitos

- **Python 3.11 ou 3.12** (não use 3.14: Pydantic ainda não tem suporte e a instalação falha)

## Setup

```bash
# Usar Python 3.11 ou 3.12 (instale com Homebrew se necessário: brew install python@3.12)
python3.12 -m venv .venv
source .venv/bin/activate   # no Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edite .env com SUPABASE_URL, SUPABASE_SERVICE_KEY e OPENAI_API_KEY
```

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
2. Tabela populada e com embeddings: `python -m scripts.seed_knowledge_chunks` (a partir da raiz do backend, com `.env` configurado).
3. Índice vetorial: migration `20260213000005_nara_chunks_vector_index.sql` (cria ivfflat quando houver dados).

**Como conferir:** Ao concluir as 15 perguntas da fase 1 e pedir as próximas, o backend chama `retrieve_for_question_generation` → RPC `match_knowledge_chunks`. Nos logs deve aparecer `RAG retrieved N chunks`. Se aparecer `RAG context empty`, não há chunks com embedding ou o threshold de similaridade não está sendo atingido.
