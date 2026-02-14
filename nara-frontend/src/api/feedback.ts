import { apiClient } from "./client";

export interface FeedbackPayload {
  diagnostic_id: string;
  nps_score: number;
  rating?: number;
  feedback_text?: string;
  feedback_type?: "public" | "private";
}

export async function submitFeedback(payload: FeedbackPayload) {
  const { data } = await apiClient.post("/feedback", payload);
  return data;
}
