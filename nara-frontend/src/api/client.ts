/**
 * API client (Axios) para o backend NARA.
 * Em dev, usa URL relativa para o proxy do Vite (/api -> localhost:8000).
 */
import axios from "axios";

const origin =
  import.meta.env.VITE_API_URL ??
  (import.meta.env.DEV ? "" : "http://localhost:8000");
const baseURL = origin ? `${origin}/api/v1` : "/api/v1";

export const apiClient = axios.create({
  baseURL,
  timeout: 30_000,
  headers: { "Content-Type": "application/json" },
});

apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    const message =
      err.response?.data?.detail ?? err.message ?? "Erro de conexão";
    console.error("[API]", err.config?.url, err.response?.status, message);
    return Promise.reject(err);
  }
);
