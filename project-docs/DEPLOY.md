# NARA Fase 1 – Deploy e Qualidade

## Backend (Railway / Render)

Guia detalhado: **nara-backend/docs/BACKEND_DEPLOY.md**.

1. **Container:** usar o `Dockerfile` em `nara-backend/`.
2. **Variáveis de ambiente:** definir no painel (ou `.env` em produção):
   - `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`
   - `OPENAI_API_KEY`
   - `RESEND_API_KEY`, `EMAIL_FROM`
   - `APP_NAME`, `ENV=production`, `DEBUG=false`
   - `FRONTEND_URL` (ex.: `https://nara.vercel.app`)
   - `MIN_QUESTIONS_TO_FINISH`, `MIN_WORDS_TO_FINISH`, `MIN_AREAS_COVERED`
   - `CORS_ORIGINS` (ex.: `https://nara.vercel.app`)
3. **Health checks:** usar `/health` (simples) ou `/health/detailed` (com DB).
4. **Comando:** `uvicorn app.main:app --host 0.0.0.0 --port 8000` (já no Dockerfile).

## Frontend (Vercel)

Guia detalhado: **nara-frontend/VERCEL_DEPLOY.md**.

Resumo:
1. **Build:** `npm run build` (saída em `dist/`). A Vercel usa isso automaticamente se Root Directory = `nara-frontend`.
2. **Variável obrigatória:** `VITE_API_URL` = URL do backend em produção (ex.: `https://nara-backend.railway.app`). Configure em Project → Settings → Environment Variables. Sem isso o frontend não sabe onde chamar a API.
3. **SPA:** `vercel.json` já configura rewrite para `index.html` em todas as rotas.
4. **Na Vercel você não gera API key:** só conecta o repositório, define a pasta (`nara-frontend` se for monorepo) e a variável `VITE_API_URL`.

## Supabase

1. Aplicar migrações: `supabase db push` (ou executar os SQL em `supabase/migrations/` na ordem).
2. Scripts SQL manuais: usar arquivos em `supabase/scripts/` pelo SQL Editor quando necessário.
3. Popular `knowledge_chunks`: `cd nara-backend && python -m scripts.seed_knowledge_chunks` (com `.env` configurado).
4. Índice vetorial: migration `20260213000005` cria o ivfflat quando houver dados.

## LGPD

- **Exportar dados:** `GET /api/v1/privacy/my-data?email=...&result_token=...`
- **Excluir dados:** `DELETE /api/v1/privacy/my-data?email=...&result_token=...&confirm=true`
- Consentimentos: coletados no formulário de início (privacidade obrigatório, marketing opcional).

## Checklist de lançamento (resumo)

- [ ] Testes automatizados (backend) passando
- [ ] RLS e políticas Supabase aplicadas e testadas
- [ ] CORS configurado para o domínio do frontend
- [ ] SSL em produção (Vercel/Railway/Render padrão)
- [ ] Variáveis de ambiente definidas (sem segredos no código)
- [ ] Health check do backend respondendo
- [ ] Views de métricas no Supabase (`v_completion_rate`, `v_weekly_nps`, `v_diagnostic_funnel`) para monitoramento

## Beta (20–30 usuários)

- Conduzir rodada fechada; monitorar taxa de conclusão, NPS e feedback qualitativo via views SQL e painel.
- Consultas úteis no Supabase SQL Editor:
  - `SELECT * FROM v_completion_rate LIMIT 7;`
  - `SELECT * FROM v_weekly_nps LIMIT 4;`
  - `SELECT * FROM v_diagnostic_funnel;`
- Coletar ajustes prioritários para próxima fase (prompts, UX, thresholds RAG, custos).
