# Guia de Integração - API NARA V2

> **Para desenvolvedores:** Como integrar sua aplicação com a API de Diagnóstico NARA V2

---

## 🚀 Quick Start

### 1. Configuração Inicial

```typescript
// api/config.ts
export const API_CONFIG = {
  baseURL: process.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
};
```

### 2. Cliente HTTP (Axios)

```typescript
// api/client.ts
import axios from 'axios';
import { API_CONFIG } from './config';

export const apiClient = axios.create(API_CONFIG);

// Interceptor de erros
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
    }
    return Promise.reject(error);
  }
);
```

---

## 📝 Fluxo Completo de Integração

### Etapa 1: Iniciar Diagnóstico

```typescript
import { apiClient } from './client';
import type { StartDiagnosticResponse } from './types';

async function startDiagnostic(email: string, fullName?: string) {
  const response = await apiClient.post<StartDiagnosticResponse>(
    '/diagnostic/start',
    {
      email,
      full_name: fullName,
      consent_privacy: true,
      consent_marketing: false,
    }
  );
  
  const { diagnostic_id, questions, result_token } = response.data;
  
  // Salvar no localStorage para recuperação
  localStorage.setItem('nara_diagnostic_id', diagnostic_id);
  localStorage.setItem('nara_result_token', result_token);
  
  return response.data;
}
```

### Etapa 2: Submeter Respostas

```typescript
async function submitAnswer(
  diagnosticId: string,
  questionId: number,
  questionText: string,
  questionArea: string,
  answerText: string
) {
  const startTime = Date.now();
  
  const response = await apiClient.post(
    `/diagnostic/${diagnosticId}/answer`,
    {
      question_id: questionId,
      question_text: questionText,
      question_area: questionArea,
      answer_text: answerText,
      response_time_seconds: Math.floor((Date.now() - startTime) / 1000),
    }
  );
  
  // Response contém progresso atualizado
  const { can_finish, progress, phase_complete } = response.data;
  
  return response.data;
}
```

### Etapa 3: Verificar Elegibilidade

```typescript
async function checkEligibility(diagnosticId: string) {
  const response = await apiClient.get(
    `/diagnostic/${diagnosticId}/eligibility`
  );
  
  const { can_finish, criteria, overall_progress } = response.data;
  
  // Mostrar modal se elegível
  if (can_finish) {
    showFinishModal(criteria);
  }
  
  return response.data;
}
```

### Etapa 4: Gerar Próxima Fase (Opcional)

```typescript
async function generateNextPhase(diagnosticId: string) {
  const response = await apiClient.post(
    `/diagnostic/${diagnosticId}/next-questions`
  );
  
  const { phase, questions } = response.data;
  
  return response.data;
}
```

### Etapa 5: Finalizar e Obter Resultado

```typescript
async function finishDiagnostic(diagnosticId: string) {
  // Mostrar loading (pode demorar 10-30s)
  showLoadingScreen();
  
  const response = await apiClient.post(
    `/diagnostic/${diagnosticId}/finish`
  );
  
  const result = response.data;
  
  // Salvar token para acesso futuro
  localStorage.setItem('nara_last_result_token', result_token);
  
  return result;
}
```

### Etapa 6: Acessar Resultado por Token

```typescript
async function getResultByToken(token: string) {
  const response = await apiClient.get(
    `/diagnostic/result/${token}`
  );
  
  return response.data;
}
```

---

## 🎨 Renderização do Resultado V2

### Componente Vetor de Estado

