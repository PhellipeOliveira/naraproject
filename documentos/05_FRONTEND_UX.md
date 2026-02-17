# 05 - FRONTEND E EXPERIÊNCIA DO USUÁRIO

> **Propósito:** Especificação técnica completa do frontend React/Vite, incluindo arquitetura, componentes, fluxos de usuário, design system, gerenciamento de estado e integração com o backend do diagnóstico NARA.

---

## 📋 ÍNDICE NAVEGÁVEL

### Parte 1: Arquitetura e Configuração
1. [Visão Geral da Arquitetura Frontend](#1-visão-geral-da-arquitetura-frontend)
2. [Stack Tecnológico Detalhado](#2-stack-tecnológico-detalhado)
3. [Estrutura de Pastas Completa](#3-estrutura-de-pastas-completa)
4. [Configuração Inicial](#4-configuração-inicial)

### Parte 2: Gerenciamento de Estado e Dados
5. [Gerenciamento de Estado (Zustand)](#5-gerenciamento-de-estado-zustand)
6. [Integração com API (React Query)](#6-integração-com-api-react-query)
7. [Gestão de Sessão e Auto-Save](#7-gestão-de-sessão-e-auto-save)

### Parte 3: Componentes e UI
8. [Design System Completo](#8-design-system-completo)
9. [Componentes Principais](#9-componentes-principais)
10. [Formulários e Validações](#10-formulários-e-validações)

### Parte 4: Fluxos e Experiência
11. [Fluxos de Usuário (11 Etapas)](#11-fluxos-de-usuário-11-etapas)
12. [Roteamento e Navegação](#12-roteamento-e-navegação)
13. [Gráfico Radar das 12 Áreas](#13-gráfico-radar-das-12-áreas)

### Parte 5: Qualidade e Performance
14. [Responsividade e Mobile-First](#14-responsividade-e-mobile-first)
15. [Acessibilidade (WCAG)](#15-acessibilidade-wcag)
16. [Performance e Otimizações](#16-performance-e-otimizações)
17. [Tratamento de Erros](#17-tratamento-de-erros)
18. [Animações e Transições](#18-animações-e-transições)
19. [Testes Frontend](#19-testes-frontend)

---

# PARTE 1: ARQUITETURA E CONFIGURAÇÃO

## 1. VISÃO GERAL DA ARQUITETURA FRONTEND

### 1.1 Arquitetura de Alto Nível

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (React + Vite)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐   ┌──────────────┐   ┌───────────────────┐   │
│  │   Pages     │ ← │  Components  │ ← │   UI Library      │   │
│  │  (Routes)   │   │  (Business)  │   │  (shadcn/ui)      │   │
│  └──────┬──────┘   └──────┬───────┘   └───────────────────┘   │
│         │                 │                                     │
│         ▼                 ▼                                     │
│  ┌─────────────────────────────────────────┐                   │
│  │           Zustand Store                  │                   │
│  │  • diagnosticStore (estado principal)   │                   │
│  │  • uiStore (loading, modals, toasts)    │                   │
│  └─────────────────┬───────────────────────┘                   │
│                    │                                            │
│                    ▼                                            │
│  ┌─────────────────────────────────────────┐                   │
│  │         React Query (TanStack)          │                   │
│  │  • Mutations (POST, PUT, DELETE)        │                   │
│  │  • Queries (GET com cache)              │                   │
│  │  • Auto-retry e invalidação             │                   │
│  └─────────────────┬───────────────────────┘                   │
│                    │                                            │
│                    ▼                                            │
│  ┌─────────────────────────────────────────┐                   │
│  │         API Client (Axios)              │                   │
│  │  • Base URL: /api/v1                    │                   │
│  │  • Interceptors (auth, errors)          │                   │
│  │  • Timeout: 30s                         │                   │
│  └─────────────────┬───────────────────────┘                   │
│                    │                                            │
└────────────────────┼────────────────────────────────────────────┘
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│               BACKEND (FastAPI + LangChain)                     │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Princípios de Arquitetura

| Princípio | Implementação |
|-----------|---------------|
| **Separação de Concerns** | Pages ← Components ← Hooks ← Services |
| **Single Source of Truth** | Zustand para estado global, React Query para server state |
| **Colocation** | Componentes com seus estilos, testes e types juntos |
| **Composition over Inheritance** | Componentes compostos usando children e render props |
| **Fail Fast** | Validação com Zod no boundary, tratamento explícito de erros |

---

## 2. STACK TECNOLÓGICO DETALHADO

### 2.1 Dependências Principais

```json
{
  "name": "nara-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,css,json}\"",
    "test": "vitest",
    "test:coverage": "vitest run --coverage"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-progress": "^1.0.3",
    "@radix-ui/react-slider": "^1.1.2",
    "@radix-ui/react-checkbox": "^1.0.4",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-toast": "^1.1.5",
    
    "zustand": "^4.4.7",
    "@tanstack/react-query": "^5.17.0",
    "axios": "^1.6.3",
    
    "react-hook-form": "^7.49.2",
    "@hookform/resolvers": "^3.3.2",
    "zod": "^3.22.4",
    
    "recharts": "^2.10.3",
    "framer-motion": "^10.17.0",
    
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.2.0",
    "lucide-react": "^0.303.0",
    
    "use-debounce": "^10.0.0",
    "canvas-confetti": "^1.9.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.45",
    "@types/react-dom": "^18.2.18",
    "@types/canvas-confetti": "^1.6.4",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "tailwindcss-animate": "^1.0.7",
    "typescript": "^5.3.3",
    "vite": "^5.0.10",
    "vitest": "^1.2.0",
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.2.0",
    "eslint": "^8.56.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "prettier": "^3.2.0"
  }
}
```

### 2.2 Justificativa das Escolhas

| Tecnologia | Versão | Justificativa |
|------------|--------|---------------|
| **React 18** | ^18.2.0 | Concurrent features, automatic batching, Suspense |
| **Vite** | ^5.0.10 | HMR ultra-rápido, ESM nativo, build otimizado |
| **TypeScript** | ^5.3.3 | Type safety, melhor DX, menos bugs em produção |
| **Zustand** | ^4.4.7 | Simples, sem boilerplate, persist middleware |
| **React Query** | ^5.17.0 | Server state, cache inteligente, mutations |
| **React Hook Form** | ^7.49.2 | Performance (uncontrolled), validação integrada |
| **Zod** | ^3.22.4 | Schema validation, TypeScript inference |
| **shadcn/ui** | latest | Componentes copiáveis, Radix UI, acessíveis |
| **Tailwind CSS** | ^3.4.0 | Utility-first, design system consistente |
| **Framer Motion** | ^10.17.0 | Animações declarativas, gestures, layout |
| **Recharts** | ^2.10.3 | Gráficos React-first, customizável, radar chart |

---

## 3. ESTRUTURA DE PASTAS COMPLETA

```
nara-frontend/
├── public/
│   ├── favicon.ico
│   ├── logo.svg
│   ├── og-image.png                    # Open Graph para compartilhamento
│   └── manifest.json                   # PWA manifest (futuro)
│
├── src/
│   ├── main.tsx                        # Entry point - ReactDOM.createRoot
│   ├── App.tsx                         # Root component - Providers wrapper
│   ├── index.css                       # Global styles + Tailwind directives
│   ├── vite-env.d.ts                   # Vite types
│   │
│   ├── api/                            # Camada de comunicação com backend
│   │   ├── client.ts                   # Axios instance configurada
│   │   ├── diagnostic.ts               # Endpoints de diagnóstico
│   │   ├── feedback.ts                 # Endpoints de feedback
│   │   └── types.ts                    # Response/Request types
│   │
│   ├── components/
│   │   ├── ui/                         # shadcn/ui components (atômicos)
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── checkbox.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   ├── label.tsx
│   │   │   ├── progress.tsx
│   │   │   ├── slider.tsx
│   │   │   ├── textarea.tsx
│   │   │   ├── toast.tsx
│   │   │   └── toaster.tsx
│   │   │
│   │   ├── layout/                     # Componentes estruturais
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Container.tsx
│   │   │   ├── PageTransition.tsx
│   │   │   └── LoadingScreen.tsx
│   │   │
│   │   ├── diagnostic/                 # Componentes do fluxo de diagnóstico
│   │   │   ├── QuestionCard.tsx        # Card de pergunta individual (V2: simplificado, sem escala)
│   │   │   ├── ScaleInput.tsx          # LEGACY: Input de escala 0-5 (não usado em V2)
│   │   │   ├── TextInput.tsx           # Textarea com contador
│   │   │   ├── ProgressBar.tsx         # Barra de progresso multi-level
│   │   │   ├── PhaseIndicator.tsx      # Indicador de fase atual
│   │   │   ├── EligibilityModal.tsx    # Modal de elegibilidade
│   │   │   ├── SaveExitModal.tsx       # Modal de "Salvar e Sair"
│   │   │   ├── ResumeModal.tsx         # Modal de retomada de sessão
│   │   │   ├── TransitionScreen.tsx    # Tela de transição entre fases
│   │   │   └── CelebrationScreen.tsx   # Tela de celebração (confete)
│   │   │
│   │   ├── result/                     # Componentes da tela de resultado (V2: redesenhada)
│   │   │   ├── RadarChart.tsx          # Gráfico radar das 12 áreas
│   │   │   ├── RadarChartMini.tsx      # Versão compacta do radar
│   │   │   ├── VetorEstadoGrid.tsx     # V2: Grid de cards do Vetor de Estado
│   │   │   ├── MemoriasVermelhas.tsx   # V2: Citações destacadas com borda vermelha
│   │   │   ├── AncorasSugeridas.tsx    # V2: Lista de Âncoras Práticas sugeridas
│   │   │   ├── CapitalSimbolico.tsx    # V2: Recursos identificados (antes "Pontos Fortes")
│   │   │   ├── AreaCard.tsx            # Card de área individual (status visual)
│   │   │   ├── AreaCardExpanded.tsx    # Card expandido com detalhes + Key Insight
│   │   │   ├── ScoreDisplay.tsx        # Display do score geral (legacy, detecta vetor_estado)
│   │   │   ├── PlanoAssuncao.tsx       # V2: Plano de Assunção Intencional
│   │   │   ├── InsightSection.tsx      # Seção de insights
│   │   │   ├── ShareModal.tsx          # Modal de compartilhamento
│   │   │   └── CreateAccountBanner.tsx # Banner para criar conta
│   │   │
│   │   ├── feedback/                   # Componentes de feedback
│   │   │   ├── FeedbackForm.tsx        # Formulário NPS + rating
│   │   │   ├── StarRating.tsx          # Componente de estrelas
│   │   │   └── NPSScale.tsx            # Escala 0-10 NPS
│   │   │
│   │   └── forms/                      # Componentes de formulário
│   │       ├── WelcomeForm.tsx         # Form da tela de boas-vindas
│   │       ├── ConsentCheckboxes.tsx   # Checkboxes LGPD
│   │       └── EmailInput.tsx          # Input de email com validação
│   │
│   ├── pages/                          # Páginas (rotas)
│   │   ├── Home.tsx                    # Landing page
│   │   ├── Welcome.tsx                 # Tela de boas-vindas
│   │   ├── Diagnostic.tsx              # Fluxo do diagnóstico
│   │   ├── Transition.tsx              # Tela de transição entre fases
│   │   ├── Celebration.tsx             # Tela de conclusão
│   │   ├── Result.tsx                  # Exibição do resultado
│   │   ├── Resume.tsx                  # Retomada via magic link
│   │   ├── Waitlist.tsx                # Cadastro na lista de espera
│   │   ├── Feedback.tsx                # Página de feedback
│   │   └── NotFound.tsx                # Página 404
│   │
│   ├── stores/                         # Estado global (Zustand)
│   │   ├── diagnosticStore.ts          # Estado do diagnóstico
│   │   ├── uiStore.ts                  # Estado de UI
│   │   └── index.ts                    # Re-exports
│   │
│   ├── hooks/                          # Custom hooks
│   │   ├── useDiagnostic.ts            # Hook principal do diagnóstico
│   │   ├── useAutoSave.ts              # Hook de auto-save
│   │   ├── useProgress.ts              # Hook de progresso
│   │   ├── useEligibility.ts           # Hook de elegibilidade
│   │   ├── useLocalStorage.ts          # Hook de localStorage
│   │   ├── useMediaQuery.ts            # Hook de media queries
│   │   └── useWordCount.ts             # Hook de contagem de palavras
│   │
│   ├── lib/                            # Utilitários
│   │   ├── utils.ts                    # Funções utilitárias (cn, etc)
│   │   ├── constants.ts                # Constantes da aplicação
│   │   ├── validation.ts               # Schemas Zod
│   │   └── formatting.ts               # Formatação de dados
│   │
│   ├── types/                          # Definições TypeScript
│   │   ├── index.ts                    # Re-exports
│   │   ├── diagnostic.ts               # Types do diagnóstico
│   │   ├── question.ts                 # Types de perguntas
│   │   ├── answer.ts                   # Types de respostas
│   │   ├── result.ts                   # Types do resultado
│   │   └── api.ts                      # Types da API
│   │
│   └── data/                           # Dados estáticos
│       ├── baselineQuestions.ts        # 15 perguntas fixas da Fase 1
│       ├── areas.ts                    # Definição das 12 áreas
│       └── phases.ts                   # Configuração das fases
│
├── .env.example                        # Template de variáveis de ambiente
├── .env.local                          # Variáveis locais (não commitado)
├── .eslintrc.cjs                       # Configuração ESLint
├── .prettierrc                         # Configuração Prettier
├── index.html                          # HTML template
├── package.json                        # Dependências
├── postcss.config.js                   # Configuração PostCSS
├── tailwind.config.js                  # Configuração Tailwind
├── tsconfig.json                       # Configuração TypeScript
├── tsconfig.node.json                  # TS config para Node
└── vite.config.ts                      # Configuração Vite
```

---

## 4. CONFIGURAÇÃO INICIAL

### 4.1 Vite Config (vite.config.ts)

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@stores': path.resolve(__dirname, './src/stores'),
      '@lib': path.resolve(__dirname, './src/lib'),
      '@types': path.resolve(__dirname, './src/types'),
      '@api': path.resolve(__dirname, './src/api'),
    },
  },
  server: {
    port: 5173,
    host: true, // Permite acesso externo
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui-vendor': ['framer-motion', 'recharts'],
          'form-vendor': ['react-hook-form', '@hookform/resolvers', 'zod'],
        },
      },
    },
  },
  preview: {
    port: 4173,
  },
});
```

### 4.2 TypeScript Config (tsconfig.json)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@pages/*": ["./src/pages/*"],
      "@hooks/*": ["./src/hooks/*"],
      "@stores/*": ["./src/stores/*"],
      "@lib/*": ["./src/lib/*"],
      "@types/*": ["./src/types/*"],
      "@api/*": ["./src/api/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### 4.3 Tailwind Config (tailwind.config.js)

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        // Sistema de cores primárias
        primary: {
          DEFAULT: '#6366f1',
          foreground: '#ffffff',
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
        // Cores secundárias
        secondary: {
          DEFAULT: '#f4f4f5',
          foreground: '#18181b',
        },
        // Cores de estado
        destructive: {
          DEFAULT: '#ef4444',
          foreground: '#ffffff',
        },
        success: {
          DEFAULT: '#22c55e',
          foreground: '#ffffff',
        },
        warning: {
          DEFAULT: '#f59e0b',
          foreground: '#000000',
        },
        info: {
          DEFAULT: '#3b82f6',
          foreground: '#ffffff',
        },
        muted: {
          DEFAULT: '#f4f4f5',
          foreground: '#71717a',
        },
        accent: {
          DEFAULT: '#f4f4f5',
          foreground: '#18181b',
        },
        // Cores das 12 Áreas Estruturantes (Círculo Narrativo)
        area: {
          1: '#22c55e',   // Saúde Física - Verde
          2: '#8b5cf6',   // Saúde Mental - Roxo
          3: '#f59e0b',   // Saúde Espiritual - Âmbar
          4: '#ec4899',   // Vida Pessoal - Rosa
          5: '#ef4444',   // Vida Amorosa - Vermelho
          6: '#06b6d4',   // Vida Familiar - Ciano
          7: '#3b82f6',   // Vida Social - Azul
          8: '#6366f1',   // Vida Profissional - Índigo
          9: '#10b981',   // Finanças - Esmeralda
          10: '#f97316',  // Educação - Laranja
          11: '#a855f7',  // Inovação - Violeta
          12: '#14b8a6',  // Lazer - Teal
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.875rem' }],
      },
      spacing: {
        18: '4.5rem',
        22: '5.5rem',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'fade-out': 'fadeOut 0.3s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'slide-out-left': 'slideOutLeft 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-subtle': 'bounceSubtle 1s infinite',
        'spin-slow': 'spin 3s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeOut: {
          '0%': { opacity: '1' },
          '100%': { opacity: '0' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        slideOutLeft: {
          '0%': { opacity: '1', transform: 'translateX(0)' },
          '100%': { opacity: '0', transform: 'translateX(-20px)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        bounceSubtle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' },
        },
      },
      transitionDuration: {
        '400': '400ms',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};
```

### 4.4 ESLint Config (.eslintrc.cjs)

```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/no-explicit-any': 'warn',
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'prefer-const': 'error',
    'no-var': 'error',
  },
};
```

### 4.5 Variáveis de Ambiente (.env.example)

```bash
# API
VITE_API_URL=http://localhost:8000/api/v1
VITE_API_TIMEOUT=30000

# Features
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true

# URLs
VITE_PUBLIC_URL=http://localhost:5173
VITE_RESULT_TOKEN_EXPIRY_DAYS=90

# External Services (se aplicável no frontend)
VITE_SENTRY_DSN=
```

---

# PARTE 2: GERENCIAMENTO DE ESTADO E DADOS

## 5. GERENCIAMENTO DE ESTADO (ZUSTAND)

### 5.1 Types Base (types/diagnostic.ts)

```typescript
// types/diagnostic.ts

export type DiagnosticStatus = 
  | 'idle' 
  | 'in_progress' 
  | 'processing' 
  | 'completed' 
  | 'abandoned' 
  | 'failed';

export type QuestionType = 
  | 'open_long' 
  | 'open_short';
  // V2: Perguntas 100% narrativas — tipos 'scale_and_text', 'scale_only' e 'multiple_choice' removidos

export type LifeArea =
  | 'Saúde Física'
  | 'Saúde Mental'
  | 'Saúde Espiritual'
  | 'Vida Pessoal'
  | 'Vida Amorosa'
  | 'Vida Familiar'
  | 'Vida Social'
  | 'Vida Profissional'
  | 'Finanças'
  | 'Educação'
  | 'Inovação'
  | 'Lazer';

export interface Question {
  id: number;
  text: string;
  area: LifeArea | string;
  type: QuestionType;
  phase: number;
  minWords: number;
  maxWords?: number;
  contextMessage?: string;
  follow_up_hint?: string;  // V2: Contexto para entender a resposta
}

export interface AnswerValue {
  text: string;
  scale: number | null;  // V2: Sempre null (perguntas 100% narrativas). Mantido por compatibilidade V1.
  words: number;
}

export interface Answer {
  questionId: number;
  questionText: string;
  questionArea: string;
  questionPhase: number;
  answerValue: AnswerValue;
  answeredAt: string;
  responseTimeSeconds?: number;
}

export interface Progress {
  overall: number;        // 0-100 (progresso geral ponderado)
  questions: number;      // Porcentagem de perguntas respondidas
  words: number;          // Porcentagem de palavras (meta: 3500)
  coverage: number;       // Porcentagem de áreas cobertas (12)
}

export interface EligibilityCriteria {
  questions: {
    current: number;
    required: number;
    met: boolean;
    percentage: number;
  };
  words: {
    current: number;
    required: number;
    met: boolean;
    percentage: number;
  };
  coverage: {
    current: number;
    required: number;
    met: boolean;
    missingAreas: string[];
  };
}

export interface VetorEstado {
  motor_dominante: string;
  motor_secundario: string;
  estagio_jornada: string;
  crise_raiz: string;
  crises_derivadas: string[];
  ponto_entrada_ideal: string;
  dominios_alavanca: string[];
  tom_emocional: string;
  risco_principal: string;
  necessidade_atual: string;
}

export interface DiagnosticResult {
  diagnosticId: string;
  overallScore: number;
  // V2: Vetor de Estado Qualitativo
  vetorEstado?: VetorEstado;
  memoriasVermelhas?: string[];
  areasSilenciadas?: number[];
  ancorasSugeridas?: string[];
  capitalSimbolico?: string[];
  // Legacy (mantidos por compatibilidade V1)
  scoresByArea: Record<string, number>;
  crisisAreas: Array<{ area: string; score: number }>;
  balancedAreas: Array<{ area: string; score: number }>;
  dominantMotor: string;
  journeyPhase: string;
  insights: {
    oldNarrative: string;
    symbolicIncongruences: string;
    circleConnections: string;
    assumptionPlan: string;
    climaxVision: string;
  };
  radarChartUrl?: string;
  pdfUrl?: string;
  completedAt: string;
}
```

### 5.2 Diagnostic Store (stores/diagnosticStore.ts)

```typescript
// stores/diagnosticStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type {
  DiagnosticStatus,
  Question,
  Answer,
  Progress,
  EligibilityCriteria,
  DiagnosticResult,
  AnswerValue,
} from '@/types';
import { LIFE_AREAS } from '@/lib/constants';

// Constantes de elegibilidade
const MIN_ANSWERS = 40;
const MIN_WORDS = 3500;
const TOTAL_AREAS = 12;
const QUESTIONS_PER_PHASE = 15;
const MAX_QUESTIONS = 60;

interface DiagnosticState {
  // === Identificadores ===
  diagnosticId: string | null;
  sessionId: string | null;
  userEmail: string | null;
  userName: string | null;
  resultToken: string | null;

  // === Estado do diagnóstico ===
  status: DiagnosticStatus;
  phase: number;
  currentQuestionIndex: number;

  // === Dados ===
  questions: Question[];
  answers: Record<number, Answer>;
  generatedQuestions: Record<number, Question[]>; // Fase -> Perguntas

  // === Progresso ===
  progress: Progress;
  eligibility: EligibilityCriteria | null;

  // === Resultado ===
  result: DiagnosticResult | null;

  // === Timestamps ===
  startedAt: string | null;
  lastActivityAt: string | null;

  // === Flags ===
  isLoading: boolean;
  isGeneratingQuestions: boolean;
  hasUnsavedChanges: boolean;

  // === Actions: Identificação ===
  setDiagnosticId: (id: string) => void;
  setSessionId: (id: string) => void;
  setUserInfo: (email: string, name?: string) => void;
  setResultToken: (token: string) => void;

  // === Actions: Estado ===
  setStatus: (status: DiagnosticStatus) => void;
  setPhase: (phase: number) => void;
  setCurrentQuestionIndex: (index: number) => void;

  // === Actions: Perguntas ===
  setQuestions: (questions: Question[]) => void;
  addGeneratedQuestions: (phase: number, questions: Question[]) => void;
  getCurrentQuestion: () => Question | null;

  // === Actions: Respostas ===
  setAnswer: (questionId: number, answer: Answer) => void;
  updateAnswerValue: (questionId: number, value: Partial<AnswerValue>) => void;
  getAnswer: (questionId: number) => Answer | undefined;

  // === Actions: Navegação ===
  nextQuestion: () => boolean;
  prevQuestion: () => boolean;
  goToQuestion: (index: number) => void;

  // === Actions: Progresso ===
  calculateProgress: () => Progress;
  checkEligibility: () => EligibilityCriteria;

  // === Actions: Resultado ===
  setResult: (result: DiagnosticResult) => void;

  // === Actions: Flags ===
  setIsLoading: (loading: boolean) => void;
  setIsGeneratingQuestions: (generating: boolean) => void;
  markAsChanged: () => void;
  markAsSaved: () => void;

  // === Actions: Reset ===
  reset: () => void;
  clearSession: () => void;
}

const initialState = {
  diagnosticId: null,
  sessionId: null,
  userEmail: null,
  userName: null,
  resultToken: null,
  status: 'idle' as DiagnosticStatus,
  phase: 1,
  currentQuestionIndex: 0,
  questions: [],
  answers: {},
  generatedQuestions: {},
  progress: { overall: 0, questions: 0, words: 0, coverage: 0 },
  eligibility: null,
  result: null,
  startedAt: null,
  lastActivityAt: null,
  isLoading: false,
  isGeneratingQuestions: false,
  hasUnsavedChanges: false,
};

export const useDiagnosticStore = create<DiagnosticState>()(
  persist(
    (set, get) => ({
      ...initialState,

      // === Actions: Identificação ===
      setDiagnosticId: (id) => set({ diagnosticId: id }),
      setSessionId: (id) => set({ sessionId: id }),
      setUserInfo: (email, name) => set({ userEmail: email, userName: name }),
      setResultToken: (token) => set({ resultToken: token }),

      // === Actions: Estado ===
      setStatus: (status) => set({ status }),
      setPhase: (phase) => set({ phase }),
      setCurrentQuestionIndex: (index) => set({ currentQuestionIndex: index }),

      // === Actions: Perguntas ===
      setQuestions: (questions) =>
        set({
          questions,
          currentQuestionIndex: 0,
          startedAt: new Date().toISOString(),
        }),

      addGeneratedQuestions: (phase, questions) =>
        set((state) => ({
          generatedQuestions: {
            ...state.generatedQuestions,
            [phase]: questions,
          },
          questions: [...state.questions, ...questions],
        })),

      getCurrentQuestion: () => {
        const state = get();
        return state.questions[state.currentQuestionIndex] || null;
      },

      // === Actions: Respostas ===
      setAnswer: (questionId, answer) =>
        set((state) => {
          const newAnswers = {
            ...state.answers,
            [questionId]: answer,
          };
          return {
            answers: newAnswers,
            hasUnsavedChanges: true,
            lastActivityAt: new Date().toISOString(),
          };
        }),

      updateAnswerValue: (questionId, value) =>
        set((state) => {
          const existingAnswer = state.answers[questionId];
          if (!existingAnswer) return state;

          return {
            answers: {
              ...state.answers,
              [questionId]: {
                ...existingAnswer,
                answerValue: { ...existingAnswer.answerValue, ...value },
              },
            },
            hasUnsavedChanges: true,
          };
        }),

      getAnswer: (questionId) => get().answers[questionId],

      // === Actions: Navegação ===
      nextQuestion: () => {
        const state = get();
        const nextIndex = state.currentQuestionIndex + 1;

        if (nextIndex < state.questions.length) {
          set({ currentQuestionIndex: nextIndex });
          return true;
        }
        return false;
      },

      prevQuestion: () => {
        const state = get();
        if (state.currentQuestionIndex > 0) {
          set({ currentQuestionIndex: state.currentQuestionIndex - 1 });
          return true;
        }
        return false;
      },

      goToQuestion: (index) => {
        const state = get();
        if (index >= 0 && index < state.questions.length) {
          set({ currentQuestionIndex: index });
        }
      },

      // === Actions: Progresso ===
      calculateProgress: () => {
        const state = get();
        const answeredCount = Object.keys(state.answers).length;
        const totalWords = Object.values(state.answers).reduce(
          (sum, a) => sum + (a.answerValue.words || 0),
          0
        );

        const coveredAreas = new Set(
          Object.values(state.answers).map((a) => a.questionArea)
        );

        const questionsProgress = Math.min(
          100,
          (answeredCount / MIN_ANSWERS) * 100
        );
        const wordsProgress = Math.min(100, (totalWords / MIN_WORDS) * 100);
        const coverageProgress = (coveredAreas.size / TOTAL_AREAS) * 100;

        // Progresso geral: média ponderada
        const overall =
          questionsProgress * 0.4 + wordsProgress * 0.4 + coverageProgress * 0.2;

        const progress = {
          overall: Math.round(overall),
          questions: Math.round(questionsProgress),
          words: Math.round(wordsProgress),
          coverage: Math.round(coverageProgress),
        };

        set({ progress });
        return progress;
      },

      checkEligibility: () => {
        const state = get();
        const answeredCount = Object.keys(state.answers).length;
        const totalWords = Object.values(state.answers).reduce(
          (sum, a) => sum + (a.answerValue.words || 0),
          0
        );

        const coveredAreas = new Set(
          Object.values(state.answers).map((a) => a.questionArea)
        );

        const missingAreas = LIFE_AREAS.filter(
          (area) => !coveredAreas.has(area)
        );

        const eligibility: EligibilityCriteria = {
          questions: {
            current: answeredCount,
            required: MIN_ANSWERS,
            met: answeredCount >= MIN_ANSWERS,
            percentage: Math.min(100, (answeredCount / MIN_ANSWERS) * 100),
          },
          words: {
            current: totalWords,
            required: MIN_WORDS,
            met: totalWords >= MIN_WORDS,
            percentage: Math.min(100, (totalWords / MIN_WORDS) * 100),
          },
          coverage: {
            current: coveredAreas.size,
            required: TOTAL_AREAS,
            met: coveredAreas.size >= TOTAL_AREAS,
            missingAreas,
          },
        };

        set({ eligibility });
        return eligibility;
      },

      // === Actions: Resultado ===
      setResult: (result) =>
        set({
          result,
          status: 'completed',
        }),

      // === Actions: Flags ===
      setIsLoading: (loading) => set({ isLoading: loading }),
      setIsGeneratingQuestions: (generating) =>
        set({ isGeneratingQuestions: generating }),
      markAsChanged: () => set({ hasUnsavedChanges: true }),
      markAsSaved: () => set({ hasUnsavedChanges: false }),

      // === Actions: Reset ===
      reset: () => set(initialState),

      clearSession: () =>
        set({
          ...initialState,
          diagnosticId: get().diagnosticId,
          userEmail: get().userEmail,
        }),
    }),
    {
      name: 'nara-diagnostic-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        diagnosticId: state.diagnosticId,
        sessionId: state.sessionId,
        userEmail: state.userEmail,
        userName: state.userName,
        phase: state.phase,
        currentQuestionIndex: state.currentQuestionIndex,
        answers: state.answers,
        progress: state.progress,
        status: state.status,
        startedAt: state.startedAt,
        lastActivityAt: state.lastActivityAt,
      }),
    }
  )
);

// Seletores utilitários
export const useCurrentQuestion = () =>
  useDiagnosticStore((state) => state.questions[state.currentQuestionIndex]);

export const useTotalAnswers = () =>
  useDiagnosticStore((state) => Object.keys(state.answers).length);

export const useTotalWords = () =>
  useDiagnosticStore((state) =>
    Object.values(state.answers).reduce(
      (sum, a) => sum + (a.answerValue.words || 0),
      0
    )
  );

export const useCanFinish = () =>
  useDiagnosticStore((state) => {
    const eligibility = state.eligibility;
    if (!eligibility) return false;
    return (
      (eligibility.questions.met || eligibility.words.met) &&
      eligibility.coverage.met
    );
  });
```

### 5.3 UI Store (stores/uiStore.ts)

```typescript
// stores/uiStore.ts
import { create } from 'zustand';

type ModalType =
  | 'eligibility'
  | 'saveExit'
  | 'resume'
  | 'share'
  | 'feedback'
  | 'error'
  | null;

interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  description?: string;
  duration?: number;
}

interface UIState {
  // === Modals ===
  activeModal: ModalType;
  modalData: Record<string, unknown>;

  // === Loading States ===
  isPageLoading: boolean;
  loadingMessage: string | null;

  // === Toasts ===
  toasts: Toast[];

  // === Sidebar/Navigation ===
  isSidebarOpen: boolean;

  // === Actions: Modals ===
  openModal: (modal: ModalType, data?: Record<string, unknown>) => void;
  closeModal: () => void;

  // === Actions: Loading ===
  setPageLoading: (loading: boolean, message?: string) => void;

  // === Actions: Toasts ===
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
  clearToasts: () => void;

  // === Actions: Navigation ===
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  activeModal: null,
  modalData: {},
  isPageLoading: false,
  loadingMessage: null,
  toasts: [],
  isSidebarOpen: false,

  openModal: (modal, data = {}) =>
    set({ activeModal: modal, modalData: data }),

  closeModal: () => set({ activeModal: null, modalData: {} }),

  setPageLoading: (loading, message = null) =>
    set({ isPageLoading: loading, loadingMessage: message }),

  addToast: (toast) =>
    set((state) => ({
      toasts: [
        ...state.toasts,
        { ...toast, id: `toast-${Date.now()}-${Math.random()}` },
      ],
    })),

  removeToast: (id) =>
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    })),

  clearToasts: () => set({ toasts: [] }),

  toggleSidebar: () =>
    set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),

  setSidebarOpen: (open) => set({ isSidebarOpen: open }),
}));
```

---

## 6. INTEGRAÇÃO COM API (REACT QUERY)

### 6.1 API Client (api/client.ts)

```typescript
// api/client.ts
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';
const API_TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT) || 30000;

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - adiciona headers de autenticação
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Adicionar token de auth se existir
    const token = localStorage.getItem('auth_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Adicionar session_id para usuários anônimos
    const sessionId = localStorage.getItem('session_id');
    if (sessionId && !token && config.headers) {
      config.headers['X-Session-ID'] = sessionId;
    }

    // Log de debug em desenvolvimento
    if (import.meta.env.DEV) {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - tratamento de erros global
apiClient.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log(`[API] Response:`, response.data);
    }
    return response;
  },
  (error: AxiosError) => {
    // Log de erro
    console.error('[API] Error:', error.response?.data || error.message);

    // Tratamento específico por status
    if (error.response?.status === 401) {
      // Token expirado - limpar auth e redirecionar
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }

    if (error.response?.status === 429) {
      // Rate limit - aguardar e tentar novamente
      const retryAfter = error.response.headers['retry-after'] || 5;
      console.warn(`Rate limited. Retry after ${retryAfter}s`);
    }

    return Promise.reject(error);
  }
);

export default apiClient;
```

### 6.2 API Endpoints (api/diagnostic.ts)

```typescript
// api/diagnostic.ts
import apiClient from './client';
import type {
  Question,
  Answer,
  Progress,
  EligibilityCriteria,
  DiagnosticResult,
} from '@/types';

// === Request Types ===
export interface CreateDiagnosticRequest {
  email: string;
  fullName?: string;
  consentPrivacy: boolean;
  consentMarketing: boolean;
  metadata?: Record<string, unknown>;
}

export interface SubmitAnswerRequest {
  questionId: number;
  questionText: string;
  questionArea: string;
  questionPhase: number;
  answerValue: {
    text: string;
    scale: number | null;
    words: number;
  };
  responseTimeSeconds?: number;
}

export interface SaveProgressRequest {
  diagnosticId: string;
  currentPhase: number;
  currentQuestion: number;
  answers: Answer[];
}

// === Response Types ===
export interface CreateDiagnosticResponse {
  diagnosticId: string;
  resultToken: string;
  status: string;
}

export interface GetQuestionsResponse {
  phase: number;
  questions: Question[];
  generationTimeMs: number;
}

export interface SubmitAnswerResponse {
  success: boolean;
  progress: {
    currentPhase: number;
    totalAnswers: number;
    totalWords: number;
    areasCovered: number;
  };
  eligibility: {
    canFinish: boolean;
    criteria: EligibilityCriteria;
  };
  nextQuestion?: Question;
  phaseCompleted?: boolean;
}

export interface CheckEligibilityResponse {
  canFinish: boolean;
  criteria: EligibilityCriteria;
  recommendation: string;
}

export interface FinishDiagnosticResponse {
  success: boolean;
  message: string;
  diagnosticId: string;
  resultToken: string;
  result: DiagnosticResult;
}

// === API Functions ===
export const diagnosticApi = {
  /**
   * Inicia um novo diagnóstico
   */
  start: async (
    data: CreateDiagnosticRequest
  ): Promise<CreateDiagnosticResponse> => {
    const response = await apiClient.post('/diagnostic/start', data);
    return response.data;
  },

  /**
   * Obtém perguntas da fase atual
   */
  getQuestions: async (diagnosticId: string): Promise<GetQuestionsResponse> => {
    const response = await apiClient.get(
      `/diagnostic/${diagnosticId}/questions`
    );
    return response.data;
  },

  /**
   * Submete uma resposta
   */
  submitAnswer: async (
    diagnosticId: string,
    data: SubmitAnswerRequest
  ): Promise<SubmitAnswerResponse> => {
    const response = await apiClient.post(
      `/diagnostic/${diagnosticId}/answer`,
      data
    );
    return response.data;
  },

  /**
   * Salva progresso parcial
   */
  saveProgress: async (data: SaveProgressRequest): Promise<{ success: boolean }> => {
    const response = await apiClient.post(
      `/diagnostic/${data.diagnosticId}/save`,
      data
    );
    return response.data;
  },

  /**
   * Verifica elegibilidade para finalização
   */
  checkEligibility: async (
    diagnosticId: string
  ): Promise<CheckEligibilityResponse> => {
    const response = await apiClient.get(
      `/diagnostic/${diagnosticId}/eligibility`
    );
    return response.data;
  },

  /**
   * Finaliza o diagnóstico e gera resultado
   */
  finish: async (diagnosticId: string): Promise<FinishDiagnosticResponse> => {
    const response = await apiClient.post(`/diagnostic/${diagnosticId}/finish`);
    return response.data;
  },

  /**
   * Obtém resultado do diagnóstico
   */
  getResult: async (
    diagnosticId: string,
    token: string
  ): Promise<DiagnosticResult> => {
    const response = await apiClient.get(
      `/diagnostic/${diagnosticId}/result`,
      { params: { token } }
    );
    return response.data;
  },

  /**
   * Envia magic link para retomada
   */
  sendMagicLink: async (
    diagnosticId: string
  ): Promise<{ success: boolean; message: string }> => {
    const response = await apiClient.post(
      `/diagnostic/${diagnosticId}/send-magic-link`
    );
    return response.data;
  },

  /**
   * Retoma diagnóstico via magic link
   */
  resumeFromToken: async (
    diagnosticId: string,
    token: string
  ): Promise<{
    diagnostic: {
      id: string;
      email: string;
      currentPhase: number;
      currentQuestion: number;
      status: string;
    };
    answers: Answer[];
    questions: Question[];
  }> => {
    const response = await apiClient.get(`/diagnostic/${diagnosticId}/resume`, {
      params: { token },
    });
    return response.data;
  },
};
```

### 6.3 Hook Principal (hooks/useDiagnostic.ts)

```typescript
// hooks/useDiagnostic.ts
import { useCallback } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { useDiagnosticStore } from '@/stores/diagnosticStore';
import { useUIStore } from '@/stores/uiStore';
import { diagnosticApi } from '@/api/diagnostic';
import type { Answer, AnswerValue } from '@/types';

export function useDiagnostic() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const store = useDiagnosticStore();
  const ui = useUIStore();

  // === Mutations ===

  // Iniciar diagnóstico
  const startMutation = useMutation({
    mutationFn: diagnosticApi.start,
    onMutate: () => {
      store.setIsLoading(true);
    },
    onSuccess: (data) => {
      store.setDiagnosticId(data.diagnosticId);
      store.setResultToken(data.resultToken);
      store.setStatus('in_progress');
      ui.addToast({
        type: 'success',
        title: 'Diagnóstico iniciado',
        description: 'Sua jornada de transformação começa agora!',
      });
      navigate('/diagnostico/fase');
    },
    onError: (error: Error) => {
      ui.addToast({
        type: 'error',
        title: 'Erro ao iniciar',
        description: error.message,
      });
    },
    onSettled: () => {
      store.setIsLoading(false);
    },
  });

  // Buscar perguntas
  const getQuestionsMutation = useMutation({
    mutationFn: (diagnosticId: string) =>
      diagnosticApi.getQuestions(diagnosticId),
    onMutate: () => {
      store.setIsGeneratingQuestions(true);
    },
    onSuccess: (data) => {
      if (data.phase === 1) {
        store.setQuestions(data.questions);
      } else {
        store.addGeneratedQuestions(data.phase, data.questions);
      }
      store.setPhase(data.phase);
    },
    onError: (error: Error) => {
      ui.addToast({
        type: 'error',
        title: 'Erro ao carregar perguntas',
        description: error.message,
      });
    },
    onSettled: () => {
      store.setIsGeneratingQuestions(false);
    },
  });

  // Submeter resposta
  const answerMutation = useMutation({
    mutationFn: ({
      questionId,
      answer,
    }: {
      questionId: number;
      answer: Answer;
    }) => {
      if (!store.diagnosticId) throw new Error('Diagnóstico não encontrado');
      return diagnosticApi.submitAnswer(store.diagnosticId, {
        questionId: answer.questionId,
        questionText: answer.questionText,
        questionArea: answer.questionArea,
        questionPhase: answer.questionPhase,
        answerValue: answer.answerValue,
        responseTimeSeconds: answer.responseTimeSeconds,
      });
    },
    onSuccess: (data, variables) => {
      // Atualizar progresso
      store.calculateProgress();

      // Verificar se completou fase
      if (data.phaseCompleted) {
        // Navegar para tela de transição
        navigate('/diagnostico/transicao');
      } else {
        // Avançar para próxima pergunta
        store.nextQuestion();
      }

      // Verificar elegibilidade
      if (data.eligibility.canFinish) {
        ui.openModal('eligibility', { criteria: data.eligibility.criteria });
      }
    },
    onError: (error: Error) => {
      ui.addToast({
        type: 'error',
        title: 'Erro ao salvar resposta',
        description: error.message,
      });
    },
  });

  // Finalizar diagnóstico
  const finishMutation = useMutation({
    mutationFn: () => {
      if (!store.diagnosticId) throw new Error('Diagnóstico não encontrado');
      return diagnosticApi.finish(store.diagnosticId);
    },
    onMutate: () => {
      store.setStatus('processing');
      ui.setPageLoading(true, 'Gerando seu Diagnóstico Narrativo...');
    },
    onSuccess: (data) => {
      store.setResult(data.result);
      store.setStatus('completed');
      navigate('/diagnostico/concluido');
    },
    onError: (error: Error) => {
      store.setStatus('failed');
      ui.addToast({
        type: 'error',
        title: 'Erro ao finalizar',
        description: error.message,
      });
    },
    onSettled: () => {
      ui.setPageLoading(false);
    },
  });

  // === Queries ===

  // Verificar elegibilidade (polling quando próximo)
  const eligibilityQuery = useQuery({
    queryKey: ['eligibility', store.diagnosticId],
    queryFn: () => diagnosticApi.checkEligibility(store.diagnosticId!),
    enabled: !!store.diagnosticId && store.progress.overall >= 60,
    refetchInterval: false,
  });

  // === Helper Functions ===

  const submitAnswer = useCallback(
    (questionId: number, value: AnswerValue) => {
      const question = store.questions.find((q) => q.id === questionId);
      if (!question) return;

      const answer: Answer = {
        questionId,
        questionText: question.text,
        questionArea: question.area,
        questionPhase: question.phase,
        answerValue: value,
        answeredAt: new Date().toISOString(),
      };

      // Salvar localmente primeiro
      store.setAnswer(questionId, answer);

      // Enviar para o servidor
      answerMutation.mutate({ questionId, answer });
    },
    [store, answerMutation]
  );

  const loadNextPhaseQuestions = useCallback(() => {
    if (store.diagnosticId) {
      getQuestionsMutation.mutate(store.diagnosticId);
    }
  }, [store.diagnosticId, getQuestionsMutation]);

  // === Return ===
  return {
    // Estado
    diagnosticId: store.diagnosticId,
    status: store.status,
    phase: store.phase,
    progress: store.progress,
    currentQuestion: store.getCurrentQuestion(),
    currentQuestionIndex: store.currentQuestionIndex,
    questions: store.questions,
    answers: store.answers,
    result: store.result,

    // Flags
    isLoading: store.isLoading,
    isGeneratingQuestions: store.isGeneratingQuestions,
    isSubmitting: answerMutation.isPending,
    isFinishing: finishMutation.isPending,

    // Actions
    start: startMutation.mutate,
    submitAnswer,
    loadNextPhaseQuestions,
    finish: finishMutation.mutate,
    nextQuestion: store.nextQuestion,
    prevQuestion: store.prevQuestion,
    goToQuestion: store.goToQuestion,
    reset: store.reset,

    // Elegibilidade
    eligibility: eligibilityQuery.data,
    canFinish:
      eligibilityQuery.data?.canFinish ||
      (store.eligibility &&
        (store.eligibility.questions.met || store.eligibility.words.met) &&
        store.eligibility.coverage.met),
  };
}
```

---

## 7. GESTÃO DE SESSÃO E AUTO-SAVE

### 7.1 Hook de Auto-Save (hooks/useAutoSave.ts)

```typescript
// hooks/useAutoSave.ts
import { useEffect, useRef, useCallback } from 'react';
import { useDebouncedCallback } from 'use-debounce';
import { useDiagnosticStore } from '@/stores/diagnosticStore';
import { useUIStore } from '@/stores/uiStore';
import { diagnosticApi } from '@/api/diagnostic';

interface UseAutoSaveOptions {
  debounceMs?: number;
  maxWaitMs?: number;
  saveEveryNAnswers?: number;
}

/**
 * Hook para auto-save de progresso do diagnóstico.
 *
 * Estratégia de persistência:
 * - LocalStorage: A cada resposta (instantâneo via Zustand persist)
 * - Servidor: A cada N respostas ou após período de inatividade
 *
 * @param options Configurações do auto-save
 */
export function useAutoSave(options: UseAutoSaveOptions = {}) {
  const {
    debounceMs = 5000,
    maxWaitMs = 30000,
    saveEveryNAnswers = 3,
  } = options;

  const {
    diagnosticId,
    phase,
    currentQuestionIndex,
    answers,
    hasUnsavedChanges,
    markAsSaved,
  } = useDiagnosticStore();

  const { addToast } = useUIStore();

  const lastSavedCount = useRef(0);
  const isSaving = useRef(false);

  // Função de save para o servidor
  const saveToServer = useCallback(async () => {
    if (!diagnosticId || isSaving.current) return;

    isSaving.current = true;

    try {
      await diagnosticApi.saveProgress({
        diagnosticId,
        currentPhase: phase,
        currentQuestion: currentQuestionIndex,
        answers: Object.values(answers),
      });

      markAsSaved();
      lastSavedCount.current = Object.keys(answers).length;

      addToast({
        type: 'success',
        title: '✓ Progresso salvo',
        duration: 2000,
      });
    } catch (error) {
      console.error('[AutoSave] Falha ao salvar:', error);
      // Não mostrar erro - localStorage mantém backup
    } finally {
      isSaving.current = false;
    }
  }, [diagnosticId, phase, currentQuestionIndex, answers, markAsSaved, addToast]);

  // Debounced save
  const debouncedSave = useDebouncedCallback(saveToServer, debounceMs, {
    maxWait: maxWaitMs,
  });

  // Trigger save quando houver mudanças
  useEffect(() => {
    if (!hasUnsavedChanges || !diagnosticId) return;

    const currentCount = Object.keys(answers).length;
    const newAnswersCount = currentCount - lastSavedCount.current;

    // Salvar a cada N novas respostas
    if (newAnswersCount >= saveEveryNAnswers) {
      saveToServer();
    } else {
      // Ou após debounce
      debouncedSave();
    }
  }, [
    hasUnsavedChanges,
    answers,
    diagnosticId,
    saveEveryNAnswers,
    saveToServer,
    debouncedSave,
  ]);

  // Save antes de sair da página
  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (hasUnsavedChanges) {
        e.preventDefault();
        e.returnValue = '';
        // Tentar save síncrono via beacon
        if (diagnosticId) {
          navigator.sendBeacon(
            `/api/v1/diagnostic/${diagnosticId}/save`,
            JSON.stringify({
              currentPhase: phase,
              currentQuestion: currentQuestionIndex,
              answers: Object.values(answers),
            })
          );
        }
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [hasUnsavedChanges, diagnosticId, phase, currentQuestionIndex, answers]);

  return {
    saveNow: saveToServer,
    isSaving: isSaving.current,
    hasUnsavedChanges,
  };
}
```

### 7.2 Hook de Recuperação de Sessão

```typescript
// hooks/useSessionRecovery.ts
import { useEffect, useState } from 'react';
import { useDiagnosticStore } from '@/stores/diagnosticStore';
import { useUIStore } from '@/stores/uiStore';
import { diagnosticApi } from '@/api/diagnostic';

interface SessionRecoveryState {
  hasExistingSession: boolean;
  sessionData: {
    diagnosticId: string;
    currentQuestion: number;
    totalAnswers: number;
    lastActivity: string;
  } | null;
  isChecking: boolean;
}

/**
 * Hook para verificar e recuperar sessões existentes
 */
export function useSessionRecovery() {
  const [state, setState] = useState<SessionRecoveryState>({
    hasExistingSession: false,
    sessionData: null,
    isChecking: true,
  });

  const store = useDiagnosticStore();
  const { openModal } = useUIStore();

  useEffect(() => {
    checkExistingSession();
  }, []);

  const checkExistingSession = async () => {
    // Verificar localStorage primeiro
    const savedDiagnosticId = store.diagnosticId;
    const savedAnswers = store.answers;
    const savedStatus = store.status;

    if (
      savedDiagnosticId &&
      savedStatus === 'in_progress' &&
      Object.keys(savedAnswers).length > 0
    ) {
      setState({
        hasExistingSession: true,
        sessionData: {
          diagnosticId: savedDiagnosticId,
          currentQuestion: store.currentQuestionIndex,
          totalAnswers: Object.keys(savedAnswers).length,
          lastActivity: store.lastActivityAt || new Date().toISOString(),
        },
        isChecking: false,
      });

      // Abrir modal de retomada
      openModal('resume', {
        diagnosticId: savedDiagnosticId,
        progress: store.progress,
        lastActivity: store.lastActivityAt,
      });
    } else {
      setState({
        hasExistingSession: false,
        sessionData: null,
        isChecking: false,
      });
    }
  };

  const resumeSession = async () => {
    if (!state.sessionData) return;

    try {
      // Sincronizar com servidor se necessário
      // O estado já está no Zustand via persist
      return true;
    } catch (error) {
      console.error('Erro ao retomar sessão:', error);
      return false;
    }
  };

  const startNewSession = () => {
    store.reset();
    setState({
      hasExistingSession: false,
      sessionData: null,
      isChecking: false,
    });
  };

  return {
    ...state,
    resumeSession,
    startNewSession,
  };
}
```

---

# PARTE 3: COMPONENTES E UI

## 8. DESIGN SYSTEM COMPLETO

### 8.1 Paleta de Cores

```css
/* Cores Primárias - Gradiente Roxo/Rosa */
--primary-50: #eef2ff;
--primary-100: #e0e7ff;
--primary-200: #c7d2fe;
--primary-300: #a5b4fc;
--primary-400: #818cf8;
--primary-500: #6366f1;    /* Principal */
--primary-600: #4f46e5;
--primary-700: #4338ca;
--primary-800: #3730a3;
--primary-900: #312e81;

/* Cores de Feedback */
--success: #22c55e;
--success-light: #dcfce7;
--warning: #f59e0b;
--warning-light: #fef3c7;
--error: #ef4444;
--error-light: #fee2e2;
--info: #3b82f6;
--info-light: #dbeafe;

/* Cores das 12 Áreas Estruturantes */
--area-saude-fisica: #22c55e;      /* Verde */
--area-saude-mental: #8b5cf6;      /* Roxo */
--area-saude-espiritual: #f59e0b;  /* Âmbar */
--area-vida-pessoal: #ec4899;      /* Rosa */
--area-vida-amorosa: #ef4444;      /* Vermelho */
--area-vida-familiar: #06b6d4;     /* Ciano */
--area-vida-social: #3b82f6;       /* Azul */
--area-vida-profissional: #6366f1; /* Índigo */
--area-financas: #10b981;          /* Esmeralda */
--area-educacao: #f97316;          /* Laranja */
--area-inovacao: #a855f7;          /* Violeta */
--area-lazer: #14b8a6;             /* Teal */

/* Neutros */
--gray-50: #fafafa;
--gray-100: #f4f4f5;
--gray-200: #e4e4e7;
--gray-300: #d4d4d8;
--gray-400: #a1a1aa;
--gray-500: #71717a;
--gray-600: #52525b;
--gray-700: #3f3f46;
--gray-800: #27272a;
--gray-900: #18181b;
```

### 8.2 Tipografia

```css
/* Font Stack */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 
             Roboto, 'Helvetica Neue', Arial, sans-serif;

/* Headings */
.h1 { 
  font-size: 2.25rem;      /* 36px */
  line-height: 2.5rem;     /* 40px */
  font-weight: 700;
  letter-spacing: -0.025em;
}

.h2 { 
  font-size: 1.5rem;       /* 24px */
  line-height: 2rem;       /* 32px */
  font-weight: 600;
}

.h3 { 
  font-size: 1.25rem;      /* 20px */
  line-height: 1.75rem;    /* 28px */
  font-weight: 500;
}

.h4 {
  font-size: 1.125rem;     /* 18px */
  line-height: 1.5rem;     /* 24px */
  font-weight: 500;
}

/* Body Text */
.body-lg { 
  font-size: 1.125rem;     /* 18px */
  line-height: 1.75rem;    /* 28px */
}

.body-md { 
  font-size: 1rem;         /* 16px */
  line-height: 1.5rem;     /* 24px */
}

.body-sm { 
  font-size: 0.875rem;     /* 14px */
  line-height: 1.25rem;    /* 20px */
}

/* Labels e Helpers */
.label { 
  font-size: 0.875rem;     /* 14px */
  font-weight: 500;
  color: var(--gray-700);
}

.helper { 
  font-size: 0.75rem;      /* 12px */
  color: var(--gray-500);
}

.caption {
  font-size: 0.625rem;     /* 10px */
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

### 8.3 Espaçamentos (Spacing Scale)

```css
/* Base: 4px */
--space-0: 0;
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

### 8.4 Componentes Base (Design Tokens)

```typescript
// lib/constants.ts

export const DESIGN_TOKENS = {
  // Border Radius
  radius: {
    none: '0',
    sm: '0.25rem',    // 4px
    md: '0.375rem',   // 6px
    lg: '0.5rem',     // 8px
    xl: '0.75rem',    // 12px
    '2xl': '1rem',    // 16px
    full: '9999px',
  },

  // Shadows
  shadow: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
  },

  // Transitions
  transition: {
    fast: '150ms ease-out',
    normal: '200ms ease-out',
    slow: '300ms ease-out',
    slower: '500ms ease-out',
  },

  // Z-Index Scale
  zIndex: {
    dropdown: 50,
    sticky: 100,
    modal: 200,
    popover: 250,
    toast: 300,
    tooltip: 350,
  },

  // Breakpoints
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
};

// Cores das 12 Áreas (para uso em componentes)
export const AREA_COLORS: Record<string, string> = {
  'Saúde Física': '#22c55e',
  'Saúde Mental': '#8b5cf6',
  'Saúde Espiritual': '#f59e0b',
  'Vida Pessoal': '#ec4899',
  'Vida Amorosa': '#ef4444',
  'Vida Familiar': '#06b6d4',
  'Vida Social': '#3b82f6',
  'Vida Profissional': '#6366f1',
  'Finanças': '#10b981',
  'Educação': '#f97316',
  'Inovação': '#a855f7',
  'Lazer': '#14b8a6',
};

export const LIFE_AREAS = [
  'Saúde Física',
  'Saúde Mental',
  'Saúde Espiritual',
  'Vida Pessoal',
  'Vida Amorosa',
  'Vida Familiar',
  'Vida Social',
  'Vida Profissional',
  'Finanças',
  'Educação',
  'Inovação',
  'Lazer',
] as const;

export const PHASES = [
  { id: 1, name: 'Baseline', description: 'Conhecendo você', questions: 15 },
  { id: 2, name: 'Aprofundamento 1', description: 'Explorando padrões', questions: 15 },
  { id: 3, name: 'Aprofundamento 2', description: 'Revelando conexões', questions: 15 },
  { id: 4, name: 'Refinamento', description: 'Refinando insights', questions: 15 },
] as const;

export const ELIGIBILITY = {
  MIN_ANSWERS: 40,
  MIN_WORDS: 3500,
  TOTAL_AREAS: 12,
  MAX_QUESTIONS: 60,
  QUESTIONS_PER_PHASE: 15,
} as const;
```

---

## 9. COMPONENTES PRINCIPAIS

### 9.1 QuestionCard (components/diagnostic/QuestionCard.tsx)

```typescript
// components/diagnostic/QuestionCard.tsx
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScaleInput } from './ScaleInput';
import { TextInput } from './TextInput';
import { Badge } from '@/components/ui/badge';
import { AREA_COLORS } from '@/lib/constants';
import type { Question, AnswerValue } from '@/types';
import { ChevronLeft, ChevronRight, Save, Loader2 } from 'lucide-react';

interface QuestionCardProps {
  question: Question;
  questionNumber: number;
  totalQuestions: number;
  initialValue?: AnswerValue;
  onSubmit: (value: AnswerValue) => void;
  onPrevious?: () => void;
  onSaveExit?: () => void;
  isSubmitting?: boolean;
  isFirst?: boolean;
  canGoBack?: boolean;
}

export function QuestionCard({
  question,
  questionNumber,
  totalQuestions,
  initialValue,
  onSubmit,
  onPrevious,
  onSaveExit,
  isSubmitting = false,
  isFirst = false,
  canGoBack = true,
}: QuestionCardProps) {
  const [text, setText] = useState(initialValue?.text || '');
  const [wordCount, setWordCount] = useState(initialValue?.words || 0);
  const [startTime] = useState(Date.now());
  const [hasInteracted, setHasInteracted] = useState(false);
  // V2: Perguntas 100% narrativas — sem lógica de escala

  // Atualizar contagem de palavras
  useEffect(() => {
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    setWordCount(words);
  }, [text]);

  // Validação (V2: apenas texto narrativo, sem escala)
  const minWords = question.minWords || 10;
  const isTextValid = wordCount >= minWords;
  const isValid = isTextValid;

  const handleSubmit = () => {
    if (!isValid) return;

    const responseTime = Math.round((Date.now() - startTime) / 1000);

    onSubmit({
      text,
      scale: null, // V2: Perguntas 100% narrativas
      words: wordCount,
    });
  };

  const areaColor = AREA_COLORS[question.area] || '#6366f1';

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className="w-full max-w-2xl mx-auto"
    >
      <Card className="shadow-lg border-0 bg-white/95 backdrop-blur">
        <CardHeader className="pb-4">
          {/* Indicador de área */}
          <div className="flex items-center justify-between mb-4">
            <Badge
              style={{ backgroundColor: areaColor }}
              className="text-white font-medium"
            >
              {question.area}
            </Badge>
            <span className="text-sm text-gray-500">
              Pergunta {questionNumber} de {totalQuestions}
            </span>
          </div>

          {/* Mensagem contextual (se existir) */}
          {question.contextMessage && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-4 p-3 bg-primary-50 rounded-lg border-l-4 border-primary-500"
            >
              <p className="text-sm text-primary-800 italic">
                {question.contextMessage}
              </p>
            </motion.div>
          )}

          {/* Texto da pergunta */}
          <h2 className="text-xl font-semibold text-gray-900 leading-relaxed">
            {question.text}
          </h2>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* V2: Perguntas 100% narrativas — ScaleInput removido */}

          {/* follow_up_hint (V2) */}
          {question.follow_up_hint && (
            <p className="text-xs text-gray-400 italic mb-2">
              {question.follow_up_hint}
            </p>
          )}

          {/* Input de texto */}
          <TextInput
            value={text}
            onChange={(value) => {
              setText(value);
              setHasInteracted(true);
            }}
            placeholder={
              question.type === 'text_only'
                ? 'Escreva sua resposta com detalhes...'
                : 'Descreva em suas palavras...'
            }
            minWords={minWords}
            maxWords={question.maxWords}
          />

          {/* Barra de ações */}
          <div className="flex items-center justify-between pt-4 border-t border-gray-100">
            <div className="flex gap-2">
              {/* Botão Anterior */}
              {canGoBack && !isFirst && (
                <Button
                  variant="ghost"
                  onClick={onPrevious}
                  disabled={isSubmitting}
                  className="text-gray-600"
                >
                  <ChevronLeft className="w-4 h-4 mr-1" />
                  Anterior
                </Button>
              )}

              {/* Botão Salvar e Sair */}
              <Button
                variant="outline"
                onClick={onSaveExit}
                disabled={isSubmitting}
                className="text-gray-600"
              >
                <Save className="w-4 h-4 mr-1" />
                Salvar e Sair
              </Button>
            </div>

            {/* Botão Próxima */}
            <Button
              onClick={handleSubmit}
              disabled={!isValid || isSubmitting}
              className="px-8 bg-primary-600 hover:bg-primary-700"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Salvando...
                </>
              ) : (
                <>
                  Continuar
                  <ChevronRight className="w-4 h-4 ml-1" />
                </>
              )}
            </Button>
          </div>

          {/* Feedback de validação */}
          {hasInteracted && !isValid && (
            <motion.div
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-sm text-amber-600 text-center"
            >
              {!isTextValid && (
                <span>
                  Mínimo de {minWords} palavras ({wordCount}/{minWords})
                </span>
              )}
            </motion.div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
```

### 9.2 ScaleInput (components/diagnostic/ScaleInput.tsx)

```typescript
// components/diagnostic/ScaleInput.tsx
import { cn } from '@/lib/utils';

interface ScaleInputProps {
  value: number | null;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  labels?: [string, string];
  className?: string;
}

export function ScaleInput({
  value,
  onChange,
  min = 0,
  max = 5,
  labels = ['Discordo totalmente', 'Concordo totalmente'],
  className,
}: ScaleInputProps) {
  const options = Array.from({ length: max - min + 1 }, (_, i) => i + min);

  return (
    <div className={cn('space-y-4', className)}>
      {/* Botões de escala */}
      <div
        className="flex justify-between gap-2"
        role="radiogroup"
        aria-label="Escala de resposta"
      >
        {options.map((num) => (
          <button
            key={num}
            type="button"
            role="radio"
            aria-checked={value === num}
            onClick={() => onChange(num)}
            className={cn(
              'flex-1 py-4 px-2 rounded-xl border-2 transition-all duration-200',
              'hover:border-primary-400 hover:bg-primary-50',
              'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
              value === num
                ? 'border-primary-500 bg-primary-100 text-primary-700 font-semibold shadow-md'
                : 'border-gray-200 bg-white text-gray-600'
            )}
          >
            <span className="text-2xl font-bold block">{num}</span>
          </button>
        ))}
      </div>

      {/* Labels extremos */}
      <div className="flex justify-between text-sm text-gray-500 px-1">
        <span>{labels[0]}</span>
        <span>{labels[1]}</span>
      </div>
    </div>
  );
}
```

### 9.3 TextInput (components/diagnostic/TextInput.tsx)

```typescript
// components/diagnostic/TextInput.tsx
import { useState, useEffect } from 'react';
import { Textarea } from '@/components/ui/textarea';
import { cn } from '@/lib/utils';

interface TextInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  minWords?: number;
  maxWords?: number;
  maxLength?: number;
  className?: string;
}

export function TextInput({
  value,
  onChange,
  placeholder = 'Digite sua resposta...',
  minWords = 10,
  maxWords,
  maxLength = 5000,
  className,
}: TextInputProps) {
  const [wordCount, setWordCount] = useState(0);
  const [charCount, setCharCount] = useState(0);

  useEffect(() => {
    setCharCount(value.length);
    setWordCount(value.trim() ? value.trim().split(/\s+/).length : 0);
  }, [value]);

  const isMinMet = wordCount >= minWords;
  const isMaxExceeded = maxWords && wordCount > maxWords;

  const getStatusColor = () => {
    if (charCount === 0) return 'text-gray-400';
    if (isMaxExceeded) return 'text-red-500';
    if (isMinMet) return 'text-green-600';
    return 'text-amber-500';
  };

  return (
    <div className={cn('space-y-2', className)}>
      <Textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        maxLength={maxLength}
        rows={6}
        className={cn(
          'resize-none transition-colors duration-200',
          'focus:ring-2 focus:ring-primary-500 focus:border-transparent',
          charCount > 0 && !isMinMet && 'border-amber-400',
          isMinMet && 'border-green-400',
          isMaxExceeded && 'border-red-400'
        )}
        aria-describedby="word-count-hint"
      />

      {/* Contador e feedback */}
      <div
        id="word-count-hint"
        className="flex justify-between text-sm"
      >
        <span className={getStatusColor()}>
          {isMinMet ? (
            <span className="flex items-center gap-1">
              <CheckIcon className="w-4 h-4" />
              {wordCount} palavras
            </span>
          ) : (
            <span>
              {wordCount} / {minWords} palavras mínimas
            </span>
          )}
        </span>
        <span className="text-gray-400">
          {charCount.toLocaleString()} caracteres
        </span>
      </div>

      {/* Barra de progresso visual */}
      <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={cn(
            'h-full transition-all duration-300',
            isMinMet ? 'bg-green-500' : 'bg-amber-500'
          )}
          style={{
            width: `${Math.min(100, (wordCount / minWords) * 100)}%`,
          }}
        />
      </div>
    </div>
  );
}

function CheckIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
    </svg>
  );
}
```

### 9.4 ProgressBar (components/diagnostic/ProgressBar.tsx)

```typescript
// components/diagnostic/ProgressBar.tsx
import { motion } from 'framer-motion';
import { Progress } from '@/components/ui/progress';
import { PHASES } from '@/lib/constants';
import { cn } from '@/lib/utils';
import type { Progress as ProgressType } from '@/types';

interface ProgressBarProps {
  progress: ProgressType;
  phase: number;
  questionsAnswered: number;
  totalWords: number;
  className?: string;
}

export function ProgressBar({
  progress,
  phase,
  questionsAnswered,
  totalWords,
  className,
}: ProgressBarProps) {
  const currentPhase = PHASES.find((p) => p.id === phase);

  return (
    <div className={cn('space-y-4 p-4 bg-gray-50 rounded-xl', className)}>
      {/* Fase atual */}
      <div className="flex justify-between items-center">
        <div>
          <span className="text-sm font-medium text-gray-700">
            Fase {phase}: {currentPhase?.name}
          </span>
          <p className="text-xs text-gray-500">
            {currentPhase?.description}
          </p>
        </div>
        <span className="text-sm text-gray-500">
          {questionsAnswered} perguntas
        </span>
      </div>

      {/* Barra de progresso principal */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600">Progresso geral</span>
          <span className="font-medium text-primary-600">
            {Math.round(progress.overall)}%
          </span>
        </div>
        <Progress value={progress.overall} className="h-3" />
      </div>

      {/* Indicadores secundários */}
      <div className="grid grid-cols-3 gap-4 pt-2 border-t border-gray-200">
        <ProgressIndicator
          label="Perguntas"
          value={progress.questions}
          detail={`${questionsAnswered}/40`}
        />
        <ProgressIndicator
          label="Palavras"
          value={progress.words}
          detail={`${totalWords.toLocaleString()}/3.500`}
        />
        <ProgressIndicator
          label="Áreas"
          value={progress.coverage}
          detail={`${Math.round((progress.coverage / 100) * 12)}/12`}
        />
      </div>

      {/* Indicador de fases */}
      <div className="flex gap-1 pt-2">
        {PHASES.map((p) => (
          <motion.div
            key={p.id}
            className={cn(
              'flex-1 h-1.5 rounded-full transition-colors',
              p.id < phase
                ? 'bg-primary-500'
                : p.id === phase
                ? 'bg-primary-300'
                : 'bg-gray-200'
            )}
            initial={false}
            animate={{
              scale: p.id === phase ? [1, 1.1, 1] : 1,
            }}
            transition={{ duration: 0.5 }}
          />
        ))}
      </div>
    </div>
  );
}

function ProgressIndicator({
  label,
  value,
  detail,
}: {
  label: string;
  value: number;
  detail: string;
}) {
  return (
    <div className="text-center">
      <div className="text-xs text-gray-500 mb-1">{label}</div>
      <div className="relative h-1 bg-gray-200 rounded-full overflow-hidden">
        <motion.div
          className="absolute h-full bg-primary-400"
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        />
      </div>
      <div className="text-xs font-medium text-gray-600 mt-1">{detail}</div>
    </div>
  );
}
```

### 9.5 EligibilityModal (components/diagnostic/EligibilityModal.tsx)

```typescript
// components/diagnostic/EligibilityModal.tsx
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import { CheckCircle2, Circle, Sparkles, ArrowRight } from 'lucide-react';
import type { EligibilityCriteria } from '@/types';

interface EligibilityModalProps {
  isOpen: boolean;
  onClose: () => void;
  onContinue: () => void;
  onFinish: () => void;
  criteria: EligibilityCriteria;
}

export function EligibilityModal({
  isOpen,
  onClose,
  onContinue,
  onFinish,
  criteria,
}: EligibilityModalProps) {
  const canFinish =
    (criteria.questions.met || criteria.words.met) && criteria.coverage.met;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-xl">
            {canFinish ? (
              <>
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: 'spring', duration: 0.5 }}
                >
                  <Sparkles className="h-6 w-6 text-amber-500" />
                </motion.div>
                Diagnóstico Pronto!
              </>
            ) : (
              <>
                <Circle className="h-6 w-6 text-amber-500" />
                Quase lá!
              </>
            )}
          </DialogTitle>
          <DialogDescription>
            {canFinish
              ? 'Você atingiu o mínimo necessário para receber seu Diagnóstico Narrativo. Deseja finalizar agora ou continuar para insights mais profundos?'
              : 'Continue respondendo para atingir os critérios mínimos do seu diagnóstico.'}
          </DialogDescription>
        </DialogHeader>

        {/* Critérios */}
        <div className="space-y-4 py-6">
          <CriteriaItem
            label="Perguntas Respondidas"
            current={criteria.questions.current}
            required={criteria.questions.required}
            met={criteria.questions.met}
          />
          <CriteriaItem
            label="Palavras Escritas"
            current={criteria.words.current}
            required={criteria.words.required}
            met={criteria.words.met}
            formatValue={(v) => v.toLocaleString()}
          />
          <CriteriaItem
            label="Áreas Cobertas"
            current={criteria.coverage.current}
            required={criteria.coverage.required}
            met={criteria.coverage.met}
          />

          {/* Áreas faltantes */}
          {criteria.coverage.missingAreas.length > 0 && (
            <div className="mt-4 p-3 bg-amber-50 rounded-lg">
              <p className="text-sm text-amber-800 font-medium mb-2">
                Áreas ainda não exploradas:
              </p>
              <div className="flex flex-wrap gap-1">
                {criteria.coverage.missingAreas.map((area) => (
                  <span
                    key={area}
                    className="text-xs px-2 py-1 bg-amber-100 text-amber-700 rounded"
                  >
                    {area}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        <DialogFooter className="flex gap-2 sm:gap-2">
          {canFinish ? (
            <>
              <Button variant="outline" onClick={onContinue} className="flex-1">
                Continuar Respondendo
              </Button>
              <Button onClick={onFinish} className="flex-1">
                Gerar Diagnóstico
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </>
          ) : (
            <Button onClick={onClose} className="w-full">
              Continuar Respondendo
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function CriteriaItem({
  label,
  current,
  required,
  met,
  formatValue = (v) => String(v),
}: {
  label: string;
  current: number;
  required: number;
  met: boolean;
  formatValue?: (v: number) => string;
}) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-sm text-gray-600">{label}</span>
      <div className="flex items-center gap-3">
        <span
          className={`text-sm font-medium ${
            met ? 'text-green-600' : 'text-gray-900'
          }`}
        >
          {formatValue(current)} / {formatValue(required)}
        </span>
        {met ? (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', duration: 0.3 }}
          >
            <CheckCircle2 className="h-5 w-5 text-green-500" />
          </motion.div>
        ) : (
          <Circle className="h-5 w-5 text-gray-300" />
        )}
      </div>
    </div>
  );
}
```

---

## 10. FORMULÁRIOS E VALIDAÇÕES

### 10.1 Schemas Zod (lib/validation.ts)

```typescript
// lib/validation.ts
import { z } from 'zod';

// Email validation com regex mais preciso
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Domínios de email descartáveis (blacklist)
const disposableEmailDomains = [
  'tempmail.com',
  'throwaway.email',
  '10minutemail.com',
  'guerrillamail.com',
  'mailinator.com',
  // ... adicionar mais conforme necessário
];

// Schema para criação de diagnóstico
export const createDiagnosticSchema = z.object({
  email: z
    .string()
    .min(1, 'E-mail é obrigatório')
    .email('E-mail inválido')
    .refine((email) => {
      const domain = email.split('@')[1]?.toLowerCase();
      return !disposableEmailDomains.includes(domain);
    }, 'Por favor, use um e-mail válido (não temporário)'),
  fullName: z
    .string()
    .max(100, 'Nome muito longo')
    .optional()
    .transform((val) => val?.trim()),
  consentPrivacy: z
    .boolean()
    .refine((val) => val === true, 'Você deve aceitar a Política de Privacidade'),
  consentMarketing: z.boolean().default(false),
});

// Schema para resposta (V2: scale sempre null — perguntas 100% narrativas)
export const answerValueSchema = z.object({
  text: z
    .string()
    .min(1, 'Resposta é obrigatória')
    .max(5000, 'Resposta muito longa'),
  scale: z.number().min(0).max(5).nullable(),  // LEGACY V1: Sempre null em V2
  words: z.number().min(0),
});

export const answerSchema = z.object({
  questionId: z.number(),
  questionText: z.string(),
  questionArea: z.string(),
  questionPhase: z.number().min(1).max(4),
  answerValue: answerValueSchema,
  answeredAt: z.string().datetime(),
  responseTimeSeconds: z.number().optional(),
});

// Schema para feedback
export const feedbackSchema = z.object({
  rating: z.number().min(1).max(5),
  npsScore: z.number().min(0).max(10),
  feedbackText: z.string().max(2000).optional(),
  feedbackType: z.enum(['public', 'private']).default('private'),
});

// Validação customizada para mínimo de palavras
export function validateMinWords(text: string, minWords: number): boolean {
  const words = text.trim().split(/\s+/).filter(Boolean).length;
  return words >= minWords;
}

// Tipos inferidos dos schemas
export type CreateDiagnosticInput = z.infer<typeof createDiagnosticSchema>;
export type AnswerValueInput = z.infer<typeof answerValueSchema>;
export type AnswerInput = z.infer<typeof answerSchema>;
export type FeedbackInput = z.infer<typeof feedbackSchema>;
```

### 10.2 WelcomeForm (components/forms/WelcomeForm.tsx)

```typescript
// components/forms/WelcomeForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { createDiagnosticSchema, CreateDiagnosticInput } from '@/lib/validation';
import { Loader2, ArrowRight, Lock, Mail, User } from 'lucide-react';

interface WelcomeFormProps {
  onSubmit: (data: CreateDiagnosticInput) => void;
  isSubmitting: boolean;
}

export function WelcomeForm({ onSubmit, isSubmitting }: WelcomeFormProps) {
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isValid },
  } = useForm<CreateDiagnosticInput>({
    resolver: zodResolver(createDiagnosticSchema),
    mode: 'onChange',
    defaultValues: {
      email: '',
      fullName: '',
      consentPrivacy: false,
      consentMarketing: false,
    },
  });

  const consentPrivacy = watch('consentPrivacy');
  const consentMarketing = watch('consentMarketing');

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Campo Nome (opcional) */}
      <div className="space-y-2">
        <Label htmlFor="fullName" className="flex items-center gap-2">
          <User className="w-4 h-4 text-gray-400" />
          Nome (opcional)
        </Label>
        <Input
          id="fullName"
          placeholder="Ex: Maria Silva"
          {...register('fullName')}
          className="h-12"
          autoComplete="name"
        />
        <p className="text-xs text-gray-500">
          Usado apenas para personalizar seu relatório
        </p>
      </div>

      {/* Campo Email (obrigatório) */}
      <div className="space-y-2">
        <Label htmlFor="email" className="flex items-center gap-2">
          <Mail className="w-4 h-4 text-gray-400" />
          E-mail <span className="text-red-500">*</span>
        </Label>
        <Input
          id="email"
          type="email"
          placeholder="seuemail@exemplo.com"
          {...register('email')}
          className={`h-12 ${errors.email ? 'border-red-500' : ''}`}
          autoComplete="email"
          aria-invalid={errors.email ? 'true' : 'false'}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && (
          <motion.p
            id="email-error"
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-sm text-red-500"
            role="alert"
          >
            {errors.email.message}
          </motion.p>
        )}
        <p className="text-xs text-gray-500">
          Usaremos para enviar seus resultados
        </p>
      </div>

      {/* Separador */}
      <div className="border-t border-gray-200 pt-6">
        <div className="flex items-center gap-2 mb-4">
          <Lock className="w-4 h-4 text-gray-400" />
          <span className="text-sm font-medium text-gray-700">
            Privacidade e Segurança
          </span>
        </div>

        {/* Checkbox Privacidade (obrigatório) */}
        <div className="space-y-4">
          <label className="flex items-start gap-3 cursor-pointer">
            <Checkbox
              id="consentPrivacy"
              checked={consentPrivacy}
              onCheckedChange={(checked) =>
                setValue('consentPrivacy', checked as boolean, {
                  shouldValidate: true,
                })
              }
              className="mt-0.5"
              aria-describedby="privacy-description"
            />
            <div className="flex-1">
              <span className="text-sm text-gray-700">
                Li e aceito a{' '}
                <a
                  href="/privacidade"
                  target="_blank"
                  className="text-primary-600 hover:underline"
                >
                  Política de Privacidade
                </a>{' '}
                <span className="text-red-500">*</span>
              </span>
              <p id="privacy-description" className="text-xs text-gray-500 mt-1">
                Seus dados são protegidos e você pode deletá-los a qualquer momento
              </p>
            </div>
          </label>
          {errors.consentPrivacy && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-sm text-red-500 ml-7"
              role="alert"
            >
              {errors.consentPrivacy.message}
            </motion.p>
          )}

          {/* Checkbox Marketing (opcional) */}
          <label className="flex items-start gap-3 cursor-pointer">
            <Checkbox
              id="consentMarketing"
              checked={consentMarketing}
              onCheckedChange={(checked) =>
                setValue('consentMarketing', checked as boolean)
              }
              className="mt-0.5"
            />
            <div className="flex-1">
              <span className="text-sm text-gray-700">
                Aceito receber conteúdos personalizados e novidades
              </span>
              <p className="text-xs text-gray-500 mt-1">
                Você pode cancelar a qualquer momento
              </p>
            </div>
          </label>
        </div>
      </div>

      {/* Botão Submit */}
      <Button
        type="submit"
        disabled={!isValid || isSubmitting}
        className="w-full h-14 text-lg font-semibold bg-primary-600 hover:bg-primary-700"
      >
        {isSubmitting ? (
          <>
            <Loader2 className="w-5 h-5 mr-2 animate-spin" />
            Iniciando...
          </>
        ) : (
          <>
            Começar Meu Diagnóstico Narrativo
            <ArrowRight className="w-5 h-5 ml-2" />
          </>
        )}
      </Button>

      {/* Texto de segurança */}
      <p className="text-xs text-center text-gray-400">
        🔒 Conexão segura. NUNCA vendemos seus dados.
      </p>
    </form>
  );
}
```

---

# PARTE 4: FLUXOS E EXPERIÊNCIA

## 11. FLUXOS DE USUÁRIO (11 ETAPAS)

### 11.1 Visão Geral do Fluxo

```
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 1: LANDING PAGE                                            │
│ • Hero section com proposta de valor                             │
│ • Grid das 12 Áreas interativo                                   │
│ • CTA: "Descobrir Minha Incongruência Simbólica"                │
│ Rota: /                                                          │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 2: TELA DE BOAS-VINDAS                                     │
│ • Explicação do processo (60 perguntas, 20-30 min)               │
│ • Form: nome (opcional), email (obrigatório)                     │
│ • Checkboxes LGPD                                                │
│ • CTA: "Começar Meu Diagnóstico Narrativo"                       │
│ Rota: /diagnostico                                               │
│ Backend: POST /diagnostic/start → diagnostic_id                  │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 3: FASE 1 - BASELINE (Perguntas 1-15)                      │
│ • 15 perguntas fixas (hardcoded)                                 │
│ • Progressive disclosure (uma por vez)                           │
│ • Validação: mínimo 10 palavras                                  │
│ • Auto-save a cada resposta                                      │
│ • Botões: [← Anterior] [Salvar e Sair] [Próxima →]              │
│ Rota: /diagnostico/fase                                          │
│ Backend: POST /diagnostic/{id}/answer para cada                  │
└────────────────────────┬─────────────────────────────────────────┘
                         │ Completa pergunta 15
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 4: TRANSIÇÃO FASE 1 → FASE 2                               │
│ • Loading animado (3-5 segundos)                                 │
│ • Mensagem: "Gerando perguntas personalizadas..."                │
│ • Backend: RAG + GPT-4o gera 15 perguntas                        │
│ Rota: /diagnostico/transicao                                     │
│ Backend: GET /diagnostic/{id}/questions                          │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 5: FASE 2 - ADAPTATIVA (Perguntas 16-30)                   │
│ • 15 perguntas geradas via RAG                                   │
│ • Mensagens contextuais: "Percebi que..."                        │
│ • Botão "Finalizar" aparece (desabilitado)                       │
│ Rota: /diagnostico/fase                                          │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 6: FASES 3-4 (Perguntas 31-60)                             │
│ • Repetição do processo RAG                                      │
│ • Modal de elegibilidade quando critérios atingidos              │
│ • Opções: [Continuar] [Gerar Diagnóstico]                        │
└────────────────────────┬─────────────────────────────────────────┘
                         │ Usuário clica "Gerar Diagnóstico"
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 7: PROCESSAMENTO FINAL                                     │
│ • Confete animado                                                │
│ • Loading elaborado (5-10 segundos)                              │
│ • Mensagens rotativas: "Calculando scores...",                   │
│   "Gerando insights...", "Preparando relatório..."               │
│ Rota: /diagnostico/processando                                   │
│ Backend: POST /diagnostic/{id}/finish                            │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 8: CELEBRAÇÃO                                              │
│ • Confete + mensagem de parabéns                                 │
│ • "Seu relatório chegará no e-mail em segundos"                  │
│ • Preview do score geral                                         │
│ Rota: /diagnostico/concluido                                     │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 9: E-MAIL RECEBIDO                                         │
│ • Gráfico radar inline                                           │
│ • Score geral + áreas críticas                                   │
│ • Insight principal                                              │
│ • PDF anexo                                                      │
│ • Botões: [Ver Análise] [Compartilhar] [Feedback] [Waitlist]     │
│ (Enviado pelo backend via Resend)                                │
└────────────────────────┬─────────────────────────────────────────┘
                         │ Usuário clica [Ver Análise Completa]
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 10: RESULTADO COMPLETO                                     │
│ • Gráfico radar interativo                                       │
│ • Score geral destacado                                          │
│ • Análise das 12 áreas (cards expandíveis)                       │
│ • Insight narrativo completo                                     │
│ • Recomendações acionáveis                                       │
│ • Banner: "Crie conta grátis para salvar"                        │
│ Rota: /dashboard/diagnostico/:id?token=xxx                       │
│ Backend: GET /diagnostic/{id}/result?token=xxx                   │
└────────────────────────┬────────────────────────────────
─────────┘
                         │ (Opcional) Criar conta
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 11: RETORNO / CRIAR CONTA                                  │
│ • Formulário de signup (email pré-preenchido)                    │
│ • Vinculação do diagnóstico ao user_id                           │
│ • Dashboard com histórico de diagnósticos                        │
│ Rota: /signup?email=xxx&diagnosticId=xxx                         │
└──────────────────────────────────────────────────────────────────┘
```

### 11.2 Wireframe Textual - Tela de Boas-Vindas

```
┌──────────────────────────────────────────────────────────────┐
│  [Logo NARA]                                                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  🎯 Revele Seu Círculo Narrativo nas 12 Áreas               │
│     Estruturantes da Vida                                    │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  📋 O que você vai fazer:                                    │
│  ✓ Responder 60 perguntas de escuta ativa                   │
│  ✓ Tempo estimado: 20-30 minutos                            │
│  ✓ Você pode pausar e voltar depois                         │
│                                                              │
│  🎁 O que você vai receber:                                  │
│  ✓ Diagnóstico Narrativo das 12 Áreas Estruturantes         │
│  ✓ Gráfico radar do seu Círculo Narrativo                   │
│  ✓ Plano de Assunção Intencional (M2X)                      │
│  ✓ PDF completo no seu e-mail                               │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  Nome (opcional):                                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Ex: Maria Silva                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  E-mail (obrigatório): *                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ seuemail@exemplo.com                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│  Usaremos para enviar seus resultados                        │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  🔒 Privacidade e Segurança:                                 │
│                                                              │
│  ☑ Li e aceito a Política de Privacidade * (obrigatório)    │
│  ☐ Aceito receber conteúdos personalizados (opcional)       │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     [Começar Meu Diagnóstico Narrativo]    →         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  🔒 Conexão segura. NUNCA vendemos seus dados.               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 11.3 Wireframe Textual - Pergunta Individual

```
┌──────────────────────────────────────────────────────────────┐
│  [████████░░░░░░░░░░] 67% completo                           │
│  40 de 60 perguntas • 3.254 palavras escritas                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Pergunta 16 de 60                         [Vida Pessoal]    │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  💭 Percebi que você mencionou sentir que está no      │ │
│  │  "piloto automático" em algumas áreas da vida...       │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Se sua vida hoje fosse um livro, qual seria o título       │
│  do capítulo atual? O quanto você se sente de fato o        │
│  protagonista da sua própria história?                      │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐     │
│  │  0   │ │  1   │ │  2   │ │  ●3  │ │  4   │ │  5   │     │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘     │
│  Não sou protagonista ←─────────────→ Totalmente protagonista│
│                                                              │
│  Descreva em detalhes (mínimo 10 palavras):                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                                                        │ │
│  │  Sinto que minha vida está parecendo um livro         │ │
│  │  onde o capítulo atual seria "A Encruzilhada".        │ │
│  │  Tenho tomado decisões mais por necessidade do        │ │
│  │  que por verdadeira escolha...                        │ │
│  │                                                        │ │
│  └────────────────────────────────────────────────────────┘ │
│  ✓ 45 palavras escritas                                      │
│  [████████████████████░░░░░░░░░░░] 45/10 palavras           │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  [← Anterior]    [Salvar e Sair]    [Continuar →]           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 12. ROTEAMENTO E NAVEGAÇÃO

### 12.1 Configuração de Rotas (App.tsx)

```typescript
// App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Suspense, lazy } from 'react';
import { Toaster } from '@/components/ui/toaster';
import { LoadingScreen } from '@/components/layout/LoadingScreen';

// Lazy loading de páginas
const Home = lazy(() => import('@/pages/Home'));
const Welcome = lazy(() => import('@/pages/Welcome'));
const Diagnostic = lazy(() => import('@/pages/Diagnostic'));
const Transition = lazy(() => import('@/pages/Transition'));
const Celebration = lazy(() => import('@/pages/Celebration'));
const Result = lazy(() => import('@/pages/Result'));
const Resume = lazy(() => import('@/pages/Resume'));
const Waitlist = lazy(() => import('@/pages/Waitlist'));
const Feedback = lazy(() => import('@/pages/Feedback'));
const NotFound = lazy(() => import('@/pages/NotFound'));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutos
      gcTime: 30 * 60 * 1000,    // 30 minutos
      retry: 2,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Suspense fallback={<LoadingScreen />}>
          <Routes>
            {/* Landing Page */}
            <Route path="/" element={<Home />} />

            {/* Fluxo do Diagnóstico */}
            <Route path="/diagnostico" element={<Welcome />} />
            <Route path="/diagnostico/fase" element={<Diagnostic />} />
            <Route path="/diagnostico/transicao" element={<Transition />} />
            <Route path="/diagnostico/concluido" element={<Celebration />} />

            {/* Retomada via Magic Link */}
            <Route path="/diagnostico/retomar/:id" element={<Resume />} />

            {/* Resultado (link público com token) */}
            <Route path="/dashboard/diagnostico/:id" element={<Result />} />

            {/* Páginas auxiliares */}
            <Route path="/waitlist" element={<Waitlist />} />
            <Route path="/feedback/:id" element={<Feedback />} />

            {/* 404 */}
            <Route path="/404" element={<NotFound />} />
            <Route path="*" element={<Navigate to="/404" replace />} />
          </Routes>
        </Suspense>

        {/* Toast global */}
        <Toaster />
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
```

### 12.2 Protected Route Guard

```typescript
// components/layout/DiagnosticGuard.tsx
import { Navigate, useLocation } from 'react-router-dom';
import { useDiagnosticStore } from '@/stores/diagnosticStore';
import { ReactNode } from 'react';

interface DiagnosticGuardProps {
  children: ReactNode;
  requireDiagnosticId?: boolean;
  requireAnswers?: boolean;
  minAnswers?: number;
}

export function DiagnosticGuard({
  children,
  requireDiagnosticId = true,
  requireAnswers = false,
  minAnswers = 0,
}: DiagnosticGuardProps) {
  const location = useLocation();
  const { diagnosticId, answers, status } = useDiagnosticStore();
  const answersCount = Object.keys(answers).length;

  // Se diagnóstico já foi completado, redirecionar para resultado
  if (status === 'completed') {
    return <Navigate to={`/dashboard/diagnostico/${diagnosticId}`} replace />;
  }

  // Verificar se tem diagnostic_id
  if (requireDiagnosticId && !diagnosticId) {
    return <Navigate to="/diagnostico" state={{ from: location }} replace />;
  }

  // Verificar mínimo de respostas
  if (requireAnswers && answersCount < minAnswers) {
    return <Navigate to="/diagnostico/fase" replace />;
  }

  return <>{children}</>;
}
```

---

## 13. GRÁFICO RADAR DAS 12 ÁREAS

### 13.1 RadarChart Component (components/result/RadarChart.tsx)

```typescript
// components/result/RadarChart.tsx
import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';
import { motion } from 'framer-motion';
import { AREA_COLORS, LIFE_AREAS } from '@/lib/constants';

interface RadarChartProps {
  scores: Record<string, number>;
  className?: string;
  showAnimation?: boolean;
  interactive?: boolean;
}

export function RadarChart({
  scores,
  className = '',
  showAnimation = true,
  interactive = true,
}: RadarChartProps) {
  // Preparar dados para o Recharts
  const data = LIFE_AREAS.map((area, index) => ({
    area,
    score: scores[area] || 0,
    fullMark: 5,
    color: Object.values(AREA_COLORS)[index],
    index,
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload }: any) => {
    if (!active || !payload || !payload.length) return null;
    
    const data = payload[0].payload;
    return (
      <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
        <p className="font-semibold text-gray-900">{data.area}</p>
        <p className="text-lg">
          <span className="font-bold" style={{ color: data.color }}>
            {data.score.toFixed(1)}
          </span>
          <span className="text-gray-500">/5</span>
        </p>
      </div>
    );
  };

  // Custom label
  const CustomLabel = ({ cx, cy, payload }: any) => {
    return (
      <text
        x={cx}
        y={cy}
        textAnchor="middle"
        dominantBaseline="middle"
        className="fill-gray-700 text-xs font-medium"
      >
        {payload.value}
      </text>
    );
  };

  return (
    <motion.div
      className={`w-full ${className}`}
      initial={showAnimation ? { opacity: 0, scale: 0.9 } : false}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      <ResponsiveContainer width="100%" height={400}>
        <RechartsRadarChart
          cx="50%"
          cy="50%"
          outerRadius="75%"
          data={data}
        >
          {/* Grid polar */}
          <PolarGrid
            gridType="polygon"
            stroke="#e5e7eb"
            strokeWidth={1}
          />

          {/* Eixo angular (labels das áreas) */}
          <PolarAngleAxis
            dataKey="area"
            tick={({ payload, x, y, textAnchor }) => {
              const areaIndex = LIFE_AREAS.indexOf(payload.value);
              const color = Object.values(AREA_COLORS)[areaIndex];
              
              return (
                <g transform={`translate(${x},${y})`}>
                  <text
                    x={0}
                    y={0}
                    dy={4}
                    textAnchor={textAnchor}
                    className="text-xs font-medium"
                    fill={color}
                  >
                    {truncateText(payload.value, 12)}
                  </text>
                </g>
              );
            }}
          />

          {/* Eixo radial (valores 0-5) */}
          <PolarRadiusAxis
            angle={90}
            domain={[0, 5]}
            tick={{ fill: '#9ca3af', fontSize: 10 }}
            tickCount={6}
          />

          {/* Área preenchida com gradiente */}
          <defs>
            <linearGradient id="radarGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#6366f1" stopOpacity={0.8} />
              <stop offset="100%" stopColor="#8b5cf6" stopOpacity={0.4} />
            </linearGradient>
          </defs>

          {/* Radar principal */}
          <Radar
            name="Score"
            dataKey="score"
            stroke="#6366f1"
            strokeWidth={2}
            fill="url(#radarGradient)"
            fillOpacity={0.6}
            dot={{
              r: 4,
              fill: '#6366f1',
              stroke: '#fff',
              strokeWidth: 2,
            }}
            activeDot={{
              r: 6,
              fill: '#4f46e5',
              stroke: '#fff',
              strokeWidth: 2,
            }}
            isAnimationActive={showAnimation}
            animationDuration={1500}
            animationEasing="ease-out"
          />

          {/* Tooltip interativo */}
          {interactive && (
            <Tooltip content={<CustomTooltip />} />
          )}
        </RechartsRadarChart>
      </ResponsiveContainer>
    </motion.div>
  );
}

// Helper para truncar texto longo
function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - 1) + '…';
}
```

### 13.2 RadarChartMini (versão compacta)

```typescript
// components/result/RadarChartMini.tsx
import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  ResponsiveContainer,
} from 'recharts';
import { AREA_COLORS, LIFE_AREAS } from '@/lib/constants';

interface RadarChartMiniProps {
  scores: Record<string, number>;
  size?: number;
}

export function RadarChartMini({ scores, size = 120 }: RadarChartMiniProps) {
  const data = LIFE_AREAS.map((area) => ({
    area,
    score: scores[area] || 0,
  }));

  return (
    <div style={{ width: size, height: size }}>
      <ResponsiveContainer>
        <RechartsRadarChart data={data}>
          <PolarGrid stroke="#e5e7eb" />
          <Radar
            dataKey="score"
            stroke="#6366f1"
            fill="#6366f1"
            fillOpacity={0.4}
          />
        </RechartsRadarChart>
      </ResponsiveContainer>
    </div>
  );
}
```

---

# PARTE 5: QUALIDADE E PERFORMANCE

## 14. RESPONSIVIDADE E MOBILE-FIRST

### 14.1 Breakpoints e Utilitários

```typescript
// hooks/useMediaQuery.ts
import { useState, useEffect } from 'react';

const BREAKPOINTS = {
  sm: '(min-width: 640px)',
  md: '(min-width: 768px)',
  lg: '(min-width: 1024px)',
  xl: '(min-width: 1280px)',
  '2xl': '(min-width: 1536px)',
};

type Breakpoint = keyof typeof BREAKPOINTS;

export function useMediaQuery(breakpoint: Breakpoint | string): boolean {
  const query = BREAKPOINTS[breakpoint as Breakpoint] || breakpoint;
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    setMatches(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => {
      setMatches(event.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, [query]);

  return matches;
}

export function useIsMobile(): boolean {
  return !useMediaQuery('md');
}

export function useIsTablet(): boolean {
  const isMd = useMediaQuery('md');
  const isLg = useMediaQuery('lg');
  return isMd && !isLg;
}

export function useIsDesktop(): boolean {
  return useMediaQuery('lg');
}
```

### 14.2 Container Responsivo

```typescript
// components/layout/Container.tsx
import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface ContainerProps {
  children: ReactNode;
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
}

const sizeClasses = {
  sm: 'max-w-md',
  md: 'max-w-2xl',
  lg: 'max-w-4xl',
  xl: 'max-w-6xl',
  full: 'max-w-full',
};

export function Container({
  children,
  className,
  size = 'lg',
}: ContainerProps) {
  return (
    <div
      className={cn(
        'mx-auto w-full px-4 sm:px-6 lg:px-8',
        sizeClasses[size],
        className
      )}
    >
      {children}
    </div>
  );
}
```

---

## 15. ACESSIBILIDADE (WCAG)

### 15.1 Componente Acessível - VisuallyHidden

```typescript
// components/ui/visually-hidden.tsx
import { ReactNode } from 'react';

interface VisuallyHiddenProps {
  children: ReactNode;
}

export function VisuallyHidden({ children }: VisuallyHiddenProps) {
  return (
    <span
      style={{
        position: 'absolute',
        width: '1px',
        height: '1px',
        padding: 0,
        margin: '-1px',
        overflow: 'hidden',
        clip: 'rect(0, 0, 0, 0)',
        whiteSpace: 'nowrap',
        border: 0,
      }}
    >
      {children}
    </span>
  );
}
```

### 15.2 Skip Link

```typescript
// components/layout/SkipLink.tsx
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-primary-600 focus:text-white focus:rounded-md"
    >
      Pular para o conteúdo principal
    </a>
  );
}
```

### 15.3 Checklist de Acessibilidade

```markdown
## Checklist WCAG 2.1 AA para NARA

### Perceivable
- [x] Textos com contraste mínimo 4.5:1 (AA)
- [x] Imagens com alt text descritivo
- [x] Formulários com labels associados
- [x] Mensagens de erro visíveis e claras
- [x] Foco visível em elementos interativos

### Operable
- [x] Navegação completa por teclado
- [x] Skip links para conteúdo principal
- [x] Timeout estendido ou desabilitável
- [x] Sem armadilhas de foco (focus traps)
- [x] Ordem de tabulação lógica

### Understandable
- [x] Linguagem clara e consistente
- [x] Labels e instruções descritivas
- [x] Validação de formulários em tempo real
- [x] Mensagens de erro específicas
- [x] Confirmação antes de ações destrutivas

### Robust
- [x] HTML semântico válido
- [x] ARIA roles e labels apropriados
- [x] Componentes compatíveis com leitores de tela
- [x] Testado com NVDA/VoiceOver
```

---

## 16. PERFORMANCE E OTIMIZAÇÕES

### 16.1 Code Splitting e Lazy Loading

```typescript
// Já implementado em App.tsx com React.lazy()

// Para componentes pesados específicos:
// components/result/RadarChart.tsx
import { lazy, Suspense } from 'react';

const RadarChartLazy = lazy(() => import('./RadarChart'));

export function RadarChartWrapper(props: RadarChartProps) {
  return (
    <Suspense fallback={<RadarChartSkeleton />}>
      <RadarChartLazy {...props} />
    </Suspense>
  );
}
```

### 16.2 Otimização de Imagens

```typescript
// components/ui/OptimizedImage.tsx
import { useState } from 'react';
import { cn } from '@/lib/utils';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width: number;
  height: number;
  className?: string;
  priority?: boolean;
}

export function OptimizedImage({
  src,
  alt,
  width,
  height,
  className,
  priority = false,
}: OptimizedImageProps) {
  const [isLoaded, setIsLoaded] = useState(false);

  return (
    <div
      className={cn('relative overflow-hidden bg-gray-100', className)}
      style={{ aspectRatio: `${width} / ${height}` }}
    >
      <img
        src={src}
        alt={alt}
        width={width}
        height={height}
        loading={priority ? 'eager' : 'lazy'}
        decoding="async"
        onLoad={() => setIsLoaded(true)}
        className={cn(
          'object-cover w-full h-full transition-opacity duration-300',
          isLoaded ? 'opacity-100' : 'opacity-0'
        )}
      />
      {!isLoaded && (
        <div className="absolute inset-0 animate-pulse bg-gray-200" />
      )}
    </div>
  );
}
```

### 16.3 Memoização de Componentes

```typescript
// Exemplo de memoização para lista de perguntas
import { memo, useMemo } from 'react';

export const QuestionList = memo(function QuestionList({
  questions,
  currentIndex,
}: {
  questions: Question[];
  currentIndex: number;
}) {
  const visibleQuestions = useMemo(
    () => questions.slice(Math.max(0, currentIndex - 2), currentIndex + 3),
    [questions, currentIndex]
  );

  return (
    <div className="space-y-4">
      {visibleQuestions.map((q) => (
        <QuestionCard key={q.id} question={q} />
      ))}
    </div>
  );
});
```

---

## 17. TRATAMENTO DE ERROS

### 17.1 Error Boundary

```typescript
// components/ErrorBoundary.tsx
import { Component, ErrorInfo, ReactNode } from 'react';
import { Button } from '@/components/ui/button';
import { AlertTriangle, RefreshCw } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
    // Aqui você pode enviar para serviço de monitoramento (Sentry, etc)
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="min-h-screen flex items-center justify-center p-4">
          <div className="max-w-md w-full text-center space-y-6">
            <div className="flex justify-center">
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
                <AlertTriangle className="w-8 h-8 text-red-600" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Ops! Algo deu errado
              </h1>
              <p className="text-gray-600">
                Encontramos um problema inesperado. Seu progresso foi salvo automaticamente.
              </p>
            </div>
            <Button onClick={this.handleReset} className="gap-2">
              <RefreshCw className="w-4 h-4" />
              Tentar novamente
            </Button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### 17.2 Hook de Tratamento de Erros da API

```typescript
// hooks/useApiError.ts
import { useCallback } from 'react';
import { AxiosError } from 'axios';
import { useUIStore } from '@/stores/uiStore';

interface ApiErrorResponse {
  detail?: string;
  message?: string;
  errors?: Record<string, string[]>;
}

export function useApiError() {
  const { addToast } = useUIStore();

  const handleError = useCallback(
    (error: unknown, customMessage?: string) => {
      console.error('API Error:', error);

      let message = customMessage || 'Ocorreu um erro inesperado';
      let title = 'Erro';

      if (error instanceof AxiosError) {
        const data = error.response?.data as ApiErrorResponse;

        if (error.response?.status === 400) {
          title = 'Dados inválidos';
          message = data?.detail || data?.message || 'Verifique os dados informados';
        } else if (error.response?.status === 401) {
          title = 'Sessão expirada';
          message = 'Por favor, faça login novamente';
        } else if (error.response?.status === 403) {
          title = 'Acesso negado';
          message = 'Você não tem permissão para esta ação';
        } else if (error.response?.status === 404) {
          title = 'Não encontrado';
          message = 'O recurso solicitado não existe';
        } else if (error.response?.status === 429) {
          title = 'Muitas requisições';
          message = 'Aguarde um momento e tente novamente';
        } else if (error.response?.status >= 500) {
          title = 'Erro no servidor';
          message = 'Tente novamente em alguns instantes';
        } else if (!error.response) {
          title = 'Sem conexão';
          message = 'Verifique sua conexão com a internet';
        }
      }

      addToast({
        type: 'error',
        title,
        description: message,
        duration: 5000,
      });
    },
    [addToast]
  );

  return { handleError };
}
```

---

## 18. ANIMAÇÕES E TRANSIÇÕES

### 18.1 Variantes de Animação (Framer Motion)

```typescript
// lib/animations.ts
import { Variants } from 'framer-motion';

// Fade simples
export const fadeVariants: Variants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
};

// Slide de baixo para cima
export const slideUpVariants: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

// Slide da direita para esquerda (navegação de perguntas)
export const slideRightVariants: Variants = {
  initial: { opacity: 0, x: 50 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -50 },
};

// Scale in (para modais e cards)
export const scaleVariants: Variants = {
  initial: { opacity: 0, scale: 0.95 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.95 },
};

// Stagger children (para listas)
export const staggerContainerVariants: Variants = {
  initial: {},
  animate: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

export const staggerItemVariants: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
};

// Transições padrão
export const defaultTransition = {
  duration: 0.3,
  ease: [0.25, 0.1, 0.25, 1], // ease-out-quad
};

export const springTransition = {
  type: 'spring',
  stiffness: 300,
  damping: 30,
};
```

### 18.2 PageTransition Component

```typescript
// components/layout/PageTransition.tsx
import { motion, AnimatePresence } from 'framer-motion';
import { ReactNode } from 'react';
import { useLocation } from 'react-router-dom';
import { slideUpVariants, defaultTransition } from '@/lib/animations';

interface PageTransitionProps {
  children: ReactNode;
}

export function PageTransition({ children }: PageTransitionProps) {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        variants={slideUpVariants}
        initial="initial"
        animate="animate"
        exit="exit"
        transition={defaultTransition}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

### 18.3 Confetti para Celebração

```typescript
// hooks/useConfetti.ts
import confetti from 'canvas-confetti';
import { useCallback } from 'react';

export function useConfetti() {
  const fire = useCallback(() => {
    // Configuração para confete roxo/rosa (cores do NARA)
    const count = 200;
    const defaults = {
      origin: { y: 0.7 },
      colors: ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#22c55e'],
    };

    function fire(particleRatio: number, opts: confetti.Options) {
      confetti({
        ...defaults,
        ...opts,
        particleCount: Math.floor(count * particleRatio),
      });
    }

    // Sequência de explosões
    fire(0.25, {
      spread: 26,
      startVelocity: 55,
    });

    fire(0.2, {
      spread: 60,
    });

    fire(0.35, {
      spread: 100,
      decay: 0.91,
      scalar: 0.8,
    });

    fire(0.1, {
      spread: 120,
      startVelocity: 25,
      decay: 0.92,
      scalar: 1.2,
    });

    fire(0.1, {
      spread: 120,
      startVelocity: 45,
    });
  }, []);

  return { fire };
}
```

---

## 19. TESTES FRONTEND

### 19.1 Configuração Vitest (vite.config.ts)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'src/test/'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### 19.2 Setup de Testes (src/test/setup.ts)

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock do localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};
global.localStorage = localStorageMock as unknown as Storage;

// Mock do matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock do ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));
```

### 19.3 Exemplo de Teste de Componente

```typescript
// src/components/diagnostic/__tests__/QuestionCard.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QuestionCard } from '../QuestionCard';

describe('QuestionCard', () => {
  const mockQuestion = {
    id: 1,
    text: 'Como você avalia sua saúde física?',
    area: 'Saúde Física',
    type: 'scale_and_text' as const,
    phase: 1,
    minWords: 10,
  };

  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('deve renderizar a pergunta corretamente', () => {
    render(
      <QuestionCard
        question={mockQuestion}
        questionNumber={1}
        totalQuestions={60}
        onSubmit={mockOnSubmit}
      />
    );

    expect(screen.getByText('Como você avalia sua saúde física?')).toBeInTheDocument();
    expect(screen.getByText('Saúde Física')).toBeInTheDocument();
    expect(screen.getByText('Pergunta 1 de 60')).toBeInTheDocument();
  });

  it('deve desabilitar botão de continuar quando resposta é inválida', () => {
    render(
      <QuestionCard
        question={mockQuestion}
        questionNumber={1}
        totalQuestions={60}
        onSubmit={mockOnSubmit}
      />
    );

    const submitButton = screen.getByRole('button', { name: /continuar/i });
    expect(submitButton).toBeDisabled();
  });

  it('deve habilitar botão quando resposta é válida', async () => {
    const user = userEvent.setup();

    render(
      <QuestionCard
        question={mockQuestion}
        questionNumber={1}
        totalQuestions={60}
        onSubmit={mockOnSubmit}
      />
    );

    // Selecionar escala
    const scaleButton = screen.getByRole('radio', { name: /3/i });
    await user.click(scaleButton);

    // Digitar texto com mínimo de palavras
    const textarea = screen.getByPlaceholderText(/descreva/i);
    await user.type(
      textarea,
      'Esta é uma resposta com mais de dez palavras para passar na validação do formulário.'
    );

    // Verificar que botão está habilitado
    const submitButton = screen.getByRole('button', { name: /continuar/i });
    await waitFor(() => {
      expect(submitButton).not.toBeDisabled();
    });
  });

  it('deve chamar onSubmit com valores corretos', async () => {
    const user = userEvent.setup();

    render(
      <QuestionCard
        question={mockQuestion}
        questionNumber={1}
        totalQuestions={60}
        onSubmit={mockOnSubmit}
      />
    );

    // Preencher resposta válida
    await user.click(screen.getByRole('radio', { name: /4/i }));
    await user.type(
      screen.getByPlaceholderText(/descreva/i),
      'Minha saúde física está boa, faço exercícios regularmente e me alimento bem.'
    );

    // Submeter
    await user.click(screen.getByRole('button', { name: /continuar/i }));

    expect(mockOnSubmit).toHaveBeenCalledWith({
      text: expect.stringContaining('Minha saúde física está boa'),
      scale: 4,
      words: expect.any(Number),
    });
  });
});
```

### 19.4 Teste de Store (Zustand)

```typescript
// src/stores/__tests__/diagnosticStore.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { useDiagnosticStore } from '../diagnosticStore';

describe('diagnosticStore', () => {
  beforeEach(() => {
    useDiagnosticStore.getState().reset();
  });

  it('deve iniciar com estado padrão', () => {
    const state = useDiagnosticStore.getState();
    expect(state.diagnosticId).toBeNull();
    expect(state.status).toBe('idle');
    expect(state.phase).toBe(1);
    expect(Object.keys(state.answers)).toHaveLength(0);
  });

  it('deve salvar resposta corretamente', () => {
    const { setAnswer } = useDiagnosticStore.getState();

    setAnswer(1, {
      questionId: 1,
      questionText: 'Pergunta teste',
      questionArea: 'Saúde Física',
      questionPhase: 1,
      answerValue: { text: 'Resposta teste', scale: 3, words: 2 },
      answeredAt: new Date().toISOString(),
    });

    const state = useDiagnosticStore.getState();
    expect(state.answers[1]).toBeDefined();
    expect(state.answers[1].answerValue.scale).toBe(3);
    expect(state.hasUnsavedChanges).toBe(true);
  });

  it('deve calcular progresso corretamente', () => {
    const store = useDiagnosticStore.getState();

    // Simular 20 respostas
    for (let i = 1; i <= 20; i++) {
      store.setAnswer(i, {
        questionId: i,
        questionText: `Pergunta ${i}`,
        questionArea: 'Saúde Física',
        questionPhase: 1,
        answerValue: { text: 'Resposta '.repeat(10), scale: 3, words: 20 },
        answeredAt: new Date().toISOString(),
      });
    }

    const progress = store.calculateProgress();
    expect(progress.questions).toBe(50); // 20/40 = 50%
    expect(progress.words).toBeGreaterThan(0);
  });
});
```

---

## 📌 CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Setup Inicial
- [ ] Criar projeto Vite com React + TypeScript
- [ ] Configurar Tailwind CSS e design tokens
- [ ] Instalar e configurar shadcn/ui
- [ ] Configurar ESLint e Prettier
- [ ] Configurar paths aliases

### Fase 2: Infraestrutura
- [ ] Implementar API client (Axios)
- [ ] Configurar React Query
- [ ] Implementar Zustand stores
- [ ] Configurar roteamento

### Fase 3: Componentes Base
- [ ] Implementar componentes UI (button, input, etc)
- [ ] Criar layout components (Container, Header, Footer)
- [ ] Implementar error boundaries

### Fase 4: Fluxo do Diagnóstico
- [ ] Tela de boas-vindas + WelcomeForm
- [ ] QuestionCard + ScaleInput + TextInput
- [ ] ProgressBar + PhaseIndicator
- [ ] Modais (Eligibility, SaveExit, Resume)
- [ ] TransitionScreen + CelebrationScreen

### Fase 5: Resultado
- [ ] RadarChart (Recharts)
- [ ] AreaCard + ScoreDisplay
- [ ] InsightSection + RecommendationCard
- [ ] ShareModal + CreateAccountBanner

### Fase 6: Qualidade
- [ ] Implementar auto-save
- [ ] Testar acessibilidade (NVDA, VoiceOver)
- [ ] Otimizar performance (Lighthouse >90)
- [ ] Escrever testes unitários e de integração

---

## 📚 REFERÊNCIAS E RECURSOS

### Documentação Oficial
- [React Documentation](https://react.dev)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [Framer Motion](https://www.framer.com/motion/)
- [Recharts](https://recharts.org/)
- [Zustand](https://docs.pmnd.rs/zustand)
- [React Query](https://tanstack.com/query)

### Ferramentas de Desenvolvimento
- [React DevTools](https://react.dev/learn/react-developer-tools)
- [React Query DevTools](https://tanstack.com/query/latest/docs/react/devtools)
- [axe DevTools](https://www.deque.com/axe/devtools/) (acessibilidade)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/) (performance)

---