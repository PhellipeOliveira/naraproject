import { Link } from "react-router-dom";
import { buttonVariants } from "../components/ui/button";
import { cn } from "../lib/utils";

export default function PrivacyPolicy() {
  return (
    <div className="min-h-screen bg-background p-6 md:p-10">
      <div className="max-w-3xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Politica de Privacidade</h1>
          <p className="text-sm text-muted-foreground mt-2">
            Ultima atualizacao: 2026-02-18
          </p>
        </div>

        <section className="space-y-2">
          <h2 className="text-xl font-semibold">1. Dados coletados</h2>
          <p className="text-sm text-muted-foreground">
            Coletamos email, respostas do diagnostico e metadados tecnicos minimos para entregar o
            relatorio e operar o servico.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-xl font-semibold">2. Finalidade</h2>
          <p className="text-sm text-muted-foreground">
            Os dados sao usados para gerar o diagnostico narrativo, melhorar o produto e realizar
            comunicacoes autorizadas pelo usuario.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-xl font-semibold">3. Compartilhamento</h2>
          <p className="text-sm text-muted-foreground">
            Dados podem ser processados por provedores operacionais (infraestrutura, email e IA),
            com controles de seguranca e acesso restrito.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-xl font-semibold">4. Retencao e exclusao</h2>
          <p className="text-sm text-muted-foreground">
            Mantemos dados pelo tempo necessario a operacao do servico. Solicitacoes de acesso,
            portabilidade e exclusao podem ser feitas pelos endpoints de privacidade da API.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-xl font-semibold">5. Direitos do titular (LGPD)</h2>
          <p className="text-sm text-muted-foreground">
            Voce pode solicitar confirmacao de tratamento, acesso, correcao, portabilidade e
            eliminacao dos dados conforme a LGPD.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-xl font-semibold">6. Contato</h2>
          <p className="text-sm text-muted-foreground">
            Para temas de privacidade: contato@phellipeoliveira.org
          </p>
        </section>

        <Link to="/" className={cn(buttonVariants({ variant: "outline" }))}>
          Voltar ao inicio
        </Link>
      </div>
    </div>
  );
}
