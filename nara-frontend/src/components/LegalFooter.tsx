import { Link } from "react-router-dom";

export function LegalFooter() {
  return (
    <footer className="pt-4 border-t text-xs text-muted-foreground">
      <div className="flex flex-wrap gap-3 items-center justify-center">
        <Link to="/politica-de-privacidade" className="hover:underline">
          Politica de Privacidade
        </Link>
        <span aria-hidden="true">|</span>
        <Link to="/termos-de-uso" className="hover:underline">
          Termos de Uso
        </Link>
      </div>
    </footer>
  );
}
