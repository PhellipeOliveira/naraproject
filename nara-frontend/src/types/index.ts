/**
 * Types globais e contratos da API de diagnóstico.
 */

export interface Question {
  id: number;
  area: string;
  type: "scale" | "open_long" | "open_short";
  text: string;
  scale_labels?: string[];
  follow_up_hint?: string;
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

export interface DiagnosticResultResponse {
  overall_score: number;
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

export interface SessionData {
  sessionId: string;
  diagnosticId?: string;
  email?: string;
  expiresAt: string;
}
