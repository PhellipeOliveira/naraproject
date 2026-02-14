import { Progress } from "../ui/progress";

interface ProgressBarProps {
  current: number;
  total: number;
  overallPercent?: number;
}

export function ProgressBar({ current, total, overallPercent }: ProgressBarProps) {
  const questionPercent = total > 0 ? ((current + 1) / total) * 100 : 0;
  const displayPercent = total > 0 ? questionPercent : (overallPercent ?? 0);

  return (
    <div className="w-full space-y-1">
      <div className="flex justify-between text-sm text-muted-foreground">
        <span>
          Pergunta {current + 1} de {total}
        </span>
        <span>{Math.round(displayPercent)}% concluído</span>
      </div>
      <Progress value={displayPercent} className="h-2" />
    </div>
  );
}
