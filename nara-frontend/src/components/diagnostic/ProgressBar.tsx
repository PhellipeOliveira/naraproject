import { motion } from "framer-motion";
import { Check, Loader2 } from "lucide-react";
import { cn } from "../../lib/utils";

const GLOBAL_TARGET_ANSWERS = 60;

interface ProgressBarProps {
  current: number;
  total: number;
  totalAnswers?: number;
  phase?: number;
  isGenerating?: boolean;
}

const PHASE_INFO = [
  { label: "Baseline", shortLabel: "1", icon: "📋" },
  { label: "Exploração", shortLabel: "2", icon: "🔍" },
  { label: "Aprofundamento", shortLabel: "3", icon: "🎯" },
  { label: "Síntese", shortLabel: "4", icon: "✨" },
];

export function ProgressBar({
  current,
  total,
  totalAnswers = 0,
  phase = 1,
  isGenerating = false,
}: ProgressBarProps) {
  const phasePercent = total > 0 ? Math.round(((current + 1) / total) * 100) : 0;
  const globalPercent = Math.min(100, Math.round((totalAnswers / GLOBAL_TARGET_ANSWERS) * 100));

  return (
    <div className="w-full space-y-6">
      {/* Step Indicator */}
      <div className="relative flex items-center justify-between px-2">
        {/* Connection lines */}
        <div className="absolute top-5 left-0 right-0 h-0.5 mx-8">
          <div className="h-full bg-border rounded-full" />
          <motion.div
            className="absolute top-0 left-0 h-full bg-gradient-primary rounded-full"
            initial={{ width: "0%" }}
            animate={{ width: `${Math.max(0, (phase - 1) / 3) * 100}%` }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          />
        </div>

        {PHASE_INFO.map((p, index) => {
          const stepNumber = index + 1;
          const isCompleted = phase > stepNumber;
          const isCurrent = phase === stepNumber;
          const isFuture = phase < stepNumber;

          return (
            <div key={stepNumber} className="relative flex flex-col items-center z-10">
              {/* Step circle */}
              <motion.div
                className={cn(
                  "flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all duration-300",
                  isCompleted && "bg-success border-success text-white shadow-md",
                  isCurrent && "bg-primary border-primary text-white shadow-glow",
                  isFuture && "bg-background border-border text-muted-foreground"
                )}
                animate={isCurrent ? { scale: [1, 1.05, 1] } : {}}
                transition={{ duration: 1, repeat: isCurrent ? Infinity : 0, repeatDelay: 2 }}
              >
                {isCompleted ? (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <Check className="w-5 h-5" />
                  </motion.div>
                ) : isCurrent && isGenerating ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <span className="text-sm font-bold">{p.shortLabel}</span>
                )}
              </motion.div>

              {/* Label (hidden on mobile) */}
              <span
                className={cn(
                  "mt-2 text-xs font-medium hidden sm:block transition-colors",
                  isCurrent && "text-primary font-semibold",
                  isCompleted && "text-success",
                  isFuture && "text-muted-foreground"
                )}
              >
                {p.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* Phase progress */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span className="font-medium text-foreground">
            Fase {phase}: {PHASE_INFO[phase - 1]?.label}
          </span>
          <span className="text-muted-foreground font-medium">{phasePercent}%</span>
        </div>
        <div className="h-2.5 bg-secondary rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-primary rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${phasePercent}%` }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          />
        </div>
      </div>

      {/* Global progress */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">
            <span className="font-semibold text-foreground">{totalAnswers}</span> respostas de{" "}
            {GLOBAL_TARGET_ANSWERS} perguntas
          </span>
          <span className="text-muted-foreground">
            <span className="font-semibold text-foreground">{globalPercent}%</span> concluído
          </span>
        </div>
        <div className="h-3 bg-secondary rounded-full overflow-hidden shadow-inner">
          <motion.div
            className="h-full bg-gradient-primary rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${globalPercent}%` }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          />
        </div>
      </div>
    </div>
  );
}
