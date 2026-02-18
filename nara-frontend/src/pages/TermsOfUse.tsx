import { Link } from "react-router-dom";
import { buttonVariants } from "../components/ui/button";
import { cn } from "../lib/utils";

export default function TermsOfUse() {
  return (
    <div className="min-h-screen bg-background p-6 md:p-10">
      <div className="max-w-3xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Termos de Uso</h1>
          <p className="text-sm text-muted-foreground mt-2">
            Ultima atualizacao: 2026-02-18
          </p>
        </div>

        <section className="space-y-2">
          <h2 className="text-xl font-semibold">1. Objeto</h2>
          <p className="text-sm text-muted-foreground">
            O NARA oferece um diagnostico narrativo informativo. O conteudo nao substitui
            aconselhamento medico, psicologico ou juridico profissional.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-xl font-semibold">2. Responsabilidade do usuario</h2>
          <p className="text-sm text-muted-foreground">
            O usuario se compromete a fornecer informacoes verdadeiras e a utilizar a plataforma de
            forma etica e legal.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-xl font-semibold">3. Propriedade intelectual</h2>
          <p className="text-sm text-muted-foreground">
            Marcas, metodologia, interface e conteudo do produto sao protegidos e nao podem ser
            reproduzidos sem autorizacao.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-xl font-semibold">4. Limitacao de responsabilidade</h2>
          <p className="text-sm text-muted-foreground">
            O servico e fornecido no melhor esforco tecnico. Podem ocorrer indisponibilidades,
            manutencoes e ajustes operacionais.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-xl font-semibold">5. Alteracoes</h2>
          <p className="text-sm text-muted-foreground">
            Estes termos podem ser atualizados periodicamente, com publicacao da nova versao nesta
            pagina.
          </p>
        </section>

        <Link to="/" className={cn(buttonVariants({ variant: "outline" }))}>
          Voltar ao inicio
        </Link>
      </div>
    </div>
  );
}
