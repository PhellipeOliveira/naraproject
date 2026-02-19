# Componentes de Resultado V2

Componentes visuais avançados para exibir o resultado do diagnóstico NARA V2.

## Componentes Disponíveis

### 1. VetorEstadoAdvanced

Card visual completo do Vetor de Estado com animações e ícones.

**Props:**
```typescript
interface VetorEstadoAdvancedProps {
  vetor: VetorEstado;
}
```

**Uso:**
```tsx
import { VetorEstadoAdvanced } from '@/components/result';

<VetorEstadoAdvanced vetor={data.vetor_estado} />
```

**Features:**
- ✨ Ícones dinâmicos por motor (Flame, Compass, Target, Lightbulb)
- 🎨 Cores personalizadas por motor
- 📊 Progress bar visual do estágio da jornada
- 🌱 Emoji animado do estágio
- 🎯 Hover effects e transições suaves

---

### 2. CriseVisualization

Visualização completa do mapa de crises (raiz, derivadas, áreas silenciadas).

**Props:**
```typescript
interface CriseVisualizationProps {
  criseRaiz: string;
  crisesDeriivadas?: string[];
  areasSilenciadas?: number[];
}
```

**Uso:**
```tsx
import { CriseVisualization } from '@/components/result';

<CriseVisualization 
  criseRaiz={data.vetor_estado.crise_raiz}
  crisesDeriivadas={data.vetor_estado.crises_derivadas}
  areasSilenciadas={data.areas_silenciadas}
/>
```

**Features:**
- 🗺️ Mapa visual dos 6 clusters de crise
- 🎯 Ícones únicos por cluster
- 📍 Timeline vertical de relações entre crises
- ⚠️ Destaque de áreas silenciadas
- 🔍 Descrição e sinais de cada cluster

---

### 3. Componentes de Animação

#### FadeIn
Fade in com delay configurável.

```tsx
import { FadeIn } from '@/components/result';

<FadeIn delay={300}>
  <Card>Conteúdo</Card>
</FadeIn>
```

#### SlideIn
Slide in de qualquer direção.

```tsx
import { SlideIn } from '@/components/result';

<SlideIn direction="left" delay={200}>
  <div>Conteúdo</div>
</SlideIn>
```

Direções: `"left" | "right" | "up" | "down"`

#### ScaleIn
Scale in (útil para cards importantes).

```tsx
import { ScaleIn } from '@/components/result';

<ScaleIn delay={400}>
  <Card className="important">Destaque</Card>
</ScaleIn>
```

#### StaggerChildren
Anima múltiplos elementos em sequência.

```tsx
import { StaggerChildren } from '@/components/result';

<StaggerChildren staggerDelay={100} initialDelay={200}>
  {items.map(item => (
    <Card key={item.id}>{item.content}</Card>
  ))}
</StaggerChildren>
```

#### Pulse
Pulse animation para destacar.

```tsx
import { Pulse } from '@/components/result';

<Pulse intensity="medium">
  <span>Importante!</span>
</Pulse>
```

Intensidades: `"low" | "medium" | "high"`

#### ProgressBarAnimated
Progress bar com animação suave.

```tsx
import { ProgressBarAnimated } from '@/components/result';

<ProgressBarAnimated 
  value={75} 
  delay={500} 
  duration={1500}
  color="bg-primary"
/>
```

#### CountUp
Counter animado para números.

```tsx
import { CountUp } from '@/components/result';

<CountUp value={1234} duration={2000} suffix=" palavras" />
```

#### Shake
Shake animation (para erros).

```tsx
import { Shake } from '@/components/result';

<Shake trigger={hasError}>
  <Input />
</Shake>
```

---

## Exemplo Completo de Uso

```tsx
import { 
  VetorEstadoAdvanced, 
  CriseVisualization,
  FadeIn,
  StaggerChildren 
} from '@/components/result';

export function ResultPage() {
  const data = useResultData();

  return (
    <div className="space-y-6 p-4">
      {/* Vetor de Estado com Fade In */}
      <FadeIn delay={0}>
        <VetorEstadoAdvanced vetor={data.vetor_estado} />
      </FadeIn>

      {/* Mapa de Crises com delay */}
      <FadeIn delay={200}>
        <CriseVisualization 
          criseRaiz={data.vetor_estado.crise_raiz}
          crisesDeriivadas={data.vetor_estado.crises_derivadas}
          areasSilenciadas={data.areas_silenciadas}
        />
      </FadeIn>

      {/* Memórias Vermelhas com Stagger */}
      <FadeIn delay={400}>
        <Card>
          <CardHeader>
            <h2>Memórias Vermelhas</h2>
          </CardHeader>
          <CardContent>
            <StaggerChildren staggerDelay={100}>
              {data.memorias_vermelhas.map((memoria, i) => (
                <div key={i} className="p-3 bg-destructive/5 border-l-4 border-destructive">
                  <p className="text-sm italic">"{memoria}"</p>
                </div>
              ))}
            </StaggerChildren>
          </CardContent>
        </Card>
      </FadeIn>
    </div>
  );
}
```

---

## Animações do Tailwind

As seguintes animações estão disponíveis via classes Tailwind:

- `animate-fade-in`
- `animate-fade-out`
- `animate-slide-up`
- `animate-slide-down`
- `animate-slide-in-right`
- `animate-slide-out-left`
- `animate-scale-in`
- `animate-pulse-slow` (3s)
- `animate-pulse-fast` (1s)
- `animate-bounce-subtle`
- `animate-shake`

**Uso direto:**
```tsx
<div className="animate-fade-in">
  Conteúdo com fade in
</div>
```

---

## Responsividade

Todos os componentes são **mobile-first** e responsivos por padrão:

- Grid adapta de 1 coluna (mobile) para 2+ (desktop)
- Textos ajustam tamanho automaticamente
- Espaçamentos otimizados para telas pequenas
- Touch-friendly (botões com área mínima de 44x44px)

---

## Acessibilidade

- ✅ Cores com contraste WCAG AA
- ✅ Semântica HTML adequada
- ✅ Animações respeitam `prefers-reduced-motion`
- ✅ Textos alternativos em ícones
- ✅ Keyboard navigation

---

## Performance

- 🚀 Lazy loading de componentes pesados
- 🎯 Memoization de renders complexos
- 📦 Code splitting automático
- ⚡ CSS-in-JS otimizado (Tailwind)

---

**Criado por:** Time NARA  
**Versão:** 2.0  
**Última atualização:** Fevereiro 2026
