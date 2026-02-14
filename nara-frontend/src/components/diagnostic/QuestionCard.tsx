import { Card, CardContent, CardHeader } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import type { Question } from "../../types";

interface QuestionCardProps {
  question: Question;
  answerText: string;
  answerScale: number | null;
  onTextChange: (value: string) => void;
  onScaleChange: (value: number) => void;
  onNext: () => void;
  onPrev: () => void;
  canPrev: boolean;
  isSubmitting: boolean;
}

export function QuestionCard({
  question,
  answerText,
  answerScale,
  onTextChange,
  onScaleChange,
  onNext,
  onPrev,
  canPrev,
  isSubmitting,
}: QuestionCardProps) {
  const isScale = question.type === "scale";
  const labels = question.scale_labels ?? ["1", "2", "3", "4", "5"];

  return (
    <Card className="w-full max-w-xl mx-auto">
      <CardHeader>
        <p className="text-sm text-muted-foreground">{question.area}</p>
        <h2 className="text-lg font-semibold leading-tight">{question.text}</h2>
      </CardHeader>
      <CardContent className="space-y-6">
        {isScale ? (
          <div className="space-y-2">
            <div className="grid grid-cols-1 gap-2 sm:grid-cols-5">
              {labels.map((label, i) => {
                const value = i + 1;
                const selected = answerScale === value;
                return (
                  <Button
                    key={value}
                    type="button"
                    variant={selected ? "default" : "outline"}
                    size="sm"
                    className="w-full min-w-0"
                    onClick={() => onScaleChange(value)}
                  >
                    <span className="truncate">{label}</span>
                  </Button>
                );
              })}
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            <textarea
              className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              placeholder="Digite sua resposta..."
              value={answerText}
              onChange={(e) => onTextChange(e.target.value)}
              rows={4}
            />
            <p className="text-xs text-muted-foreground">
              {answerText.trim().split(/\s+/).filter(Boolean).length} palavras
            </p>
          </div>
        )}

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
            disabled={
              isSubmitting ||
              (isScale ? answerScale === null : answerText.trim().length === 0)
            }
          >
            {isSubmitting ? "Salvando..." : "Continuar"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
