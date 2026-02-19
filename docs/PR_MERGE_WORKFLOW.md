# Guia de PR e Merge (Solo Dev)

Este guia padroniza como trabalhar com as branches `main`, `dev` e `plan`.

## Objetivo
- Evitar quebra em producao.
- Garantir que CI rode antes de merge.
- Manter historico claro e rollback simples.

## Estrategia de branches
- `main`: producao (somente codigo validado).
- `dev`: integracao continua (base do trabalho diario).
- `plan`: experimentos/planejamento (sem deploy direto).

## Fluxo recomendado
1. Atualizar `dev`.
2. Criar branch de feature a partir de `dev`.
3. Implementar mudancas.
4. Rodar validacoes locais.
5. Abrir PR para `dev`.
6. Aguardar CI (`Backend CI` e `Frontend CI`).
7. Merge para `dev`.
8. Em janela de release, abrir PR `dev -> main`.
9. Validar smoke tests e merge para `main`.

## Comandos (repositorio local)

### 1) Sincronizar base
```bash
git checkout dev
git pull origin dev
```

### 2) Criar branch de trabalho
```bash
git checkout -b feat/nome-da-mudanca
```

### 3) Verificar alteracoes
```bash
git status
```

### 4) Adicionar e commitar
```bash
git add .
git commit -m "feat: descricao curta da mudanca"
```

### 5) Enviar branch para remoto
```bash
git push -u origin feat/nome-da-mudanca
```

### 6) Após merge, limpar local
```bash
git checkout dev
git pull origin dev
git branch -d feat/nome-da-mudanca
```

## O que fazer no GitHub (manual)

### Abrir PR
- Base: `dev`
- Compare: sua branch `feat/...`
- Preencher template de PR.

### Validar CI
- `Backend CI` deve ficar verde.
- `Frontend CI` deve ficar verde.

### Merge
- Se checks verdes, merge no PR.
- Preferir `Squash and merge` para historico limpo.

### Release para producao
- Abrir PR `dev -> main`.
- Rodar checklist de smoke test.
- Fazer merge somente com checks verdes.

## Definition of Done (antes de merge)
- [ ] Escopo fechado e objetivo entregue.
- [ ] Backend CI e Frontend CI verdes.
- [ ] Sem segredos no commit (`.env` nao versionado).
- [ ] Fluxo principal afetado testado manualmente.
- [ ] Health check OK (`/health`).
- [ ] Rollback simples definido.

## Checklist de validacao local (rapido)

### Backend
```bash
cd nara-backend
source ../.venv/bin/activate
pytest tests/unit -q
```

### Frontend
```bash
cd nara-frontend
npm run build
npm run test -- --run --passWithNoTests
```

## Branch protection (recomendado)
No GitHub:
1. Settings -> Branches -> Add rule.
2. Branch pattern: `main` (e opcionalmente `dev`).
3. Marcar:
   - Require a pull request before merging
   - Require status checks to pass before merging
4. Selecionar checks:
   - `Backend CI`
   - `Frontend CI`

## Observacoes
- CI verde reduz risco, mas nao substitui smoke test.
- Se expor token/chave acidentalmente, rotacione imediatamente.
- Para mudanca critica (auth, banco, deploy), sempre usar PR.
