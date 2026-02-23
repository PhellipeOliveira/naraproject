import { apiClient } from "./client";
import { supabaseClient } from "../lib/supabaseClient";

export interface AuthUser {
  id: string;
  email: string;
  user_metadata?: Record<string, unknown>;
}

export interface MyDiagnosticsResponse {
  items: Array<{
    id: string;
    result_token: string;
    status: string;
    created_at: string;
    completed_at?: string | null;
    current_phase?: number;
    total_answers?: number;
  }>;
}

async function getAccessToken(): Promise<string> {
  const { data } = await supabaseClient.auth.getSession();
  const token = data.session?.access_token;
  if (!token) {
    throw new Error("Usuário não autenticado.");
  }
  return token;
}

export async function getMe(): Promise<AuthUser> {
  const accessToken = await getAccessToken();
  const { data } = await apiClient.get<AuthUser>("/auth/me", {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  return data;
}

export async function getMyDiagnostics(): Promise<MyDiagnosticsResponse> {
  const accessToken = await getAccessToken();
  const { data } = await apiClient.get<MyDiagnosticsResponse>("/auth/my-diagnostics", {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  return data;
}
