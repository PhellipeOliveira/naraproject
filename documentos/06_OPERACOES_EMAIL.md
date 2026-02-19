# 06 - OPERAÇÕES E EMAIL

> **Propósito:** Gestão de sessão, auto-save, sistema de email e operações auxiliares do diagnóstico NARA.

---

## 📋 ÍNDICE

1. [Gestão de Sessão](#1-gestão-de-sessão)
2. [Sistema de Auto-Save](#2-sistema-de-auto-save)
3. [Sistema de Email (Resend)](#3-sistema-de-email-resend)
4. [Templates de Email](#4-templates-de-email)
5. [Magic Links e Autenticação](#5-magic-links-e-autenticação)
6. [Lista de Espera](#6-lista-de-espera)
7. [Retomada de Diagnóstico](#7-retomada-de-diagnóstico)

---

## 1. GESTÃO DE SESSÃO

### Estratégia de Identificação

O diagnóstico pode ser iniciado por usuários **anônimos** ou **autenticados**:

| Tipo | Identificador | Persistência | Limitações |
|------|---------------|--------------|------------|
| Anônimo | `session_id` + `email` | localStorage + servidor | 1 diagnóstico ativo por email |
| Autenticado | `user_id` (JWT) | Servidor | Múltiplos diagnósticos |

### Geração de Session ID

```typescript
// lib/session.ts
import { v4 as uuidv4 } from 'uuid';

const SESSION_KEY = 'nara_session_id';
const SESSION_EXPIRY_KEY = 'nara_session_expiry';
const DIAGNOSTIC_KEY = 'nara_diagnostic_id';
const SESSION_DURATION_DAYS = 30;

export interface SessionData {
  sessionId: string;
  diagnosticId?: string;
  email?: string;
  expiresAt: string;
}

export function getOrCreateSessionId(): string {
  // Verificar se já existe e não expirou
  const existingId = localStorage.getItem(SESSION_KEY);
  const expiry = localStorage.getItem(SESSION_EXPIRY_KEY);
  
  if (existingId && expiry) {
    const expiryDate = new Date(expiry);
    if (expiryDate > new Date()) {
      return existingId;
    }
  }
  
  // Criar novo session_id
  const newId = `sess_${uuidv4()}`;
  const newExpiry = new Date();
  newExpiry.setDate(newExpiry.getDate() + SESSION_DURATION_DAYS);
  
  localStorage.setItem(SESSION_KEY, newId);
  localStorage.setItem(SESSION_EXPIRY_KEY, newExpiry.toISOString());
  
  return newId;
}

export function getStoredDiagnosticId(): string | null {
  return localStorage.getItem(DIAGNOSTIC_KEY);
}

export function setStoredDiagnosticId(diagnosticId: string): void {
  localStorage.setItem(DIAGNOSTIC_KEY, diagnosticId);
}

export function clearSession(): void {
  localStorage.removeItem(SESSION_KEY);
  localStorage.removeItem(SESSION_EXPIRY_KEY);
  localStorage.removeItem(DIAGNOSTIC_KEY);
}

export function getSessionData(): SessionData | null {
  const sessionId = localStorage.getItem(SESSION_KEY);
  const expiresAt = localStorage.getItem(SESSION_EXPIRY_KEY);
  const diagnosticId = localStorage.getItem(DIAGNOSTIC_KEY);
  
  if (!sessionId || !expiresAt) return null;
  
  return {
    sessionId,
    diagnosticId: diagnosticId || undefined,
    expiresAt
  };
}
```

### Fluxo de Identificação do Usuário

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USUÁRIO ACESSA O SITE                                        │
│    • Verifica localStorage por session_id existente             │
│    • Se não existir, gera novo session_id                       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. USUÁRIO INFORMA EMAIL PARA INICIAR                           │
│    • Verifica se existe diagnóstico em andamento para o email   │
│    • Se sim: oferece retomar ou começar novo                    │
│    • Se não: cria novo diagnóstico                              │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. DIAGNÓSTICO CRIADO                                           │
│    • diagnostic_id salvo no localStorage                        │
│    • Vinculado ao email + session_id                            │
│    • result_token gerado para acesso futuro                     │
└─────────────────────────────────────────────────────────────────┘
```

### Verificação de Diagnóstico Existente (Backend)

```python
# services/diagnostic_service.py

async def check_existing_diagnostic(email: str) -> Optional[Dict]:
    """
    Verifica se existe diagnóstico em andamento para o email.
    """
    result = supabase.table("diagnostics").select(
        "id, status, current_phase, total_answers, created_at"
    ).eq("email", email).eq("status", "in_progress").order(
        "created_at", desc=True
    ).limit(1).execute()
    
    if result.data:
        diagnostic = result.data[0]
        return {
            "exists": True,
            "diagnostic_id": diagnostic["id"],
            "status": diagnostic["status"],
            "current_phase": diagnostic["current_phase"],
            "total_answers": diagnostic["total_answers"],
            "started_at": diagnostic["created_at"]
        }
    
    return {"exists": False}
```

---

## 2. SISTEMA DE AUTO-SAVE

### Estratégia de Persistência

| Camada | Dados | Frequência | Propósito |
|--------|-------|------------|-----------|
| localStorage | Resposta atual + progresso | A cada keystroke (debounced) | Recuperação offline |
| Servidor | Respostas confirmadas | Ao clicar "Continuar" | Persistência real |
| IndexedDB | Fila de retry | Quando offline | Sincronização posterior |

### Implementação do Auto-Save

```typescript
// hooks/useAutoSave.ts
import { useCallback, useEffect, useRef, useState } from 'react';
import { useDiagnosticStore } from '@/stores/diagnosticStore';
import { apiClient } from '@/api/client';

const SAVE_DEBOUNCE_MS = 1000;
const LOCAL_DRAFT_KEY = 'nara_answer_draft';

interface AnswerDraft {
  diagnosticId: string;
  questionId: number;
  questionText: string;
  questionArea: string;
  answerText?: string;
  answerScale?: number;
  timestamp: number;
}

export function useAutoSave() {
  const { diagnosticId } = useDiagnosticStore();
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  const saveTimeoutRef = useRef<NodeJS.Timeout>();
  
  // Salvar rascunho no localStorage
  const saveDraft = useCallback((draft: Omit<AnswerDraft, 'timestamp'>) => {
    const fullDraft: AnswerDraft = {
      ...draft,
      timestamp: Date.now()
    };
    localStorage.setItem(LOCAL_DRAFT_KEY, JSON.stringify(fullDraft));
  }, []);
  
  // Recuperar rascunho
  const getDraft = useCallback((): AnswerDraft | null => {
    const stored = localStorage.getItem(LOCAL_DRAFT_KEY);
    if (!stored) return null;
    
    try {
      const draft = JSON.parse(stored) as AnswerDraft;
      // Verificar se é do diagnóstico atual
      if (draft.diagnosticId === diagnosticId) {
        return draft;
      }
    } catch {
      // JSON inválido
    }
    return null;
  }, [diagnosticId]);
  
  // Limpar rascunho após salvar com sucesso
  const clearDraft = useCallback(() => {
    localStorage.removeItem(LOCAL_DRAFT_KEY);
  }, []);
  
  // Salvar no servidor com debounce
  const saveToServer = useCallback(async (answer: AnswerDraft) => {
    if (!diagnosticId) return;
    
    setSaveStatus('saving');
    
    try {
      await apiClient.post(`/diagnostic/${diagnosticId}/answer`, {
        question_id: answer.questionId,
        question_text: answer.questionText,
        question_area: answer.questionArea,
        answer_text: answer.answerText,
        answer_scale: answer.answerScale,
      });
      
      clearDraft();
      setSaveStatus('saved');
      
      // Reset status após 2 segundos
      setTimeout(() => setSaveStatus('idle'), 2000);
      
    } catch (error) {
      console.error('Erro ao salvar resposta:', error);
      setSaveStatus('error');
      
      // Se offline, manter no localStorage para retry
      if (!navigator.onLine) {
        console.log('Offline - resposta salva localmente para retry');
      }
    }
  }, [diagnosticId, clearDraft]);
  
  // Função principal de save (chamada pelo componente)
  const save = useCallback((
    questionId: number,
    questionText: string,
    questionArea: string,
    answerText?: string,
    answerScale?: number
  ) => {
    if (!diagnosticId) return;
    
    const draft: AnswerDraft = {
      diagnosticId,
      questionId,
      questionText,
      questionArea,
      answerText,
      answerScale,
      timestamp: Date.now()
    };
    
    // Salvar local imediatamente
    saveDraft(draft);
    
    // Debounce para servidor (apenas para texto)
    if (saveTimeoutRef.current) {
      clearTimeout(saveTimeoutRef.current);
    }
    
    saveTimeoutRef.current = setTimeout(() => {
      saveToServer(draft);
    }, SAVE_DEBOUNCE_MS);
  }, [diagnosticId, saveDraft, saveToServer]);
  
  // Processar fila quando voltar online
  useEffect(() => {
    const handleOnline = async () => {
      const draft = getDraft();
      if (draft) {
        console.log('Online - processando resposta pendente');
        await saveToServer(draft);
      }
    };
    
    window.addEventListener('online', handleOnline);
    return () => window.removeEventListener('online', handleOnline);
  }, [getDraft, saveToServer]);
  
  return { 
    save, 
    saveStatus, 
    getDraft, 
    clearDraft,
    saveToServer 
  };
}
```

### Indicador Visual de Status

```tsx
// components/diagnostic/SaveIndicator.tsx
import { Cloud, CloudOff, Check, Loader2, AlertCircle } from 'lucide-react';

interface Props {
  status: 'idle' | 'saving' | 'saved' | 'error';
}

export function SaveIndicator({ status }: Props) {
  const config = {
    idle: {
      icon: null,
      text: '',
      className: ''
    },
    saving: {
      icon: <Loader2 className="h-4 w-4 animate-spin" />,
      text: 'Salvando...',
      className: 'text-blue-500'
    },
    saved: {
      icon: <Check className="h-4 w-4" />,
      text: 'Salvo',
      className: 'text-green-500'
    },
    error: {
      icon: <AlertCircle className="h-4 w-4" />,
      text: 'Erro ao salvar',
      className: 'text-red-500'
    }
  };
  
  const { icon, text, className } = config[status];
  
  if (status === 'idle') return null;
  
  return (
    <div className={`flex items-center gap-1.5 text-sm ${className}`}>
      {icon}
      <span>{text}</span>
    </div>
  );
}
```

---

## 3. SISTEMA DE EMAIL (RESEND)

### Configuração

```python
# services/email_service.py
import resend
from app.config import settings
from app.database import supabase
from typing import Optional
import logging

logger = logging.getLogger(__name__)

resend.api_key = settings.RESEND_API_KEY


class EmailService:
    """Serviço de envio de emails via Resend."""
    
    FROM_EMAIL = settings.EMAIL_FROM
    FROM_NAME = "NARA Diagnóstico"
    
    async def send_email(
        self,
        to: str,
        subject: str,
        html: str,
        email_type: str,
        diagnostic_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> dict:
        """
        Envia um email e registra no log.
        """
        try:
            response = resend.Emails.send({
                "from": f"{self.FROM_NAME} <{self.FROM_EMAIL}>",
                "to": [to],
                "subject": subject,
                "html": html,
            })
            
            resend_id = response.get("id")
            
            # Registrar no log
            await self._log_email(
                recipient_email=to,
                diagnostic_id=diagnostic_id,
                user_id=user_id,
                email_type=email_type,
                subject=subject,
                status="sent",
                resend_id=resend_id
            )
            
            logger.info(f"Email sent: {email_type} to {to}")
            return {"status": "sent", "resend_id": resend_id}
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            
            await self._log_email(
                recipient_email=to,
                diagnostic_id=diagnostic_id,
                user_id=user_id,
                email_type=email_type,
                subject=subject,
                status="failed",
                error_message=str(e)
            )
            raise
    
    async def _log_email(
        self,
        recipient_email: str,
        email_type: str,
        subject: str,
        status: str,
        diagnostic_id: Optional[str] = None,
        user_id: Optional[str] = None,
        resend_id: Optional[str] = None,
        error_message: Optional[str] = None
    ):
        """Registra email na tabela de logs."""
        supabase.table("email_logs").insert({
            "recipient_email": recipient_email,
            "diagnostic_id": diagnostic_id,
            "user_id": user_id,
            "email_type": email_type,
            "subject": subject,
            "status": status,
            "resend_id": resend_id,
            "error_message": error_message,
        }).execute()
    
    async def send_diagnostic_result(
        self,
        to: str,
        user_name: Optional[str],
        diagnostic_id: str,
        result_token: str,
        overall_score: float,
        summary: str
    ):
        """Envia email com resultado do diagnóstico."""
        html = self._render_template(
            "diagnostic_result",
            user_name=user_name or "Viajante",
            overall_score=overall_score,
            summary=summary,
            view_url=f"{settings.FRONTEND_URL}/resultado/{result_token}"
        )
        
        return await self.send_email(
            to=to,
            subject="🎯 Seu Diagnóstico NARA está pronto!",
            html=html,
            email_type="diagnostic_result",
            diagnostic_id=diagnostic_id
        )
    
    async def send_resume_link(
        self,
        to: str,
        user_name: Optional[str],
        diagnostic_id: str,
        progress: int
    ):
        """Envia link para retomar diagnóstico."""
        html = self._render_template(
            "resume_link",
            user_name=user_name or "Viajante",
            progress=progress,
            resume_url=f"{settings.FRONTEND_URL}/diagnostico/{diagnostic_id}/retomar"
        )
        
        return await self.send_email(
            to=to,
            subject="📝 Continue seu Diagnóstico NARA",
            html=html,
            email_type="resume_link",
            diagnostic_id=diagnostic_id
        )
    
    async def send_waitlist_welcome(
        self,
        to: str,
        user_name: Optional[str] = None
    ):
        """Envia email de boas-vindas à lista de espera."""
        html = self._render_template(
            "waitlist_welcome",
            user_name=user_name or "Viajante"
        )
        
        return await self.send_email(
            to=to,
            subject="🚀 Você está na lista de espera da NARA!",
            html=html,
            email_type="waitlist_welcome"
        )
    
    def _render_template(self, template_name: str, **kwargs) -> str:
        """Renderiza template de email."""
        templates = {
            "diagnostic_result": self._template_diagnostic_result,
            "resume_link": self._template_resume_link,
            "waitlist_welcome": self._template_waitlist_welcome,
        }
        
        template_func = templates.get(template_name)
        if not template_func:
            raise ValueError(f"Template não encontrado: {template_name}")
        
        return template_func(**kwargs)
    
    def _template_diagnostic_result(
        self,
        user_name: str,
        overall_score: float,
        summary: str,
        view_url: str
    ) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f9fafb;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; padding: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <div style="text-align: center; margin-bottom: 24px;">
                    <h1 style="color: #6366f1; font-size: 24px; margin: 0;">Olá, {user_name}! 👋</h1>
                </div>
                
                <p style="color: #374151; line-height: 1.6;">Seu Diagnóstico de Transformação Narrativa está pronto!</p>
                
                <div style="width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 24px auto; text-align: center;">
                    <span style="font-size: 42px; font-weight: bold; line-height: 1;">{overall_score:.1f}</span>
                    <span style="font-size: 12px; opacity: 0.9;">Score Geral</span>
                </div>
                
                <div style="background: #f3f4f6; border-radius: 8px; padding: 16px; margin: 24px 0;">
                    <strong>Resumo:</strong>
                    <p style="margin: 8px 0 0 0; color: #4b5563;">{summary[:300]}...</p>
                </div>
                
                <a href="{view_url}" style="display: block; background: #6366f1; color: white; text-decoration: none; padding: 14px 28px; border-radius: 8px; text-align: center; font-weight: 600; margin: 24px 0;">
                    Ver Diagnóstico Completo →
                </a>
                
                <p style="color: #6b7280; font-size: 14px; text-align: center; margin-top: 32px;">
                    © {settings.APP_NAME}. Todos os direitos reservados.
                </p>
            </div>
        </body>
        </html>
        """
    
    def _template_resume_link(
        self,
        user_name: str,
        progress: int,
        resume_url: str
    ) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f9fafb;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; padding: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h1 style="color: #6366f1; font-size: 24px; margin: 0 0 16px 0;">Olá, {user_name}! 👋</h1>
                
                <p style="color: #374151; line-height: 1.6;">
                    Notamos que você começou seu Diagnóstico de Transformação Narrativa mas ainda não finalizou.
                </p>
                
                <div style="background: #f3f4f6; border-radius: 8px; padding: 16px; margin: 24px 0;">
                    <p style="margin: 0; color: #4b5563;">
                        <strong>Seu progresso:</strong> {progress}% concluído
                    </p>
                    <div style="background: #e5e7eb; border-radius: 4px; height: 8px; margin-top: 8px;">
                        <div style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); border-radius: 4px; height: 8px; width: {progress}%;"></div>
                    </div>
                </div>
                
                <p style="color: #374151; line-height: 1.6;">
                    Suas respostas estão salvas. Clique no botão abaixo para continuar de onde parou:
                </p>
                
                <a href="{resume_url}" style="display: block; background: #6366f1; color: white; text-decoration: none; padding: 14px 28px; border-radius: 8px; text-align: center; font-weight: 600; margin: 24px 0;">
                    Continuar Diagnóstico →
                </a>
                
                <p style="color: #6b7280; font-size: 14px; text-align: center; margin-top: 32px;">
                    © {settings.APP_NAME}. Todos os direitos reservados.
                </p>
            </div>
        </body>
        </html>
        """
    
    def _template_waitlist_welcome(self, user_name: str) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f9fafb;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; padding: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h1 style="color: #6366f1; font-size: 24px; margin: 0 0 16px 0;">🎉 Você está na lista!</h1>
                
                <p style="color: #374151; line-height: 1.6;">Olá, {user_name}!</p>
                
                <p style="color: #374151; line-height: 1.6;">
                    Você agora faz parte da lista de espera da NARA. Estamos trabalhando 
                    para construir uma plataforma transformadora de desenvolvimento 
                    pessoal baseada na metodologia do Círculo Narrativo.
                </p>
                
                <h2 style="color: #374151; font-size: 18px; margin: 24px 0 12px 0;">O que vem por aí:</h2>
                <ul style="color: #4b5563; line-height: 1.8;">
                    <li>🎯 Diagnósticos mais profundos e personalizados</li>
                    <li>📊 Acompanhamento da sua evolução ao longo do tempo</li>
                    <li>🧭 Planos de ação customizados para sua jornada</li>
                    <li>👥 Comunidade de pessoas em transformação</li>
                </ul>
                
                <p style="color: #374151; line-height: 1.6;">
                    Você será um dos primeiros a saber quando lançarmos novas funcionalidades!
                </p>
                
                <p style="color: #6b7280; font-size: 14px; text-align: center; margin-top: 32px;">
                    © {settings.APP_NAME}. Todos os direitos reservados.
                </p>
            </div>
        </body>
        </html>
        """


# Instância singleton
email_service = EmailService()
```

---

## 4. TEMPLATES DE EMAIL

### Tipos de Email Suportados

| Tipo | Gatilho | Conteúdo |
|------|---------|----------|
| `diagnostic_result` | Diagnóstico finalizado | Score, resumo, link para resultado |
| `resume_link` | Diagnóstico abandonado (24h) | Progresso, link para retomar |
| `waitlist_welcome` | Cadastro na waitlist | Boas-vindas, próximos passos |
| `magic_link` | Login solicitado | Link de acesso único |

### Boas Práticas

1. **Design responsivo** - Funciona em mobile e desktop
2. **Fallback para texto** - Inclui versão texto plano
3. **CTA claro** - Um botão principal por email
4. **Branding consistente** - Cores e tom da marca NARA
5. **Unsubscribe** - Link de descadastro quando aplicável

---

## 5. MAGIC LINKS E AUTENTICAÇÃO

### Fluxo de Magic Link com Supabase

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USUÁRIO SOLICITA ACESSO                                      │
│    • Frontend: POST /auth/magic-link com email                  │
│    • Backend: Chama Supabase Auth signInWithOtp                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. SUPABASE ENVIA EMAIL                                         │
│    • Email com link: {FRONTEND_URL}/auth/callback?token=xxx     │
│    • Válido por 15 minutos                                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. USUÁRIO CLICA NO LINK                                        │
│    • Frontend: Página /auth/callback                            │
│    • Supabase JS verifica token automaticamente                 │
│    • Cria sessão e retorna access_token                         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. SESSÃO ESTABELECIDA                                          │
│    • Token JWT salvo pelo Supabase client                       │
│    • Diagnósticos anônimos associados ao user_id                │
│    • Redireciona para dashboard                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Implementação Frontend

```typescript
// pages/auth/callback.tsx
import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { supabase } from '@/lib/supabase';

export function AuthCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Supabase verifica o token automaticamente via URL hash
        const { data: { session }, error } = await supabase.auth.getSession();
        
        if (error) throw error;
        
        if (session) {
          // Verificar se há diagnóstico para migrar
          const diagnosticId = localStorage.getItem('nara_diagnostic_id');
          if (diagnosticId) {
            // Migrar diagnóstico anônimo para o usuário
            await migrateAnonymousDiagnostic(diagnosticId, session.user.id);
          }
          
          // Redirecionar para dashboard ou diagnóstico
          navigate(diagnosticId ? `/diagnostico/${diagnosticId}` : '/dashboard');
        } else {
          setError('Sessão não encontrada. O link pode ter expirado.');
        }
      } catch (err: any) {
        setError(err.message || 'Erro ao processar autenticação');
      }
    };
    
    handleCallback();
  }, [navigate]);
  
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-xl font-semibold text-red-600 mb-2">Erro</h1>
          <p className="text-gray-600">{error}</p>
          <a href="/login" className="text-primary underline mt-4 inline-block">
            Solicitar novo link
          </a>
        </div>
      </div>
    );
  }
  
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4" />
        <p className="text-gray-600">Autenticando...</p>
      </div>
    </div>
  );
}

async function migrateAnonymousDiagnostic(diagnosticId: string, userId: string) {
  const { error } = await supabase
    .from('diagnostics')
    .update({ user_id: userId, anonymous_session_id: null })
    .eq('id', diagnosticId)
    .is('user_id', null);
  
  if (!error) {
    localStorage.removeItem('nara_diagnostic_id');
    localStorage.removeItem('nara_session_id');
  }
}
```

---

## 6. LISTA DE ESPERA

### Endpoint de Inscrição

```python
# api/v1/waitlist.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.database import supabase
from app.services.email_service import email_service

router = APIRouter(prefix="/waitlist", tags=["Waitlist"])


class WaitlistRequest(BaseModel):
    email: EmailStr
    full_name: str | None = None
    diagnostic_id: str | None = None
    source: str = "diagnostic"
    utm_source: str | None = None


class WaitlistResponse(BaseModel):
    status: str
    message: str
    position: int | None = None


@router.post("", response_model=WaitlistResponse)
async def join_waitlist(request: WaitlistRequest):
    """
    Adiciona email à lista de espera.
    """
    # Verificar se já existe
    existing = supabase.table("waitlist").select("id").eq(
        "email", request.email
    ).execute()
    
    if existing.data:
        return WaitlistResponse(
            status="already_registered",
            message="Você já está na lista de espera!"
        )
    
    # Inserir na lista
    result = supabase.table("waitlist").insert({
        "email": request.email,
        "full_name": request.full_name,
        "diagnostic_id": request.diagnostic_id,
        "source": request.source,
        "utm_source": request.utm_source,
    }).execute()
    
    # Contar posição
    count_result = supabase.table("waitlist").select("id", count="exact").execute()
    position = count_result.count
    
    # Enviar email de boas-vindas
    try:
        await email_service.send_waitlist_welcome(
            to=request.email,
            user_name=request.full_name
        )
    except Exception as e:
        # Log mas não falha a requisição
        print(f"Erro ao enviar email: {e}")
    
    return WaitlistResponse(
        status="registered",
        message="Você está na lista! Verifique seu email.",
        position=position
    )


@router.get("/count")
async def get_waitlist_count():
    """Retorna contagem da lista de espera (para social proof)."""
    result = supabase.table("waitlist").select("id", count="exact").execute()
    
    return {"count": result.count}
```

### Componente Frontend

```tsx
// components/waitlist/WaitlistForm.tsx
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { apiClient } from '@/api/client';
import { CheckCircle, Loader2 } from 'lucide-react';

const schema = z.object({
  email: z.string().email('Email inválido'),
  full_name: z.string().min(2, 'Nome muito curto').optional(),
});

type FormData = z.infer<typeof schema>;

interface Props {
  diagnosticId?: string;
  source?: string;
  onSuccess?: () => void;
}

export function WaitlistForm({ diagnosticId, source = 'diagnostic', onSuccess }: Props) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<{ status: string; position?: number } | null>(null);
  
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });
  
  const onSubmit = async (data: FormData) => {
    setIsSubmitting(true);
    
    try {
      const response = await apiClient.post('/waitlist', {
        ...data,
        diagnostic_id: diagnosticId,
        source,
      });
      
      setResult({
        status: response.data.status,
        position: response.data.position
      });
      onSuccess?.();
    } catch (error) {
      console.error('Erro ao cadastrar:', error);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  if (result) {
    return (
      <div className="text-center p-6 bg-green-50 rounded-lg">
        <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-3" />
        <h3 className="text-lg font-semibold text-green-800">
          {result.status === 'already_registered' 
            ? 'Você já está na lista!' 
            : 'Você está na lista!'
          }
        </h3>
        {result.position && (
          <p className="text-green-600 mt-1">
            Você é o #{result.position} na fila
          </p>
        )}
        <p className="text-green-600 text-sm mt-2">
          Verifique seu email para mais informações.
        </p>
      </div>
    );
  }
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Input
          {...register('full_name')}
          placeholder="Seu nome (opcional)"
          className={errors.full_name ? 'border-red-500' : ''}
        />
        {errors.full_name && (
          <p className="text-red-500 text-sm mt-1">{errors.full_name.message}</p>
        )}
      </div>
      
      <div>
        <Input
          {...register('email')}
          type="email"
          placeholder="seu@email.com"
          className={errors.email ? 'border-red-500' : ''}
        />
        {errors.email && (
          <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
        )}
      </div>
      
      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? (
          <>
            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
            Cadastrando...
          </>
        ) : (
          'Entrar na Lista de Espera'
        )}
      </Button>
      
      <p className="text-xs text-gray-500 text-center">
        Sem spam. Apenas atualizações importantes.
      </p>
    </form>
  );
}
```

---

## 7. RETOMADA DE DIAGNÓSTICO

### Verificação ao Iniciar

Quando o usuário informa o email para iniciar um diagnóstico, verificamos se existe um em andamento:

```typescript
// hooks/useDiagnosticStart.ts
import { useState } from 'react';
import { apiClient } from '@/api/client';

interface ExistingDiagnostic {
  exists: boolean;
  diagnostic_id?: string;
  status?: string;
  current_phase?: number;
  total_answers?: number;
  started_at?: string;
}

export function useDiagnosticStart() {
  const [existingDiagnostic, setExistingDiagnostic] = useState<ExistingDiagnostic | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  
  const checkExisting = async (email: string): Promise<ExistingDiagnostic> => {
    setIsChecking(true);
    try {
      const response = await apiClient.get(`/diagnostic/check-existing?email=${email}`);
      const result = response.data;
      setExistingDiagnostic(result);
      return result;
    } finally {
      setIsChecking(false);
    }
  };
  
  const resumeDiagnostic = async (diagnosticId: string) => {
    const response = await apiClient.get(`/diagnostic/${diagnosticId}/current-state`);
    return response.data;
  };
  
  const startNew = async (email: string, abandonPrevious: boolean = false) => {
    if (abandonPrevious && existingDiagnostic?.diagnostic_id) {
      // Marcar anterior como abandonado
      await apiClient.post(`/diagnostic/${existingDiagnostic.diagnostic_id}/abandon`);
    }
    
    // Iniciar novo
    const response = await apiClient.post('/diagnostic/start', { email });
    return response.data;
  };
  
  return {
    existingDiagnostic,
    isChecking,
    checkExisting,
    resumeDiagnostic,
    startNew
  };
}
```

### Modal de Retomada

```tsx
// components/diagnostic/ResumeModal.tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';

interface Props {
  open: boolean;
  onClose: () => void;
  diagnostic: {
    diagnostic_id: string;
    total_answers: number;
    started_at: string;
  };
  onResume: () => void;
  onStartNew: () => void;
}

export function ResumeModal({ open, onClose, diagnostic, onResume, onStartNew }: Props) {
  const progress = Math.round((diagnostic.total_answers / 40) * 100);
  const startedAgo = formatDistanceToNow(new Date(diagnostic.started_at), {
    addSuffix: true,
    locale: ptBR
  });
  
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Diagnóstico em Andamento</DialogTitle>
        </DialogHeader>
        
        <div className="py-4">
          <p className="text-gray-600 mb-4">
            Você tem um diagnóstico iniciado {startedAgo} com {progress}% de progresso.
          </p>
          
          <div className="bg-gray-100 rounded-lg p-4 mb-4">
            <div className="flex justify-between text-sm mb-2">
              <span>Progresso</span>
              <span className="font-medium">{diagnostic.total_answers} perguntas</span>
            </div>
            <div className="bg-gray-200 rounded-full h-2">
              <div 
                className="bg-primary rounded-full h-2 transition-all"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
          
          <p className="text-sm text-gray-500">
            O que você gostaria de fazer?
          </p>
        </div>
        
        <div className="flex gap-3">
          <Button variant="outline" onClick={onStartNew} className="flex-1">
            Começar Novo
          </Button>
          <Button onClick={onResume} className="flex-1">
            Continuar
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
```

### Endpoint de Estado Atual

```python
# api/v1/diagnostic.py

@router.get("/{diagnostic_id}/current-state")
async def get_current_state(diagnostic_id: str):
    """
    Retorna o estado atual do diagnóstico para retomada.
    """
    # Buscar diagnóstico
    diag_result = supabase.table("diagnostics").select("*").eq(
        "id", diagnostic_id
    ).single().execute()
    
    if not diag_result.data:
        raise HTTPException(status_code=404, detail="Diagnóstico não encontrado")
    
    diagnostic = diag_result.data
    
    # Buscar próximas perguntas
    if diagnostic["current_phase"] == 1:
        from app.core.constants import BASELINE_QUESTIONS
        questions = BASELINE_QUESTIONS[diagnostic["current_question"]:]
    else:
        # Para fases adaptativas, regenerar se necessário
        questions = await service.get_phase_questions(
            diagnostic_id, 
            diagnostic["current_phase"]
        )
    
    return {
        "diagnostic_id": diagnostic_id,
        "status": diagnostic["status"],
        "current_phase": diagnostic["current_phase"],
        "current_question": diagnostic["current_question"],
        "total_answers": diagnostic["total_answers"],
        "total_words": diagnostic["total_words"],
        "areas_covered": diagnostic["areas_covered"],
        "questions": questions,
        "progress": {
            "overall": min(100, (diagnostic["total_answers"] / 40) * 100),
            "questions": min(100, (diagnostic["total_answers"] / 40) * 100),
            "words": min(100, (diagnostic["total_words"] / 3500) * 100),
            "coverage": (len(diagnostic["areas_covered"]) / 12) * 100
        }
    }
```

---

**Referências Cruzadas:**
- Tabelas de banco: [02_BANCO_DADOS.md](./02_BANCO_DADOS.md)
- Endpoints relacionados: [04_BACKEND_API.md](./04_BACKEND_API.md)
- Integração no frontend: [05_FRONTEND_UX.md](./05_FRONTEND_UX.md)
