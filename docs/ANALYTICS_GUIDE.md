# Guia de Analytics NARA

> **Sistema completo de métricas e dashboard para o diagnóstico NARA V2**

---

## 📊 Visão Geral

O sistema de analytics do NARA permite tracking granular de eventos e visualização de métricas agregadas para entender o comportamento dos usuários e a performance do diagnóstico.

### Componentes

1. **Backend (Python/FastAPI)**
   - Serviço de analytics (`analytics_service.py`)
   - Endpoints REST (`/api/v1/analytics`)
   - Funções SQL de agregação

2. **Banco de Dados (Supabase/PostgreSQL)**
   - Tabela de eventos (`analytics_events`)
   - Métricas agregadas (`analytics_metrics`)
   - Views pré-computadas (realtime, distribuições, heatmaps)

3. **Frontend (React/TypeScript)**
   - Dashboard admin (`pages/Dashboard.tsx`)
   - Componentes de visualização (charts, KPIs, heatmaps)
   - Tracking automático de eventos

---

## 🚀 Setup

### 1. Executar Migration SQL

No Supabase SQL Editor, execute:

```bash
# Conectar ao Supabase
# Abrir SQL Editor
# Copiar e executar: supabase/migrations/20260217000002_analytics_tables.sql
```

**O que a migration cria:**
- Tabela `analytics_events` (tracking de eventos)
- Tabela `analytics_metrics` (métricas agregadas)
- View `analytics_realtime` (últimos 7 dias)
- View `analytics_areas_silenciadas` (heatmap)
- View `analytics_motores_distribution`
- View `analytics_crises_distribution`
- Função `aggregate_daily_metrics()` (CRON)

### 2. Instalar Dependências do Frontend

```bash
cd nara-frontend
npm install recharts
```

### 3. Configurar CRON (Opcional)

Para agregar métricas diárias automaticamente:

**Opção A: Supabase pg_cron**
```sql
SELECT cron.schedule(
    'aggregate-daily-metrics',
    '0 1 * * *',  -- Todo dia às 01:00 UTC
    $$SELECT aggregate_daily_metrics()$$
);
```

**Opção B: External CRON (curl)**
```bash
# Adicionar ao crontab
0 1 * * * curl -X POST https://seu-backend.com/api/v1/analytics/aggregate
```

---

## 📡 API Endpoints

### GET `/api/v1/analytics/dashboard`

Retorna resumo completo para o dashboard.

**Response:**
```json
{
  "period": {
    "days": 7,
    "start_date": "2026-02-10",
    "end_date": "2026-02-17"
  },
  "totals": {
    "diagnostics_started": 145,
    "diagnostics_completed": 87,
    "completion_rate": 60.0
  },
  "realtime_metrics": [...],
  "motores_distribution": [...],
  "crises_distribution": [...],
  "areas_silenciadas": [...]
}
```

### GET `/api/v1/analytics/kpis`

Retorna KPIs principais (últimos 30 dias).

**Response:**
```json
{
  "period_days": 30,
  "total_diagnostics_started": 542,
  "total_diagnostics_completed": 324,
  "avg_completion_rate": 59.78,
  "motor_mais_comum": {
    "name": "Necessidade",
    "count": 156
  },
  "crise_mais_comum": {
    "name": "Identidade Raiz",
    "count": 98
  },
  "area_mais_silenciada": {
    "name": "Vida Amorosa",
    "count": 87
  }
}
```

### GET `/api/v1/analytics/motores`

Distribuição de motores motivacionais.

**Response:**
```json
[
  {
    "motor_dominante": "Necessidade",
    "count": 156,
    "percentage": 48.15
  },
  {
    "motor_dominante": "Valor",
    "count": 89,
    "percentage": 27.47
  },
  ...
]
```

### GET `/api/v1/analytics/areas-silenciadas`

Heatmap de áreas silenciadas.

**Response:**
```json
[
  {
    "area_id": 5,
    "area_name": "Vida Amorosa",
    "silence_count": 87,
    "percentage": 32.5
  },
  {
    "area_id": 6,
    "area_name": "Vida Familiar",
    "silence_count": 65,
    "percentage": 24.3
  },
  ...
]
```

---

## 🎯 Tracking de Eventos

### Backend (Automático)

Os eventos são trackados automaticamente em pontos-chave do fluxo:

**Eventos Principais:**

| Evento | Quando | Dados |
|--------|--------|-------|
| `diagnostic_started` | Usuário inicia diagnóstico | diagnostic_id, utm_source |
| `answer_submitted` | Resposta enviada | question_id, word_count, area |
| `phase_completed` | Fase completada | phase, total_answers |
| `diagnostic_finished` | Diagnóstico finalizado | motor, crise, total_words, time |
| `result_viewed` | Resultado visualizado | result_token, motor |
| `nps_submitted` | NPS enviado | nps_score |

**Como Adicionar Tracking:**

```python
from app.services.analytics_service import analytics_service

# Em qualquer lugar do backend
await analytics_service.track_event(
    event_name="custom_event",
    event_category="user",  # diagnostic, user, navigation, error, conversion
    diagnostic_id=diagnostic_id,
    event_data={
        "custom_field": "value"
    }
)
```

### Frontend (Manual)

Para tracking no frontend (opcional):

```typescript
// Criar serviço de analytics
async function trackEvent(eventName: string, data: any) {
  await fetch('/api/v1/analytics/event', {
    method: 'POST',
    body: JSON.stringify({
      event_name: eventName,
      event_category: 'user',
      event_data: data
    })
  });
}

// Usar
trackEvent('button_clicked', { button_id: 'finish_diagnostic' });
```

