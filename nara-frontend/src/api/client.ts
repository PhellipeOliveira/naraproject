/**
 * API client (Axios) para o backend NARA.
 * Em dev, usa URL relativa para o proxy do Vite (/api -> localhost:8000).
 */
import axios from "axios";
import { clearAdminToken, getAdminToken } from "../lib/adminSession";
import { clearSession } from "../lib/session";

const raw = import.meta.env.VITE_API_URL ?? (import.meta.env.DEV ? "" : "");
const origin = typeof raw === "string" ? raw.replace(/\/+$/, "") : "";
if (import.meta.env.PROD && !origin) {
  throw new Error("VITE_API_URL não configurada para produção.");
}
// Evita duplicar /api/v1 quando VITE_API_URL já inclui (ex.: http://localhost:8000/api/v1)
const baseURL = origin
  ? origin.endsWith("/api/v1")
    ? origin
    : `${origin}/api/v1`
  : "/api/v1";

export const apiClient = axios.create({
  baseURL,
  timeout: 30_000,
  headers: { "Content-Type": "application/json" },
});

apiClient.interceptors.request.use((config) => {
  const url = config.url ?? "";
  const token = getAdminToken();
  if (token && (url.includes("/analytics") || url.includes("/admin/me"))) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    const message =
      err.response?.data?.detail ?? err.message ?? "Erro de conexão";
    const status = err.response?.status as number | undefined;
    if (status === 401 || status === 403) {
      const url = String(err.config?.url ?? "");
      if (url.includes("/analytics")) {
        clearAdminToken();
        if (window.location.pathname !== "/admin/login") {
          window.location.assign("/admin/login");
        }
      } else {
        clearSession();
        if (window.location.pathname !== "/") {
          window.location.assign("/");
        }
      }
    }
    if (import.meta.env.DEV) {
      console.error("[API]", err.config?.url, status, message);
    }
    return Promise.reject(err);
  }
);
