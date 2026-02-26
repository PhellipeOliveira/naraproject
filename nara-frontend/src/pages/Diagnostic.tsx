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
  const [validAnswersInCurrentPhase, setValidAnswersInCurrentPhase] = useState(0);
  const [currentPhaseQuestionsCount, setCurrentPhaseQuestionsCount] = useState(15);

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
  const MIN_VALID_WORDS = 10;
  const requiredAnswersInCurrentPhase = Math.min(10, Math.max(1, currentPhaseQuestionsCount));
  const canGenerateNextPhase = validAnswersInCurrentPhase >= requiredAnswersInCurrentPhase;
  const missingAnswersForNextPhase = Math.max(
    0,
    requiredAnswersInCurrentPhase - validAnswersInCurrentPhase
  );

  const countWords = (text: string): number =>
    text
      .trim()
      .split(/\s+/)
      .filter(Boolean).length;

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
        
        if (state.result_token) {
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
        setCurrentPhaseQuestionsCount(
          Math.max(1, state.current_phase_questions_count ?? state.questions?.length ?? 1)
        );
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
        setValidAnswersInCurrentPhase(Math.max(0, state.valid_answers_in_current_phase ?? 0));
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
      if (phase >= 2) {
        const previousWords = countWords(answersByQuestionId[currentQuestion.id] ?? "");
        const currentWords = countWords(localAnswerText);
        const delta = Number(currentWords >= MIN_VALID_WORDS) - Number(previousWords >= MIN_VALID_WORDS);
        if (delta !== 0) {
          setValidAnswersInCurrentPhase((prev) => Math.max(0, prev + delta));
        }
      }
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
            setCurrentPhaseQuestionsCount(Math.max(1, next.total_questions ?? next.questions.length));
            setValidAnswersInCurrentPhase(0);
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
      setCurrentPhaseQuestionsCount(Math.max(1, next.total_questions ?? next.questions.length));
      setValidAnswersInCurrentPhase(0);
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
    if (!id) return;
    setFinishing(true);
    setSubmitError(null);
    try {
      let tokenToUse = resultToken;
      if (!tokenToUse) {
        const currentState = await getCurrentState(id);
        tokenToUse = currentState.result_token ?? null;
        if (tokenToUse) {
          useDiagnosticStore.setState({ resultToken: tokenToUse });
        }
      }
      if (!tokenToUse) {
        setSubmitError("Não foi possível localizar seu link de resultado. Atualize a página e tente novamente.");
        return;
      }
      await finishDiagnostic(id);
      reset();
      navigate(`/resultado/${tokenToUse}`, { state: { diagnosticId: id } });
    } catch (e: unknown) {
      if (import.meta.env.DEV) {
        console.error(e);
      }
      const msg = getErrorDetailMessage(e);
      setSubmitError(msg || "Erro ao finalizar o diagnóstico. Tente novamente.");
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
    const isMiddlePhaseEnd = questions.length > 0 && phase >= 2 && phase < 4;
    if (isMiddlePhaseEnd) {
      return (
        <div className="min-h-screen flex flex-col items-center justify-center p-4 text-center max-w-md space-y-4">
          <p className="text-muted-foreground">
            Você chegou ao fim desta fase. Para avançar, é necessário responder no mínimo{" "}
            <strong>{requiredAnswersInCurrentPhase}</strong> perguntas com{" "}
            <strong>{MIN_VALID_WORDS}+ palavras</strong>.
          </p>
          <p className="text-sm text-muted-foreground">
            Respondidas nesta fase: <strong>{validAnswersInCurrentPhase}</strong> de{" "}
            <strong>{requiredAnswersInCurrentPhase}</strong>.
          </p>
          {canGenerateNextPhase ? (
            <Button onClick={handleLoadNextPhaseFromResume} disabled={generatingNextPhase}>
              {generatingNextPhase ? "Gerando..." : "Gerar próxima fase"}
            </Button>
          ) : (
            <p className="text-sm text-amber-700 bg-amber-50 dark:bg-amber-950/30 dark:text-amber-400 border border-amber-200 dark:border-amber-800 p-3 rounded">
              Faltam <strong>{missingAnswersForNextPhase}</strong> respostas válidas nesta fase.
              Use &quot;Anterior&quot; para voltar e &quot;Gravar e continuar&quot; para salvar.
            </p>
          )}
          {submitError && (
            <p className="text-sm text-destructive bg-destructive/10 p-3 rounded">{submitError}</p>
          )}
        </div>
      );
    }

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

      {/* Ações rápidas abaixo da barra de progresso */}
      <div className={`flex items-center gap-3 pt-2 pb-4 ${canFinish ? "justify-between" : "justify-end"}`}>
        {canFinish ? (
          <Button
            variant="outline"
            onClick={handleFinish}
            disabled={finishing}
            className="border-2 border-primary-200 bg-primary-50 text-foreground hover:bg-primary-100 hover:border-primary-300"
          >
            {finishing ? "Gerando relatório..." : "Finalizar e ver resultado"}
          </Button>
        ) : (
          <div />
        )}
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
        <div className="text-center pt-4">
          <p className="text-xs text-muted-foreground">
            Você atingiu os critérios (40+ perguntas ou 3.500 palavras em 12 áreas). Se quiser, finalize no botão acima.
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