---

## 📈 Dashboard Admin

### Acessar Dashboard

**URL:** `http://localhost:5173/dashboard` (desenvolvimento)

**Produção:** Adicionar rota no React Router:

```tsx
// src/App.tsx ou router config
import Dashboard from './pages/Dashboard';

<Route path="/dashboard" element={<Dashboard />} />
```

### Funcionalidades

1. **KPIs Principais**
   - Diagnósticos iniciados/completados
   - Taxa de conclusão média
   - Motor e crise mais comuns
   - Área mais silenciada

2. **Gráfico de Motores**
   - Distribuição em pizza
   - Cores por motor
   - Percentuais e contagens

3. **Heatmap de Áreas Silenciadas**
   - Grid visual com opacidade proporcional
   - Top 5 áreas mais evitadas
   - Insights automáticos

4. **Distribuição de Crises**
   - Barras horizontais
   - Cores por cluster

5. **Métricas Diárias**
   - Tabela dos últimos 7 dias
   - Evolução de iniciados/completados
   - Taxas de conclusão

### Exportar Dados

Botão "Exportar" no header do dashboard gera JSON com todas as métricas.

---

## 🔍 Queries Úteis

### Diagnósticos por Dia (Últimos 30 Dias)

```sql
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE status = 'completed') as completed
FROM diagnostics
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### Top 10 Motores por Mês

```sql
SELECT 
    DATE_TRUNC('month', created_at) as month,
    motor_dominante,
    COUNT(*) as count
FROM diagnostic_results dr
JOIN diagnostics d ON d.id = dr.diagnostic_id
WHERE created_at >= NOW() - INTERVAL '6 months'
GROUP BY month, motor_dominante
ORDER BY month DESC, count DESC;
```

### Usuários com Mais de 3 Áreas Silenciadas

```sql
SELECT 
    diagnostic_id,
    areas_silenciadas,
    ARRAY_LENGTH(areas_silenciadas, 1) as num_areas
FROM diagnostic_results
WHERE ARRAY_LENGTH(areas_silenciadas, 1) > 3
ORDER BY num_areas DESC;
```

---

## 📊 Métricas Recomendadas

### Saúde do Sistema

- **Taxa de Conclusão:** > 50% (saudável), < 30% (crítico)
- **Palavras Médias:** > 3500 (engajamento alto)
- **Áreas Cobertas:** > 8 (diagnóstico rico)

### Comportamento de Usuários

- **Motor Dominante:** Se > 60% é Necessidade, usuários estão em crise aguda
- **Áreas Silenciadas:** Se Vida Amorosa/Familiar > 30%, indica tabus fortes
- **Tempo de Conclusão:** < 30min (muito rápido, superficial), 45-90min (ideal)

### Qualidade de Respostas

- **Respostas < 30 palavras:** < 10% do total (ideal)
- **Respostas > 100 palavras:** > 40% do total (usuário engajado)

---

## 🎨 Customização do Dashboard

### Adicionar Novo Chart

1. Criar componente em `src/components/dashboard/`:

```tsx
// MeuNovoChart.tsx
export function MeuNovoChart({ data }: Props) {
  return (
    <Card>
      <CardHeader>Meu Chart</CardHeader>
      <CardContent>
        {/* Recharts ou custom visualization */}
      </CardContent>
    </Card>
  );
}
```

2. Importar e usar em `Dashboard.tsx`:

```tsx
import { MeuNovoChart } from '../components/dashboard/MeuNovoChart';

<FadeIn delay={700}>
  <MeuNovoChart data={data.custom_metric} />
</FadeIn>
```

### Adicionar Nova Métrica

1. **Backend:** Adicionar endpoint em `analytics.py`
2. **Frontend:** Buscar no `fetchDashboardData()`
3. **Componente:** Criar visualização

---

## 🔒 Segurança e Permissões

### Proteção do Dashboard

**Recomendações:**

1. **Adicionar autenticação:**
```tsx
// Proteger rota
<Route 
  path="/dashboard" 
  element={
    <RequireAuth roles={['admin']}>
      <Dashboard />
    </RequireAuth>
  } 
/>
```

2. **Backend:** Adicionar middleware de auth nos endpoints `/analytics`:

```python
@router.get("/dashboard")
async def get_dashboard(user: User = Depends(require_admin)):
    ...
```

3. **Supabase RLS:** Restringir acesso direto às tabelas:

```sql
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;
-- Apenas service_role pode inserir
```

---

## 🐛 Troubleshooting

### Dashboard não carrega

1. Verificar se migration SQL foi executada:
```sql
SELECT * FROM analytics_events LIMIT 1;
```

2. Verificar se backend está respondendo:
```bash
curl http://localhost:8000/api/v1/analytics/kpis
```

3. Verificar console do browser (F12) para erros CORS ou 404

### Métricas zeradas

1. Verificar se há diagnósticos finalizados:
```sql
SELECT COUNT(*) FROM diagnostics WHERE status = 'completed';
```

2. Executar agregação manual:
```sql
SELECT aggregate_daily_metrics();
```

### Recharts não renderiza

1. Instalar dependência:
```bash
npm install recharts
```

2. Verificar compatibilidade de versão:
```bash
npm list recharts
```

---

## 📚 Referências

- [Recharts Documentation](https://recharts.org/)
- [Supabase Analytics](https://supabase.com/docs/guides/analytics)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)

---

**Versão:** 1.0  
**Autor:** Time NARA  
**Última atualização:** Fevereiro 2026
