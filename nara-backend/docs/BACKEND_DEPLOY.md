# Deploy do backend NARA (Railway ou Render)

Conforme `documentos/07_DEPLOY_QUALIDADE.md` e [project-docs/DEPLOY.md](../../project-docs/DEPLOY.md): o backend FastAPI sobe em **Railway** ou **Render**. Este guia traz o passo a passo para ambos.

---

## Onde fazer o deploy e por quê?

| Plataforma | Motivo da escolha | Plano gratuito |
|------------|-------------------|----------------|
| **Render** | Interface simples, suporte nativo a Docker, bom para FastAPI. Free tier com limite de horas. | Sim. Serviços “spin down” após inatividade (primeira requisição pode demorar ~30s). |
| **Railway** | Também suporta Docker, deploy rápido. Free tier com créditos mensais. | Sim. Créditos limitados por mês no free tier. |

**Recomendação:** comece com **Render** (passo a passo abaixo). Se preferir Railway, o fluxo é parecido: conectar repo → apontar para a pasta `nara-backend` → usar o Dockerfile → configurar variáveis.

---

## Deploy já foi feito?

No repositório **não há** configuração de deploy do backend (sem `railway.json`, `render.yaml` ou URLs salvas). Ou seja, **o backend ainda não foi publicado** em nenhum lugar. O frontend na Vercel vai precisar da URL do backend **depois** que você fizer este deploy.

---

## O que é “criar um placeholder” para VITE_API_URL?

- **Placeholder** = um valor **temporário** que você coloca na variável `VITE_API_URL` na Vercel.  
  Exemplo: você cria na Vercel a variável com valor `https://nara-backend.onrender.com` (um endereço que ainda não existe). Quando o backend estiver no ar no Render, a URL real será parecida com essa; aí você só **troca** o valor na Vercel pela URL que o Render te der.  
  Ou seja: é só um texto “provisório” no campo da variável, **não** é um serviço nem um domínio.

- **Seu domínio na Hostinger (`www.phellipeoliveira.org`)** é outra coisa: é o **domínio do site**. Você pode usá-lo para o **frontend** (apontando para a Vercel) ou, no futuro, para um subdomínio do backend (ex.: `api.phellipeoliveira.org`). Para o **primeiro** deploy do backend, a URL que você vai colocar em `VITE_API_URL` vem da **própria Render** (ou Railway), algo como `https://nara-backend-xxxx.onrender.com`. O domínio da Hostinger não substitui essa URL; você só usaria ele se quisesse trocar depois para um endereço próprio.

---

## Passo a passo: deploy do backend no Render

### 1. Conta e repositório

