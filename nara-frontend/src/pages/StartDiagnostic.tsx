import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { startDiagnostic, checkExistingDiagnostic } from "../api/diagnostic";
import { useDiagnosticStore } from "../stores";
import { getOrCreateSessionId, setStoredDiagnosticId } from "../lib/session";

const schema = z.object({
  email: z.string().email("Informe um e-mail válido"),
  full_name: z.string().min(0).optional(),
  consent_privacy: z.literal(true, {
    errorMap: () => ({ message: "É necessário aceitar a política de privacidade" }),
  }),
  consent_marketing: z.boolean().optional(),
});

type FormData = z.infer<typeof schema>;

export default function StartDiagnostic() {
  const navigate = useNavigate();
  const [isChecking, setIsChecking] = useState(false);
  const [existingDiagnostic, setExistingDiagnostic] = useState<{
    exists: boolean;
    diagnostic_id?: string;
    total_answers?: number;
    started_at?: string;
  } | null>(null);
  const [startError, setStartError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    watch,
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { consent_privacy: false, consent_marketing: false },
  });

  const email = watch("email");

  const onCheckExisting = async () => {
    if (!email) return;
    setIsChecking(true);
    try {
      const data = await checkExistingDiagnostic(email);
      setExistingDiagnostic(
        data.exists
          ? {
              exists: true,
              diagnostic_id: data.diagnostic_id,
              total_answers: data.total_answers,
              started_at: data.started_at,
            }
          : { exists: false }
      );
    } catch {
      setExistingDiagnostic({ exists: false });
    } finally {
      setIsChecking(false);
    }
  };

  const onSubmit = async (data: FormData) => {
    setStartError(null);
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
      console.error(err);
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

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-background">
      <Card className="w-full max-w-md">
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
                <Button variant="outline" onClick={() => setExistingDiagnostic(null)}>
                  Começar novo
                </Button>
                <Button onClick={handleResume}>Continuar</Button>
              </div>
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
                  Aceito a política de privacidade e o uso dos meus dados para geração do
                  diagnóstico.
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
            </form>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
