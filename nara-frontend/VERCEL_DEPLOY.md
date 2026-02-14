# Deploy do frontend NARA no Vercel

Seguindo o **documento 07_DEPLOY_QUALIDADE**: o frontend React sobe na Vercel; o backend FastAPI sobe no Railway ou Render. Este guia foca só no **Vercel (frontend)**.

---

## O que a Vercel NÃO te dá (e o que você precisa)

- **A Vercel não gera “API key” ou “token” para o seu app.**  
  Ela só hospeda o site e te dá uma URL (ex.: `https://nara-frontend-xxx.vercel.app`).

- **O que você precisa configurar na Vercel:**
  1. **De onde puxar o código** (GitHub/GitLab/Bitbucket ou upload).
  2. **Pasta do projeto** (se o repositório for a raiz do monorepo, apontar para `nara-frontend`).
  3. **Uma variável de ambiente:** `VITE_API_URL` = URL do seu **backend** em produção (ex.: Railway ou Render).  
  O frontend usa essa variável para saber para onde enviar as chamadas de API (diagnóstico, feedback, etc.).

- **Conexões que o frontend usa:**
  - **Backend (FastAPI):** via `VITE_API_URL` (você informa a URL onde o backend está rodando).
  - **Supabase / OpenAI / Resend:** o frontend **não** fala com esses serviços direto; quem fala é o **backend**. Então você não precisa colocar chave de Supabase ou OpenAI no Vercel.

---

## Passo a passo no site da Vercel

### 1. Entrar na Vercel

- Acesse [vercel.com](https://vercel.com) e faça login (ou crie conta; pode usar “Continue with GitHub” se o código estiver no GitHub).

### 2. Importar o projeto

- Clique em **“Add New…”** → **“Project”**.
- Se conectou com GitHub: escolha o **repositório** onde está o código do NARA (ex.: `NARA_CURSOR` ou o nome que você deu).
- Clique em **Import** (ou “Import Project”).

### 3. Configurar o projeto (tela de import)

- **Framework Preset:** a Vercel pode detectar “Vite”. Se não detectar, em “Build and Output Settings”:
  - **Build Command:** `npm run build`
  - **Output Directory:** `dist`
- **Root Directory:**  
  - Se o repositório é **só** a pasta do frontend, deixe em branco.  
  - Se o repositório é a **raiz do monorepo** (ex.: tem `nara-frontend/` e `nara-backend/`), clique em **Edit** ao lado de “Root Directory” e digite: **`nara-frontend`**.
- **Environment Variables:**  
  - Nome: **`VITE_API_URL`**  
  - Valor: a URL do seu backend em produção, **sem** barra no final.  
  - Exemplos:
    - Backend no Railway: `https://nara-backend-production.up.railway.app`
    - Backend no Render: `https://nara-backend.onrender.com`
  - Se o **backend ainda não estiver no ar**, você pode:
    - Deixar em branco por enquanto (o build sobe, mas as chamadas de API vão falhar até você colocar a URL), ou
    - Colocar um placeholder e trocar depois quando fizer o deploy do backend.

Depois disso, clique em **Deploy**.

### 4. Depois do primeiro deploy

- A Vercel vai mostrar a URL do site (ex.: `https://nara-frontend-xxxx.vercel.app`).
- **Quando você tiver o backend em produção**, volte em:
  - **Project** → seu projeto → **Settings** → **Environment Variables**
  - Ajuste ou crie **`VITE_API_URL`** com a URL correta do backend.
  - Faça um novo deploy (ou use “Redeploy” na aba Deployments) para a nova variável valer no build.

---

## Resumo do que você faz “no site da Vercel”

| O quê | Onde / Como |
|-------|-------------|
| Conta / login | vercel.com → Sign up / Log in (ex.: com GitHub) |
| Conectar repositório | Add New → Project → escolher repo → Import |
| Pasta do frontend | Root Directory = `nara-frontend` (se for monorepo) |
| URL do backend | Environment Variable: `VITE_API_URL` = `https://sua-url-backend` |
| Domínio | Depois do deploy, a Vercel te dá um domínio; em Settings → Domains você pode adicionar um domínio próprio |

Não é necessário “obter API” na Vercel: você só configura **uma** variável de ambiente (`VITE_API_URL`) com a URL do backend que **você** vai colocar no ar (Railway, Render, etc.).

---

## Backend (para o app funcionar de ponta a ponta)

Conforme **07_DEPLOY_QUALIDADE** e **DEPLOY.md**:

1. **Subir o backend** no Railway ou Render (usando o `Dockerfile` em `nara-backend/`).
2. **Lá no painel do backend**, configurar:
   - `FRONTEND_URL` = URL do seu app na Vercel (ex.: `https://nara-frontend-xxx.vercel.app`)
   - `CORS_ORIGINS` = mesma URL do frontend (para o navegador permitir as requisições).
3. **No Vercel**, garantir que `VITE_API_URL` aponta para a URL pública desse backend.

Assim o frontend (Vercel) e o backend (Railway/Render) ficam conectados e o diagnóstico funciona em produção.
