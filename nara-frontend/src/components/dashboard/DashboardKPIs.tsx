import { Card, CardContent } from "../ui/card";
import { TrendingUp, TrendingDown, Target, CheckCircle, AlertCircle } from "lucide-react";

interface DashboardKPIsProps {
  kpis: {
    period_days: number;
    total_diagnostics_started: number;
    total_diagnostics_completed: number;
    avg_completion_rate: number;
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
  };
}

export function DashboardKPIs({ kpis }: DashboardKPIsProps) {
  const cards = [
    {
      title: "Diagnósticos Iniciados",
      value: kpis.total_diagnostics_started.toLocaleString(),
      subtitle: `Últimos ${kpis.period_days} dias`,
      icon: Target,
      color: "text-blue-600",
      bgColor: "bg-blue-50 dark:bg-blue-950/20",
    },
    {
      title: "Diagnósticos Completados",
      value: kpis.total_diagnostics_completed.toLocaleString(),
      subtitle: `${kpis.avg_completion_rate.toFixed(1)}% taxa de conclusão`,
      icon: CheckCircle,
      color: "text-green-600",
      bgColor: "bg-green-50 dark:bg-green-950/20",
    },
    {
      title: "Motor Mais Comum",
      value: kpis.motor_mais_comum.name,
      subtitle: `${kpis.motor_mais_comum.count} usuários`,
      icon: kpis.avg_completion_rate >= 50 ? TrendingUp : TrendingDown,
      color: "text-purple-600",
      bgColor: "bg-purple-50 dark:bg-purple-950/20",
    },
    {
      title: "Crise Mais Comum",
      value: kpis.crise_mais_comum.name,
      subtitle: `${kpis.crise_mais_comum.count} diagnósticos`,
      icon: AlertCircle,
      color: "text-red-600",
      bgColor: "bg-red-50 dark:bg-red-950/20",
    },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {cards.map((card, index) => (
        <Card key={index} className="overflow-hidden">
          <CardContent className="p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium text-muted-foreground mb-1">
                  {card.title}
                </p>
                <h3 className="text-2xl font-bold mb-1 truncate">{card.value}</h3>
                <p className="text-xs text-muted-foreground">{card.subtitle}</p>
              </div>
              <div className={`p-3 rounded-lg ${card.bgColor}`}>
                <card.icon className={`${card.color}`} size={24} />
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
