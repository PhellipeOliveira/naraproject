# NARA Frontend

Frontend do Diagnóstico de Transformação Narrativa (React + Vite + TypeScript).

## Fase 1 — Setup Inicial ✓

- [x] Projeto Vite com React + TypeScript
- [x] Tailwind CSS e design tokens (cores primárias, áreas, animações)
- [x] shadcn/ui configurado (utils, variáveis CSS, Button, Input, Card)
- [x] ESLint e Prettier
- [x] Path aliases (`@/`, `@components/`, `@lib/`, etc.)

## Desenvolvimento

```bash
# Instalar dependências
npm install

# Servidor de desenvolvimento (porta 5173)
npm run dev

# Build de produção
npm run build

# Preview do build
npm run preview

# Lint
npm run lint
npm run lint:fix

# Formatar
npm run format
```

## Proxy da API

O `vite.config.ts` configura proxy de `/api` para `http://localhost:8000`. Com o backend rodando na porta 8000, as chamadas a `/api/v1/...` são encaminhadas automaticamente.

## Próximas fases (05_FRONTEND_UX.md)

- **Fase 2:** Infraestrutura (API client, React Query, Zustand, roteamento)
- **Fase 3:** Componentes base (layout, error boundaries)
- **Fase 4:** Fluxo do diagnóstico
- **Fase 5:** Tela de resultado (radar, insights)
- **Fase 6:** Qualidade (auto-save, a11y, testes)
