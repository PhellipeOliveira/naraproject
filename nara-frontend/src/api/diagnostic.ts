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
  DiagnosticOwnerEmailResponse,
  DiagnosticCurrentStateResponse,
  MicroDiagnosticAnswerInput,
  MicroDiagnosticStartResponse,
  MicroDiagnosticStateResponse,
  MicroReportResponse,
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

export async function getOwnerEmailByToken(
  token: string
): Promise<DiagnosticOwnerEmailResponse> {
  const { data } = await apiClient.get<DiagnosticOwnerEmailResponse>(
    `/diagnostic/result/${token}/owner-email`
  );
  return data;
}

export async function getResultPdfByToken(token: string): Promise<Blob> {
  const res = await apiClient.get(`/diagnostic/result/${token}/pdf`, {
    responseType: "blob",
  });
  return res.data as Blob;
}

export async function getCurrentState(
  diagnosticId: string
): Promise<DiagnosticCurrentStateResponse> {
  const { data } = await apiClient.get<DiagnosticCurrentStateResponse>(
    `/diagnostic/${diagnosticId}/current-state`
  );
  return data;
}

export async function startMicroDiagnostic(
  token: string,
  area: string
): Promise<MicroDiagnosticStartResponse> {
  const { data } = await apiClient.post<MicroDiagnosticStartResponse>(
    `/diagnostic/result/${token}/micro-diagnostic/start`,
    { area }
  );
  return data;
}

export async function getMicroDiagnosticState(
  token: string,
  microId: string
): Promise<MicroDiagnosticStateResponse> {
  const { data } = await apiClient.get<MicroDiagnosticStateResponse>(
    `/diagnostic/result/${token}/micro-diagnostic/${microId}`
  );
  return data;
}

export async function submitMicroDiagnosticAnswers(
  token: string,
  microId: string,
  answers: MicroDiagnosticAnswerInput[]
): Promise<MicroDiagnosticStateResponse> {
  const { data } = await apiClient.post<MicroDiagnosticStateResponse>(
    `/diagnostic/result/${token}/micro-diagnostic/${microId}/submit`,
    { answers }
  );
  return data;
}

export async function finishMicroDiagnostic(
  token: string,
  microId: string
): Promise<MicroReportResponse> {
  const { data } = await apiClient.post<MicroReportResponse>(
    `/diagnostic/result/${token}/micro-diagnostic/${microId}/finish`
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

/**
 * Abandona o diagnóstico em andamento (status → abandoned).
 * Permite iniciar um novo diagnóstico com o mesmo e-mail.
 */
export async function abandonDiagnostic(diagnosticId: string): Promise<void> {
  await apiClient.post(`/diagnostic/${diagnosticId}/abandon`);
}
