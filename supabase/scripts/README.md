# SQL manual do projeto NARA

Esta pasta contém scripts SQL de execução manual no **Supabase Dashboard > SQL Editor**.

- Para migrações versionadas, use `../migrations/`.
- Para scripts pontuais (não versionados no fluxo de migration), use os arquivos desta pasta.

## micro_diagnostics

- **Arquivo:** `create_micro_diagnostics.sql`
- **Uso:** Copie o conteúdo e cole no SQL Editor do Supabase; execute.
- **Nota:** Se a tabela `diagnostics` usar `id` como `BIGINT` em vez de `UUID`, edite no script a linha de `diagnostic_id` para usar `BIGINT` e a referência correta.
