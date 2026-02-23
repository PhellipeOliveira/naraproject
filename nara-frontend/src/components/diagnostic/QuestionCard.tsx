import { Card, CardContent, CardHeader } from "../ui/card";
import { Button } from "../ui/button";
import { Progress } from "../ui/progress";
import type { Question } from "../../types";

const MIN_WORDS = 10;

interface QuestionCardProps {
  question: Question;
  answerText: string;
  onTextChange: (value: string) => void;
  onNext: () => void;
  onPrev: () => void;
  onSkip: () => void;
  canPrev: boolean;
  isSubmitting: boolean;
  isLastQuestion: boolean;
}

export function QuestionCard({
  question,
  answerText,
  onTextChange,
  onNext,
  onPrev,
  onSkip,
  canPrev,
  isSubmitting,
  isLastQuestion,
}: QuestionCardProps) {
  const wordCount = answerText.trim().split(/\s+/).filter(Boolean).length;
  const canSave = wordCount >= MIN_WORDS;

  // Todas as perguntas são narrativas agora (open_long ou open_short)
  const isShort = question.type === "open_short";
  const minRows = isShort ? 2 : 4;
  const minHeight = isShort ? "80px" : "120px";

  return (
    <Card className="w-full max-w-xl mx-auto">
      <CardHeader>
        <p className="text-sm text-muted-foreground">{question.area}</p>
        <h2 className="text-lg font-semibold leading-tight">{question.text}</h2>
        {question.follow_up_hint && (
          <p className="text-xs text-muted-foreground italic mt-2">
            {question.follow_up_hint}
          </p>
        )}
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <textarea
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            style={{ minHeight }}
            placeholder="Digite sua resposta..."
            value={answerText}
            onChange={(e) => onTextChange(e.target.value)}
            rows={minRows}
          />
          <div className="space-y-1">
            <p className="text-xs text-muted-foreground">
              {wordCount} palavras
            </p>
            {wordCount < MIN_WORDS && (
              <p className="text-xs text-muted-foreground">
                mínimo 10 palavras para gravar e continuar
              </p>
            )}
            <Progress
              value={Math.min(wordCount, MIN_WORDS)}
              max={MIN_WORDS}
              className="h-1.5 w-full max-w-[120px]"
            />
          </div>
        </div>

        <div className="flex justify-between items-center gap-2 pt-4">
          <Button
            type="button"
            variant="outline"
            onClick={onPrev}
            disabled={!canPrev || isSubmitting}
          >
            Anterior
          </Button>
          <div className="flex gap-2">
            {!isLastQuestion && (
              <Button
                type="button"
                variant="outline"
                onClick={onSkip}
                disabled={isSubmitting}
              >
                Próximo
              </Button>
            )}
            <Button
              type="button"
              onClick={onNext}
              disabled={isSubmitting || !canSave}
              className={!canSave ? "opacity-60" : undefined}
            >
              {isSubmitting ? "Salvando..." : "Gravar e Continuar"}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
