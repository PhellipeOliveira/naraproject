import { useEffect, useState } from "react";
import { useParams, useLocation, Link } from "react-router-dom";
import { getResultByToken } from "../api/diagnostic";
import { submitFeedback } from "../api/feedback";
import { joinWaitlist } from "../api/waitlist";
import type { DiagnosticResultResponse } from "../types";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { Button, buttonVariants } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { cn } from "../lib/utils";

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
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-muted-foreground">Carregando resultado...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4">
        <p className="text-destructive">{error ?? "Resultado não encontrado."}</p>
        <Link to="/" className={cn(buttonVariants({ variant: "outline" }), "mt-4")}>
          Voltar ao início
        </Link>
      </div>
    );
  }

  const vetorEstado = data.vetor_estado;

  return (
    <div className="min-h-screen p-4 max-w-3xl mx-auto space-y-6">
      {/* VETOR DE ESTADO */}
      <Card>
        <CardHeader>
          <h1 className="text-2xl font-bold">Seu Diagnóstico NARA</h1>
          <p className="text-sm text-muted-foreground">
            Transformação Narrativa · Metodologia Phellipe Oliveira
          </p>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Vetor de Estado - Cards em grid */}
          {vetorEstado && (
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="p-4 rounded-lg bg-primary/5 border border-primary/10">
                <p className="text-xs text-muted-foreground mb-1">Motor Dominante</p>
                <p className="font-semibold text-lg text-primary">{vetorEstado.motor_dominante}</p>
              </div>
              <div className="p-4 rounded-lg bg-primary/5 border border-primary/10">
                <p className="text-xs text-muted-foreground mb-1">Estágio da Jornada</p>
                <p className="font-semibold text-lg text-primary">{vetorEstado.estagio_jornada}</p>
              </div>
              <div className="p-4 rounded-lg bg-destructive/5 border border-destructive/10 sm:col-span-2">
                <p className="text-xs text-muted-foreground mb-1">Crise Raiz Identificada</p>
                <p className="font-semibold text-destructive">{vetorEstado.crise_raiz}</p>
              </div>
              <div className="p-4 rounded-lg bg-muted sm:col-span-2">
                <p className="text-xs text-muted-foreground mb-1">Necessidade Atual</p>
                <p className="text-sm">{vetorEstado.necessidade_atual}</p>
              </div>
            </div>
          )}

          {/* Executive Summary */}
          <div>
            <h2 className="font-semibold mb-2">Diagnóstico Narrativo</h2>
            <p className="text-sm text-muted-foreground whitespace-pre-wrap">
              {data.executive_summary}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* MEMÓRIAS VERMELHAS */}
      {data.memorias_vermelhas && data.memorias_vermelhas.length > 0 && (
        <Card>
          <CardHeader>
            <h2 className="text-lg font-bold">Memórias Vermelhas</h2>
            <p className="text-sm text-muted-foreground">
              Frases suas que revelam conflitos não dominados
            </p>
          </CardHeader>
          <CardContent className="space-y-3">
            {data.memorias_vermelhas.map((memoria, i) => (
              <div key={i} className="p-3 rounded-lg bg-destructive/5 border-l-4 border-destructive">
                <p className="text-sm italic">"{memoria}"</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* ÂNCORAS PRÁTICAS SUGERIDAS */}
      {data.ancoras_sugeridas && data.ancoras_sugeridas.length > 0 && (
        <Card>
          <CardHeader>
            <h2 className="text-lg font-bold">Âncoras Práticas para Assunção</h2>
            <p className="text-sm text-muted-foreground">
              Ações concretas para encarnar sua nova identidade
            </p>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {data.ancoras_sugeridas.map((ancor, i) => (
                <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-primary/5">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xs font-bold">
                    {i + 1}
                  </div>
                  <p className="text-sm font-medium">{ancor}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* PONTOS FORTES */}
      {data.strengths && data.strengths.length > 0 && (
        <Card>
          <CardHeader>
            <h2 className="text-lg font-bold">Capital Simbólico</h2>
            <p className="text-sm text-muted-foreground">Recursos e forças identificados</p>
          </CardHeader>
          <CardContent>
            <ul className="list-disc list-inside text-sm space-y-2">
              {data.strengths.map((s, i) => (
                <li key={i} className="text-muted-foreground">{s}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* ANÁLISE POR ÁREA */}
      {data.area_analysis && data.area_analysis.length > 0 && (
        <Card>
          <CardHeader>
            <h2 className="text-lg font-bold">Análise do Círculo Narrativo</h2>
            <p className="text-sm text-muted-foreground">As 12 Áreas Estruturantes</p>
          </CardHeader>
          <CardContent className="space-y-4">
            {data.area_analysis.map((area, i) => (
              <div key={i} className="p-4 rounded-lg border">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold">{area.area_name}</h3>
                  <span className={cn(
                    "px-2 py-1 rounded text-xs font-medium",
                    area.status === "crítico" && "bg-destructive/10 text-destructive",
                    area.status === "atenção" && "bg-yellow-500/10 text-yellow-700 dark:text-yellow-500",
                    area.status === "estável" && "bg-blue-500/10 text-blue-700 dark:text-blue-500",
                    area.status === "forte" && "bg-green-500/10 text-green-700 dark:text-green-500"
                  )}>
                    {area.status}
                  </span>
                </div>
                <p className="text-sm text-muted-foreground mb-2">{area.analysis}</p>
                {area.key_insight && (
                  <p className="text-sm font-medium italic border-l-4 border-primary pl-3">
                    {area.key_insight}
                  </p>
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* RECOMENDAÇÕES */}
      {data.recommendations && data.recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <h2 className="text-lg font-bold">Plano de Assunção Intencional (M2X)</h2>
            <p className="text-sm text-muted-foreground">Próximos passos para sua travessia</p>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {data.recommendations.map((r, i) => (
                <div key={i} className="p-3 rounded-lg border-l-4 border-primary bg-muted">
                  <p className="text-sm font-medium mb-1">{r.action}</p>
                  <div className="flex gap-2 text-xs text-muted-foreground">
                    <span className="px-2 py-0.5 rounded bg-background">
                      {r.timeframe === "imediato" && "Imediato"}
                      {r.timeframe === "curto_prazo" && "Curto prazo"}
                      {r.timeframe === "medio_prazo" && "Médio prazo"}
                    </span>
                    {r.area_related && (
                      <span className="px-2 py-0.5 rounded bg-background">
                        {r.area_related}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {!npsSent && diagnosticId && (
        <Card>
          <CardHeader>
            <h2 className="font-semibold">Como foi sua experiência? (NPS 0-10)</h2>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-2">
            {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((n) => (
              <Button
                key={n}
                type="button"
                variant={npsScore === n ? "default" : "outline"}
                size="sm"
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
          </CardContent>
        </Card>
      )}

      {!waitlistSent && (
        <Card>
          <CardHeader>
            <h2 className="font-semibold">Lista de espera</h2>
            <p className="text-sm text-muted-foreground">
              Receba novidades e avisos de novas funcionalidades.
            </p>
          </CardHeader>
          <CardContent>
            <form
              className="flex gap-2"
              onSubmit={async (e) => {
                e.preventDefault();
                if (!waitlistEmail.trim()) return;
                try {
                  const res = await joinWaitlist({
                    email: waitlistEmail.trim(),
                    source: "diagnostic",
                    diagnostic_id: token ?? undefined,
                  });
                  setWaitlistSent(true);
                  setWaitlistMessage(res.message);
                } catch {
                  setWaitlistMessage("Erro ao cadastrar.");
                }
              }}
            >
              <Input
                type="email"
                placeholder="seu@email.com"
                value={waitlistEmail}
                onChange={(e) => setWaitlistEmail(e.target.value)}
                className="flex-1"
              />
              <Button type="submit">Entrar</Button>
            </form>
            {waitlistMessage && (
              <p className="text-sm text-muted-foreground mt-2">{waitlistMessage}</p>
            )}
          </CardContent>
        </Card>
      )}

      <div className="flex justify-center gap-2">
        <Link to="/" className={buttonVariants({ variant: "outline" })}>
          Fazer novo diagnóstico
        </Link>
      </div>
    </div>
  );
}
