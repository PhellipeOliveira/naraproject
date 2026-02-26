import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion } from "framer-motion";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { startDiagnostic, checkExistingDiagnostic, abandonDiagnostic } from "../api/diagnostic";
import { LegalFooter } from "../components/LegalFooter";
import { SharePopup } from "../components/SharePopup";
import { useDiagnosticStore } from "../stores";
import { getOrCreateSessionId, setStoredDiagnosticId, clearDiagnosticId } from "../lib/session";
import { 
  Clock, 
  FileText, 
  Target, 
  Pause, 
  CheckCircle2, 
  Mail, 
  User, 
  Shield,
  Sparkles,
  ArrowRight
} from "lucide-react";

const schema = z.object({
  email: z.string().email("Informe um e-mail válido"),
  full_name: z.string().min(0).optional(),
  consent_privacy: z
    .boolean()
    .refine((v) => v === true, { message: "É necessário aceitar a política de privacidade" }),
  consent_marketing: z.boolean().optional(),
});

type FormData = z.infer<typeof schema>;

const BENEFITS_WHAT_YOU_DO = [
  { icon: Target, text: "Responder no mínimo 40 perguntas" },
  { icon: Clock, text: "Tempo estimado: 20-30 min" },
  { icon: Pause, text: "Possibilidade de pausar e voltar" },
];

