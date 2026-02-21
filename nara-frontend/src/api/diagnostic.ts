/**
 * Endpoints de diagnóstico.
 */
import { apiClient } from "./client";
import type {
  DiagnosticStartResponse,
  AnswerSubmitResponse,
  NextQuestionsResponse,
  EligibilityResponse,
  DiagnosticResultResponse,
} from "../types";

export interface StartDiagnosticPayload {
  email: string;
  full_name?: string;
  session_id?: string;
  consent_privacy: boolean;
  consent_marketing?: boolean;
  device_info?: Record<string, unknown>;
  utm_source?: string;
}

export interface SubmitAnswerPayload {
  question_id: number;
  question_text: string;
  question_area: string;
  answer_text?: string;
  answer_scale?: number;
  response_time_seconds?: number;
}

export async function startDiagnostic(
  payload: StartDiagnosticPayload
): Promise<DiagnosticStartResponse> {
  const { data } = await apiClient.post<DiagnosticStartResponse>(
    "/diagnostic/start",
    payload
  );
  return data;
}

export async function submitAnswer(
  diagnosticId: string,
  payload: SubmitAnswerPayload
): Promise<AnswerSubmitResponse> {
  const { data } = await apiClient.post<AnswerSubmitResponse>(
    `/diagnostic/${diagnosticId}/answer`,
    payload
  );
  return data;
}

export async function sendResumeLink(
  diagnosticId: string
): Promise<{ status: string; message: string }> {
  const { data } = await apiClient.post(
    `/diagnostic/${diagnosticId}/send-resume-link`
  );
  return data;
}

/** Timeout para geração de próximas perguntas (RAG + LLM). Backend pode levar 35–45s; margem extra evita erro no front. */
const NEXT_QUESTIONS_TIMEOUT_MS = 90_000;

export async function getNextQuestions(
  diagnosticId: string
): Promise<NextQuestionsResponse> {
  const { data } = await apiClient.get<NextQuestionsResponse>(
    `/diagnostic/${diagnosticId}/next-questions`,
    { timeout: NEXT_QUESTIONS_TIMEOUT_MS }
  );
  return data;
}

export async function checkEligibility(
  diagnosticId: string
): Promise<EligibilityResponse> {
  const { data } = await apiClient.get<EligibilityResponse>(
    `/diagnostic/${diagnosticId}/eligibility`
  );
  return data;
}

export async function finishDiagnostic(
  diagnosticId: string
): Promise<DiagnosticResultResponse> {
  const { data } = await apiClient.post<DiagnosticResultResponse>(
    `/diagnostic/${diagnosticId}/finish`
  );
  return data;
}

export async function getResultByToken(
  token: string
): Promise<DiagnosticResultResponse> {
  const { data } = await apiClient.get<DiagnosticResultResponse>(
    `/diagnostic/result/${token}`
  );
  return data;
}

export async function getCurrentState(diagnosticId: string) {
  const { data } = await apiClient.get(
    `/diagnostic/${diagnosticId}/current-state`
  );
  return data;
}

/** Normaliza e-mail para comparação (trim + minúsculas). */
function normalizeEmail(email: string): string {
  return email.trim().toLowerCase();
}

export async function checkExistingDiagnostic(email: string) {
  const { data } = await apiClient.get<{
    exists: boolean;
    diagnostic_id?: string;
    status?: string;
    current_phase?: number;
    total_answers?: number;
    started_at?: string;
  }>(`/diagnostic/check-existing`, { params: { email: normalizeEmail(email) } });
  return data;
}
