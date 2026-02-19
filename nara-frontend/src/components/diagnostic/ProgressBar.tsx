import { Progress } from "../ui/progress";

/** Meta de perguntas no total (doc: até 60). Usado para exibir "X de 60". */
const TOTAL_QUESTIONS_REF = 60;

interface ProgressBarProps {
  /** Índice da pergunta atual na fase (0-based). */
  current: number;
  /** Total de perguntas nesta fase. */
  total: number;
  /** Total de respostas já enviadas (todas as fases). */
  totalAnswers?: number;
  /** Percentual geral 0–100 (vindo da API). */
  overallPercent?: number;
}

export function ProgressBar({
  current,
  total,
  totalAnswers = 0,
  overallPercent,
}: ProgressBarProps) {
  const currentQuestionNumber = totalAnswers + 1;
  const displayPercent = overallPercent ?? (total > 0 ? ((current + 1) / total) * 100 : 0);

  return (
    <div className="w-full space-y-1">
      <div className="flex justify-between text-sm text-muted-foreground">
        <span>
          Pergunta {currentQuestionNumber} de {TOTAL_QUESTIONS_REF}
          {total > 0 && (
            <span className="ml-1 text-muted-foreground/80">
              · {current + 1}/{total} nesta fase
            </span>
          )}
        </span>
        <span>{Math.round(displayPercent)}% concluído</span>
      </div>
      <Progress value={Math.min(100, displayPercent)} className="h-2" />
    </div>
  );
}