```tsx
// components/VetorEstadoCard.tsx
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import type { VetorEstado } from '@/types';

interface Props {
  vetor: VetorEstado;
}

export function VetorEstadoCard({ vetor }: Props) {
  return (
    <Card>
      <CardHeader>
        <h2 className="text-2xl font-bold">Vetor de Estado</h2>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 sm:grid-cols-2">
          {/* Motor Dominante */}
          <div className="p-4 rounded-lg bg-primary/5 border border-primary/10">
            <p className="text-xs text-muted-foreground mb-1">
              Motor Dominante
            </p>
            <p className="font-semibold text-lg text-primary">
              {vetor.motor_dominante}
            </p>
            <p className="text-xs text-muted-foreground mt-2">
              {getMotorDescription(vetor.motor_dominante)}
            </p>
          </div>
          
          {/* Estágio da Jornada */}
          <div className="p-4 rounded-lg bg-blue-500/5 border border-blue-500/10">
            <p className="text-xs text-muted-foreground mb-1">
              Estágio da Jornada
            </p>
            <p className="font-semibold text-lg text-blue-700">
              {vetor.estagio_jornada}
            </p>
            <p className="text-xs text-muted-foreground mt-2">
              {getEstagioDescription(vetor.estagio_jornada)}
            </p>
          </div>
          
          {/* Crise Raiz */}
          <div className="p-4 rounded-lg bg-destructive/5 border border-destructive/10 sm:col-span-2">
            <p className="text-xs text-muted-foreground mb-1">
              Crise Raiz Identificada
            </p>
            <p className="font-semibold text-destructive">
              {vetor.crise_raiz}
            </p>
            {vetor.crises_derivadas.length > 0 && (
              <p className="text-xs text-muted-foreground mt-2">
                Também presente: {vetor.crises_derivadas.join(', ')}
              </p>
            )}
          </div>
          
          {/* Necessidade Atual */}
          <div className="p-4 rounded-lg bg-muted sm:col-span-2">
            <p className="text-xs text-muted-foreground mb-1">
              Necessidade Atual
            </p>
            <p className="text-sm">{vetor.necessidade_atual}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function getMotorDescription(motor: string): string {
  const descriptions = {
    'Necessidade': 'Afastar-se da dor e buscar alívio',
    'Valor': 'Viver com integridade e coerência',
    'Desejo': 'Conquistar e realizar objetivos',
    'Propósito': 'Deixar legado e impactar vidas'
  };
  return descriptions[motor] || '';
}

function getEstagioDescription(estagio: string): string {
  const descriptions = {
    'Germinar': 'Início do despertar',
    'Enraizar': 'Busca de fundamentos',
    'Desenvolver': 'Construção ativa',
    'Florescer': 'Expressão autêntica',
    'Frutificar': 'Resultados tangíveis',
    'Realizar': 'Plenitude e maestria'
  };
  return descriptions[estagio] || '';
}
```

### Componente Memórias Vermelhas

```tsx
// components/MemoriasVermelhas.tsx
import { Card, CardHeader, CardContent } from '@/components/ui/card';

interface Props {
  memorias: string[];
}

export function MemoriasVermelhas({ memorias }: Props) {
  if (!memorias || memorias.length === 0) return null;
  
  return (
    <Card>
      <CardHeader>
        <h2 className="text-lg font-bold">Memórias Vermelhas</h2>
        <p className="text-sm text-muted-foreground">
          Frases suas que revelam conflitos não dominados
        </p>
      </CardHeader>
      <CardContent className="space-y-3">
        {memorias.map((memoria, i) => (
          <div 
            key={i}
            className="p-3 rounded-lg bg-destructive/5 border-l-4 border-destructive"
          >
            <p className="text-sm italic">"{memoria}"</p>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
```

### Componente Âncoras Práticas

```tsx
// components/AncorasPraticas.tsx
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Check } from 'lucide-react';
import { useState } from 'react';

interface Props {
  ancoras: string[];
}

export function AncorasPraticas({ ancoras }: Props) {
  const [checked, setChecked] = useState<Set<number>>(new Set());
  
  if (!ancoras || ancoras.length === 0) return null;
  
  const toggleCheck = (index: number) => {
    const newChecked = new Set(checked);
    if (newChecked.has(index)) {
      newChecked.delete(index);
    } else {
      newChecked.add(index);
    }
    setChecked(newChecked);
  };
  
  return (
    <Card>
      <CardHeader>
        <h2 className="text-lg font-bold">Âncoras Práticas para Assunção</h2>
        <p className="text-sm text-muted-foreground">
          Ações concretas para encarnar sua nova identidade
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {ancoras.map((ancor, i) => (
            <button
              key={i}
              onClick={() => toggleCheck(i)}
              className="flex items-start gap-3 p-3 rounded-lg bg-primary/5 hover:bg-primary/10 transition-colors w-full text-left"
            >
              <div className={`
                flex-shrink-0 w-6 h-6 rounded-full 
                flex items-center justify-center text-xs font-bold
                ${checked.has(i) 
                  ? 'bg-primary text-primary-foreground' 
                  : 'bg-muted text-muted-foreground'
                }
              `}>
                {checked.has(i) ? <Check size={14} /> : i + 1}
              </div>
              <p className="text-sm font-medium">{ancor}</p>
            </button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
```

