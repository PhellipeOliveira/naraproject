/**
 * Estado global do fluxo de diagnóstico (Zustand).
 */
import { create } from "zustand";
import type { Question } from "../types";

interface ProgressInfo {
  overall: number;
  questions: number;
  words: number;
  coverage: number;
}

interface DiagnosticState {
  diagnosticId: string | null;
  resultToken: string | null;
  phase: number;
  questions: Question[];
  currentQuestionIndex: number;
  totalAnswers: number;
  totalWords: number;
  areasCovered: number;
  canFinish: boolean;
  progress: ProgressInfo | null;
  status: "idle" | "in_progress" | "eligible" | "processing" | "completed";

  setStarted: (payload: {
    diagnosticId: string;
    resultToken: string;
    phase: number;
    questions: Question[];
  }) => void;
  setQuestions: (questions: Question[]) => void;
  setCurrentIndex: (index: number) => void;
  setProgress: (payload: {
    totalAnswers: number;
    totalWords: number;
    areasCovered: number;
    canFinish: boolean;
    progress: ProgressInfo;
    status?: string;
  }) => void;
  goNext: () => void;
  goPrev: () => void;
  reset: () => void;
}

export const useDiagnosticStore = create<DiagnosticState>((set) => ({
  diagnosticId: null,
  resultToken: null,
  phase: 1,
  questions: [],
  currentQuestionIndex: 0,
  totalAnswers: 0,
  totalWords: 0,
  areasCovered: 0,
  canFinish: false,
  progress: null,
  status: "idle",

  setStarted: (payload) =>
    set({
      diagnosticId: payload.diagnosticId,
      resultToken: payload.resultToken,
      phase: payload.phase,
      questions: payload.questions,
      currentQuestionIndex: 0,
      totalAnswers: 0,
      totalWords: 0,
      areasCovered: 0,
      canFinish: false,
      progress: null,
      status: "in_progress",
    }),

  setQuestions: (questions) => set({ questions, currentQuestionIndex: 0 }),

  setCurrentIndex: (currentQuestionIndex) => set({ currentQuestionIndex }),

  setProgress: (payload) =>
    set({
      totalAnswers: payload.totalAnswers,
      totalWords: payload.totalWords,
      areasCovered: payload.areasCovered,
      canFinish: payload.canFinish,
      progress: payload.progress,
      status: (payload.status as DiagnosticState["status"]) ?? "in_progress",
    }),

  goNext: () =>
    set((s) => ({
      currentQuestionIndex: Math.min(s.currentQuestionIndex + 1, s.questions.length - 1),
    })),

  goPrev: () =>
    set((s) => ({
      currentQuestionIndex: Math.max(0, s.currentQuestionIndex - 1),
    })),

  reset: () =>
    set({
      diagnosticId: null,
      resultToken: null,
      phase: 1,
      questions: [],
      currentQuestionIndex: 0,
      totalAnswers: 0,
      totalWords: 0,
      areasCovered: 0,
      canFinish: false,
      progress: null,
      status: "idle",
    }),
}));
