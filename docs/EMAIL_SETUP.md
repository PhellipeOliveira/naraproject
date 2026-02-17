# 📧 Configuração de Email (Resend)

## Problema: Email não está sendo enviado

Se você clicou em "Sim, enviar email" mas não recebeu, é porque a chave do Resend não está configurada.

---

## ✅ Solução Rápida

### **Passo 1: Obter chave do Resend**

1. Acesse: https://resend.com/
2. Faça login ou crie uma conta gratuita
3. Vá em: **API Keys** no menu lateral
4. Clique em **Create API Key**
5. Copie a chave (formato: `re_xxxxxxxxxxxxx`)

### **Passo 2: Configurar no backend**

Edite o arquivo: `nara-backend/.env`

```bash
# === Resend (obrigatória para envio de emails) ===
RESEND_API_KEY=re_SUA_CHAVE_AQUI_COMPLETA
EMAIL_FROM=diagnostic.nara@phellipeoliveira.org
RESEND_REPLY_TO=contato@phellipeoliveira.org
```

**Importante:** Cole a chave COMPLETA que você copiou do Resend.

### **Passo 3: Verificar domínio de envio**

No Resend Dashboard:
1. Vá em **Domains**
2. Adicione o domínio: `phellipeoliveira.org`
3. Configure os registros DNS (SPF, DKIM, DMARC)
4. Aguarde verificação (pode levar alguns minutos)

**OU** use o domínio de teste do Resend (para desenvolvimento):
```bash
EMAIL_FROM=onboarding@resend.dev
```

### **Passo 4: Reiniciar o backend**

```bash
# Parar o backend (Ctrl + C no terminal)

# Reiniciar
cd /Users/phellipeoliveira/Documents/naraproject/nara-backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## 🧪 Testar Envio

1. Volte ao diagnóstico no navegador
2. Clique em **"Sair e Continuar Depois"**
3. Clique em **"Sim, enviar email"**
4. Verifique sua caixa de entrada (e spam)

---

## 📊 Verificar se Email foi Enviado

### **No Supabase:**

```sql
-- Ver últimos emails enviados
SELECT 
  recipient_email,
  email_type,
  subject,
  status,
  error_message,
  created_at
FROM email_logs
ORDER BY created_at DESC
LIMIT 10;
```

**Se `status = 'sent'`**: Email foi enviado com sucesso ✅  
**Se `status = 'failed'`**: Veja o `error_message` para entender o erro ❌

### **No Resend Dashboard:**

1. Acesse: https://resend.com/emails
2. Veja os emails enviados
3. Status: **Delivered** (sucesso) ou **Failed** (erro)

---

## 🆓 Plano Gratuito do Resend

O plano gratuito permite:
- ✅ **100 emails por dia**
- ✅ **1 domínio verificado**
- ✅ **Emails ilimitados para testes** (`onboarding@resend.dev`)

Perfeito para desenvolvimento e testes iniciais!

---

## ⚠️ Troubleshooting

### Email não chega mesmo com chave configurada

1. **Verifique o spam** da sua caixa de entrada
2. **Use email de teste** temporariamente:
   ```bash
   EMAIL_FROM=onboarding@resend.dev
   ```
3. **Verifique logs do backend** no terminal (procure por "Email sent" ou "Error sending email")
4. **Verifique no Supabase** a tabela `email_logs`:
   ```sql
   SELECT * FROM email_logs 
   WHERE recipient_email = 'seu@email.com' 
   ORDER BY created_at DESC LIMIT 5;
   ```

### Erro: "Domain not verified"

- Configure os registros DNS no seu domínio
- OU use o domínio de teste: `onboarding@resend.dev`

### Erro: "Invalid API key"

- Verifique se a chave está completa no `.env`
- Gere uma nova chave no Resend Dashboard
- Reinicie o backend após alterar

---

**Próximo passo:** Configure a chave do Resend e teste novamente! 📧
