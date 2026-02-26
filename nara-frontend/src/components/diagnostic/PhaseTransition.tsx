import { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import confetti from "canvas-confetti";
import { Button } from "../ui/button";
import { Sparkles, ArrowRight, Trophy, Target, Compass, Star } from "lucide-react";

interface PhaseTransitionProps {
  isOpen: boolean;
  completedPhase: number;
  totalAnswers: number;
  onContinue: () => void;
}

const PHASE_INFO = [
  { name: "Baseline", icon: Compass, description: "Mapeamos seus pontos de partida" },
  { name: "Exploração", icon: Target, description: "Exploramos suas experiências e padrões" },
  { name: "Aprofundamento", icon: Star, description: "Aprofundamos nas áreas mais relevantes" },
  { name: "Síntese", icon: Trophy, description: "Sintetizamos sua jornada narrativa" },
];

export function PhaseTransition({
  isOpen,
  completedPhase,
  totalAnswers,
  onContinue,
}: PhaseTransitionProps) {
  const nextPhase = completedPhase + 1;
  const hasNextPhase = nextPhase <= 4;
  const completedInfo = PHASE_INFO[completedPhase - 1];
  const nextInfo = hasNextPhase ? PHASE_INFO[nextPhase - 1] : null;
  const CompletedIcon = completedInfo?.icon || Sparkles;

  useEffect(() => {
    if (isOpen) {
      // Dispara confetti
      const duration = 2000;
      const end = Date.now() + duration;

      const colors = ["#7C3AED", "#06B6D4", "#10B981", "#F59E0B"];

      (function frame() {
        confetti({
          particleCount: 3,
          angle: 60,
          spread: 55,
          origin: { x: 0, y: 0.6 },
          colors: colors,
        });
        confetti({
          particleCount: 3,
          angle: 120,
          spread: 55,
          origin: { x: 1, y: 0.6 },
          colors: colors,
        });

        if (Date.now() < end) {
          requestAnimationFrame(frame);
        }
      })();
    }
  }, [isOpen]);

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center bg-background/95 backdrop-blur-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className="max-w-md mx-auto p-8 text-center space-y-8"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            transition={{ delay: 0.1, type: "spring", stiffness: 200 }}
          >
            {/* Ícone de celebração */}
            <motion.div
              className="mx-auto w-24 h-24 rounded-full bg-gradient-primary flex items-center justify-center shadow-glow"
              animate={{ scale: [1, 1.1, 1], rotate: [0, 5, -5, 0] }}
              transition={{ duration: 0.6, repeat: 2 }}
            >
              <CompletedIcon className="w-12 h-12 text-white" />
            </motion.div>

            {/* Título */}
            <div className="space-y-3">
              <motion.h2
                className="text-4xl font-bold font-display text-gradient"
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                Fase {completedPhase} Completa! 🎉
              </motion.h2>
              <motion.p
                className="text-lg text-muted-foreground"
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
              >
                {completedInfo?.name}: {completedInfo?.description}
              </motion.p>
            </div>

            {/* Stats */}
            <motion.div
              className="py-5 px-6 rounded-2xl bg-primary/5 border border-primary/20"
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              <p className="text-sm text-muted-foreground mb-1">Progresso total</p>
              <p className="text-3xl font-bold text-primary font-display">
                {totalAnswers} perguntas
              </p>
              <p className="text-sm text-muted-foreground mt-1">respondidas com sucesso</p>
            </motion.div>

            {/* Próxima fase */}
            {hasNextPhase && nextInfo && (
              <motion.div
                className="space-y-2"
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                <p className="text-sm font-medium text-muted-foreground">Próxima fase:</p>
                <div className="flex items-center justify-center gap-2">
                  {nextInfo.icon && <nextInfo.icon className="w-5 h-5 text-primary" />}
                  <p className="text-xl font-semibold text-foreground">{nextInfo.name}</p>
                </div>
                <p className="text-sm text-muted-foreground max-w-xs mx-auto">
                  Perguntas personalizadas baseadas nas suas respostas anteriores
                </p>
              </motion.div>
            )}

            {/* CTA */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              <Button
                onClick={onContinue}
                size="lg"
                variant="gradient"
                className="gap-2 px-8"
              >
                {hasNextPhase ? (
                  <>
                    Continuar para Fase {nextPhase}
                    <ArrowRight className="w-5 h-5" />
                  </>
                ) : (
                  <>
                    <Trophy className="w-5 h-5" />
                    Ver meu resultado
                  </>
                )}
              </Button>
            </motion.div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
