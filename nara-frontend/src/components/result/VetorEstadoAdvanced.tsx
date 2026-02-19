import { Card, CardContent, CardHeader } from "../ui/card";
import type { VetorEstado } from "../../types";
import { 
  Flame, 
  Sprout, 
  Target, 
  AlertTriangle,
  Compass,
  Lightbulb 
} from "lucide-react";

interface VetorEstadoAdvancedProps {
  vetor: VetorEstado;
}

const motorIcons = {
  Necessidade: Flame,
  Valor: Compass,
  Desejo: Target,
  Propósito: Lightbulb,
};

const motorColors = {
  Necessidade: "bg-red-500/10 text-red-700 dark:text-red-400 border-red-500/20",
  Valor: "bg-blue-500/10 text-blue-700 dark:text-blue-400 border-blue-500/20",
  Desejo: "bg-purple-500/10 text-purple-700 dark:text-purple-400 border-purple-500/20",
  Propósito: "bg-yellow-500/10 text-yellow-700 dark:text-yellow-400 border-yellow-500/20",
};

const estagioProgress = {
  Germinar: 16,
  Enraizar: 33,
  Desenvolver: 50,
  Florescer: 66,
  Frutificar: 83,
  Realizar: 100,
};

const estagioEmoji = {
  Germinar: "🌱",
  Enraizar: "🌿",
  Desenvolver: "🌳",
  Florescer: "🌸",
  Frutificar: "🍎",
  Realizar: "✨",
};

