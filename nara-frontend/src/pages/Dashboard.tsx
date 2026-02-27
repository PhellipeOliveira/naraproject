import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { useNavigate } from "react-router-dom";
import { apiClient } from "../api/client";
import { DashboardKPIs } from "../components/dashboard/DashboardKPIs";
import { MotoresChart } from "../components/dashboard/MotoresChart";
import { AreasSilenciadasHeatmap } from "../components/dashboard/AreasSilenciadasHeatmap";
import { FadeIn } from "../components/result/AnimatedTransitions";
import { RefreshCw, Download, TrendingUp } from "lucide-react";
import { clearAdminToken } from "../lib/adminSession";
import type {
  DashboardCriseDistribution,
  DashboardDataResponse,
  DashboardRealtimeMetric,
} from "../types";

type DashboardData = DashboardDataResponse;

interface KPIsData {
  period_days: number;
  total_diagnostics_started: number;
  total_diagnostics_completed: number;
  avg_completion_rate: number;
  avg_words_per_answer?: number;
  motor_mais_comum: {
    name: string;
    count: number;
  };
  crise_mais_comum: {
    name: string;
    count: number;
  };
  area_mais_silenciada: {
    name: string;
    count: number;
  };
  recent_completed_diagnostics?: Array<{
    diagnostic_id: string;
    motor_dominante?: string;
    crise_raiz?: string;
    phase_identified?: string | number | null;
    created_at?: string;
  }>;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState<DashboardData | null>(null);
  const [kpis, setKPIs] = useState<KPIsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [periodDays, setPeriodDays] = useState<7 | 30 | 90>(30);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);

    try {
      const [dashboardRes, kpisRes] = await Promise.all([
        apiClient.get("/analytics/dashboard", { params: { days: periodDays } }),
        apiClient.get("/analytics/kpis", { params: { days: periodDays } }),
      ]);

      setData(dashboardRes.data);
      setKPIs(kpisRes.data);
      setLastUpdate(new Date());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro desconhecido");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [periodDays]);

  const handleRefresh = () => {
    fetchDashboardData();
  };

  const handleExportData = () => {
    if (!data) return;
    
    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `nara-dashboard-${new Date().toISOString().split("T")[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleLogout = () => {
    clearAdminToken();
    navigate("/admin/login", { replace: true });
  };

  if (loading && !data) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto text-primary" />
          <p className="text-muted-foreground">Carregando analytics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="max-w-md">
          <CardHeader>
            <h2 className="text-lg font-bold text-destructive">Erro ao carregar dashboard</h2>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-muted-foreground">{error}</p>
            <Button onClick={handleRefresh} variant="outline" className="w-full">
              <RefreshCw className="w-4 h-4 mr-2" />
              Tentar Novamente
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!data || !kpis) {
    return null;
  }

  const recentCompleted = (kpis as KPIsData).recent_completed_diagnostics ?? [];

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <FadeIn>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold mb-2">Dashboard NARA</h1>
              <p className="text-sm text-muted-foreground">
                Analytics e métricas do sistema · Período: {data.period.days} dias
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                Última atualização: {lastUpdate.toLocaleTimeString()}
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <div className="flex gap-2">
                {[7, 30, 90].map((d) => (
                  <Button
                    key={d}
                    onClick={() => setPeriodDays(d as 7 | 30 | 90)}
                    variant={periodDays === d ? "default" : "outline"}
                    size="sm"
                    disabled={loading}
                  >
                    {d} dias
                  </Button>
                ))}
              </div>
              <Button onClick={handleRefresh} variant="outline" size="sm">
                <RefreshCw className={`w-4 h-4 mr-2 ${loading ? "animate-spin" : ""}`} />
                Atualizar
              </Button>
              <Button onClick={handleExportData} variant="outline" size="sm">
                <Download className="w-4 h-4 mr-2" />
                Exportar
              </Button>
              <Button onClick={handleLogout} variant="outline" size="sm">
                Sair
              </Button>
            </div>
          </div>
        </FadeIn>

        {/* KPIs */}
        <FadeIn delay={100}>
          <DashboardKPIs kpis={kpis} />
        </FadeIn>

        {/* Charts Grid */}
        <div className="grid gap-6 lg:grid-cols-2">
          <FadeIn delay={200}>
            <MotoresChart data={data.motores_distribution} />
          </FadeIn>

          <FadeIn delay={300}>
            <Card>
              <CardHeader>
                <h3 className="text-lg font-semibold">Distribuição de Crises</h3>
                <p className="text-sm text-muted-foreground">
                  Os 6 Clusters Operacionais (M1)
                </p>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {data.crises_distribution.map((crise: DashboardCriseDistribution, index: number) => {
                    const criseColors: Record<string, string> = {
                      "Identidade Raiz": "bg-red-500",
                      "Sentido e Direção": "bg-blue-500",
                      "Execução e Estrutura": "bg-yellow-500",
                      "Conexão e Expressão": "bg-purple-500",
                      "Incongruência Identidade-Cultura": "bg-orange-500",
                      "Transformação de Personagem": "bg-green-500",
                    };
                    
                    const color = criseColors[crise.crise_raiz] || "bg-gray-500";
                    
                    return (
                      <div key={index} className="space-y-1">
                        <div className="flex items-center justify-between text-sm">
                          <span className="font-medium">{crise.crise_raiz}</span>
                          <span className="text-muted-foreground">
                            {crise.count} ({crise.percentage.toFixed(1)}%)
                          </span>
                        </div>
                        <div className="h-2 bg-muted rounded-full overflow-hidden">
                          <div
                            className={`h-full ${color} transition-all`}
                            style={{ width: `${crise.percentage}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </FadeIn>
        </div>

        {/* Heatmap de Áreas Silenciadas */}
        <FadeIn delay={400}>
          <AreasSilenciadasHeatmap data={data.areas_silenciadas} />
        </FadeIn>

        {/* Métricas Realtime */}
        <FadeIn delay={500}>
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold">Métricas Diárias (Últimos 7 Dias)</h3>
                  <p className="text-sm text-muted-foreground">
                    Evolução diária de diagnósticos
                  </p>
                </div>
                <TrendingUp className="text-primary" size={24} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="border-b">
                    <tr className="text-left">
                      <th className="p-2 font-semibold">Data</th>
                      <th className="p-2 font-semibold">Iniciados</th>
                      <th className="p-2 font-semibold">Completados</th>
                      <th className="p-2 font-semibold">Em Progresso</th>
                      <th className="p-2 font-semibold">Taxa</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.realtime_metrics.map((metric: DashboardRealtimeMetric, index: number) => (
                      <tr key={index} className="border-b last:border-0 hover:bg-muted/50">
                        <td className="p-2 font-medium">
                          {new Date(metric.date).toLocaleDateString("pt-BR")}
                        </td>
                        <td className="p-2">{metric.total_diagnostics}</td>
                        <td className="p-2 text-green-600 font-medium">
                          {metric.completed}
                        </td>
                        <td className="p-2 text-blue-600">{metric.in_progress}</td>
                        <td className="p-2">
                          <span className={`font-medium ${
                            metric.completion_rate >= 50 ? "text-green-600" : "text-yellow-600"
                          }`}>
                            {metric.completion_rate.toFixed(1)}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </FadeIn>

        {/* Diagnósticos completados recentes */}
        <FadeIn delay={550}>
          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold">Últimos diagnósticos completados</h3>
              <p className="text-sm text-muted-foreground">
                Lista dos diagnósticos finalizados mais recentes (motor, crise e fase).
              </p>
            </CardHeader>
            <CardContent>
              {recentCompleted.length === 0 ? (
                <p className="text-sm text-muted-foreground">Sem diagnósticos completados recentes.</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="border-b">
                      <tr className="text-left">
                        <th className="p-2 font-semibold">Data</th>
                        <th className="p-2 font-semibold">Motor</th>
                        <th className="p-2 font-semibold">Crise</th>
                        <th className="p-2 font-semibold">Fase</th>
                        <th className="p-2 font-semibold">ID</th>
                      </tr>
                    </thead>
                    <tbody>
                      {recentCompleted.map((row, index) => (
                        <tr key={`${row.diagnostic_id}-${index}`} className="border-b last:border-0 hover:bg-muted/50">
                          <td className="p-2 font-medium">
                            {row.created_at ? new Date(row.created_at).toLocaleDateString("pt-BR") : "-"}
                          </td>
                          <td className="p-2">{row.motor_dominante ?? "-"}</td>
                          <td className="p-2">{row.crise_raiz ?? "-"}</td>
                          <td className="p-2">{row.phase_identified ?? "-"}</td>
                          <td className="p-2 font-mono text-xs text-muted-foreground">
                            {String(row.diagnostic_id).slice(0, 8)}…
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
          </Card>
        </FadeIn>

        {/* Footer com insights */}
        <FadeIn delay={600}>
          <Card className="bg-gradient-to-r from-primary/5 to-primary/10 border-primary/20">
            <CardContent className="p-6">
              <h4 className="font-semibold mb-2">💡 Insights Automáticos</h4>
              <ul className="text-sm space-y-1 text-muted-foreground">
                <li>
                  • Taxa de conclusão média: {data.totals.completion_rate.toFixed(1)}% 
                  {data.totals.completion_rate >= 50 ? " (Boa! 👍)" : " (Melhorar comunicação)"}
                </li>
                <li>
                  • Motor dominante: {kpis.motor_mais_comum.name} indica que a maioria busca 
                  {kpis.motor_mais_comum.name === "Necessidade" ? " alívio de dores" : 
                   kpis.motor_mais_comum.name === "Valor" ? " integridade" :
                   kpis.motor_mais_comum.name === "Desejo" ? " conquistas" : " propósito"}
                </li>
                <li>
                  • Área mais evitada: {kpis.area_mais_silenciada.name} - considere criar 
                  conteúdo específico para ajudar usuários nesta área
                </li>
              </ul>
            </CardContent>
          </Card>
        </FadeIn>
      </div>
    </div>
  );
}
