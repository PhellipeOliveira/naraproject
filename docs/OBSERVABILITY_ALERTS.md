# Observabilidade e Alertas Operacionais

## Objetivo
Definir monitoramento mínimo de produção para detectar:
- degradação de health checks,
- spikes de erro,
- aumento anormal de custo OpenAI.

## 1) Request ID e correlação de logs

### O que deve estar ativo
- Header de resposta `X-Request-ID` em todas as requisições.
- Campo `request_id` presente nos logs estruturados JSON.
- Mensagem de acesso com: método, path, status, latência e cliente.

### Verificação rápida
```bash
curl -i https://api.nara.app/health | grep -i X-Request-ID
```

## 2) Alertas de Health

### Regras recomendadas
- **P1:** `/health` ou `/health/ready` fora de 200 por 3 checagens consecutivas (1 min).
- **P2:** `/health/detailed` com `status=degraded` por mais de 10 min.

### Script de exemplo
```bash
#!/bin/bash
response=$(curl -s https://api.nara.app/health/detailed)
status=$(echo "$response" | jq -r '.status')
if [ "$status" = "unhealthy" ]; then
  echo "[P1] API unhealthy"
fi
```

## 3) Alertas de erro (spikes)

### Regras recomendadas
- **P1:** taxa de erro 5xx > 2% por 5 min.
- **P2:** taxa de erro 5xx > 1% por 15 min.
- **P1:** aumento > 3x no volume de erros em 10 min vs baseline.

### Checklist de implementação
- [ ] Agregar logs por minuto (status >= 500)
- [ ] Alertar Slack/Email com janela + endpoint mais afetado
- [ ] Incluir `request_id` no alerta para facilitar investigação

## 4) Alertas de custo OpenAI

### Regras recomendadas
- **P2:** custo diário estimado > R$ 10
- **P1:** custo diário estimado > R$ 30
- **P2:** aumento de chamadas OpenAI > 2x na janela de 24h

### Consulta SQL base (ajuste para sua telemetria)
```sql
SELECT
  DATE(created_at) AS dia,
  COUNT(*) FILTER (WHERE event_type = 'openai_call') AS chamadas
FROM analytics_events
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY dia
ORDER BY dia;
```

## 5) Rotina operacional diária (10 minutos)
- [ ] Verificar health checks (`/health`, `/health/ready`, `/health/detailed`)
- [ ] Verificar taxa de erro da última hora
- [ ] Verificar volume de chamadas OpenAI no dia
- [ ] Verificar fila de incidentes abertos

## 6) Runbook de resposta
Quando alerta disparar:
1. Abrir incidente com severidade (P1/P2).
2. Coletar `request_id` e endpoints impactados.
3. Aplicar mitigação (rollback, throttling, fallback).
4. Registrar causa raiz e ação corretiva.

Referência: `docs/INCIDENT_RESPONSE.md`.
