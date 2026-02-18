import { useEffect, useState } from "react";
import { Button } from "./ui/button";

const CONSENT_KEY = "nara_cookie_consent_v1";

type ConsentValue = "accepted" | "rejected";

export function CookieConsentBanner() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const current = localStorage.getItem(CONSENT_KEY);
    if (!current) {
      setVisible(true);
    }
  }, []);

  const setConsent = (value: ConsentValue) => {
    localStorage.setItem(CONSENT_KEY, value);
    setVisible(false);
  };

  if (!visible) {
    return null;
  }

  return (
    <div className="fixed bottom-4 left-4 right-4 z-50">
      <div className="max-w-3xl mx-auto bg-card border rounded-lg p-4 shadow-lg">
        <p className="text-sm text-muted-foreground mb-3">
          Utilizamos cookies e armazenamento local para sessao, funcionamento do diagnostico e
          melhoria do servico. Voce pode aceitar ou recusar cookies nao essenciais.
        </p>
        <div className="flex gap-2 justify-end">
          <Button variant="outline" size="sm" onClick={() => setConsent("rejected")}>
            Recusar
          </Button>
          <Button size="sm" onClick={() => setConsent("accepted")}>
            Aceitar
          </Button>
        </div>
      </div>
    </div>
  );
}
