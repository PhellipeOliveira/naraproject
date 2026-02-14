import { useEffect, useState } from "react";
import { useParams, useLocation, Link } from "react-router-dom";
import { getResultByToken } from "../api/diagnostic";
import { submitFeedback } from "../api/feedback";
import { joinWaitlist } from "../api/waitlist";
import type { DiagnosticResultResponse } from "../types";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

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
        <Button asChild variant="outline" className="mt-4">
          <Link to="/">Voltar ao início</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4 max-w-3xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <h1 className="text-2xl font-bold">Seu Diagnóstico NARA</h1>
          <p className="text-muted-foreground">
            Fase da jornada: {data.phase_identified} · Motor dominante: {data.motor_dominante}
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-4">
            <div className="text-4xl font-bold text-primary">
              {data.overall_score != null ? data.overall_score.toFixed(1) : "—"}
            </div>
            <span className="text-muted-foreground">Score geral (0–10)</span>
          </div>
          <div>
            <h2 className="font-semibold mb-2">Resumo</h2>
            <p className="text-sm text-muted-foreground whitespace-pre-wrap">
              {data.executive_summary}
            </p>
          </div>
          {data.strengths && data.strengths.length > 0 && (
            <div>
              <h2 className="font-semibold mb-2">Pontos fortes</h2>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
                {data.strengths.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          )}
          {data.recommendations && data.recommendations.length > 0 && (
            <div>
              <h2 className="font-semibold mb-2">Recomendações</h2>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
                {data.recommendations.map((r, i) => (
                  <li key={i}>{r.action}</li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>

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
        <Button asChild variant="outline">
          <Link to="/">Fazer novo diagnóstico</Link>
        </Button>
      </div>
    </div>
  );
}