---

## 🔄 Gerenciamento de Estado (Zustand)

```typescript
// stores/diagnosticStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { VetorEstado, DiagnosticResultResponse } from '@/types';

interface DiagnosticState {
  // Estado atual
  diagnosticId: string | null;
  currentQuestion: number;
  answers: Record<number, string>;
  
  // Resultado
  result: DiagnosticResultResponse | null;
  
  // Ações
  setDiagnosticId: (id: string) => void;
  saveAnswer: (questionId: number, text: string) => void;
  setResult: (result: DiagnosticResultResponse) => void;
  reset: () => void;
}

export const useDiagnosticStore = create<DiagnosticState>()(
  persist(
    (set) => ({
      diagnosticId: null,
      currentQuestion: 0,
      answers: {},
      result: null,
      
      setDiagnosticId: (id) => set({ diagnosticId: id }),
      
      saveAnswer: (questionId, text) =>
        set((state) => ({
          answers: { ...state.answers, [questionId]: text },
          currentQuestion: state.currentQuestion + 1,
        })),
      
      setResult: (result) => set({ result }),
      
      reset: () => set({
        diagnosticId: null,
        currentQuestion: 0,
        answers: {},
        result: null,
      }),
    }),
    {
      name: 'nara-diagnostic-storage',
    }
  )
);
```

---

## 🧪 Testes de Integração

### Teste E2E com Playwright

```typescript
// tests/e2e/diagnostic-flow.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Fluxo completo de diagnóstico V2', () => {
  test('deve completar diagnóstico e exibir vetor de estado', async ({ page }) => {
    // 1. Iniciar diagnóstico
    await page.goto('/');
    await page.fill('input[name="email"]', 'teste@example.com');
    await page.fill('input[name="full_name"]', 'João Silva');
    await page.click('button[type="submit"]');
    
    // 2. Responder primeiras 15 perguntas
    for (let i = 0; i < 15; i++) {
      await page.fill('textarea', 'Resposta de teste com pelo menos 50 palavras para atender o mínimo '.repeat(5));
      await page.click('button:has-text("Continuar")');
      await page.waitForTimeout(500);
    }
    
    // 3. Gerar próxima fase
    await page.click('button:has-text("Gerar novas perguntas")');
    await page.waitForSelector('textarea');
    
    // 4. Responder mais 25 perguntas para atingir elegibilidade
    for (let i = 0; i < 25; i++) {
      await page.fill('textarea', 'Resposta narrativa detalhada '.repeat(10));
      await page.click('button:has-text("Continuar")');
      await page.waitForTimeout(500);
    }
    
    // 5. Finalizar
    await page.click('button:has-text("Finalizar diagnóstico")');
    await page.waitForSelector('h1:has-text("Seu Diagnóstico NARA")', { timeout: 60000 });
    
    // 6. Verificar Vetor de Estado
    await expect(page.locator('text=Motor Dominante')).toBeVisible();
    await expect(page.locator('text=Estágio da Jornada')).toBeVisible();
    await expect(page.locator('text=Crise Raiz Identificada')).toBeVisible();
    
    // 7. Verificar Memórias Vermelhas
    await expect(page.locator('h2:has-text("Memórias Vermelhas")')).toBeVisible();
    
    // 8. Verificar Âncoras
    await expect(page.locator('h2:has-text("Âncoras Práticas")')).toBeVisible();
  });
});
```

### Testes Unitários dos Componentes