1. Acesse [render.com](https://render.com) e crie conta (pode usar “Sign up with GitHub”).
2. No dashboard, clique em **New +** → **Web Service**.
3. Conecte o repositório **PhellipeOliveira/naraproject** (se ainda não estiver conectado, autorize o Render no GitHub).
4. Selecione o repo **naraproject**.

### 2. Configuração do serviço

| Campo | Valor |
|-------|--------|
| **Name** | `nara-backend` (ou outro nome; será parte da URL). |
| **Region** | Escolha a mais próxima (ex.: Oregon). |
| **Branch** | `main`. |
| **Root Directory** | **`nara-backend`** (obrigatório: o código do backend está nessa pasta). |
| **Runtime** | **Docker** (o projeto tem `Dockerfile` na pasta `nara-backend`). |
| **Instance Type** | **Free** (para começar). |

### 3. Variáveis de ambiente

No Render, cada variável tem **dois campos**: **Key** (nome) e **Value** (valor). Não digite `=` em nenhum campo — o nome vai só na Key e o valor só na Value.

**Obrigatórias** (Key → Value):

| Key | Value |
|-----|--------|
| `SUPABASE_URL` | URL do projeto Supabase |
| `SUPABASE_SERVICE_KEY` | Service Role Key do Supabase |
| `OPENAI_API_KEY` | Chave da API OpenAI |
| `RESEND_API_KEY` | Chave do Resend |
| `EMAIL_FROM` | Email de envio (ex.: `diagnostic.nara@phellipeoliveira.org`) |
| `FRONTEND_URL` | URL do frontend na Vercel (ex.: `https://naraproject-beige.vercel.app`) **sem** barra no final |
| `CORS_ORIGINS` | **Formato exato:** JSON array com a URL do frontend, **sem** parênteses, **sem** barra no final. Ex.: `["https://naraproject-beige.vercel.app"]` (use colchetes `[ ]` e aspas na URL). No Render, no campo Value coloque exatamente isso. |

**Opcionais** (Key → Value). Se não adicionar, o código usa o default:

| Key | Value |
|-----|--------|
| `APP_NAME` | `NARA Diagnostic API` (ou o que quiser) |
| `ENV` | `production` |
| `DEBUG` | `false` |
| `MIN_QUESTIONS_TO_FINISH` | `40` |
| `MIN_WORDS_TO_FINISH` | `3500` |
| `MIN_AREAS_COVERED` | `12` |
| `RAG_TOP_K` | `10` |
| `RAG_SIMILARITY_THRESHOLD` | `0.5` |

Ou seja: para **ENV** e **DEBUG** você adiciona **duas linhas** — uma com Key `ENV` e Value `production`, outra com Key `DEBUG` e Value `false`. Nunca coloque `ENV=production` em um único campo; o Render não aceita esse formato.

**Atenção:** No campo **Value** coloque **sempre o valor real** (número, URL, texto). **Não** coloque o caminho do arquivo (ex.: `nara-backend/.env.example`). Se você usou "Add from .env", confira que as variáveis numéricas têm número no Value (ex.: `40`, `3500`, `10`, `0.5`), não o path do arquivo — senão o app falha na subida com erro de validação do Pydantic.

**Quais variáveis precisam de valor real no Render e quais não**

No Render **não** use o texto `nara-backend/.env.example` como valor de nenhuma variável — isso é só o caminho do arquivo. O backend precisa de valores reais ou numéricos.

| No Render | Precisa de valor real? | Motivo |
|-----------|------------------------|--------|
| **SUPABASE_URL** | ✅ Sim | Conexão com o banco; URL do projeto Supabase. |
| **SUPABASE_SERVICE_KEY** | ✅ Sim | Autenticação no Supabase; sem isso o app não sobe. |
| **OPENAI_API_KEY** | ✅ Sim | Geração de perguntas e relatório; sem isso o diagnóstico falha. |
| **RESEND_API_KEY** | ✅ Sim | Envio de e-mails; sem isso o envio falha. |
| **EMAIL_FROM** | ✅ Sim | Remetente dos e-mails (ex.: `diagnostic.nara@seudominio.org`). |
| **FRONTEND_URL** | ✅ Sim | URL do front na Vercel (ex.: `https://naraproject-beige.vercel.app`), sem barra no final. |
| **CORS_ORIGINS** | ✅ Sim | JSON array com a URL do front (ex.: `["https://naraproject-beige.vercel.app"]`). |
| **APP_NAME**, **ENV**, **DEBUG** | ⚠️ Opcional | O código tem default; pode deixar como está ou ajustar. |
| **MIN_QUESTIONS_TO_FINISH**, **MIN_WORDS_TO_FINISH**, **MIN_AREAS_COVERED**, **RAG_TOP_K**, **RAG_SIMILARITY_THRESHOLD** | ⚠️ Opcional | O código tem default; se definir, use **números** (ex.: `40`, `3500`), nunca `nara-backend/.env.example`. |

Resumo: **todas as variáveis que o backend usa para conectar a serviços externos (Supabase, OpenAI, Resend) e para CORS/FRONTEND_URL precisam de valor real no Render.** Nenhuma pode ficar com o texto `nara-backend/.env.example`.

Use como referência o arquivo **`nara-backend/.env.example`** (nomes das variáveis = Key; valores reais você preenche com os segredos que já usa em desenvolvimento).

### 4. Deploy

1. Clique em **Create Web Service**.
2. O Render vai buildar a imagem Docker a partir do `Dockerfile` em `nara-backend/` e subir o serviço.
3. Quando o deploy terminar, a **URL do serviço** aparecerá no topo (ex.: `https://nara-backend-xxxx.onrender.com`). **Essa é a URL do backend.**

### 5. Configurar o frontend (Vercel)

1. No projeto **naraproject** na Vercel, vá em **Settings** → **Environment Variables** (do **projeto**, não do time).
2. Crie ou edite a variável **`VITE_API_URL`** com o valor = **URL do backend no Render** (ex.: `https://nara-backend-xxxx.onrender.com`), **sem** barra no final.
3. Faça um **Redeploy** do frontend na Vercel para a nova variável ser usada no build.

---

## Resumo

- **Onde:** Render (recomendado) ou Railway.  
- **Por quê:** Alinhado aos seus documentos; ambos têm plano gratuito e suportam Docker/FastAPI.  
- **Deploy do backend no repo:** Ainda **não** foi feito; este guia é o passo a passo para fazer.  
- **Placeholder:** Valor temporário em `VITE_API_URL` na Vercel; você troca pela URL real depois do deploy.  
- **Domínio Hostinger:** Pode ser usado para o site (frontend) ou, depois, para o backend; a primeira URL do backend vem da Render (ou Railway).  
- **Ordem:** Fazer deploy do backend (Render) → copiar URL → colocar em `VITE_API_URL` na Vercel → redeploy do frontend.

---

## Erro: "unable to parse string as an integer/number" com valor `nara-backend/.env.example`

Se o deploy falhar com **ValidationError** para `RAG_TOP_K`, `RAG_SIMILARITY_THRESHOLD`, `MIN_QUESTIONS_TO_FINISH`, `MIN_WORDS_TO_FINISH` ou `MIN_AREAS_COVERED` e o log mostrar `input_value='nara-backend/.env.example'`, é porque o **Value** dessas variáveis no Render está com o caminho do arquivo em vez do número.

**Correção:** No Render → **Environment** (ou **Environment Variables**) → edite cada uma e coloque no **Value**:

| Key | Value (correto) |
|-----|------------------|
| `RAG_TOP_K` | `10` |
| `RAG_SIMILARITY_THRESHOLD` | `0.5` |
| `MIN_QUESTIONS_TO_FINISH` | `40` |
| `MIN_WORDS_TO_FINISH` | `3500` |
| `MIN_AREAS_COVERED` | `12` |

Depois salve e faça **Manual Deploy** (ou aguarde um novo deploy).

---

## Erro: "SupabaseException: Invalid URL"

Se o deploy falhar com **Invalid URL** ao criar o cliente Supabase, a variável **SUPABASE_URL** no Render está inválida.

**Correção:**

1. No Render → **Environment**, abra a variável **SUPABASE_URL**.
2. O **Value** deve ser **apenas** a URL do seu projeto Supabase, no formato:
   - `https://SEU_PROJECT_REF.supabase.co`
   - **Sem** barra no final, **sem** espaços, **sem** caminho de arquivo (ex.: não use `nara-backend/.env.example`).
3. Para obter a URL correta: no [dashboard do Supabase](https://supabase.com/dashboard) → seu projeto → **Settings** → **API** → em "Project URL" copie o valor.
4. Se existir **SUPABASE_SERVICE_KEY**, confira também que o valor é a **service_role** key (em Settings → API → "Project API keys" → `service_role`), sem espaços ou quebras de linha.

Depois salve e faça **Manual Deploy** novamente.

---

## Erro no front: "Não foi possível iniciar o diagnóstico" (CORS ou backend)

Se o front na Vercel mostra essa mensagem ao clicar em "Iniciar diagnóstico":

1. **Formato de CORS_ORIGINS no Render**  
   O valor deve ser um **JSON array**, não texto com parênteses.  
   - **Errado:** `(https://naraproject-beige.vercel.app)`  
   - **Certo:** `["https://naraproject-beige.vercel.app"]`  
   No Render → Environment → **CORS_ORIGINS** → Value = `["https://naraproject-beige.vercel.app"]` (com colchetes e aspas). Salve e faça **Manual Deploy** do backend.

2. **Ver o erro real no navegador**  
   Abra a página do diagnóstico → F12 (DevTools) → aba **Console**. Tente iniciar de novo. Se aparecer erro de **CORS** (ex.: "blocked by CORS policy"), o backend não está aceitando a origem do front; confira o passo 1.  
   Na aba **Network**, filtre por "Fetch/XHR", tente iniciar e clique na requisição para `diagnostic/start`. Veja o **Status** (ex.: 403 CORS, 500, 422) e o **Response**; isso indica se o problema é CORS ou resposta de erro do backend.

3. **Backend acordado (plano Free)**  
   No plano gratuito do Render o serviço “dorme”. Abra primeiro **https://nara-backend-11dg.onrender.com/health** em outra aba, espere responder, e depois tente o diagnóstico de novo.
