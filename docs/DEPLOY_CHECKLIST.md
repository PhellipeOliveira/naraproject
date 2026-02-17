# ✅ Checklist de Deploy - NARA

> **Conforme:** 07_DEPLOY_QUALIDADE.md - Seção 6

---

## 📦 Pré-Lançamento

### Código
- [ ] Todos os testes passando (`pytest tests/`)
- [ ] Code review completo do código crítico
- [ ] Sem secrets hardcoded (`.env.example` atualizado)
- [ ] Linting sem erros (`ruff check .` ou `flake8`)
- [ ] Type hints validados (`mypy app/`)

### Infraestrutura
- [ ] SSL/TLS configurado (HTTPS ativo)
- [ ] DNS propagado e validado
- [ ] Backups automáticos configurados no Supabase
- [ ] Rate limiting ativo (Render/Cloudflare)
- [ ] CDN configurado (Vercel para frontend)

### Segurança
- [ ] RLS (Row Level Security) testado em todas as tabelas Supabase
- [ ] CORS configurado corretamente (`CORS_ORIGINS`)
- [ ] Headers de segurança ativos:
  - [ ] `X-Content-Type-Options: nosniff`
  - [ ] `X-Frame-Options: DENY`
  - [ ] `Strict-Transport-Security`
- [ ] Validação de inputs em todos os endpoints

### LGPD / Privacidade
- [ ] Banner de cookies implementado no frontend
- [ ] Política de privacidade publicada
- [ ] Termos de uso publicados
- [ ] Endpoints de direitos do titular funcionando:
  - [ ] `/api/v1/privacy/my-data` (exportar)
  - [ ] `/api/v1/privacy/my-data` (deletar)

### Monitoramento
- [ ] Logs estruturados configurados
- [ ] Alertas configurados (Slack/Email)
- [ ] Health checks funcionando:
  - [ ] `/health` (básico)
  - [ ] `/health/detailed` (completo)
  - [ ] `/health/ready` (Kubernetes readiness)
  - [ ] `/health/live` (Kubernetes liveness)
- [ ] Sentry ou similar configurado para error tracking

### Banco de Dados
- [ ] Todas as migrations aplicadas no Supabase
- [ ] Chunks de conhecimento populados (`knowledge_chunks`)
- [ ] Indexes criados em campos de busca frequente
- [ ] Analytics tables criadas

### Conteúdo
- [ ] 15 perguntas baseline revisadas e testadas
- [ ] Chunks de conhecimento validados (version=1)
- [ ] Prompts do LLM testados com exemplos reais
- [ ] Templates de email testados (resultado, retomada, waitlist)

### Variáveis de Ambiente

**Backend (Render):**
```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJ...
OPENAI_API_KEY=sk-...
RESEND_API_KEY=re_...
EMAIL_FROM=nara@seudominio.com
FRONTEND_URL=https://nara.app
ENV=production
DEBUG=false
MIN_QUESTIONS_TO_FINISH=40
MIN_WORDS_TO_FINISH=3500
MIN_AREAS_COVERED=12
CORS_ORIGINS=["https://nara.app"]
```

**Frontend (Vercel):**
```bash
VITE_API_BASE_URL=https://api.nara.app
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
```

---

## 🚀 Lançamento

### Deploy
- [ ] Deploy backend (Render/Railway)
  ```bash
  git push origin main
  # Ou via dashboard do Render
  ```
- [ ] Deploy frontend (Vercel)
  ```bash
  git push origin main
  # Ou: vercel --prod
  ```
- [ ] Verificar que builds passaram sem erro
- [ ] Verificar health checks
  ```bash
  curl https://api.nara.app/health
  curl https://api.nara.app/health/detailed
  ```

### Testes de Fumaça (Manual)
- [ ] Acessar frontend em produção
- [ ] Iniciar novo diagnóstico
- [ ] Responder 3-5 perguntas
- [ ] Verificar auto-save funcionando
- [ ] Verificar progresso sendo atualizado
- [ ] Finalizar diagnóstico (ou testar elegibilidade)
- [ ] Verificar email de resultado chegou
- [ ] Acessar resultado via link do email
- [ ] Testar exportar dados (LGPD)

### Validações Técnicas
- [ ] Verificar logs por erros no Render
- [ ] Verificar Supabase por queries lentas
- [ ] Verificar latência da API (< 2s p95)
- [ ] Verificar taxa de erro (< 1%)

---

## 📊 Pós-Lançamento (Primeiras 24h)

### Monitoramento Contínuo
- [ ] Monitorar métricas em tempo real (1h, 4h, 24h)
- [ ] Verificar logs por erros críticos
- [ ] Verificar custos OpenAI (alertar se > R$10/dia)
- [ ] Verificar taxa de conclusão (meta: > 50%)

### Coleta de Feedback
- [ ] Coletar primeiros 3-5 feedbacks qualitativos
- [ ] Verificar NPS (se disponível)
- [ ] Identificar pontos de fricção (heatmap áreas silenciadas)

### Ajustes Rápidos
- [ ] Corrigir bugs P0 imediatamente
- [ ] Ajustar prompts se respostas não fizerem sentido
- [ ] Ajustar rate limits se necessário

---

## 🔧 Troubleshooting Rápido

### Backend não responde
```bash
# Verificar logs
render logs --tail

# Verificar health
curl https://api.nara.app/health/detailed
```

### Frontend com erro de CORS
- Verificar `CORS_ORIGINS` no backend
- Verificar que frontend está acessando URL correta

### Email não chega
```sql
-- Verificar logs de email no Supabase
SELECT * FROM email_logs 
WHERE recipient_email = 'teste@email.com' 
ORDER BY created_at DESC LIMIT 5;
```

### RAG retorna chunks errados
```sql
-- Verificar chunks ativos
SELECT COUNT(*), chapter 
FROM knowledge_chunks 
WHERE is_active = true AND version = 1 
GROUP BY chapter;
```

---

## 📈 Métricas de Sucesso (Primeiros 7 dias)

| Métrica | Meta | Como Medir |
|---------|------|------------|
| Taxa de Conclusão | > 50% | Dashboard Analytics |
| Tempo Médio | 15-25min | Analytics events |
| Taxa de Erro | < 1% | Logs / Sentry |
| NPS | > 50 | Feedback table |
| Conversão Waitlist | > 40% | Waitlist inscriptions |

---

## 🎯 Próximos Passos

Após validação inicial (7 dias):
- [ ] Análise de dados coletados
- [ ] Ajustes de UX baseados em feedback
- [ ] Otimização de custos OpenAI
- [ ] Planejamento de features V2

---

**Última atualização:** 2026-02-17
