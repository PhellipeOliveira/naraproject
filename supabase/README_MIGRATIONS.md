# Aplicar migrações no Supabase

As tabelas do NARA (`diagnostics`, `answers`, etc.) precisam existir no seu projeto Supabase. Rode os SQL **na ordem** abaixo.

## Estrutura de SQL no repositório

- `migrations/`: migrações versionadas para fluxo `supabase db push`.
- `scripts/`: scripts manuais (uso pontual no SQL Editor).

## Opção 1: Supabase Dashboard (SQL Editor)

1. Acesse [Supabase Dashboard](https://supabase.com/dashboard) → seu projeto.
2. Menu lateral: **SQL Editor** → **New query**.
3. Para cada arquivo em `migrations/`, na ordem:
   - Abra o arquivo no seu editor.
   - Copie **todo** o conteúdo.
   - Cole no SQL Editor do Supabase.
   - Clique em **Run** (ou Cmd+Enter).

**Ordem dos arquivos:**
1. `20260213000001_nara_extensions.sql`
2. `20260213000002_nara_tables.sql`
3. `20260213000003_nara_rpc.sql`
4. `20260213000004_nara_rls.sql`
5. `20260213000005_nara_chunks_vector_index.sql` (só depois de ter dados em `knowledge_chunks`, ou pule no início)
6. `20260213000006_nara_views_metrics.sql`

## Opção 2: Supabase CLI

Se tiver o [Supabase CLI](https://supabase.com/docs/guides/cli) instalado e o projeto linkado:

```bash
cd /Users/phellipeoliveira/Documents/NARA_CURSOR
supabase db push
```

---

Depois de aplicar **pelo menos 1, 2, 3 e 4**, o backend conseguirá criar diagnósticos. A migration 5 (índice vetorial) pode ser rodada depois de popular `knowledge_chunks` com o script `python -m scripts.seed_knowledge_chunks`.

## Scripts manuais

Os arquivos em `scripts/` não entram automaticamente no fluxo de migrations do Supabase CLI.

Quando necessário, execute no SQL Editor do Supabase, por exemplo:

- `scripts/create_micro_diagnostics.sql`
- `scripts/20260224_add_source_to_knowledge_chunks.sql`
