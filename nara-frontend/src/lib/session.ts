/**
 * Gestão de sessão e persistência local do diagnóstico.
 * Conforme 06_OPERACOES_EMAIL.md - Seção 1
 */

import { v4 as uuidv4 } from 'uuid';

const SESSION_KEY = 'nara_session_id';
const SESSION_EXPIRY_KEY = 'nara_session_expiry';
const DIAGNOSTIC_KEY = 'nara_diagnostic_id';
const RESULT_TOKEN_KEY = 'nara_result_token';
const SESSION_DURATION_DAYS = 30;

export interface SessionData {
  sessionId: string;
  diagnosticId?: string;
  email?: string;
  expiresAt: string;
}

/**
 * Obtém ou cria um session_id único para o usuário anônimo.
 * Session ID é usado para tracking e associação de diagnósticos.
 */
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

/**
 * Obtém diagnostic_id armazenado localmente (diagnóstico em andamento).
 */
export function getStoredDiagnosticId(): string | null {
  return localStorage.getItem(DIAGNOSTIC_KEY);
}

/**
 * Salva diagnostic_id no localStorage.
 */
export function setStoredDiagnosticId(diagnosticId: string): void {
  localStorage.setItem(DIAGNOSTIC_KEY, diagnosticId);
}

/**
 * Obtém result_token do último diagnóstico concluído.
 */
export function getStoredResultToken(): string | null {
  return localStorage.getItem(RESULT_TOKEN_KEY);
}

/**
 * Salva result_token do diagnóstico concluído.
 */
export function setStoredResultToken(token: string): void {
  localStorage.setItem(RESULT_TOKEN_KEY, token);
}

/**
 * Limpa todos os dados da sessão (logout ou novo diagnóstico).
 */
export function clearSession(): void {
  localStorage.removeItem(SESSION_KEY);
  localStorage.removeItem(SESSION_EXPIRY_KEY);
  localStorage.removeItem(DIAGNOSTIC_KEY);
  // Não remove RESULT_TOKEN_KEY para manter acesso ao último resultado
}

/**
 * Limpa apenas o diagnostic_id (ao finalizar ou abandonar).
 */
export function clearDiagnosticId(): void {
  localStorage.removeItem(DIAGNOSTIC_KEY);
}

/**
 * Obtém todos os dados da sessão atual.
 */
export function getSessionData(): SessionData | null {
  const sessionId = localStorage.getItem(SESSION_KEY);
  const expiresAt = localStorage.getItem(SESSION_EXPIRY_KEY);
  const diagnosticId = localStorage.getItem(DIAGNOSTIC_KEY);
  
  if (!sessionId || !expiresAt) return null;
  
  // Verificar se expirou
  const expiryDate = new Date(expiresAt);
  if (expiryDate <= new Date()) {
    clearSession();
    return null;
  }
  
  return {
    sessionId,
    diagnosticId: diagnosticId || undefined,
    expiresAt
  };
}

/**
 * Verifica se há sessão ativa e válida.
 */
export function hasActiveSession(): boolean {
  return getSessionData() !== null;
}

/**
 * Estende a expiração da sessão (chamado ao interagir com o app).
 */
export function extendSession(): void {
  const session = getSessionData();
  if (session) {
    const newExpiry = new Date();
    newExpiry.setDate(newExpiry.getDate() + SESSION_DURATION_DAYS);
    localStorage.setItem(SESSION_EXPIRY_KEY, newExpiry.toISOString());
  }
}

/**
 * Migra diagnóstico anônimo para usuário autenticado.
 * Chamado após login/signup bem-sucedido.
 */
export async function migrateAnonymousDiagnostic(
  diagnosticId: string, 
  userId: string
): Promise<boolean> {
  try {
    // Chamar API para migrar
    const response = await fetch(`/api/v1/diagnostic/${diagnosticId}/migrate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId })
    });
    
    if (response.ok) {
      clearDiagnosticId();
      return true;
    }
    return false;
  } catch (error) {
    if (import.meta.env.DEV) {
      console.error('Erro ao migrar diagnóstico:', error);
    }
    return false;
  }
}
