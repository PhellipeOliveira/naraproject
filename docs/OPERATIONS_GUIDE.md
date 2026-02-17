# Guia de Operações - NARA

> **Conforme:** 06_OPERACOES_EMAIL.md e 07_DEPLOY_QUALIDADE.md

---

## 📧 Sistema de Email

### Configuração do Resend

1. **Criar conta em resend.com**
2. **Adicionar domínio** e configurar DNS (SPF, DKIM, DMARC)
3. **Gerar API Key**
4. **Configurar variáveis de ambiente:**

```bash
RESEND_API_KEY=re_xxxxx
EMAIL_FROM=nara@seudominio.com
RESEND_REPLY_TO=contato@seudominio.com
```

### Tipos de Email

| Tipo | Quando Enviado | Template |
|------|----------------|----------|
| `diagnostic_result` | Diagnóstico finalizado | Resultado com score e link |
| `resume_link` | Diagnóstico abandonado (24h) | Link para retomar |
| `waitlist_welcome` | Inscrição na lista de espera | Boas-vindas |

### Verificar Envios

```sql
-- Últimos 10 emails enviados
SELECT 
  recipient_email,
  email_type,
  subject,
  status,
  created_at
FROM email_logs
ORDER BY created_at DESC
LIMIT 10;

-- Taxa de falha de emails
SELECT 
  email_type,
  COUNT(*) FILTER (WHERE status = 'sent') as enviados,
  COUNT(*) FILTER (WHERE status = 'failed') as falhados,
  ROUND(
    COUNT(*) FILTER (WHERE status = 'failed')::NUMERIC / 
    COUNT(*) * 100, 2
  ) as taxa_falha_pct
FROM email_logs
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY email_type;
```

---

## 💾 Sistema de Auto-Save

### Como Funciona

1. **localStorage**: Salva rascunho a cada keystroke (debounced 1s)
2. **Servidor**: Sincroniza após delay (evita sobrecarga)
3. **Modo Offline**: Mantém dados locais e sincroniza ao voltar online

### Componentes

- `useAutoSave` hook: Lógica de salvamento
- `SaveIndicator`: Feedback visual (salvando, salvo, erro)
- `lib/session.ts`: Gestão de sessão e diagnostic_id

### Testar Auto-Save

1. Abrir DevTools > Application > Local Storage
2. Iniciar diagnóstico
3. Digitar resposta
4. Verificar key `nara_answer_draft` sendo atualizada
5. Simular offline (DevTools > Network > Offline)
6. Digitar mais texto
7. Voltar online
8. Verificar sincronização automática

---

## 🔄 Retomada de Diagnóstico

### Fluxo

```
Usuário informa email
    ↓
API: GET /diagnostic/check-existing?email=xxx
    ↓
Se exists=true → Mostrar ResumeModal
    ↓
Usuário escolhe: [Continuar] ou [Começar Novo]
    ↓
[Continuar]: GET /diagnostic/{id}/current-state
[Novo]: POST /diagnostic/start (marca anterior como abandonado)
```

### Endpoints

**Verificar existente:**
```bash
GET /api/v1/diagnostic/check-existing?email=user@example.com
```

**Response:**
```json
{
  "exists": true,
  "diagnostic_id": "uuid",
  "status": "in_progress",
  "current_phase": 2,
  "total_answers": 25,
  "started_at": "2026-02-15T10:30:00Z"
}
```

**Buscar estado atual:**
```bash
GET /api/v1/diagnostic/{diagnostic_id}/current-state
```

---

## 🛡️ LGPD / Privacidade

### Direitos do Titular

**1. Exportar dados (Portabilidade):**
```bash
GET /api/v1/privacy/my-data?email=user@example.com&result_token=xxx
```

**2. Deletar dados (Eliminação):**
```bash
DELETE /api/v1/privacy/my-data?email=user@example.com&result_token=xxx&confirm=true
```

### Retenção de Dados

| Dado | Período | Motivo |
|------|---------|--------|
| Diagnósticos completos | 2 anos | Histórico do usuário |
| Diagnósticos abandonados | 90 dias | Retomada |
| Email logs | 1 ano | Auditoria |
| Analytics events | 2 anos | Métricas |

### Limpeza Automática (CRON)

```sql
-- Deletar diagnósticos abandonados > 90 dias
DELETE FROM diagnostics
WHERE status = 'abandoned'
  AND updated_at < NOW() - INTERVAL '90 days';

-- Anonimizar diagnósticos antigos (opcional)
UPDATE diagnostics
SET email = 'anonymized@nara.app'
WHERE status = 'completed'
  AND updated_at < NOW() - INTERVAL '2 years';
```

