# Deploy do frontend NARA na Vercel (React + Vite)

Conforme o plano em `documentos/07_DEPLOY_QUALIDADE.md`: frontend React sobe na **Vercel**; backend FastAPI sobe no Railway ou Render. Este guia é só para o **frontend na Vercel**.

---

## 1. Conectar GitHub à Vercel

1. Acesse [vercel.com](https://vercel.com) e faça login.
2. Use **Continue with GitHub** para vincular sua conta ao GitHub.
3. Autorize a Vercel a acessar seus repositórios (pode ser “All” ou só o repo `naraproject`).

---

## 2. Criar o projeto (tela “New Project”)

Depois de conectar o GitHub, clique em **Add New…** → **Project**. Na tela de importação, preencha assim:

| Campo | O que colocar |
|-------|----------------|
| **Repositório** | Já vem preenchido: `PhellipeOliveira/naraproject` (branch `main`). Se não estiver, escolha esse repo. |
| **Project Name** | Pode deixar `naraproject` ou usar `nara-frontend`. |
| **Framework Preset** | Selecione **Vite** (o projeto é React + Vite). Se aparecer “Other”, clique e mude para **Vite**. |
| **Root Directory** | Clique em **Edit** e digite: **`nara-frontend`**. (O código do frontend está dentro dessa pasta no monorepo.) |
| **Build and Output Settings** | Abra a seção e preencha: **Build Command:** `npm run build` | **Output Directory:** `dist` (obrigatório para Vite; não deixe em branco) | **Install Command:** `npm install` (ou deixe o padrão da Vercel). |
| **Environment Variables** | **Importante:** `VITE_API_URL` não é o endereço da pasta no GitHub. É a URL **pública** do backend **quando ele estiver rodando** (ex.: depois de subir no Railway ou Render). Exemplo: `https://nara-backend.onrender.com` (sem barra no final). Se o backend ainda não foi feito deploy, **remova** essa variável ou deixe em branco e adicione depois. |

Depois clique em **Deploy**.

### Build and Output Settings (valores exatos)

- **Build Command:** `npm run build`
- **Output Directory:** `dist` ← preencha isso (é onde o Vite gera os arquivos; não use o placeholder).
- **Install Command:** `npm install` (ou deixe o padrão).

### Sobre a variável VITE_API_URL

- **Não use** o link da pasta do backend no GitHub (ex.: `.../naraproject/tree/main/nara-backend`). Isso é só o código no repositório.
- **Use** a URL do backend **em produção**, quando você subir o `nara-backend` no Railway ou Render. Exemplo: `https://nara-backend-xxxx.onrender.com`.
- Se o backend **ainda não está no ar**, apague o valor de `VITE_API_URL` ou remova a variável; você adiciona quando fizer o deploy do backend.

---

## 3. Depois do deploy

- A Vercel vai mostrar a URL do site (ex.: `https://naraproject.vercel.app`).
- Para alterar a URL do backend depois: **Project** → **Settings** → **Environment Variables** → edite ou crie `VITE_API_URL` → **Redeploy** (aba Deployments) para aplicar.

---

## Resumo rápido

- **Conta:** Vercel logada com GitHub.  
- **Repo:** `PhellipeOliveira/naraproject`, branch `main`.  
- **Root Directory:** `nara-frontend`.  
- **Framework:** Vite (React + Vite).  
- **Variável:** `VITE_API_URL` = URL do backend em produção (quando tiver).

Não é necessário criar “API” na Vercel: você só informa **uma** variável de ambiente (`VITE_API_URL`) com a URL do backend que você sobe no Railway ou Render. Chaves de Supabase, OpenAI etc. ficam **no backend**, não no frontend.
