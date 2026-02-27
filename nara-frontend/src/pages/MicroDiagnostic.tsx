import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  finishMicroDiagnostic,
  getMicroDiagnosticPdfByToken,
  getMicroDiagnosticState,
  submitMicroDiagnosticAnswers,
} from "../api/diagnostic";
import type { MicroDiagnosticAnswerInput, MicroDiagnosticStateResponse, Question } from "../types";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { Button, buttonVariants } from "../components/ui/button";
import { cn } from "../lib/utils";

export default function MicroDiagnostic() {
  const { token, microId } = useParams<{ token: string; microId: string }>();
  const [state, setState] = useState<MicroDiagnosticStateResponse | null>(null);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [downloadingPdf, setDownloadingPdf] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function refreshState() {
    if (!token || !microId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await getMicroDiagnosticState(token, microId);
      setState(data);
      const preset: Record<number, string> = {};
      for (const q of data.questions || []) {
        preset[q.id] = "";
      }
      setAnswers(preset);
    } catch (err: unknown) {
      const message =
        err && typeof err === "object" && "response" in err
          ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : null;
      setError(typeof message === "string" ? message : "Erro ao carregar microdiagnóstico.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refreshState();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token, microId]);

  const isCompleted = state?.status === "completed";
  const currentQuestions = useMemo(() => state?.questions || [], [state?.questions]);

  function updateAnswer(questionId: number, value: string) {
    setAnswers((prev) => ({ ...prev, [questionId]: value }));
  }

  async function handleSubmitPhase() {
    if (!token || !microId || !state) return;
    const payload: MicroDiagnosticAnswerInput[] = currentQuestions.map((q: Question) => ({
      question_id: q.id,
      question_text: q.text,
      question_area: q.area,
      answer_text: (answers[q.id] || "").trim(),
    }));
    const incomplete = payload.some((item: MicroDiagnosticAnswerInput) => !item.answer_text);
    if (incomplete) {
      setError("Responda todas as perguntas antes de continuar.");
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      const nextState = await submitMicroDiagnosticAnswers(token, microId, payload);
      setState(nextState);
      if (nextState.phase === 2 && nextState.total_questions > 0) {
        const preset: Record<number, string> = {};
        for (const q of nextState.questions) {
          preset[q.id] = "";
        }
        setAnswers(preset);
      }
    } catch (err: unknown) {
      const message =
        err && typeof err === "object" && "response" in err
          ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : null;
      setError(typeof message === "string" ? message : "Erro ao enviar respostas.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleFinish() {
    if (!token || !microId) return;
    setSubmitting(true);
    setError(null);
    try {
      await finishMicroDiagnostic(token, microId);
      await refreshState();
    } catch (err: unknown) {
      const message =
        err && typeof err === "object" && "response" in err
          ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : null;
      setError(typeof message === "string" ? message : "Erro ao finalizar microdiagnóstico.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDownloadMicroPdf() {
    if (!token || !microId || !state?.result) return;
    setDownloadingPdf(true);
    setError(null);
    try {
      const blob = await getMicroDiagnosticPdfByToken(token, microId);
      const areaSlug = (state.result.area || "area")
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "_")
        .replace(/^_+|_+$/g, "");
      const safeArea = areaSlug || "area";
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `microdiagnostico_nara_${safeArea}_${token}.pdf`;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(url);
    } catch (err: unknown) {
      const message =
        err && typeof err === "object" && "response" in err
          ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : null;
      setError(typeof message === "string" ? message : "Erro ao baixar PDF do microdiagnóstico.");
    } finally {
      setDownloadingPdf(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-muted-foreground">Carregando microdiagnóstico...</p>
      </div>
    );
  }

  if (!state || error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 p-4">
        <p className="text-destructive">{error ?? "Microdiagnóstico indisponível."}</p>
        <Link to={`/meu-diagnostico/${token}`} className={buttonVariants({ variant: "outline" })}>
          Voltar ao dashboard
        </Link>
      </div>
    );
  }

  if (isCompleted && state.result) {
    return (
      <div className="min-h-screen p-4 max-w-4xl mx-auto space-y-6">
        <Card>
          <CardHeader>
            <h1 className="text-2xl font-bold">Microdiagnóstico concluído</h1>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm text-muted-foreground whitespace-pre-wrap">
              {state.result.micro_summary}
            </p>
            <p>
              <span className="font-medium">Técnica TCC:</span> {state.result.foco_tcc}
            </p>
            <p>
              <span className="font-medium">Ação para 7 dias:</span> {state.result.proxima_acao_7_dias}
            </p>
            <div className="flex flex-wrap gap-2">
              {state.result.ancoras.map((a: string) => (
                <span key={a} className="text-xs px-2 py-1 rounded bg-primary/10">
                  {a}
                </span>
              ))}
            </div>
            <div className="flex flex-wrap gap-2">
              <Button variant="outline" onClick={handleDownloadMicroPdf} disabled={downloadingPdf}>
                {downloadingPdf ? "Gerando PDF..." : "Baixar PDF"}
              </Button>
              <Link
                to={`/meu-diagnostico/${token}`}
                className={cn(buttonVariants({ variant: "outline" }))}
              >
                Voltar ao dashboard
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4 max-w-4xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <h1 className="text-2xl font-bold">
            Microdiagnóstico · Fase {state.phase}
          </h1>
          <p className="text-sm text-muted-foreground">
            Responda {state.total_questions} perguntas para aprofundar uma área específica.
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          {currentQuestions.map((question: Question) => (
            <div key={question.id} className="space-y-2">
              <p className="font-medium">{question.text}</p>
              <textarea
                value={answers[question.id] ?? ""}
                onChange={(e) => updateAnswer(question.id, e.target.value)}
                placeholder="Escreva sua resposta..."
                rows={4}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              />
            </div>
          ))}
          {error && <p className="text-sm text-destructive">{error}</p>}

          {state.phase === 1 && (
            <Button onClick={handleSubmitPhase} disabled={submitting} className="w-full">
              {submitting ? "Enviando..." : "Enviar respostas da fase 1"}
            </Button>
          )}

          {state.phase === 2 && state.total_questions > 0 && (
            <Button onClick={handleSubmitPhase} disabled={submitting} className="w-full">
              {submitting ? "Enviando..." : "Enviar respostas da fase 2"}
            </Button>
          )}

          {state.phase === 2 && state.total_questions === 0 && (
            <Button onClick={handleFinish} disabled={submitting} className="w-full">
              {submitting ? "Finalizando..." : "Finalizar microdiagnóstico"}
            </Button>
          )}
        </CardContent>
      </Card>
      <Link
        to={`/meu-diagnostico/${token}`}
        className={cn(buttonVariants({ variant: "outline" }))}
      >
        Voltar ao dashboard
      </Link>
    </div>
  );
}
