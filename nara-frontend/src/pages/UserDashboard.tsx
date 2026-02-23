import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  startMicroDiagnostic,
  getResultByToken,
  getResultPdfByToken,
  getOwnerEmailByToken,
} from "../api/diagnostic";
import { getMe, getMyDiagnostics } from "../api/auth";
import type { DiagnosticResultResponse } from "../types";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { Button, buttonVariants } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { SharePopup } from "../components/SharePopup";
import { cn } from "../lib/utils";
import { supabaseClient } from "../lib/supabaseClient";

const areaById: Record<number, string> = {
  1: "Saúde Física",
  2: "Saúde Mental",
  3: "Saúde Espiritual",
  4: "Vida Pessoal",
  5: "Vida Amorosa",
  6: "Vida Familiar",
  7: "Vida Social",
  8: "Vida Profissional",
  9: "Finanças",
  10: "Educação",
  11: "Inovação",
  12: "Lazer",
};

export default function UserDashboard() {
  const navigate = useNavigate();
  const { token } = useParams<{ token: string }>();
  const [activeToken, setActiveToken] = useState<string | null>(token ?? null);
  const [data, setData] = useState<DiagnosticResultResponse | null>(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [hasSession, setHasSession] = useState(false);
  const [ownerEmail, setOwnerEmail] = useState<string | null>(null);
  const [authWarning, setAuthWarning] = useState<string | null>(null);
  const [myDiagnostics, setMyDiagnostics] = useState<
    Array<{
      id: string;
      result_token: string;
      status: string;
      created_at: string;
    }>
  >([]);
  const [startingArea, setStartingArea] = useState<string | null>(null);
  const [sharePopupOpen, setSharePopupOpen] = useState(false);
  const [showPasswordSetup, setShowPasswordSetup] = useState(false);
  const [setupEmail, setSetupEmail] = useState("");
  const [setupPassword, setSetupPassword] = useState("");
  const [setupPasswordConfirm, setSetupPasswordConfirm] = useState("");
  const [setupLoading, setSetupLoading] = useState(false);
  const [setupFeedback, setSetupFeedback] = useState<string | null>(null);

  const startDiagnosticUrl = `${typeof window !== "undefined" ? window.location.origin : ""}/diagnostico/iniciar`;
  const isLinkMode = Boolean(token) && !hasSession;

  useEffect(() => {
    async function bootstrapAuthAndData() {
      setAuthLoading(true);
      setLoading(true);
      setError(null);
      setAuthWarning(null);
      setSetupFeedback(null);

      const { data: sessionData } = await supabaseClient.auth.getSession();
      const session = sessionData.session;
      if (!session) {
        setHasSession(false);
        setMyDiagnostics([]);
        if (token) {
          try {
            const [result, owner] = await Promise.all([
              getResultByToken(token),
              getOwnerEmailByToken(token).catch(() => null),
            ]);
            setActiveToken(token);
            setData(result);
            const normalizedOwner = (owner?.email || "").trim().toLowerCase();
            setOwnerEmail(normalizedOwner || null);
            setSetupEmail(normalizedOwner || "");
          } catch (e: unknown) {
            const message =
              e && typeof e === "object" && "response" in e
                ? (e as { response?: { data?: { detail?: string } } }).response?.data?.detail
                : null;
            setError(typeof message === "string" ? message : "Erro ao carregar dashboard");
          } finally {
            setAuthLoading(false);
            setLoading(false);
          }
          return;
        }
        const next = token ? `/meu-diagnostico/${token}` : "/meu-diagnostico";
        navigate(`/entrar?next=${encodeURIComponent(next)}`, { replace: true });
        return;
      }

      try {
        setHasSession(true);
        const me = await getMe();
        const userEmail = (me.email || "").trim().toLowerCase();
        const diagnostics = await getMyDiagnostics();
        setMyDiagnostics(diagnostics.items ?? []);

        const selectedToken = token ?? diagnostics.items?.[0]?.result_token ?? null;
        setActiveToken(selectedToken);
        if (!selectedToken) {
          setData(null);
          setOwnerEmail(null);
          setSetupEmail(userEmail || "");
          return;
        }
        const [result, owner] = await Promise.all([
          getResultByToken(selectedToken),
          getOwnerEmailByToken(selectedToken).catch(() => null),
        ]);
        setData(result);
        const normalizedOwner = (owner?.email || "").trim().toLowerCase();
        setOwnerEmail(normalizedOwner || null);
        setSetupEmail(normalizedOwner || userEmail || "");
        if (token && normalizedOwner && userEmail && normalizedOwner !== userEmail) {
          setAuthWarning(
            `Este diagnóstico foi feito com ${normalizedOwner}. Você entrou com ${userEmail}. Para ver este item na sua lista, use o mesmo e-mail do diagnóstico ou acesse pelo link recebido no e-mail.`
          );
        }
      } catch (e: unknown) {
        const message =
          e && typeof e === "object" && "response" in e
            ? (e as { response?: { data?: { detail?: string } } }).response?.data?.detail
            : null;
        setError(typeof message === "string" ? message : "Erro ao carregar dashboard");
      } finally {
        setAuthLoading(false);
        setLoading(false);
      }
    }

    bootstrapAuthAndData();
  }, [navigate, token]);

  const allAreas = useMemo(
    () =>
      Object.values(areaById).map((areaName) => {
        const match = data?.area_analysis?.find((a) => a.area_name === areaName);
        return { area: areaName, status: match?.status ?? "sem dados" };
      }),
    [data?.area_analysis]
  );

  const handleContinueWithGoogle = () => {
    if (!activeToken) return;
    const next = `/meu-diagnostico/${activeToken}`;
    navigate(`/entrar?next=${encodeURIComponent(next)}`);
  };

  const handleSetPassword = async () => {
    setSetupFeedback(null);
    const email = setupEmail.trim().toLowerCase();
    if (!email) {
      setSetupFeedback("Informe o e-mail para criar acesso com senha.");
      return;
    }
    if (!setupPassword || setupPassword.length < 8) {
      setSetupFeedback("A senha deve ter ao menos 8 caracteres.");
      return;
    }
    if (setupPassword !== setupPasswordConfirm) {
      setSetupFeedback("As senhas não coincidem.");
      return;
    }

    setSetupLoading(true);
    try {
      const redirectTo = `${window.location.origin}/meu-diagnostico/${activeToken ?? ""}`;
      const { error: signUpError } = await supabaseClient.auth.signUp({
        email,
        password: setupPassword,
        options: { emailRedirectTo: redirectTo },
      });
      if (signUpError) {
        throw signUpError;
      }
      setSetupFeedback(
        "Conta criada. Se o Supabase exigir confirmação, verifique seu e-mail para ativar o acesso."
      );
      setSetupPassword("");
      setSetupPasswordConfirm("");
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : "Não foi possível criar acesso com senha.";
      setSetupFeedback(message);
    } finally {
      setSetupLoading(false);
    }
  };

  async function handleDownloadPdf() {
    if (!activeToken) return;
    setPdfLoading(true);
    try {
      const blob = await getResultPdfByToken(activeToken);
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `diagnostico-nara-${activeToken}.pdf`;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(url);
    } finally {
      setPdfLoading(false);
    }
  }

  async function handleStartMicroDiagnostic(area: string) {
    if (!activeToken) return;
    setStartingArea(area);
    try {
      const started = await startMicroDiagnostic(activeToken, area);
      navigate(`/meu-diagnostico/${activeToken}/micro/${started.micro_id}`);
    } finally {
      setStartingArea(null);
    }
  }

  if (authLoading || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-muted-foreground">Carregando dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 p-4">
        <p className="text-destructive">{error}</p>
        <Link to="/" className={buttonVariants({ variant: "outline" })}>
          Voltar ao início
        </Link>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen p-4 max-w-5xl mx-auto space-y-6">
        <Card>
          <CardHeader>
            <h1 className="text-2xl font-bold">Meu Dashboard NARA</h1>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm text-muted-foreground">
              Nenhum diagnóstico finalizado encontrado para sua conta.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link to="/diagnostico/iniciar" className={buttonVariants({ variant: "outline" })}>
                Iniciar diagnóstico
              </Link>
              <Button variant="outline" onClick={() => setSharePopupOpen(true)}>
                Convidar alguém a fazer o diagnóstico
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4 max-w-5xl mx-auto space-y-6">
      {isLinkMode && (
        <Card className="border-primary/30 bg-primary/5">
          <CardHeader>
            <h2 className="text-lg font-bold">Acesso por link</h2>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm text-muted-foreground">
              Você está acessando este painel por link do e-mail. Se quiser acessar de qualquer
              lugar sem depender do link, vincule uma conta.
            </p>
            {ownerEmail && (
              <p className="text-sm">
                <span className="font-medium">E-mail do diagnóstico:</span> {ownerEmail}
              </p>
            )}
            <div className="flex flex-wrap gap-2">
              <Button onClick={handleContinueWithGoogle}>Entrar com Google</Button>
              <Button
                variant="outline"
                onClick={() => setShowPasswordSetup((v) => !v)}
              >
                {showPasswordSetup ? "Cancelar senha" : "Definir senha"}
              </Button>
            </div>
            {showPasswordSetup && (
              <div className="space-y-2 rounded-lg border p-3">
                <p className="text-sm font-medium">Criar acesso com e-mail e senha</p>
                <Input
                  type="email"
                  value={setupEmail}
                  onChange={(e) => !isLinkMode && setSetupEmail(e.target.value)}
                  placeholder="seu@email.com"
                  readOnly={isLinkMode}
                  aria-readonly={isLinkMode}
                />
                <Input
                  type="password"
                  value={setupPassword}
                  onChange={(e) => setSetupPassword(e.target.value)}
                  placeholder="Senha (mínimo 8 caracteres)"
                />
                <Input
                  type="password"
                  value={setupPasswordConfirm}
                  onChange={(e) => setSetupPasswordConfirm(e.target.value)}
                  placeholder="Confirmar senha"
                />
                <Button onClick={handleSetPassword} disabled={setupLoading}>
                  {setupLoading ? "Salvando..." : "Criar acesso com senha"}
                </Button>
              </div>
            )}
            {setupFeedback && (
              <p className="text-sm text-muted-foreground">{setupFeedback}</p>
            )}
          </CardContent>
        </Card>
      )}

      {authWarning && (
        <Card className="border-destructive/30 bg-destructive/5">
          <CardContent className="p-4">
            <p className="text-sm text-destructive">{authWarning}</p>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <h1 className="text-2xl font-bold">Meu Dashboard NARA</h1>
          <p className="text-sm text-muted-foreground">
            Seu panorama completo de diagnóstico, evolução e próximos passos.
          </p>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-3">
          <Button onClick={handleDownloadPdf} disabled={pdfLoading}>
            {pdfLoading ? "Gerando PDF..." : "Baixar relatório em PDF"}
          </Button>
          {hasSession && (
            <Button
              variant="outline"
              onClick={async () => {
                await supabaseClient.auth.signOut();
                navigate("/entrar", { replace: true });
              }}
            >
              Sair
            </Button>
          )}
          <Link
            to={`/resultado/${activeToken}`}
            className={cn(buttonVariants({ variant: "outline" }))}
          >
            Ver página de resultado
          </Link>
          <Button variant="outline" onClick={() => setSharePopupOpen(true)}>
            Convidar alguém a fazer o diagnóstico
          </Button>
        </CardContent>
      </Card>

      {hasSession && myDiagnostics.length > 0 && (
        <Card>
          <CardHeader>
            <h2 className="text-lg font-bold">Meus diagnósticos</h2>
          </CardHeader>
          <CardContent className="space-y-2">
            {myDiagnostics.map((item) => (
              <div key={item.id} className="flex flex-wrap items-center justify-between gap-2 p-3 border rounded-lg">
                <div>
                  <p className="text-sm font-medium">Token: {item.result_token}</p>
                  <p className="text-xs text-muted-foreground">
                    Status: {item.status} · {new Date(item.created_at).toLocaleDateString("pt-BR")}
                  </p>
                </div>
                <Link
                  to={`/meu-diagnostico/${item.result_token}`}
                  className={buttonVariants({ variant: "outline" })}
                >
                  Abrir
                </Link>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <h2 className="text-lg font-bold">Vetor de Estado</h2>
        </CardHeader>
        <CardContent className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
          <div className="p-3 rounded bg-primary/10">
            <p className="text-xs text-muted-foreground">Motor Dominante</p>
            <p className="font-semibold">{data.vetor_estado?.motor_dominante}</p>
          </div>
          <div className="p-3 rounded bg-primary/10">
            <p className="text-xs text-muted-foreground">Estágio</p>
            <p className="font-semibold">{data.vetor_estado?.estagio_jornada}</p>
          </div>
          <div className="p-3 rounded bg-destructive/10">
            <p className="text-xs text-muted-foreground">Crise Raiz</p>
            <p className="font-semibold">{data.vetor_estado?.crise_raiz}</p>
          </div>
          <div className="p-3 rounded bg-muted">
            <p className="text-xs text-muted-foreground">Ponto de Entrada</p>
            <p className="font-semibold">{data.vetor_estado?.ponto_entrada_ideal}</p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <h2 className="text-lg font-bold">Círculo Narrativo (12 Áreas)</h2>
          <p className="text-sm text-muted-foreground">
            Mapa visual com status das áreas e foco para aprofundamento.
          </p>
        </CardHeader>
        <CardContent className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {allAreas.map(({ area, status }) => (
            <div key={area} className="p-3 border rounded-lg">
              <div className="flex items-center justify-between">
                <p className="font-medium">{area}</p>
                <span
                  className={cn(
                    "text-xs px-2 py-1 rounded",
                    status === "crítico" && "bg-destructive/10 text-destructive",
                    status === "atenção" && "bg-yellow-500/10 text-yellow-700 dark:text-yellow-500",
                    status === "estável" && "bg-blue-500/10 text-blue-700 dark:text-blue-500",
                    status === "forte" && "bg-green-500/10 text-green-700 dark:text-green-500",
                    status === "sem dados" && "bg-muted text-muted-foreground"
                  )}
                >
                  {status}
                </span>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <h2 className="text-lg font-bold">Microdiagnóstico por Área (5Q para 5Q)</h2>
          <p className="text-sm text-muted-foreground">
            Escolha uma área para iniciar um microdiagnóstico exclusivo. Ao concluir, você recebe um micro-relatório final.
          </p>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
            {Object.values(areaById).map((area) => (
              <Button
                key={area}
                variant="outline"
                disabled={startingArea === area}
                onClick={() => handleStartMicroDiagnostic(area)}
              >
                {startingArea === area ? "Iniciando..." : `Iniciar: ${area}`}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {data.memorias_vermelhas?.length > 0 && (
        <Card>
          <CardHeader>
            <h2 className="text-lg font-bold">Memórias Vermelhas</h2>
          </CardHeader>
          <CardContent className="space-y-2">
            {data.memorias_vermelhas.map((item, idx) => (
              <div key={idx} className="p-3 rounded border-l-4 border-destructive bg-destructive/5">
                <p className="text-sm italic">"{item}"</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
      <SharePopup
        open={sharePopupOpen}
        onClose={() => setSharePopupOpen(false)}
        url={startDiagnosticUrl}
      />
    </div>
  );
}