---

## 🏥 Health Checks

### Endpoints

| Endpoint | Uso | Resposta |
|----------|-----|----------|
| `/health` | Load balancer básico | `{"status": "healthy"}` |
| `/health/detailed` | Troubleshooting | Status de cada dependência |
| `/health/ready` | Kubernetes readiness probe | `{"ready": true}` |
| `/health/live` | Kubernetes liveness probe | `{"alive": true}` |

### Monitorar Health

**Via curl:**
```bash
curl https://api.nara.app/health/detailed
```

**Via script (alertar se unhealthy):**
```bash
#!/bin/bash
response=$(curl -s https://api.nara.app/health/detailed)
status=$(echo $response | jq -r '.status')

if [ "$status" != "healthy" ]; then
  echo "ALERTA: API unhealthy!"
  # Enviar para Slack/Email
fi
```

---

## 📊 Métricas e Analytics

### KPIs Principais

```sql
-- Taxa de conclusão (últimos 7 dias)
SELECT 
  COUNT(*) as iniciados,
  COUNT(*) FILTER (WHERE status = 'completed') as finalizados,
  ROUND(
    COUNT(*) FILTER (WHERE status = 'completed')::NUMERIC / 
    COUNT(*) * 100, 2
  ) as taxa_conclusao
FROM diagnostics
WHERE created_at > NOW() - INTERVAL '7 days';

-- Tempo médio de conclusão
SELECT 
  AVG(EXTRACT(EPOCH FROM (updated_at - created_at)) / 60) as minutos_medio
FROM diagnostics
WHERE status = 'completed'
  AND created_at > NOW() - INTERVAL '7 days';

-- Distribuição de motores
SELECT 
  vetor_estado->>'motor_motivacional_primario' as motor,
  COUNT(*) as count
FROM diagnostic_results
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY motor
ORDER BY count DESC;
```

### Dashboard Admin

Acessar: `https://nara.app/dashboard` (requer autenticação)

**Features:**
- KPIs em tempo real
- Distribuição de motores (gráfico pizza)
- Heatmap de áreas silenciadas
- Métricas diárias agregadas

---

## 🚨 Troubleshooting Comum

### 1. Email não chega

**Diagnóstico:**
```sql
SELECT * FROM email_logs 
WHERE recipient_email = 'user@example.com' 
ORDER BY created_at DESC LIMIT 5;
```

**Possíveis causas:**
- RESEND_API_KEY inválida
- Domínio não verificado no Resend
- Email na caixa de spam (verificar SPF/DKIM)

**Solução:**
```bash
# Testar envio manual
curl -X POST https://api.nara.app/api/v1/test/send-email \
  -H "Content-Type: application/json" \
  -d '{"to": "test@example.com"}'
```

### 2. RAG retorna chunks errados

**Diagnóstico:**
```sql
-- Verificar chunks ativos
SELECT chapter, COUNT(*) 
FROM knowledge_chunks 
WHERE is_active = true AND version = 1 
GROUP BY chapter;

-- Testar similaridade
SELECT content, 1 - (embedding <=> '[vector]') as similarity
FROM knowledge_chunks
WHERE is_active = true
ORDER BY embedding <=> '[vector]'
LIMIT 5;
```

**Solução:**
- Verificar `filter_chunk_strategy='semantic'` na query
- Verificar `filter_version=1`
- Reprocessar chunks se necessário

### 3. Alto custo OpenAI

**Diagnóstico:**
```sql
-- Contar chamadas de API (via analytics_events)
SELECT 
  DATE(created_at) as dia,
  COUNT(*) FILTER (WHERE event_type = 'openai_call') as chamadas
FROM analytics_events
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY dia
ORDER BY dia;
```

**Solução:**
- Implementar cache de perguntas frequentes
- Reduzir `top_k` no retriever
- Ajustar `max_tokens` no LLM

---

## 🔐 Backup e Recuperação

### Backup Automático (Supabase)

- **Frequência:** Diário (incluído no plano)
- **Retenção:** 7 dias (Free), 30 dias (Pro)
- **Acesso:** Supabase Dashboard > Database > Backups

### Backup Manual

```bash
# Exportar todas as tabelas
pg_dump -h db.xxxxx.supabase.co -U postgres -d postgres > backup.sql

# Restaurar
psql -h db.xxxxx.supabase.co -U postgres -d postgres < backup.sql
```

### Dados Críticos

- `diagnostics`
- `diagnostic_results`
- `answers`
- `knowledge_chunks`

---

**Última atualização:** 2026-02-17
