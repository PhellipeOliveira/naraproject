/**
 * Types globais e contratos da API de diagnóstico.
 */

export interface Question {
  id: number;
  area: string;
  type: "open_long" | "open_short";  // Removido "scale" - apenas perguntas narrativas
  text: string;
  follow_up_hint?: string;
  scale_labels?: string[];
}

export interface DiagnosticStartResponse {
  diagnostic_id: string;
  status: string;
  phase: number;
  questions: Question[];
  total_questions: number;
  result_token: string;
}

export interface ProgressInfo {
  overall: number;
  questions: number;
  words: number;
  coverage: number;
}

export interface AnswerSubmitResponse {
  status: string;
  can_finish: boolean;
  phase_complete: boolean;
  progress: ProgressInfo;
  total_answers: number;
  total_words: number;
  areas_covered: number;
}

export interface NextQuestionsResponse {
  phase: number;
  questions: Question[];
  total_questions: number;
}

export interface EligibilityResponse {
  can_finish: boolean;
  criteria: {
    questions: { current: number; required: number; percentage: number; met: boolean };
    words: { current: number; required: number; percentage: number; met: boolean };
    coverage: {
      current: number;
      required: number;
      percentage: number;
      met: boolean;
      missing_areas?: string[];
    };
  };
  overall_progress: number;
}

export interface AreaAnalysis {
  area_name: string;
  score: number;
  status: string;
  analysis: string;
  key_insight: string;
}

export interface Recommendation {
  action: string;
  timeframe: string;
  area_related?: string;
}

export interface VetorEstado {
  motor_dominante: string;
  motor_secundario: string;
  estagio_jornada: string;
  crise_raiz: string;
  crises_derivadas: string[];
  ponto_entrada_ideal: string;
  dominios_alavanca: string[];
  tom_emocional: string;
  risco_principal: string;
  necessidade_atual: string;
}

export interface DiagnosticResultResponse {
  // Novos campos V2
  vetor_estado: VetorEstado;
  memorias_vermelhas: string[];
  areas_silenciadas: number[];
  ancoras_sugeridas: string[];
  
  // Campos legacy (mantidos por compatibilidade)
  overall_score?: number;
  phase_identified: string;
  motor_dominante: string;
  motor_secundario?: string;
  crise_raiz: string;
  ponto_entrada_ideal: string;
  executive_summary: string;
  area_analysis: AreaAnalysis[];
  patterns: { correlations?: string[]; contradictions?: string[]; self_sabotage_cycles?: string[] };
  strengths: string[];
  development_areas: Array<{ area_name: string; priority: string; reasoning: string }>;
  recommendations: Recommendation[];
}

export interface MicroReportResponse {
  area: string;
  micro_summary: string;
  foco_tcc: string;
  ancoras: string[];
  proxima_acao_7_dias: string;
}

export interface MicroDiagnosticStartResponse {
  micro_id: string;
  status: string;
  phase: number;
  questions: Question[];
  total_questions: number;
}

export interface MicroDiagnosticStateResponse {
  micro_id: string;
  status: string;
  phase: number;
  questions: Question[];
  total_questions: number;
  result?: MicroReportResponse | null;
}

export interface MicroDiagnosticAnswerInput {
  question_id: number;
  question_text: string;
  question_area: string;
  answer_text: string;
}

export interface DiagnosticOwnerEmailResponse {
  email: string;
}

export interface DiagnosticCurrentStateResponse {
  diagnostic_id: string;
  result_token?: string;
  email?: string;
  status: string;
  current_phase: number;
  current_question: number;
  current_phase_questions_count?: number;
  total_answers: number;
  total_words: number;
  areas_covered: string[];
  questions: Question[];
  answers_prefill?: Record<string, string>;
  valid_answers_in_current_phase?: number;
  can_finish: boolean;
  progress: ProgressInfo;
}

export interface DashboardPeriod {
  days: number;
  start_date: string;
  end_date: string;
}

export interface DashboardTotals {
  diagnostics_started: number;
  diagnostics_completed: number;
  completion_rate: number;
}

export interface DashboardRealtimeMetric {
  date: string;
  total_diagnostics: number;
  completed: number;
  in_progress: number;
  completion_rate: number;
}

export interface DashboardMotorDistribution {
  motor_dominante: string;
  count: number;
  percentage: number;
}

export interface DashboardCriseDistribution {
  crise_raiz: string;
  count: number;
  percentage: number;
}

export interface DashboardAreaSilenciada {
  area_id: number;
  area_name: string;
  silence_count: number;
  percentage: number;
}

export interface DashboardDataResponse {
  period: DashboardPeriod;
  totals: DashboardTotals;
  realtime_metrics: DashboardRealtimeMetric[];
  motores_distribution: DashboardMotorDistribution[];
  crises_distribution: DashboardCriseDistribution[];
  areas_silenciadas: DashboardAreaSilenciada[];
}

export interface SessionData {
  sessionId: string;
  diagnosticId?: string;
  email?: string;
  expiresAt: string;
}
