import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { startDiagnostic, checkExistingDiagnostic, abandonDiagnostic } from "../api/diagnostic";
import { LegalFooter } from "../components/LegalFooter";
import { SharePopup } from "../components/SharePopup";
import { useDiagnosticStore } from "../stores";
import { getOrCreateSessionId, setStoredDiagnosticId, clearDiagnosticId } from "../lib/session";

const schema = z.object({
  email: z.string().email("Informe um e-mail válido"),
  full_name: z.string().min(0).optional(),
  consent_privacy: z
    .boolean()
    .refine((v) => v === true, { message: "É necessário aceitar a política de privacidade" }),
  consent_marketing: z.boolean().optional(),
});

type FormData = z.infer<typeof schema>;

export default function StartDiagnostic() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [isChecking, setIsChecking] = useState(false);
  const [existingDiagnostic, setExistingDiagnostic] = useState<{
    exists: boolean;
    diagnostic_id?: string;
    total_answers?: number;
    started_at?: string;
  } | null>(null);
  const [startError, setStartError] = useState<string | null>(null);
  const [isAbandoning, setIsAbandoning] = useState(false);
  const [sharePopupOpen, setSharePopupOpen] = useState(false);
  const [checkExistingFeedback, setCheckExistingFeedback] = useState<{
    type: "info" | "error";
    message: string;
  } | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    watch,
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { email: "", consent_privacy: false, consent_marketing: false },
  });

  const email = watch("email");
  const startDiagnosticShareUrl = useMemo(
    () => `${typeof window !== "undefined" ? window.location.origin : ""}/diagnostico/iniciar`,
    []
  );

  useEffect(() => {
    const shouldOpenShare =
      searchParams.get("compartilhar") === "1" || searchParams.get("share") === "1";
    if (shouldOpenShare) {
      setSharePopupOpen(true);
    }
  }, [searchParams]);

  const handleCloseSharePopup = () => {
    setSharePopupOpen(false);
    if (searchParams.get("compartilhar") === "1" || searchParams.get("share") === "1") {
      navigate("/diagnostico/iniciar", { replace: true });
    }
  };

  const onCheckExisting = async () => {
    if (!email) return;
    setCheckExistingFeedback(null);
    setStartError(null);
    setIsChecking(true);
    try {
      const data = await checkExistingDiagnostic((email as string).trim().toLowerCase());
      if (data.exists) {
        setExistingDiagnostic({
          exists: true,
          diagnostic_id: data.diagnostic_id,
          total_answers: data.total_answers,
          started_at: data.started_at,
        });
        return;
      }
      setExistingDiagnostic({ exists: false });
      setCheckExistingFeedback({
        type: "info",
        message: "Nenhum diagnóstico em andamento foi encontrado para este e-mail.",
      });
    } catch (err) {
      if (import.meta.env.DEV) {
        console.error(err);
      }
      setExistingDiagnostic(null);
      setCheckExistingFeedback({
        type: "error",
        message: "Não foi possível verificar seu diagnóstico agora. Tente novamente em instantes.",
      });
    } finally {
      setIsChecking(false);
    }
  };

  const onSubmit = async (data: FormData) => {
    setStartError(null);
    setCheckExistingFeedback(null);
    const emailNorm = (data.email || "").trim().toLowerCase();
    try {
      const existing = await checkExistingDiagnostic(emailNorm);
      if (existing.exists) {
        setExistingDiagnostic({
          exists: true,
          diagnostic_id: existing.diagnostic_id,
          total_answers: existing.total_answers,
          started_at: existing.started_at,
        });
        return;
      }
    } catch {
      // segue para iniciar novo
    }
    const sessionId = getOrCreateSessionId();
    try {
      const result = await startDiagnostic({
        email: data.email,
        full_name: data.full_name || undefined,
        session_id: sessionId,
        consent_privacy: data.consent_privacy,
        consent_marketing: data.consent_marketing ?? false,
      });

      useDiagnosticStore.getState().setStarted({
        diagnosticId: result.diagnostic_id,
        resultToken: result.result_token,
        phase: result.phase,
        questions: result.questions,
      });
      setStoredDiagnosticId(result.diagnostic_id);
      navigate(`/diagnostico/${result.diagnostic_id}`);
    } catch (err: unknown) {
      if (import.meta.env.DEV) {
        console.error(err);
      }
      const message =
        err && typeof err === "object" && "response" in err
          ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : null;
      setStartError(
        message && typeof message === "string"
          ? message
          : "Não foi possível iniciar o diagnóstico. Verifique se o servidor está rodando e tente novamente."
      );
    }
  };

  const handleResume = () => {
    if (existingDiagnostic?.diagnostic_id) {
      setStoredDiagnosticId(existingDiagnostic.diagnostic_id);
      navigate(`/diagnostico/${existingDiagnostic.diagnostic_id}`);
    }
  };

  const handleStartNew = async () => {
    if (!existingDiagnostic?.diagnostic_id) {
      setExistingDiagnostic(null);
      return;
    }
    setIsAbandoning(true);
    setStartError(null);
    try {
      await abandonDiagnostic(existingDiagnostic.diagnostic_id);
      clearDiagnosticId();
      useDiagnosticStore.getState().reset();
      setStartError(null);
      setExistingDiagnostic(null);
    } catch (err: unknown) {
      if (import.meta.env.DEV) {
        console.error(err);
      }
      const message =
        err && typeof err === "object" && "response" in err
          ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : null;
      setStartError(
        message && typeof message === "string"
          ? message
          : "Não foi possível iniciar um novo diagnóstico. Tente novamente."
      );
    } finally {
      setIsAbandoning(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-background">
      <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8 items-stretch">
        <Card className="w-full max-w-md mx-auto md:max-w-none">
          <CardHeader>
            <h1 className="text-2xl font-bold text-center">Diagnóstico NARA</h1>
            <p className="text-sm text-muted-foreground text-center">
              Transformação Narrativa — 12 Áreas da Vida
            </p>
          </CardHeader>
          <CardContent className="space-y-4">
            {existingDiagnostic?.exists ? (
              <div className="space-y-3 text-center">
                <p className="text-sm text-muted-foreground">
                  Você já tem um diagnóstico em andamento ({existingDiagnostic.total_answers ?? 0}{" "}
                  respostas).
                </p>
                <div className="flex gap-2 justify-center">
                  <Button
                    variant="outline"
                    onClick={handleStartNew}
                    disabled={isAbandoning}
                  >
                    {isAbandoning ? "Preparando..." : "Começar novo"}
                  </Button>
                  <Button onClick={handleResume} disabled={isAbandoning}>
                    Continuar
                  </Button>
                </div>
                {startError && (
                  <p className="text-sm text-destructive bg-destructive/10 p-3 rounded text-center">
                    {startError}
                  </p>
                )}
              </div>
            ) : (
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div>
                  <label className="text-sm font-medium">E-mail</label>
                  <Input
                    type="email"
                    placeholder="seu@email.com"
                    className="mt-1"
                    {...register("email")}
                  />
                  {errors.email && (
                    <p className="text-sm text-destructive mt-1">{errors.email.message}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium">Nome (opcional)</label>
                  <Input placeholder="Seu nome" className="mt-1" {...register("full_name")} />
                </div>
                <div className="flex items-start gap-2">
                  <input
                    type="checkbox"
                    id="consent_privacy"
                    {...register("consent_privacy")}
                    className="mt-1"
                  />
                  <label htmlFor="consent_privacy" className="text-sm">
                    Aceito a{" "}
                    <Link to="/politica-de-privacidade" className="underline">
                      politica de privacidade
                    </Link>{" "}
                    e os{" "}
                    <Link to="/termos-de-uso" className="underline">
                      termos de uso
                    </Link>
                    , incluindo o uso dos meus dados para geracao do diagnostico.
                  </label>
                </div>
                {errors.consent_privacy && (
                  <p className="text-sm text-destructive">{errors.consent_privacy.message}</p>
                )}
                <div className="flex items-start gap-2">
                  <input
                    type="checkbox"
                    id="consent_marketing"
                    {...register("consent_marketing")}
                    className="mt-1"
                  />
                  <label htmlFor="consent_marketing" className="text-sm">
                    Desejo receber novidades e conteúdos da NARA por e-mail.
                  </label>
                </div>
                {startError && (
                  <p className="text-sm text-destructive bg-destructive/10 p-3 rounded">
                    {startError}
                  </p>
                )}
                {checkExistingFeedback && (
                  <p
                    className={`text-sm p-3 rounded ${
                      checkExistingFeedback.type === "error"
                        ? "text-destructive bg-destructive/10"
                        : "text-muted-foreground bg-muted"
                    }`}
                  >
                    {checkExistingFeedback.message}
                  </p>
                )}
                <div className="flex gap-2">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={onCheckExisting}
                    disabled={!email || isChecking}
                  >
                    {isChecking ? "Verificando..." : "Já tenho diagnóstico"}
                  </Button>
                  <Button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? "Iniciando..." : "Iniciar diagnóstico"}
                  </Button>
                </div>
                <LegalFooter />
              </form>
            )}
          </CardContent>
        </Card>

        <Card className="w-full max-w-md mx-auto md:max-w-none flex flex-col bg-muted/30 border-primary/20">
          <CardHeader>
            <h2 className="text-xl font-bold leading-tight">
              🎯 Revele Seu Círculo Narrativo nas 12 Áreas Estruturantes da Vida.
            </h2>
          </CardHeader>
          <CardContent className="space-y-6 flex-1">
            <section className="space-y-3">
              <h3 className="text-sm font-semibold text-foreground">O que você vai fazer</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-0.5" aria-hidden>
                    ✓
                  </span>
                  Responder no mínimo 40 perguntas
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-0.5" aria-hidden>
                    ✓
                  </span>
                  Tempo estimado: 20-30 min
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-0.5" aria-hidden>
                    ✓
                  </span>
                  Possibilidade de pausar e voltar
                </li>
              </ul>
            </section>
            <section className="space-y-3">
              <h3 className="text-sm font-semibold text-foreground">O que você vai receber</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-0.5" aria-hidden>
                    ✓
                  </span>
                  Diagnóstico Narrativo
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-0.5" aria-hidden>
                    ✓
                  </span>
                  PDF completo por e-mail
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-0.5" aria-hidden>
                    ✓
                  </span>
                  Acesso ao Dashboard com Gráfico Radar
                </li>
              </ul>
            </section>
          </CardContent>
        </Card>
      </div>
      <SharePopup
        open={sharePopupOpen}
        onClose={handleCloseSharePopup}
        url={startDiagnosticShareUrl}
      />
    </div>
  );
}
