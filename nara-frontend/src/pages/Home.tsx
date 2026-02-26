import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { LegalFooter } from "../components/LegalFooter";
import { Button } from "../components/ui/button";
import { ArrowRight, Sparkles, Target, Compass, BarChart3, Users } from "lucide-react";

const FEATURES = [
  {
    icon: Target,
    title: "12 Áreas da Vida",
    description: "Diagnóstico completo em todas as áreas estruturantes",
  },
  {
    icon: Compass,
    title: "Jornada Personalizada",
    description: "Perguntas adaptadas às suas respostas",
  },
  {
    icon: BarChart3,
    title: "Relatório Detalhado",
    description: "Análise completa com recomendações práticas",
  },
];

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-subtle">
      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 md:py-20">
        <div className="w-full max-w-2xl mx-auto text-center space-y-8">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium">
              <Sparkles className="w-4 h-4" />
              Metodologia Círculo Narrativo
            </span>
          </motion.div>

          {/* Title */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="space-y-4"
          >
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold font-display tracking-tight">
              <span className="text-gradient">NARA</span>
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground font-medium">
              Diagnóstico de Transformação Narrativa
            </p>
          </motion.div>

          {/* Description */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-lg text-muted-foreground max-w-lg mx-auto leading-relaxed"
          >
            Descubra seu perfil nas 12 Áreas Estruturantes da Vida e receba um relatório
            personalizado para sua jornada de transformação.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4"
          >
            <Link to="/diagnostico/iniciar">
              <Button size="xl" variant="gradient" className="gap-2 shadow-glow">
                Iniciar Diagnóstico Gratuito
                <ArrowRight className="w-5 h-5" />
              </Button>
            </Link>
            <Link to="/diagnostico/iniciar">
              <Button size="lg" variant="ghost" className="text-muted-foreground">
                <Users className="w-4 h-4 mr-2" />
                Já tenho diagnóstico
              </Button>
            </Link>
          </motion.div>
        </div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="w-full max-w-4xl mx-auto mt-16 md:mt-24"
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {FEATURES.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.6 + index * 0.1 }}
                className="flex flex-col items-center text-center p-6 rounded-2xl bg-card border shadow-card hover:shadow-card-hover hover:border-primary/20 transition-all duration-300"
              >
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="py-8 px-4">
        <div className="max-w-lg mx-auto">
          <LegalFooter />
        </div>
      </footer>
    </div>
  );
}
