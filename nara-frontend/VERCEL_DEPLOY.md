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

---

## 4. Ajustar no dashboard (Framework Preset + VITE_API_URL)

Se o deploy já foi feito mas o **Framework Preset** ficou em "Other" ou você ainda não configurou a **VITE_API_URL**, faça no dashboard:

### 4.1 Definir Framework Preset como Vite

1. No projeto **naraproject**, clique em **Settings** (menu lateral ou ícone de engrenagem).
2. No menu lateral de Settings, abra **Build & Development** (ou **General**, dependendo do layout).
3. Em **Framework Preset**, troque de "Other" para **Vite**.
4. Confira também:
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Clique em **Save** se aparecer o botão.

### 4.2 Incluir a variável VITE_API_URL

1. Ainda em **Settings**, clique em **Environment Variables** (no menu lateral).
2. Em **Key**, digite: **`VITE_API_URL`**.
3. Em **Value**, coloque a URL do seu backend em produção, **sem barra no final**.  
   Exemplos:
   - Backend no Render: `https://nara-backend-xxxx.onrender.com`
   - Backend no Railway: `https://nara-backend-production.up.railway.app`
4. Marque o ambiente (**Production**, e opcionalmente Preview/Development se quiser).
5. Clique em **Save**.
6. Para a variável valer no site já publicado: vá em **Deployments** → no último deploy → **⋯** (três pontos) → **Redeploy**. Ou faça um novo commit e a Vercel fará um novo deploy automático.

**Se o backend ainda não está no ar:** você pode criar a variável com um valor placeholder (ex.: `https://seu-backend.onrender.com`) e trocar depois; ou deixar sem valor e adicionar quando subir o backend.

---

## Resumo rápido

- **Conta:** Vercel logada com GitHub.  
- **Repo:** `PhellipeOliveira/naraproject`, branch `main`.  
- **Root Directory:** `nara-frontend`.  
- **Framework:** Vite (React + Vite).  
- **Variável:** `VITE_API_URL` = URL do backend em produção (quando tiver).

Não é necessário criar “API” na Vercel: você só informa **uma** variável de ambiente (`VITE_API_URL`) com a URL do backend que você sobe no Railway ou Render. Chaves de Supabase, OpenAI etc. ficam **no backend**, não no frontend.
