import { useEffect, useMemo, useRef, useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card, CardContent, CardHeader } from "./ui/card";

interface SharePopupProps {
  open: boolean;
  onClose: () => void;
  url: string;
  title?: string;
  shareText?: string;
}

export function SharePopup({
  open,
  onClose,
  url,
  title = "Compartilhar",
  shareText = "Faça seu Diagnóstico de Transformação Narrativa na NARA.",
}: SharePopupProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [copyFeedback, setCopyFeedback] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    const onEsc = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };
    window.addEventListener("keydown", onEsc);
    return () => window.removeEventListener("keydown", onEsc);
  }, [open, onClose]);

  useEffect(() => {
    if (!open) return;
    const timer = window.setTimeout(() => {
      inputRef.current?.focus();
      inputRef.current?.select();
    }, 30);
    return () => window.clearTimeout(timer);
  }, [open]);

  useEffect(() => {
    if (!copyFeedback) return;
    const timer = window.setTimeout(() => setCopyFeedback(null), 2500);
    return () => window.clearTimeout(timer);
  }, [copyFeedback]);

  const links = useMemo(() => {
    const encodedUrl = encodeURIComponent(url);
    const encodedText = encodeURIComponent(`${shareText}\n${url}`);

    return [
      {
        key: "whatsapp",
        label: "WhatsApp",
        href: `https://wa.me/?text=${encodedText}`,
      },
      {
        key: "facebook",
        label: "Facebook",
        href: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`,
      },
      {
        key: "x",
        label: "X",
        href: `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodeURIComponent(shareText)}`,
      },
      {
        key: "email",
        label: "E-mail",
        href: `mailto:?subject=${encodeURIComponent("Convite para o Diagnóstico NARA")}&body=${encodedText}`,
      },
    ];
  }, [shareText, url]);

  const onCopy = async () => {
    try {
      await navigator.clipboard.writeText(url);
      setCopyFeedback("Link copiado!");
    } catch {
      setCopyFeedback("Não foi possível copiar o link.");
    }
  };

  if (!open) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      onClick={onClose}
      role="presentation"
    >
      <Card
        className="w-full max-w-xl"
        onClick={(event) => event.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-label={title}
      >
        <CardHeader className="border-b border-primary/30 pb-4">
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-xl font-semibold">{title}</h2>
            <Button variant="outline" size="sm" onClick={onClose}>
              Fechar
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-5 pt-5">
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-[1fr_auto]">
            <Input ref={inputRef} value={url} readOnly aria-label="Link para compartilhar" />
            <Button onClick={onCopy}>Copiar</Button>
          </div>
          {copyFeedback && <p className="text-sm text-muted-foreground">{copyFeedback}</p>}

          <div className="flex flex-wrap gap-2">
            {links.map((item) => (
              <a
                key={item.key}
                href={item.href}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex min-w-24 items-center justify-center rounded-full border px-4 py-2 text-sm font-medium hover:bg-muted"
                aria-label={`Compartilhar via ${item.label}`}
              >
                {item.label}
              </a>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
