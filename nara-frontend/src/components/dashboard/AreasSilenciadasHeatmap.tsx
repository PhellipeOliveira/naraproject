import { Card, CardContent, CardHeader } from "../ui/card";
import { AlertTriangle } from "lucide-react";

interface AreasSilenciadasHeatmapProps {
  data: Array<{
    area_id: number;
    area_name: string;
    silence_count: number;
    percentage: number;
  }>;
}

const AREA_COLORS: Record<number, string> = {
  1: "#22c55e",  // Saúde Física
  2: "#8b5cf6",  // Saúde Mental
  3: "#f59e0b",  // Saúde Espiritual
  4: "#ec4899",  // Vida Pessoal
  5: "#ef4444",  // Vida Amorosa
  6: "#06b6d4",  // Vida Familiar
  7: "#3b82f6",  // Vida Social
  8: "#6366f1",  // Vida Profissional
  9: "#10b981",  // Finanças
  10: "#f97316", // Educação
  11: "#a855f7", // Inovação
  12: "#14b8a6", // Lazer
};

export function AreasSilenciadasHeatmap({ data }: AreasSilenciadasHeatmapProps) {
  if (!data || data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <h3 className="text-lg font-semibold">Áreas Mais Silenciadas</h3>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Sem dados disponíveis</p>
        </CardContent>
      </Card>
    );
  }

  // Normalizar para escala de opacidade (10% = min, 100% = max)
  const maxCount = Math.max(...data.map((d) => d.silence_count));
  const getOpacity = (count: number) => {
    if (maxCount === 0) return 0.1;
    return Math.max(0.1, (count / maxCount) * 1);
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-lg font-semibold">Áreas Mais Silenciadas</h3>
            <p className="text-sm text-muted-foreground">
              Áreas que os usuários evitam explorar
            </p>
          </div>
          <AlertTriangle className="text-yellow-600" size={24} />
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Grid Heatmap */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
          {data.map((area) => {
            const opacity = getOpacity(area.silence_count);
            const bgColor = AREA_COLORS[area.area_id] || "#gray";
            
            return (
              <div
                key={area.area_id}
                className="group relative p-4 rounded-lg border-2 transition-all hover:scale-105 cursor-pointer"
                style={{
                  backgroundColor: bgColor,
                  opacity: opacity,
                }}
              >
                <div className="text-center">
                  <p className="text-xs font-semibold text-white mb-1 drop-shadow">
                    {area.area_name}
                  </p>
                  <p className="text-lg font-bold text-white drop-shadow-lg">
                    {area.silence_count}
                  </p>
                  <p className="text-2xs text-white/90 drop-shadow">
                    {area.percentage.toFixed(1)}%
                  </p>
                </div>
                
                {/* Tooltip ao hover */}
                <div className="absolute inset-0 bg-black/80 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center p-2">
                  <p className="text-xs text-white text-center">
                    Silenciada {area.silence_count} vezes
                    <br />
                    ({area.percentage.toFixed(1)}% dos casos)
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Top 5 List */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Top 5 Áreas Mais Evitadas</h4>
          <div className="space-y-2">
            {data.slice(0, 5).map((area, index) => (
              <div
                key={area.area_id}
                className="flex items-center gap-3 p-2 rounded-lg bg-muted/50"
              >
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-yellow-500/20 flex items-center justify-center">
                  <span className="text-sm font-bold text-yellow-700">
                    {index + 1}
                  </span>
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium">{area.area_name}</p>
                  <p className="text-xs text-muted-foreground">
                    {area.silence_count} usuários ({area.percentage.toFixed(1)}%)
                  </p>
                </div>
                {/* Barra de progresso */}
                <div className="w-24 h-2 bg-muted rounded-full overflow-hidden">
                  <div
                    className="h-full bg-yellow-500 transition-all"
                    style={{ width: `${area.percentage}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Insight */}
        <div className="p-4 rounded-lg bg-yellow-50 dark:bg-yellow-950/20 border border-yellow-200 dark:border-yellow-900">
          <p className="text-xs text-yellow-800 dark:text-yellow-200">
            <span className="font-semibold">💡 Insight:</span> Áreas silenciadas 
            geralmente indicam bloqueios emocionais ou tabus pessoais. Usuários 
            tendem a evitar áreas onde há maior desconforto não resolvido.
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
