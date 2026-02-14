/**
 * Gestão de sessão no browser (session_id, diagnostic_id, expiração).
 */

const SESSION_KEY = "nara_session_id";
const SESSION_EXPIRY_KEY = "nara_session_expiry";
const DIAGNOSTIC_KEY = "nara_diagnostic_id";
const SESSION_DURATION_DAYS = 30;

export interface SessionData {
  sessionId: string;
  diagnosticId?: string;
  email?: string;
  expiresAt: string;
}

export function getOrCreateSessionId(): string {
  const existingId = localStorage.getItem(SESSION_KEY);
  const expiry = localStorage.getItem(SESSION_EXPIRY_KEY);

  if (existingId && expiry) {
    const expiryDate = new Date(expiry);
    if (expiryDate > new Date()) {
      return existingId;
    }
  }

  const newId = `sess_${crypto.randomUUID()}`;
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
    diagnosticId: diagnosticId ?? undefined,
    expiresAt,
  };
}