export function VetorEstadoAdvanced({ vetor }: VetorEstadoAdvancedProps) {
  const MotorIcon = motorIcons[vetor.motor_dominante as keyof typeof motorIcons] || Flame;
  const motorColorClass = motorColors[vetor.motor_dominante as keyof typeof motorColors];
  const progressPercent = estagioProgress[vetor.estagio_jornada as keyof typeof estagioProgress] || 0;
  const estagioIcon = estagioEmoji[vetor.estagio_jornada as keyof typeof estagioEmoji] || "🌱";

  return (
    <Card className="overflow-hidden">
      <CardHeader className="bg-gradient-to-r from-primary/5 to-primary/10 pb-8">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Seu Diagnóstico NARA</h1>
            <p className="text-sm text-muted-foreground">
              Transformação Narrativa · Metodologia Phellipe Oliveira
            </p>
          </div>
          <div className="text-4xl animate-pulse">{estagioIcon}</div>
        </div>
      </CardHeader>

      <CardContent className="pt-6 space-y-6">
        {/* Motor Dominante - Card Destaque */}
        <div className={`p-6 rounded-xl border-2 ${motorColorClass} transition-all hover:scale-[1.02]`}>
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-lg bg-background/50">
              <MotorIcon size={32} className="stroke-current" />
            </div>
            <div className="flex-1">
              <p className="text-xs uppercase tracking-wider opacity-70 mb-1">
                Motor Motivacional Dominante
              </p>
              <h3 className="text-2xl font-bold mb-2">{vetor.motor_dominante}</h3>
              <p className="text-sm opacity-90">
                {getMotorDescription(vetor.motor_dominante)}
              </p>
              {vetor.motor_secundario && (
                <p className="text-xs mt-2 opacity-70">
                  Secundário: {vetor.motor_secundario}
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Estágio da Jornada - Com Progress Bar */}
        <div className="p-6 rounded-xl bg-gradient-to-br from-blue-500/5 to-purple-500/5 border border-blue-500/10">
          <div className="flex items-start gap-4 mb-4">
            <div className="p-3 rounded-lg bg-background/50">
              <Sprout size={28} className="text-blue-600 dark:text-blue-400" />
            </div>
            <div className="flex-1">
              <p className="text-xs uppercase tracking-wider text-muted-foreground mb-1">
                Estágio da Jornada
              </p>
              <h3 className="text-xl font-bold text-blue-700 dark:text-blue-400 mb-1">
                {vetor.estagio_jornada}
              </h3>
              <p className="text-sm text-muted-foreground">
                {getEstagioDescription(vetor.estagio_jornada)}
              </p>
            </div>
          </div>
          
          {/* Progress Bar Visual */}
          <div className="space-y-2">
            <div className="h-2 bg-muted rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-1000 ease-out"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>Germinar</span>
              <span>Realizar</span>
            </div>
          </div>
        </div>

        {/* Grid: Crise Raiz + Ponto de Entrada */}
        <div className="grid gap-4 sm:grid-cols-2">
          {/* Crise Raiz */}
          <div className="p-5 rounded-xl bg-destructive/5 border-2 border-destructive/20">
            <div className="flex items-start gap-3 mb-3">
              <AlertTriangle size={24} className="text-destructive flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-xs uppercase tracking-wider text-destructive/70 mb-1">
                  Crise Raiz Identificada
                </p>
                <h3 className="font-bold text-destructive leading-tight">
                  {vetor.crise_raiz}
                </h3>
              </div>
            </div>
            {vetor.crises_derivadas && vetor.crises_derivadas.length > 0 && (
              <div className="pt-3 border-t border-destructive/10">
                <p className="text-xs text-muted-foreground mb-2">Também presente:</p>
                <div className="space-y-1">
                  {vetor.crises_derivadas.slice(0, 2).map((crise, i) => (
                    <p key={i} className="text-xs text-destructive/70">
                      • {crise}
                    </p>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Ponto de Entrada Ideal */}
          <div className="p-5 rounded-xl bg-primary/5 border border-primary/10">
            <div className="flex items-start gap-3 mb-3">
              <Compass size={24} className="text-primary flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-xs uppercase tracking-wider text-muted-foreground mb-1">
                  Ponto de Entrada Ideal
                </p>
                <h3 className="font-bold text-primary leading-tight">
                  {vetor.ponto_entrada_ideal}
                </h3>
              </div>
            </div>
            <p className="text-xs text-muted-foreground">
              {getPontoEntradaDescription(vetor.ponto_entrada_ideal)}
            </p>
          </div>
        </div>

        {/* Necessidade Atual - Call to Action */}
        <div className="p-6 rounded-xl bg-gradient-to-r from-primary/10 to-primary/5 border-l-4 border-primary">
          <p className="text-xs uppercase tracking-wider text-primary mb-2 font-semibold">
            Necessidade Atual (O que fazer agora)
          </p>
          <p className="text-base leading-relaxed font-medium">
            {vetor.necessidade_atual}
          </p>
        </div>

        {/* Tom Emocional & Risco */}
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="p-4 rounded-lg bg-muted/50 border border-muted">
            <p className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
              Tom Emocional
            </p>
            <p className="text-sm italic">{vetor.tom_emocional}</p>
          </div>
          <div className="p-4 rounded-lg bg-muted/50 border border-muted">
            <p className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
              Risco Principal
            </p>
            <p className="text-sm">{vetor.risco_principal}</p>
          </div>
        </div>

        {/* Domínios Alavanca (se houver) */}
        {vetor.dominios_alavanca && vetor.dominios_alavanca.length > 0 && (
          <div className="p-4 rounded-lg bg-muted/30 border border-muted">
            <p className="text-xs uppercase tracking-wider text-muted-foreground mb-3">
              Domínios de Alavancagem
            </p>
            <div className="flex flex-wrap gap-2">
              {vetor.dominios_alavanca.map((dominio, i) => (
                <span 
                  key={i}
                  className="px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-medium"
                >
                  {dominio}: {getDominioName(dominio)}
                </span>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// Helper functions
function getMotorDescription(motor: string): string {
  const descriptions: Record<string, string> = {
    'Necessidade': 'Você está sendo impulsionado pela urgência de afastar-se da dor e buscar alívio do sofrimento interno.',
    'Valor': 'Sua motivação vem da necessidade de viver com integridade e coerência com seus princípios mais profundos.',
    'Desejo': 'Você é movido pela vontade de conquistar objetivos e alcançar realizações tangíveis.',
    'Propósito': 'Sua força vem da busca por deixar um legado significativo e impactar positivamente as vidas ao seu redor.'
  };
  return descriptions[motor] || 'Motor de transformação identificado.';
}

function getEstagioDescription(estagio: string): string {
  const descriptions: Record<string, string> = {
    'Germinar': 'Você está no início do despertar, questionando padrões e sentindo desconforto necessário para mudança.',
    'Enraizar': 'Está buscando fundamentos sólidos, revisando crenças e valores que sustentarão sua nova identidade.',
    'Desenvolver': 'Em construção ativa, testando novas formas de ser e agir no mundo.',
    'Florescer': 'Expressando autenticamente sua nova narrativa, com crescente confiança.',
    'Frutificar': 'Colhendo resultados tangíveis da sua transformação, vendo o impacto real.',
    'Realizar': 'Vivendo em plenitude e maestria, dominando sua nova identidade.'
  };
  return descriptions[estagio] || 'Fase da jornada de transformação.';
}

function getPontoEntradaDescription(ponto: string): string {
  const descriptions: Record<string, string> = {
    'Emocional': 'Comece validando e regulando suas emoções antes de agir.',
    'Simbólico': 'Ressignifique sua narrativa, reescreva a história que conta para si mesmo.',
    'Comportamental': 'Foque em criar protocolos práticos e âncoras de ação concretas.',
    'Existencial': 'Redefina seu papel de vida e reposicione sua missão no mundo.'
  };
  return descriptions[ponto] || 'Porta de entrada para transformação.';
}

function getDominioName(dominio: string): string {
  const names: Record<string, string> = {
    'D1': 'Motivações e Conflitos',
    'D2': 'Crenças e Valores',
    'D3': 'Evolução e Desenvolvimento',
    'D4': 'Congruência Identidade-Cultura',
    'D5': 'Transformação de Identidade',
    'D6': 'Papel na Sociedade'
  };
  return names[dominio] || dominio;
}
