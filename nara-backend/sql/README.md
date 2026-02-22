# SQL do projeto NARA

Scripts aqui devem ser executados manualmente no **Supabase Dashboard > SQL Editor**, a menos que você configure o Supabase CLI e migrations.

## micro_diagnostics

- **Arquivo:** `create_micro_diagnostics.sql`
- **Uso:** Copie o conteúdo e cole no SQL Editor do Supabase; execute.
- **Nota:** Se a tabela `diagnostics` usar `id` como `BIGINT` em vez de `UUID`, edite no script a linha de `diagnostic_id` para usar `BIGINT` e a referência correta.
