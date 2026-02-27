import { useEffect, useState } from "react";
import { useParams, useLocation, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { getResultByToken } from "../api/diagnostic";
import { submitFeedback } from "../api/feedback";
import { joinWaitlist } from "../api/waitlist";
import type { DiagnosticResultResponse } from "../types";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { Button, buttonVariants } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { cn } from "../lib/utils";
import {
  Zap,
  Map,
  AlertTriangle,
  Target,
  Lightbulb,
  Shield,
  Star,
  TrendingUp,
  Clock,
  ArrowRight,
  RefreshCw,
  Mail,
  Loader2,
} from "lucide-react";

// Mapa de cores por área
const AREA_BORDER_COLORS: Record<string, string> = {
  "Saúde Física": "border-l-area-1",
  "Saúde Mental": "border-l-area-2",
  "Saúde Espiritual": "border-l-area-3",
  "Vida Pessoal": "border-l-area-4",
  "Vida Amorosa": "border-l-area-5",
  "Vida Familiar": "border-l-area-6",
  "Vida Social": "border-l-area-7",
  "Vida Profissional": "border-l-area-8",
  "Finanças": "border-l-area-9",
  "Educação": "border-l-area-10",
  "Inovação": "border-l-area-11",
  "Lazer": "border-l-area-12",
};

export default function Result() {
  const { token } = useParams<{ token: string }>();
  const location = useLocation();
  const diagnosticId = (location.state as { diagnosticId?: string } | null)?.diagnosticId;
  const [data, setData] = useState<DiagnosticResultResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [npsSent, setNpsSent] = useState(false);
  const [npsScore, setNpsScore] = useState<number | null>(null);
  const [waitlistEmail, setWaitlistEmail] = useState("");
  const [waitlistSent, setWaitlistSent] = useState(false);
  const [waitlistMessage, setWaitlistMessage] = useState("");
  const [waitlistSubmitting, setWaitlistSubmitting] = useState(false);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }
    getResultByToken(token)
      .then(setData)
      .catch((e) => setError(e?.response?.data?.detail ?? "Erro ao carregar resultado"))
      .finally(() => setLoading(false));
  }, [token]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-subtle">
        <div className="text-center space-y-4">
          <Loader2 className="w-10 h-10 animate-spin text-primary mx-auto" />
          <p className="text-muted-foreground">Carregando resultado...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-subtle">
        <Card className="max-w-md text-center p-8">
          <AlertTriangle className="w-12 h-12 text-destructive mx-auto mb-4" />
          <p className="text-destructive mb-4">{error ?? "Resultado não encontrado."}</p>
          <Link to="/" className={cn(buttonVariants({ variant: "outline" }))}>
            Voltar ao início
          </Link>
        </Card>
      </div>
    );
  }

  const vetorEstado = data.vetor_estado;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <div className="min-h-screen p-4 md:p-6 bg-gradient-subtle">
      <motion.div
        className="max-w-3xl mx-auto space-y-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* HEADER / VETOR DE ESTADO */}
        <motion.div variants={itemVariants}>
          <Card variant="elevated" className="overflow-hidden">
            <div className="h-2 bg-gradient-primary" />
            <CardHeader className="text-center pb-4">
              <h1 className="text-3xl font-bold font-display text-gradient">
                Seu Diagnóstico NARA
              </h1>
              <p className="text-sm text-muted-foreground">
                Transformação Narrativa · Metodologia Phellipe Oliveira
              </p>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Vetor de Estado - Cards em grid */}
              {vetorEstado && (
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="p-5 rounded-xl bg-primary/5 border border-primary/20 hover:shadow-card transition-shadow">
                    <div className="flex items-center gap-2 mb-2">
                      <Zap className="w-5 h-5 text-primary" />
                      <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide">
                        Motor Dominante
                      </p>
                    </div>
                    <p className="font-bold text-xl text-primary">{vetorEstado.motor_dominante}</p>
                  </div>
                  <div className="p-5 rounded-xl bg-accent/5 border border-accent/20 hover:shadow-card transition-shadow">
                    <div className="flex items-center gap-2 mb-2">
                      <Map className="w-5 h-5 text-accent" />
                      <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide">
                        Estágio da Jornada
                      </p>
                    </div>
                    <p className="font-bold text-xl text-accent">{vetorEstado.estagio_jornada}</p>
                  </div>
                  <div className="p-5 rounded-xl bg-destructive/5 border border-destructive/20 sm:col-span-2 hover:shadow-card transition-shadow">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertTriangle className="w-5 h-5 text-destructive" />
                      <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide">
                        Crise Raiz Identificada
                      </p>
                    </div>
                    <p className="font-semibold text-lg text-destructive">{vetorEstado.crise_raiz}</p>
                  </div>
                  <div className="p-5 rounded-xl bg-muted sm:col-span-2 hover:shadow-card transition-shadow">
                    <div className="flex items-center gap-2 mb-2">
                      <Target className="w-5 h-5 text-foreground" />
                      <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide">
                        Necessidade Atual
                      </p>
                    </div>
                    <p className="text-sm text-foreground">{vetorEstado.necessidade_atual}</p>
                  </div>
                </div>
              )}

              {/* Executive Summary */}
              <div className="pt-4 border-t">
                <h2 className="font-semibold mb-3 flex items-center gap-2">
                  <Lightbulb className="w-5 h-5 text-accent-warm" />
                  Diagnóstico Narrativo
                </h2>
                <p className="text-sm text-muted-foreground whitespace-pre-wrap leading-relaxed">
                  {data.executive_summary}
                </p>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* MEMÓRIAS VERMELHAS */}
        {data.memorias_vermelhas && data.memorias_vermelhas.length > 0 && (
          <motion.div variants={itemVariants}>
            <Card>
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-destructive/10 flex items-center justify-center">
                    <AlertTriangle className="w-5 h-5 text-destructive" />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold font-display">Memórias Vermelhas</h2>
                    <p className="text-sm text-muted-foreground">
                      Frases suas que revelam conflitos não dominados
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                {data.memorias_vermelhas.map((memoria, i) => (
                  <div
                    key={i}
                    className="p-4 rounded-xl bg-destructive/5 border-l-4 border-destructive"
                  >
                    <p className="text-sm italic text-foreground">"{memoria}"</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* ÂNCORAS PRÁTICAS SUGERIDAS */}
        {data.ancoras_sugeridas && data.ancoras_sugeridas.length > 0 && (
          <motion.div variants={itemVariants}>
            <Card>
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-accent-fresh/10 flex items-center justify-center">
                    <Shield className="w-5 h-5 text-accent-fresh" />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold font-display">Âncoras Práticas</h2>
                    <p className="text-sm text-muted-foreground">
                      Ações concretas para encarnar sua nova identidade
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {data.ancoras_sugeridas.map((ancora, i) => (
                    <div key={i} className="flex items-start gap-4 p-4 rounded-xl bg-accent-fresh/5">
                      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-fresh text-white flex items-center justify-center text-sm font-bold">
                        {i + 1}
                      </div>
                      <p className="text-sm font-medium text-foreground pt-1">{ancora}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* PONTOS FORTES */}
        {data.strengths && data.strengths.length > 0 && (
          <motion.div variants={itemVariants}>
            <Card>
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-accent-warm/10 flex items-center justify-center">
                    <Star className="w-5 h-5 text-accent-warm" />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold font-display">Capital Simbólico</h2>
                    <p className="text-sm text-muted-foreground">Recursos e forças identificados</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {data.strengths.map((s, i) => (
                    <li key={i} className="flex items-start gap-3 text-sm">
                      <TrendingUp className="w-4 h-4 text-accent-warm mt-0.5 flex-shrink-0" />
                      <span className="text-muted-foreground">{s}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* ANÁLISE POR ÁREA */}
        {data.area_analysis && data.area_analysis.length > 0 && (
          <motion.div variants={itemVariants}>
            <Card>
              <CardHeader className="pb-4">
                <h2 className="text-lg font-bold font-display">Análise do Círculo Narrativo</h2>
                <p className="text-sm text-muted-foreground">As 12 Áreas Estruturantes</p>
              </CardHeader>
              <CardContent className="space-y-4">
                {data.area_analysis.map((area, i) => (
                  <div
                    key={i}
                    className={cn(
                      "p-5 rounded-xl border border-l-4 hover:shadow-card transition-shadow",
                      AREA_BORDER_COLORS[area.area_name] || "border-l-primary"
                    )}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="font-semibold text-foreground">{area.area_name}</h3>
                      <span
                        className={cn(
                          "px-3 py-1 rounded-full text-xs font-semibold",
                          area.status === "crítico" &&
                            "bg-destructive/10 text-destructive",
                          area.status === "atenção" &&
                            "bg-yellow-500/10 text-yellow-700 dark:text-yellow-500",
                          area.status === "estável" &&
                            "bg-blue-500/10 text-blue-700 dark:text-blue-500",
                          area.status === "forte" &&
                            "bg-green-500/10 text-green-700 dark:text-green-500"
                        )}
                      >
                        {area.status}
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground mb-3">{area.analysis}</p>
                    {area.key_insight && (
                      <p className="text-sm font-medium italic border-l-4 border-primary/50 pl-4 text-foreground bg-primary/5 py-2 rounded-r-lg">
                        {area.key_insight}
                      </p>
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* RECOMENDAÇÕES */}
        {data.recommendations && data.recommendations.length > 0 && (
          <motion.div variants={itemVariants}>
            <Card>
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                    <ArrowRight className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold font-display">
                      Plano de Assunção Intencional
                    </h2>
                    <p className="text-sm text-muted-foreground">Próximos passos para sua travessia</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {data.recommendations.map((r, i) => (
                    <div
                      key={i}
                      className="p-4 rounded-xl border-l-4 border-primary bg-muted/50"
                    >
                      <p className="text-sm font-medium mb-2 text-foreground">{r.action}</p>
                      <div className="flex flex-wrap gap-2 text-xs">
                        <span
                          className={cn(
                            "px-2.5 py-1 rounded-full font-medium",
                            r.timeframe === "imediato" && "bg-destructive/10 text-destructive",
                            r.timeframe === "curto_prazo" && "bg-accent-warm/10 text-accent-warm",
                            r.timeframe === "medio_prazo" && "bg-accent/10 text-accent"
                          )}
                        >
                          <Clock className="w-3 h-3 inline mr-1" />
                          {r.timeframe === "imediato" && "Imediato"}
                          {r.timeframe === "curto_prazo" && "Curto prazo"}
                          {r.timeframe === "medio_prazo" && "Médio prazo"}
                        </span>
                        {r.area_related && (
                          <span className="px-2.5 py-1 rounded-full bg-background text-muted-foreground">
                            {r.area_related}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* NPS */}
        {!npsSent && diagnosticId && (
          <motion.div variants={itemVariants}>
            <Card>
              <CardHeader className="pb-4">
                <h2 className="font-semibold">Como foi sua experiência? (NPS 0-10)</h2>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((n) => (
                    <Button
                      key={n}
                      type="button"
                      variant={npsScore === n ? "gradient" : "outline"}
                      size="sm"
                      className="w-10 h-10"
                      onClick={async () => {
                        setNpsScore(n);
                        try {
                          if (diagnosticId) {
                            await submitFeedback({
                              diagnostic_id: diagnosticId,
                              nps_score: n,
                              feedback_type: "private",
                            });
                          }
                          setNpsSent(true);
                        } catch {
                          // ignore
                        }
                      }}
                    >
                      {n}
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* WAITLIST */}
        <motion.div variants={itemVariants}>
          <Card className="bg-primary/5 border-primary/20">
            <CardHeader className="pb-4">
              <div className="flex items-center gap-3">
                <Mail className="w-5 h-5 text-primary" />
                <div>
                  <h2 className="font-semibold">A nova NARA está chegando</h2>
                  <p className="text-sm text-muted-foreground">
                    Phellipe está preparando uma versão 100x mais robusta e inovadora. Deixe seu
                    e-mail para ser avisado em primeira mão e não perder essa evolução.
                  </p>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              {!waitlistSent && (
                <form
                  className="flex gap-2"
                  onSubmit={async (e) => {
                    e.preventDefault();
                    if (!waitlistEmail.trim()) return;
                    setWaitlistSubmitting(true);
                    setWaitlistMessage("");
                    try {
                      const res = await joinWaitlist({
                        email: waitlistEmail.trim(),
                        source: "diagnostic",
                        diagnostic_id: diagnosticId ?? undefined,
                      });
                      setWaitlistSent(true);
                      setWaitlistMessage(`${res.message} Você será avisado quando a nova NARA for lançada.`);
                    } catch (err: unknown) {
                      const detail =
                        err && typeof err === "object" && "response" in err
                          ? (err as { response?: { data?: { detail?: string | string[] } } }).response?.data?.detail
                          : null;
                      if (Array.isArray(detail)) {
                        setWaitlistMessage(detail.join(" "));
                      } else if (typeof detail === "string" && detail.trim()) {
                        setWaitlistMessage(detail);
                      } else {
                        setWaitlistMessage("Erro ao cadastrar.");
                      }
                    } finally {
                      setWaitlistSubmitting(false);
                    }
                  }}
                >
                  <Input
                    type="email"
                    placeholder="seu@email.com"
                    value={waitlistEmail}
                    onChange={(e) => setWaitlistEmail(e.target.value)}
                    className="flex-1"
                    disabled={waitlistSubmitting}
                  />
                  <Button type="submit" variant="gradient" disabled={waitlistSubmitting}>
                    {waitlistSubmitting ? "Enviando..." : "Quero ser avisado"}
                  </Button>
                </form>
              )}
              {waitlistMessage && (
                <p className="text-sm text-muted-foreground mt-2">{waitlistMessage}</p>
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* ACTIONS */}
        <motion.div variants={itemVariants} className="flex justify-center gap-3 pb-8">
          <Link to="/" className={buttonVariants({ variant: "outline" })}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Fazer novo diagnóstico
          </Link>
        </motion.div>
      </motion.div>
    </div>
  );
}
