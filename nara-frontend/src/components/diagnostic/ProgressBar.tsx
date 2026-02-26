import { Progress } from "../ui/progress";

const GLOBAL_TARGET_ANSWERS = 40;

interface ProgressBarProps {
  current: number;
  total: number;
  totalAnswers?: number;
  phase?: number;
}

const PHASE_LABELS: Record<number, string> = {
  1: "primeira",
  2: "segunda",
  3: "terceira",
  4: "quarta",
};

export function ProgressBar({
  current,
  total,
  totalAnswers = 0,
  phase = 1,
}: ProgressBarProps) {
  const phasePercent = total > 0 ? Math.round(((current + 1) / total) * 100) : 0;
  const globalPercent = Math.min(100, Math.round((totalAnswers / GLOBAL_TARGET_ANSWERS) * 100));
  const phaseLabel = PHASE_LABELS[phase] ?? `fase ${phase}`;

  return (
    <div className="w-full space-y-4">
      <div className="space-y-1.5">
        <div className="flex justify-between text-sm text-muted-foreground">
          <span>
            {phasePercent}% da {phaseLabel} fase
          </span>
        </div>
        <Progress value={Math.min(100, phasePercent)} className="h-2" />
      </div>
      <div className="space-y-1.5">
        <div className="flex justify-between text-sm text-muted-foreground">
          <span>{totalAnswers} perguntas respondidas</span>
          <span>{globalPercent}% do total</span>
        </div>
        <Progress value={globalPercent} className="h-2" />
      </div>
    </div>
  );
}
