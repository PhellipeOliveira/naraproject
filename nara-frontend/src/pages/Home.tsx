import { Link } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader } from "../components/ui/card";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8 bg-background">
      <Card className="w-full max-w-lg">
        <CardHeader>
          <h1 className="text-3xl font-bold text-center text-primary">NARA</h1>
          <p className="text-center text-muted-foreground">
            Diagnóstico de Transformação Narrativa
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground text-center">
            Descubra seu perfil nas 12 Áreas da Vida e receba um relatório personalizado com
            base na metodologia do Círculo Narrativo.
          </p>
          <Button asChild className="w-full">
            <Link to="/diagnostico/iniciar">Iniciar diagnóstico</Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
