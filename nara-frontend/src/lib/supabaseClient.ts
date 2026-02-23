import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string | undefined;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined;

if (!supabaseUrl || !supabaseAnonKey) {
  // Mantém erro explícito para evitar auth silenciosa quebrada em produção.
  console.warn("VITE_SUPABASE_URL ou VITE_SUPABASE_ANON_KEY ausentes.");
}

export const supabaseClient = createClient(
  supabaseUrl ?? "",
  supabaseAnonKey ?? ""
);
