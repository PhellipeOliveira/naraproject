import { motion } from "framer-motion";
import { Check, ChevronLeft, ChevronRight, SkipForward, Loader2 } from "lucide-react";
import { Card, CardContent, CardHeader } from "../ui/card";
import { Button } from "../ui/button";
import { cn } from "../../lib/utils";
import type { Question } from "../../types";

const MIN_WORDS = 10;

// Mapa de cores por área
const AREA_COLORS: Record<string, { border: string; bg: string; text: string }> = {
  "Saúde Física": { border: "border-l-area-1", bg: "bg-area-1/10", text: "text-area-1" },
  "Saúde Mental": { border: "border-l-area-2", bg: "bg-area-2/10", text: "text-area-2" },
  "Saúde Espiritual": { border: "border-l-area-3", bg: "bg-area-3/10", text: "text-area-3" },
  "Vida Pessoal": { border: "border-l-area-4", bg: "bg-area-4/10", text: "text-area-4" },
  "Vida Amorosa": { border: "border-l-area-5", bg: "bg-area-5/10", text: "text-area-5" },
  "Vida Familiar": { border: "border-l-area-6", bg: "bg-area-6/10", text: "text-area-6" },
  "Vida Social": { border: "border-l-area-7", bg: "bg-area-7/10", text: "text-area-7" },
  "Vida Profissional": { border: "border-l-area-8", bg: "bg-area-8/10", text: "text-area-8" },
  "Finanças": { border: "border-l-area-9", bg: "bg-area-9/10", text: "text-area-9" },
  "Educação": { border: "border-l-area-10", bg: "bg-area-10/10", text: "text-area-10" },
  "Inovação": { border: "border-l-area-11", bg: "bg-area-11/10", text: "text-area-11" },
  "Lazer": { border: "border-l-area-12", bg: "bg-area-12/10", text: "text-area-12" },
};

const DEFAULT_COLORS = { border: "border-l-primary", bg: "bg-primary/10", text: "text-primary" };

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
  isPhase1Required?: boolean;
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
  isPhase1Required = false,
}: QuestionCardProps) {
  const wordCount = answerText.trim().split(/\s+/).filter(Boolean).length;
  const canSave = wordCount >= MIN_WORDS;
  const wordProgress = Math.min(100, (wordCount / MIN_WORDS) * 100);

  const progressColor =
    wordCount < 5
      ? "bg-destructive"
      : wordCount < 10
      ? "bg-warning"
      : "bg-success";

  const isShort = question.type === "open_short";
  const minRows = isShort ? 3 : 5;

  const areaColors = AREA_COLORS[question.area] || DEFAULT_COLORS;

  return (
    <motion.div
      key={question.id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      <Card className={cn("w-full max-w-xl mx-auto border-l-4 shadow-card", areaColors.border)}>
        <CardHeader className="space-y-4 pb-4">
          {/* Badge da área */}
          <span
            className={cn(
              "self-start px-3 py-1.5 rounded-full text-xs font-semibold",
              areaColors.bg,
              areaColors.text
            )}
          >
            {question.area}
          </span>

          {/* Pergunta */}
          <h2 className="text-lg font-semibold leading-relaxed text-foreground">
            {question.text}
          </h2>

          {question.follow_up_hint && (
            <p className="text-sm text-muted-foreground italic flex items-start gap-2">
              <span className="text-accent-warm">💡</span>
              {question.follow_up_hint}
            </p>
          )}
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Textarea */}
          <div className="space-y-3">
            <textarea
              className={cn(
                "flex w-full rounded-xl border-2 border-input bg-background px-4 py-3",
                "text-base ring-offset-background resize-none",
                "placeholder:text-muted-foreground/60",
                "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2",
                "focus-visible:border-primary/50",
                "disabled:cursor-not-allowed disabled:opacity-50",
                "transition-all duration-200",
                "min-h-[150px] md:min-h-[120px]"
              )}
              placeholder="Escreva sua resposta com pelo menos 10 palavras..."
              value={answerText}
              onChange={(e) => onTextChange(e.target.value)}
              rows={minRows}
            />

            {/* Progress de palavras */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground font-medium">{wordCount} palavras</span>
                {canSave ? (
                  <motion.span
                    initial={{ scale: 0, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="flex items-center text-success font-semibold"
                  >
                    <Check className="w-4 h-4" />
                  </motion.span>
                ) : (
                  <span className="text-muted-foreground">mínimo 10 palavras</span>
                )}
              </div>

              {/* Barra visual */}
              <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                <motion.div
                  className={cn("h-full rounded-full transition-colors duration-300", progressColor)}
                  initial={{ width: 0 }}
                  animate={{ width: `${wordProgress}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>
            </div>
          </div>

          {/* Botões de navegação */}
          <div className="flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-3 pt-2">
            <Button
              type="button"
              variant="outline"
              onClick={onPrev}
              disabled={!canPrev || isSubmitting}
              className="order-2 sm:order-1"
              iconLeft={<ChevronLeft className="w-4 h-4" />}
            >
              Anterior
            </Button>

            <div className="flex gap-3 order-1 sm:order-2">
              {!isLastQuestion && !isPhase1Required && (
                <Button
                  type="button"
                  variant="ghost"
                  onClick={onSkip}
                  disabled={isSubmitting}
                  className="text-muted-foreground hover:text-foreground"
                  iconRight={<SkipForward className="w-4 h-4" />}
                >
                  Pular
                </Button>
              )}
              <Button
                type="button"
                variant={canSave ? "gradient" : "default"}
                onClick={onNext}
                disabled={isSubmitting || !canSave}
                className={cn("min-w-[160px]", !canSave && "opacity-60")}
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    Gravar e Continuar
                    <ChevronRight className="ml-2 w-4 h-4" />
                  </>
                )}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
