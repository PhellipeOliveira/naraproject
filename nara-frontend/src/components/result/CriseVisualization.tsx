import { Card, CardContent, CardHeader } from "../ui/card";
import { AlertTriangle, User, Compass, Wrench, Users, Shuffle, TrendingUp } from "lucide-react";
import type { LucideIcon } from "lucide-react";

interface CriseVisualizationProps {
  criseRaiz: string;
  crisesDeriivadas?: string[];
  areasSilenciadas?: number[];
}

const criseIcons: Record<string, LucideIcon> = {
  "Identidade Raiz": User,
  "Sentido e Direção": Compass,
  "Execução e Estrutura": Wrench,
  "Conexão e Expressão": Users,
  "Incongruência Identidade-Cultura": Shuffle,
  "Transformação de Personagem": TrendingUp,
};

const criseColors: Record<string, string> = {
  "Identidade Raiz": "from-red-500/20 to-red-600/10 border-red-500/30",
  "Sentido e Direção": "from-blue-500/20 to-blue-600/10 border-blue-500/30",
  "Execução e Estrutura": "from-yellow-500/20 to-yellow-600/10 border-yellow-500/30",
  "Conexão e Expressão": "from-purple-500/20 to-purple-600/10 border-purple-500/30",
  "Incongruência Identidade-Cultura": "from-orange-500/20 to-orange-600/10 border-orange-500/30",
  "Transformação de Personagem": "from-green-500/20 to-green-600/10 border-green-500/30",
};

const criseDescriptions: Record<string, { description: string; sinais: string[] }> = {
  "Identidade Raiz": {
    description: "Crise profunda sobre \"quem eu sou\". Identidades herdadas, vergonha ou autoimagem desatualizada.",
    sinais: ["Identidades herdadas não escolhidas", "Vergonha e indignidade", "Autoimagem desatualizada"]
  },
  "Sentido e Direção": {
    description: "Crise de \"para onde vou\". Vazio existencial, falta de visão de futuro.",
    sinais: ["Vazio e fragmentação", "Falta de visão de futuro", "Urgência tóxica"]
  },
  "Execução e Estrutura": {
    description: "Crise de \"como faço\". Paralisia decisória e ausência de ritos.",
    sinais: ["Paralisia decisória", "Ausência de ritos e rotinas", "Desorganização material"]
  },
  "Conexão e Expressão": {
    description: "Crise de \"como me relaciono\". Invisibilidade simbólica e solidão existencial.",
    sinais: ["Invisibilidade simbólica", "Solidão existencial", "Dificuldade de expressão"]
  },
  "Incongruência Identidade-Cultura": {
    description: "Crise de \"não pertenço\". Desajuste entre quem você é e o ambiente.",
    sinais: ["Choque ambiental", "Desajuste sistêmico", "Exaustão por mascaramento"]
  },
  "Transformação de Personagem": {
    description: "Crise de \"medo de mudar\". Apego a papéis obsoletos e medo de crescer.",
    sinais: ["Apego a papéis obsoletos", "Medo de crescer", "Dificuldade em encerrar capítulos"]
  },
};

