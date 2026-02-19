import { apiClient } from "./client";

export interface WaitlistPayload {
  email: string;
  full_name?: string;
  diagnostic_id?: string;
  source?: string;
  utm_source?: string;
}

export async function joinWaitlist(payload: WaitlistPayload) {
  const { data } = await apiClient.post<{ status: string; message: string; position?: number }>(
    "/waitlist",
    payload
  );
  return data;
}

export async function getWaitlistCount() {
  const { data } = await apiClient.get<{ count: number }>("/waitlist/count");
  return data;
}
