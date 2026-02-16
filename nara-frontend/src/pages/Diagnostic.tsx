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
  const [localAnswerScale, setLocalAnswerScale] = useState<number | null>(null);

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

  const syncState = useCallback(
    async (diagId: string) => {
      try {
        const state = await getCurrentState(diagId);
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
            state.questions.map((q: { id: number; area: string; type: string; text: string; scale_labels?: string[] }) => ({
              id: q.id,
              area: q.area,
              type: q.type as "scale" | "open_long" | "open_short",
              text: q.text,
              scale_labels: q.scale_labels,
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
        answer_text: currentQuestion.type !== "scale" ? localAnswerText : undefined,
        answer_scale: currentQuestion.type === "scale" ? (localAnswerScale ?? undefined) : undefined,
      });

      useDiagnosticStore.setState({
        totalAnswers: res.total_answers,
        totalWords: res.total_words,
        areasCovered: res.areas_covered,
        canFinish: res.can_finish,
        progress: res.progress,
        status: res.status as "in_progress" | "eligible",
      });

      setLocalAnswerText("");
      setLocalAnswerScale(null);

      if (res.phase_complete && res.status !== "eligible") {
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
          console.error(e);
          const msg =
            e && typeof e === "object" && "response" in e
              ? (e as { response?: { data?: { detail?: string } } }).response?.data?.detail
              : null;
          setSubmitError(
            typeof msg === "string" ? msg : "Erro ao carregar próximas perguntas. Tente novamente."
          );
        } finally {
          setGeneratingNextPhase(false);
        }
      } else {
        goNext();
      }
    } catch (e: unknown) {
      console.error(e);
      const msg =
        e && typeof e === "object" && "response" in e
          ? (e as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : null;
      setSubmitError(
        typeof msg === "string" ? msg : "Erro ao salvar. Tente novamente."
      );
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
      console.error(e);
      const msg =
        e && typeof e === "object" && "response" in e
          ? (e as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : null;
      setSubmitError(
        typeof msg === "string" ? msg : "Erro ao carregar próximas perguntas. Tente novamente."
      );
    } finally {
      setGeneratingNextPhase(false);
    }
  };

  const handleFinish = async () => {
    if (!id || !resultToken) return;
    setFinishing(true);
    try {
      await finishDiagnostic(id);
      reset();
      navigate(`/resultado/${resultToken}`, { state: { diagnosticId: id } });
    } catch (e) {
      console.error(e);
    } finally {
      setFinishing(false);
    }
  };

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
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4 text-center max-w-md">
        {canLoadNextPhase ? (
          <>
            <p className="text-muted-foreground mb-4">
              Suas perguntas desta fase não estavam salvas (retomada antiga). Você pode gerar a
              próxima fase e continuar de onde parou — seu progresso ({totalAnswers} respostas) será
              mantido.
            </p>
            <Button onClick={handleLoadNextPhaseFromResume} disabled={generatingNextPhase}>
              {generatingNextPhase ? "Gerando..." : "Gerar próxima fase"}
            </Button>
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
        overallPercent={progress?.overall}
      />

      {submitError && (
        <p className="text-sm text-destructive bg-destructive/10 p-3 rounded mb-4">
          {submitError}
        </p>
      )}
      <div className="flex-1 py-6">
        <QuestionCard
          question={currentQuestion}
          answerText={localAnswerText}
          answerScale={localAnswerScale}
          onTextChange={setLocalAnswerText}
          onScaleChange={setLocalAnswerScale}
          onNext={handleSubmitAndNext}
          onPrev={() => goPrev()}
          canPrev={currentQuestionIndex > 0}
          isSubmitting={submitting}
        />
      </div>

      {canFinish && (
        <div className="text-center pt-4">
          <Button variant="outline" onClick={handleFinish} disabled={finishing}>
            {finishing ? "Gerando relatório..." : "Finalizar diagnóstico"}
          </Button>
        </div>
      )}
    </div>
  );
}