```typescript
// tests/components/VetorEstadoCard.test.tsx
import { render, screen } from '@testing-library/react';
import { VetorEstadoCard } from '@/components/VetorEstadoCard';

describe('VetorEstadoCard', () => {
  const mockVetor = {
    motor_dominante: 'Necessidade',
    motor_secundario: 'Valor',
    estagio_jornada: 'Germinar',
    crise_raiz: 'Identidade Raiz',
    crises_derivadas: ['Sentido e Direção'],
    ponto_entrada_ideal: 'Existencial',
    dominios_alavanca: ['D1', 'D5'],
    tom_emocional: 'confusão',
    risco_principal: 'Colapso identitário',
    necessidade_atual: 'Criar espaço de experimentação'
  };
  
  it('renderiza motor dominante corretamente', () => {
    render(<VetorEstadoCard vetor={mockVetor} />);
    expect(screen.getByText('Necessidade')).toBeInTheDocument();
  });
  
  it('renderiza estágio da jornada', () => {
    render(<VetorEstadoCard vetor={mockVetor} />);
    expect(screen.getByText('Germinar')).toBeInTheDocument();
  });
  
  it('renderiza crise raiz com destaque', () => {
    render(<VetorEstadoCard vetor={mockVetor} />);
    const criseElement = screen.getByText('Identidade Raiz');
    expect(criseElement).toHaveClass('text-destructive');
  });
});
```

---

## 📊 Analytics e Tracking

### Eventos Recomendados

```typescript
// lib/analytics.ts
export const trackDiagnosticEvents = {
  started: (diagnosticId: string) => {
    analytics.track('Diagnostic Started', {
      diagnostic_id: diagnosticId,
      timestamp: new Date().toISOString(),
    });
  },
  
  answerSubmitted: (questionId: number, wordCount: number) => {
    analytics.track('Answer Submitted', {
      question_id: questionId,
      word_count: wordCount,
    });
  },
  
  phaseCompleted: (phase: number, totalAnswers: number) => {
    analytics.track('Phase Completed', {
      phase,
      total_answers: totalAnswers,
    });
  },
  
  finished: (
    diagnosticId: string, 
    motor: string, 
    crise: string,
    totalWords: number
  ) => {
    analytics.track('Diagnostic Finished', {
      diagnostic_id: diagnosticId,
      motor_dominante: motor,
      crise_raiz: crise,
      total_words: totalWords,
    });
  },
  
  resultViewed: (token: string, motor: string) => {
    analytics.track('Result Viewed', {
      result_token: token,
      motor_dominante: motor,
    });
  },
};
```

---

## 🚨 Tratamento de Erros

### Error Boundary React

```tsx
// components/ErrorBoundary.tsx
import React from 'react';

interface Props {
  children: React.ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class DiagnosticErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Diagnostic Error:', error, errorInfo);
    // Enviar para serviço de logging (Sentry, etc.)
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center p-4">
          <div className="max-w-md text-center space-y-4">
            <h1 className="text-2xl font-bold">Algo deu errado</h1>
            <p className="text-muted-foreground">
              Ocorreu um erro ao processar seu diagnóstico. 
              Seus dados foram salvos e você pode retomar mais tarde.
            </p>
            <button
              onClick={() => window.location.href = '/'}
              className="btn-primary"
            >
              Voltar ao início
            </button>
          </div>
        </div>
      );
    }
    
    return this.props.children;
  }
}
```

### Retry Logic para API

```typescript
// lib/apiRetry.ts
import axios, { AxiosError } from 'axios';

export async function fetchWithRetry<T>(
  fetcher: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> {
  let lastError: Error;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fetcher();
    } catch (error) {
      lastError = error as Error;
      
      // Não retry em erros 4xx (client errors)
      if (axios.isAxiosError(error) && error.response) {
        const status = error.response.status;
        if (status >= 400 && status < 500) {
          throw error;
        }
      }
      
      // Esperar antes de retry (exponential backoff)
      if (attempt < maxRetries) {
        await new Promise(resolve => 
          setTimeout(resolve, Math.pow(2, attempt) * 1000)
        );
      }
    }
  }
  
  throw lastError!;
}

// Uso:
const result = await fetchWithRetry(() => 
  finishDiagnostic(diagnosticId)
);
```

---

## 📚 Recursos Adicionais

- [API_V2_DOCUMENTATION.md](./API_V2_DOCUMENTATION.md) - Documentação completa dos campos
- [01_BASE_METODOLOGICA_NARA.md](../documentos/01_BASE_METODOLOGICA_NARA.md) - Base conceitual
- [Postman Collection](#) - Coleção de requests para testes

---

**Última atualização:** Fevereiro 2026  
**Mantenedor:** Time NARA  
**Suporte:** dev@naraproject.com