const areaNames: Record<number, string> = {
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

export function CriseVisualization({ criseRaiz, crisesDeriivadas, areasSilenciadas }: CriseVisualizationProps) {
  const CriseIcon = criseIcons[criseRaiz] || AlertTriangle;
  const criseGradient = criseColors[criseRaiz] || "from-destructive/20 to-destructive/10 border-destructive/30";
  const criseInfo = criseDescriptions[criseRaiz];

  return (
    <Card>
      <CardHeader>
        <h2 className="text-lg font-bold">Mapa das Crises</h2>
        <p className="text-sm text-muted-foreground">
          Entendendo os bloqueios da sua jornada
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Crise Raiz - Card Principal */}
        <div className={`p-6 rounded-xl bg-gradient-to-br ${criseGradient} border-2`}>
          <div className="flex items-start gap-4 mb-4">
            <div className="p-3 rounded-lg bg-background/80 shadow-sm">
              <CriseIcon size={32} className="text-destructive" />
            </div>
            <div className="flex-1">
              <p className="text-xs uppercase tracking-wider text-destructive/70 mb-1 font-semibold">
                Crise Raiz
              </p>
              <h3 className="text-xl font-bold text-destructive mb-2">
                {criseRaiz}
              </h3>
              {criseInfo && (
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {criseInfo.description}
                </p>
              )}
            </div>
          </div>

          {/* Sinais da Crise */}
          {criseInfo && criseInfo.sinais.length > 0 && (
            <div className="pt-4 border-t border-destructive/10">
              <p className="text-xs font-semibold text-destructive/70 mb-3 uppercase tracking-wider">
                Sinais Identificados:
              </p>
              <div className="grid gap-2 sm:grid-cols-3">
                {criseInfo.sinais.map((sinal, i) => (
                  <div key={i} className="flex items-start gap-2">
                    <div className="flex-shrink-0 w-1.5 h-1.5 rounded-full bg-destructive mt-1.5" />
                    <p className="text-xs text-muted-foreground leading-tight">{sinal}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Crises Derivadas */}
        {crisesDeriivadas && crisesDeriivadas.length > 0 && (
          <div>
            <p className="text-sm font-semibold text-muted-foreground mb-3">
              Crises secundárias também presentes:
            </p>
            <div className="grid gap-3 sm:grid-cols-2">
              {crisesDeriivadas.map((crise, i) => {
                const Icon = criseIcons[crise] || AlertTriangle;
                const gradient = criseColors[crise] || "from-muted/50 to-muted/30";
                return (
                  <div 
                    key={i}
                    className={`p-4 rounded-lg bg-gradient-to-br ${gradient} border`}
                  >
                    <div className="flex items-center gap-3">
                      <Icon size={20} className="text-muted-foreground flex-shrink-0" />
                      <p className="text-sm font-medium">{crise}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Áreas Silenciadas */}
        {areasSilenciadas && areasSilenciadas.length > 0 && (
          <div className="p-5 rounded-lg bg-muted/50 border border-muted">
            <div className="flex items-start gap-3 mb-3">
              <div className="p-2 rounded-lg bg-background">
                <AlertTriangle size={20} className="text-yellow-600" />
              </div>
              <div>
                <h3 className="text-sm font-semibold mb-1">Áreas Silenciadas</h3>
                <p className="text-xs text-muted-foreground mb-3">
                  Áreas que você evitou explorar ou respondeu superficialmente. 
                  Silêncios também revelam bloqueios.
                </p>
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              {areasSilenciadas.map((areaId, i) => (
                <span 
                  key={i}
                  className="px-3 py-1.5 rounded-full bg-yellow-500/10 text-yellow-700 dark:text-yellow-500 text-xs font-medium border border-yellow-500/20"
                >
                  {areaNames[areaId] || `Área ${areaId}`}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Insight Visual - Timeline de Crises */}
        <div className="p-5 rounded-lg bg-gradient-to-r from-muted/30 to-muted/10 border border-muted">
          <p className="text-xs uppercase tracking-wider text-muted-foreground mb-4 font-semibold">
            Como as crises se relacionam:
          </p>
          <div className="relative">
            {/* Timeline vertical */}
            <div className="absolute left-2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-destructive/50 to-transparent" />
            
            <div className="space-y-4 pl-8">
              <div>
                <p className="text-sm font-medium text-destructive mb-1">
                  1. Crise Raiz
                </p>
                <p className="text-xs text-muted-foreground">
                  O bloqueio fundamental que causa os outros
                </p>
              </div>
              {crisesDeriivadas && crisesDeriivadas.length > 0 && (
                <>
                  <div>
                    <p className="text-sm font-medium text-orange-600 dark:text-orange-500 mb-1">
                      2. Crises Derivadas
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Consequências e manifestações da crise raiz
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-blue-600 dark:text-blue-500 mb-1">
                      3. Sintomas nas Áreas
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Como as crises aparecem no seu círculo narrativo
                    </p>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
