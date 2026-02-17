import { Card, CardContent, CardHeader } from "../ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";

interface MotoresChartProps {
  data: Array<{
    motor_dominante: string;
    count: number;
    percentage: float;
  }>;
}

const MOTOR_COLORS: Record<string, string> = {
  Necessidade: "#ef4444", // red-500
  Valor: "#3b82f6", // blue-500
  Desejo: "#a855f7", // purple-500
  Propósito: "#eab308", // yellow-500
};

export function MotoresChart({ data }: MotoresChartProps) {
  if (!data || data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <h3 className="text-lg font-semibold">Distribuição de Motores</h3>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Sem dados disponíveis</p>
        </CardContent>
      </Card>
    );
  }

  // Formatar dados para Recharts
  const chartData = data.map((item) => ({
    name: item.motor_dominante,
    value: item.count,
    percentage: item.percentage,
  }));

  const renderCustomLabel = ({
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    percent,
  }: any) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * (Math.PI / 180));
    const y = cy + radius * Math.sin(-midAngle * (Math.PI / 180));

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor={x > cx ? "start" : "end"}
        dominantBaseline="central"
        className="text-xs font-bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-semibold">Distribuição de Motores Motivacionais</h3>
        <p className="text-sm text-muted-foreground">
          O que impulsiona a transformação dos usuários
        </p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomLabel}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={MOTOR_COLORS[entry.name] || "#gray"} 
                />
              ))}
            </Pie>
            <Tooltip
              formatter={(value: number, name: string, props: any) => [
                `${value} diagnósticos (${props.payload.percentage.toFixed(1)}%)`,
                name
              ]}
            />
            <Legend 
              verticalAlign="bottom" 
              height={36}
              formatter={(value: string, entry: any) => (
                <span className="text-sm">{value} ({entry.payload.value})</span>
              )}
            />
          </PieChart>
        </ResponsiveContainer>

        {/* Legenda com descrições */}
        <div className="mt-4 space-y-2">
          {chartData.map((item) => (
            <div key={item.name} className="flex items-start gap-2 text-xs">
              <div 
                className="w-3 h-3 rounded-sm mt-0.5 flex-shrink-0" 
                style={{ backgroundColor: MOTOR_COLORS[item.name] }}
              />
              <div>
                <span className="font-medium">{item.name}</span>
                <span className="text-muted-foreground ml-2">
                  {getMotorDescription(item.name)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function getMotorDescription(motor: string): string {
  const descriptions: Record<string, string> = {
    Necessidade: "Afastar-se da dor",
    Valor: "Viver com integridade",
    Desejo: "Conquistar objetivos",
    Propósito: "Deixar legado",
  };
  return descriptions[motor] || "";
}
