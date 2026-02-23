import { useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { supabaseClient } from "../lib/supabaseClient";

export default function UserLogin() {
  const location = useLocation();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const nextPath = useMemo(() => {
    const params = new URLSearchParams(location.search);
    const next = params.get("next");
    return next && next.startsWith("/") ? next : "/meu-diagnostico";
  }, [location.search]);

  async function handleGoogleSignIn() {
    setLoading(true);
    setError(null);
    try {
      const redirectTo = `${window.location.origin}${nextPath}`;
      const { error: authError } = await supabaseClient.auth.signInWithOAuth({
        provider: "google",
        options: { redirectTo },
      });
      if (authError) {
        throw authError;
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao iniciar login com Google.");
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-background">
      <Card className="w-full max-w-md">
        <CardHeader>
          <h1 className="text-xl font-bold text-center">Entrar no Dashboard NARA</h1>
          <p className="text-sm text-muted-foreground text-center">
            Faça login com Google para acessar seus diagnósticos e microdiagnóstico.
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button className="w-full" onClick={handleGoogleSignIn} disabled={loading}>
            {loading ? "Redirecionando..." : "Entrar com Google"}
          </Button>
          {error && <p className="text-sm text-destructive">{error}</p>}
        </CardContent>
      </Card>
    </div>
  );
}