const BENEFITS_WHAT_YOU_GET = [
  { icon: FileText, text: "Diagnóstico Narrativo completo" },
  { icon: Mail, text: "PDF completo por e-mail" },
  { icon: Sparkles, text: "Dashboard com Gráfico Radar" },
];

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
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-subtle">
      <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8 items-stretch">
        {/* Form Card */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card variant="elevated" className="w-full h-full">
            <CardHeader className="text-center pb-2">
              <div className="mx-auto w-12 h-12 rounded-xl bg-gradient-primary flex items-center justify-center mb-4">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold font-display text-gradient">Diagnóstico NARA</h1>
              <p className="text-sm text-muted-foreground">
                Transformação Narrativa — 12 Áreas da Vida
              </p>
            </CardHeader>
            <CardContent className="space-y-5">
              {existingDiagnostic?.exists ? (
                <div className="space-y-4 text-center py-4">
                  <div className="p-4 rounded-xl bg-primary/5 border border-primary/20">
                    <p className="text-sm text-muted-foreground">
                      Você já tem um diagnóstico em andamento
                    </p>
                    <p className="text-2xl font-bold text-primary mt-1">
                      {existingDiagnostic.total_answers ?? 0} respostas
                    </p>
                  </div>
                  <div className="flex gap-3 justify-center">
                    <Button
                      variant="outline"
                      onClick={handleStartNew}
                      disabled={isAbandoning}
                    >
                      {isAbandoning ? "Preparando..." : "Começar novo"}
                    </Button>
                    <Button variant="gradient" onClick={handleResume} disabled={isAbandoning}>
                      Continuar
                      <ArrowRight className="ml-2 w-4 h-4" />
                    </Button>
                  </div>
                  {startError && (
                    <p className="text-sm text-destructive bg-destructive/10 p-3 rounded-lg text-center">
                      {startError}
                    </p>
                  )}
                </div>
              ) : (
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
                  <div className="space-y-2">
                    <label className="text-sm font-medium flex items-center gap-2">
                      <Mail className="w-4 h-4 text-muted-foreground" />
                      E-mail <span className="text-destructive">*</span>
                    </label>
                    <Input
                      type="email"
                      placeholder="seu@email.com"
                      className="h-11"
                      {...register("email")}
                    />
                    {errors.email && (
                      <p className="text-sm text-destructive">{errors.email.message}</p>
                    )}
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium flex items-center gap-2">
                      <User className="w-4 h-4 text-muted-foreground" />
                      Nome <span className="text-muted-foreground text-xs">(opcional)</span>
                    </label>
                    <Input placeholder="Seu nome" className="h-11" {...register("full_name")} />
                  </div>
                  
                  {/* Checkboxes */}
                  <div className="space-y-3 pt-2">
                    <label className="flex items-start gap-3 cursor-pointer group">
                      <input
                        type="checkbox"
                        {...register("consent_privacy")}
                        className="mt-1 h-4 w-4 rounded border-input text-primary focus:ring-primary"
                      />
                      <span className="text-sm text-muted-foreground group-hover:text-foreground transition-colors">
                        <Shield className="w-4 h-4 inline mr-1 text-primary" />
                        Aceito a{" "}
                        <Link to="/politica-de-privacidade" className="underline text-primary hover:text-primary-600">
                          política de privacidade
                        </Link>{" "}
                        e os{" "}
                        <Link to="/termos-de-uso" className="underline text-primary hover:text-primary-600">
                          termos de uso
                        </Link>
                      </span>
                    </label>
                    {errors.consent_privacy && (
                      <p className="text-sm text-destructive pl-7">{errors.consent_privacy.message}</p>
                    )}
                    
                    <label className="flex items-start gap-3 cursor-pointer group">
                      <input
                        type="checkbox"
                        {...register("consent_marketing")}
                        className="mt-1 h-4 w-4 rounded border-input text-primary focus:ring-primary"
                      />
                      <span className="text-sm text-muted-foreground group-hover:text-foreground transition-colors">
                        Desejo receber novidades e conteúdos da NARA por e-mail
                      </span>
                    </label>
                  </div>
                  
                  {startError && (
                    <p className="text-sm text-destructive bg-destructive/10 p-3 rounded-lg">
                      {startError}
                    </p>
                  )}
                  {checkExistingFeedback && (
                    <p
                      className={`text-sm p-3 rounded-lg ${
                        checkExistingFeedback.type === "error"
                          ? "text-destructive bg-destructive/10"
                          : "text-muted-foreground bg-muted"
                      }`}
                    >
                      {checkExistingFeedback.message}
                    </p>
                  )}
                  
                  <div className="flex flex-col sm:flex-row gap-3 pt-2">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={onCheckExisting}
                      disabled={!email || isChecking}
                      className="sm:flex-1"
                    >
                      {isChecking ? "Verificando..." : "Já tenho diagnóstico"}
                    </Button>
                    <Button 
                      type="submit" 
                      variant="gradient" 
                      disabled={isSubmitting}
                      className="sm:flex-1"
                    >
                      {isSubmitting ? "Iniciando..." : "Iniciar diagnóstico"}
                      <ArrowRight className="ml-2 w-4 h-4" />
                    </Button>
                  </div>
                  <LegalFooter />
                </form>
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* Benefits Card */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <Card className="w-full h-full bg-primary/5 border-primary/20">
            <CardHeader className="pb-4">
              <h2 className="text-xl font-bold font-display leading-tight flex items-center gap-2">
                <Target className="w-6 h-6 text-primary" />
                Revele Seu Círculo Narrativo
              </h2>
              <p className="text-sm text-muted-foreground">
                nas 12 Áreas Estruturantes da Vida
              </p>
            </CardHeader>
            <CardContent className="space-y-8">
              <section className="space-y-4">
                <h3 className="text-sm font-semibold text-foreground uppercase tracking-wide">
                  O que você vai fazer
                </h3>
                <ul className="space-y-3">
                  {BENEFITS_WHAT_YOU_DO.map((item, index) => (
                    <motion.li
                      key={index}
                      initial={{ opacity: 0, x: 10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.2 + index * 0.1 }}
                      className="flex items-center gap-3 text-sm text-muted-foreground"
                    >
                      <div className="w-8 h-8 rounded-lg bg-success/10 flex items-center justify-center flex-shrink-0">
                        <item.icon className="w-4 h-4 text-success" />
                      </div>
                      {item.text}
                    </motion.li>
                  ))}
                </ul>
              </section>
              
              <section className="space-y-4">
                <h3 className="text-sm font-semibold text-foreground uppercase tracking-wide">
                  O que você vai receber
                </h3>
                <ul className="space-y-3">
                  {BENEFITS_WHAT_YOU_GET.map((item, index) => (
                    <motion.li
                      key={index}
                      initial={{ opacity: 0, x: 10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.5 + index * 0.1 }}
                      className="flex items-center gap-3 text-sm text-muted-foreground"
                    >
                      <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                        <item.icon className="w-4 h-4 text-primary" />
                      </div>
                      {item.text}
                    </motion.li>
                  ))}
                </ul>
              </section>

              {/* Trust badge */}
              <div className="flex items-center gap-2 pt-4 border-t border-primary/10">
                <CheckCircle2 className="w-5 h-5 text-success" />
                <p className="text-xs text-muted-foreground">
                  Seus dados são protegidos e criptografados
                </p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
      <SharePopup
        open={sharePopupOpen}
        onClose={handleCloseSharePopup}
        url={startDiagnosticShareUrl}
      />
    </div>
  );
}
