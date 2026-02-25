import { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  submitAnswer,
  getNextQuestions,
  getCurrentState,
  finishDiagnostic,
} from "../api/diagnostic";
import { useDiagnosticStore } from "../stores";
import { ProgressBar } from "../components/diagnostic/ProgressBar";
import { QuestionCard } from "../components/diagnostic/QuestionCard";
import { SaveAndExitButton } from "../components/diagnostic/SaveAndExitButton";
import { Button } from "../components/ui/button";
import { setStoredDiagnosticId } from "../lib/session";

export default function Diagnostic() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [finishing, setFinishing] = useState(false);
  const [generatingNextPhase, setGeneratingNextPhase] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [localAnswerText, setLocalAnswerText] = useState("");
  /** Respostas já dadas nesta sessão (por question_id), para restaurar ao clicar "Anterior". */
  const [answersByQuestionId, setAnswersByQuestionId] = useState<Record<number, string>>({});
  const [userEmail, setUserEmail] = useState<string>("");

  const {
    diagnosticId,
    resultToken,
    questions,
    currentQuestionIndex,
    totalAnswers,
    canFinish,
    progress,
    phase,
    setQuestions,
    setProgress,
    goNext,
    goPrev,
    reset,
  } = useDiagnosticStore();

  const currentQuestion = questions[currentQuestionIndex];

  // Restaurar o texto da pergunta atual ao navegar (Anterior/Próximo), para o usuário poder editar.
  useEffect(() => {
    const questionId = questions[currentQuestionIndex]?.id;
    if (questionId !== undefined) {
      setLocalAnswerText(answersByQuestionId[questionId] ?? "");
    }
  }, [questions, currentQuestionIndex, answersByQuestionId]);

  const getErrorDetailMessage = (error: unknown): string | null => {
    const raw =
      error && typeof error === "object" && "response" in error
        ? (
            error as {
              response?: { data?: { detail?: string | string[] | { message?: string } | unknown } };
            }
          ).response?.data?.detail
        : null;

    if (typeof raw === "string") return raw;
    if (Array.isArray(raw) && raw.length > 0) return String(raw[0]);
    if (raw && typeof raw === "object" && "message" in raw) {
      return String((raw as { message?: unknown }).message ?? "");
    }
    return null;
  };

  const syncState = useCallback(
    async (diagId: string) => {
      try {
        const state = await getCurrentState(diagId);
        
        // Salvar email do diagnóstico
        if (state.email) {
          setUserEmail(state.email);
        }
        
        if (state.result_token && useDiagnosticStore.getState().diagnosticId !== diagId) {
          useDiagnosticStore.setState({
            diagnosticId: diagId,
            resultToken: state.result_token,
            phase: state.current_phase,
            status: "in_progress",
          });
        }
        if (state.questions && state.questions.length > 0) {
          setQuestions(
            state.questions.map((q: { id: number; area: string; type: string; text: string; follow_up_hint?: string }) => ({
              id: q.id,
              area: q.area,
              type: q.type as "open_long" | "open_short",  // Apenas tipos narrativos
              text: q.text,
              follow_up_hint: q.follow_up_hint,
            }))
          );
        }
        setProgress({
          totalAnswers: state.total_answers,
          totalWords: state.total_words,
          areasCovered: Array.isArray(state.areas_covered) ? state.areas_covered.length : 0,
          canFinish: Boolean(state.can_finish),
          progress: state.progress ?? {
            overall: 0,
            questions: 0,
            words: 0,
            coverage: 0,
          },
        });
        // Preencher respostas já salvas para restaurar ao clicar "Anterior" (ex.: após retomar pelo link do email)
        const prefill = state.answers_prefill as Record<string, string> | undefined;
        if (prefill && typeof prefill === "object") {
          const byId: Record<number, string> = {};
          for (const [k, v] of Object.entries(prefill)) {
            const id = Number(k);
            if (!Number.isNaN(id) && typeof v === "string") byId[id] = v;
          }
          setAnswersByQuestionId(byId);
        }
      } catch {
        setLoading(false);
      }
    },
    [setQuestions, setProgress]
  );

  useEffect(() => {
    if (!id) {
      setLoading(false);
      return;
    }
    setStoredDiagnosticId(id);

    // Já temos este diagnóstico no store (ex.: acabou de iniciar) e já temos perguntas
    if (diagnosticId === id && questions.length > 0) {
      setLoading(false);
      return;
    }
    if (diagnosticId !== id) {
      syncState(id).finally(() => setLoading(false));
      return;
    }
    setLoading(false);
  }, [id, diagnosticId, questions.length, syncState]);

  const handleSubmitAndNext = async () => {
    if (!id || !currentQuestion) return;

    setSubmitting(true);
    setSubmitError(null);
    try {
      const res = await submitAnswer(id, {
        question_id: currentQuestion.id,
        question_text: currentQuestion.text,
        question_area: currentQuestion.area,
        answer_text: localAnswerText,  // Sempre texto agora (perguntas narrativas)
        answer_scale: undefined,  // Não mais usado
      });

      useDiagnosticStore.setState({
        totalAnswers: res.total_answers,
        totalWords: res.total_words,
        areasCovered: res.areas_covered,
        canFinish: res.can_finish,
        progress: res.progress,
        status: res.status as "in_progress" | "eligible",
      });

      setAnswersByQuestionId((prev) => ({
        ...prev,
        [currentQuestion.id]: localAnswerText,
      }));
      setLocalAnswerText("");

      if (res.phase_complete && res.status !== "eligible") {
        setGeneratingNextPhase(true);
        setSubmitError(null);
        try {
          const next = await getNextQuestions(id);
          if (next.questions && next.questions.length > 0) {
            useDiagnosticStore.setState({
              phase: next.phase,
              questions: next.questions,
              currentQuestionIndex: 0,
            });
          } else {
            setSubmitError(
              "As próximas perguntas ainda não foram geradas. Atualize a página ou tente novamente em instantes."
            );
          }
        } catch (e) {
          if (import.meta.env.DEV) {
            console.error(e);
          }
          const msg = getErrorDetailMessage(e);
          setSubmitError(msg || "Erro ao carregar próximas perguntas. Tente novamente.");
        } finally {
          setGeneratingNextPhase(false);
        }
      } else {
        goNext();
      }
    } catch (e: unknown) {
      if (import.meta.env.DEV) {
        console.error(e);
      }
      const msg = getErrorDetailMessage(e);
      setSubmitError(msg || "Erro ao salvar. Tente novamente.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleLoadNextPhaseFromResume = async () => {
    if (!id) return;
    setGeneratingNextPhase(true);
    setSubmitError(null);
    try {
      const next = await getNextQuestions(id);
      useDiagnosticStore.setState({
        phase: next.phase,
        questions: next.questions,
        currentQuestionIndex: 0,
      });
    } catch (e) {
      if (import.meta.env.DEV) {
        console.error(e);
      }
      const msg = getErrorDetailMessage(e);
      setSubmitError(msg || "Erro ao carregar próximas perguntas. Tente novamente.");
    } finally {
      setGeneratingNextPhase(false);
    }
  };

  const handleSkip = () => {
    goNext();
  };

  const handleFinish = async () => {
    if (!id || !resultToken) return;
    setFinishing(true);
    try {
      await finishDiagnostic(id);
      reset();
      navigate(`/resultado/${resultToken}`, { state: { diagnosticId: id } });
    } catch (e) {
      if (import.meta.env.DEV) {
        console.error(e);
      }
    } finally {
      setFinishing(false);
    }
  };

  const isLastAvailableQuestion =
    currentQuestionIndex === questions.length - 1 &&
    totalAnswers + currentQuestionIndex + 1 >= 60;
  const showOverSkipWarning =
    !canFinish && isLastAvailableQuestion;
  const questionsNeededToFinish = Math.max(0, 40 - totalAnswers);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-muted-foreground">Carregando...</p>
      </div>
    );
  }

  if (generatingNextPhase) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-6 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent mb-6" />
        <h2 className="text-lg font-semibold mb-2">Gerando perguntas personalizadas...</h2>
        <p className="text-muted-foreground text-sm max-w-sm">
          Estamos processando suas respostas para preparar as próximas perguntas. Isso pode levar alguns segundos.
        </p>
      </div>
    );
  }

  if (!currentQuestion && questions.length === 0) {
    const canLoadNextPhase = totalAnswers > 0 && phase >= 2;
    const errStr = submitError ? String(submitError) : "";
    const isMaxPhaseReached =
      submitError &&
      (errStr.includes("completou todas as fases") ||
        errStr.includes("Não há próxima fase") ||
        errStr.includes("current_phase_check") ||
        errStr.includes("violates check constraint") ||
        errStr.includes("23514"));
    const maxPhaseMessage =
      "Você completou todas as fases (máximo 4). Finalize o diagnóstico para ver seu resultado.";
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4 text-center max-w-md space-y-4">
        {canLoadNextPhase ? (
          <>
            {isMaxPhaseReached ? (
              <>
                <p className="text-muted-foreground">
                  {errStr.includes("completou todas as fases") || errStr.includes("Não há próxima fase")
                    ? submitError
                    : maxPhaseMessage}
                </p>
                <p className="text-sm text-muted-foreground">
                  Você já tem {totalAnswers} respostas (acima do mínimo). Clique abaixo para gerar seu relatório.
                </p>
                <div className="w-full flex justify-center">
                  <Button onClick={handleFinish} disabled={finishing}>
                    {finishing ? "Gerando relatório..." : "Finalizar e ver resultado"}
                  </Button>
                </div>
              </>
            ) : (
              <>
                <p className="text-muted-foreground mb-4">
                  Suas perguntas desta fase não estavam salvas (retomada antiga). Você pode gerar a
                  próxima fase e continuar de onde parou — seu progresso ({totalAnswers} respostas) será
                  mantido.
                </p>
                {submitError && (
                  <p className="text-sm text-destructive">{submitError}</p>
                )}
                <Button onClick={handleLoadNextPhaseFromResume} disabled={generatingNextPhase}>
                  {generatingNextPhase ? "Gerando..." : "Gerar próxima fase"}
                </Button>
              </>
            )}
          </>
        ) : (
          <p className="text-muted-foreground">Nenhuma pergunta disponível.</p>
        )}
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4 space-y-4">
        <p className="text-muted-foreground">Você pode finalizar o diagnóstico.</p>
        <Button onClick={handleFinish} disabled={finishing || !canFinish}>
          {finishing ? "Gerando relatório..." : "Finalizar e ver resultado"}
        </Button>
        {!canFinish && progress && (
          <p className="text-sm text-muted-foreground">
            Progresso: {progress.questions.toFixed(0)}% perguntas · {progress.words.toFixed(0)}%
            palavras · {progress.coverage.toFixed(0)}% áreas
          </p>
        )}
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col p-4 max-w-2xl mx-auto">
      <ProgressBar
        current={currentQuestionIndex}
        total={questions.length}
        totalAnswers={totalAnswers}
        phase={phase}
      />

      {/* Botão para salvar e sair */}
      <div className="flex justify-end pt-2 pb-4">
        <SaveAndExitButton
          diagnosticId={diagnosticId || ""}
          email={userEmail || "usuario@exemplo.com"}
          totalAnswers={totalAnswers}
          onExit={() => navigate("/")}
        />
      </div>

      {submitError && (
        <p className="text-sm text-destructive bg-destructive/10 p-3 rounded mb-4">
          {submitError}
        </p>
      )}
      {showOverSkipWarning && (
        <p className="text-sm text-amber-700 bg-amber-50 dark:bg-amber-950/30 dark:text-amber-400 border border-amber-200 dark:border-amber-800 p-3 rounded mb-4">
          Você pulou muitas perguntas. Para finalizar o diagnóstico, volte e responda pelo menos{" "}
          <strong>{questionsNeededToFinish}</strong> perguntas com 10+ palavras. Use o botão
          &quot;Anterior&quot; para revisitar.
        </p>
      )}
      <div className="flex-1 py-6">
        <QuestionCard
          question={currentQuestion}
          answerText={localAnswerText}
          onTextChange={setLocalAnswerText}
          onNext={handleSubmitAndNext}
          onPrev={() => {
            setAnswersByQuestionId((prev) => ({
              ...prev,
              [currentQuestion.id]: localAnswerText,
            }));
            goPrev();
          }}
          onSkip={handleSkip}
          canPrev={currentQuestionIndex > 0}
          isSubmitting={submitting}
          isLastQuestion={isLastAvailableQuestion}
          isPhase1Required={phase === 1}
        />
      </div>

      {canFinish ? (
        <div className="text-center pt-4 space-y-3">
          <p className="text-sm text-muted-foreground">
            Continue respondendo para diagnóstico ainda mais preciso.
          </p>
          <Button
            variant="outline"
            onClick={handleFinish}
            disabled={finishing}
            className="border-2 border-primary-200 bg-primary-50 text-foreground hover:bg-primary-100 hover:border-primary-300"
          >
            {finishing ? "Gerando relatório..." : "Finalizar e ver resultado"}
          </Button>
          <p className="text-xs text-muted-foreground">
            Você atingiu os critérios (40+ perguntas ou 3.500 palavras em 12 áreas).
          </p>
        </div>
      ) : (
        totalAnswers >= 25 && (
          <p className="text-center pt-4 text-sm text-muted-foreground">
            Finalizar disponível ao atingir <strong>40 perguntas</strong> ou{" "}
            <strong>3.500 palavras</strong> em 12 áreas. Faltam{" "}
            <strong>{Math.max(0, 40 - totalAnswers)} perguntas</strong> pelo critério de quantidade.
          </p>
        )
      )}
    </div>
  );
}
