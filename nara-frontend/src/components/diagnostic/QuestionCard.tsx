import { Card, CardContent, CardHeader } from "../ui/card";
import { Button } from "../ui/button";
import type { Question } from "../../types";

interface QuestionCardProps {
  question: Question;
  answerText: string;
  onTextChange: (value: string) => void;
  onNext: () => void;
  onPrev: () => void;
  canPrev: boolean;
  isSubmitting: boolean;
}

export function QuestionCard({
  question,
  answerText,
  onTextChange,
  onNext,
  onPrev,
  canPrev,
  isSubmitting,
}: QuestionCardProps) {
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
          <p className="text-xs text-muted-foreground">
            {answerText.trim().split(/\s+/).filter(Boolean).length} palavras
          </p>
        </div>

        <div className="flex justify-between pt-4">
          <Button
            type="button"
            variant="outline"
            onClick={onPrev}
            disabled={!canPrev || isSubmitting}
          >
            Anterior
          </Button>
          <Button
            type="button"
            onClick={onNext}
            disabled={isSubmitting || answerText.trim().length === 0}
          >
            {isSubmitting ? "Salvando..." : "Continuar"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
