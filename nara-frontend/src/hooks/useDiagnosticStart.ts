/**
 * Hook para gerenciar início e retomada de diagnóstico.
 * Conforme 06_OPERACOES_EMAIL.md - Seção 7
 */

import { useState } from 'react';
import { apiClient } from '../api/client';
import type { Question, ProgressInfo } from '../types';

export interface ExistingDiagnostic {
  exists: boolean;
  diagnostic_id?: string;
  status?: string;
  current_phase?: number;
  total_answers?: number;
  started_at?: string;
}

export interface CurrentState {
  diagnostic_id: string;
  status: string;
  current_phase: number;
  current_question: number;
  total_answers: number;
  total_words: number;
  areas_covered: string[];
  questions: Question[];
  progress: ProgressInfo;
}

export function useDiagnosticStart() {
  const [existingDiagnostic, setExistingDiagnostic] = useState<ExistingDiagnostic | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  /**
   * Verifica se existe diagnóstico em andamento para o email.
   */
  const checkExisting = async (email: string): Promise<ExistingDiagnostic> => {
    setIsChecking(true);
    try {
      const response = await apiClient.get(`/diagnostic/check-existing?email=${encodeURIComponent(email)}`);
      const result = response.data as ExistingDiagnostic;
      setExistingDiagnostic(result);
      return result;
    } catch (error) {
      console.error('Erro ao verificar diagnóstico existente:', error);
      const fallback: ExistingDiagnostic = { exists: false };
      setExistingDiagnostic(fallback);
      return fallback;
    } finally {
      setIsChecking(false);
    }
  };
  
  /**
   * Busca estado atual de um diagnóstico para retomada.
   */
  const resumeDiagnostic = async (diagnosticId: string): Promise<CurrentState> => {
    setIsLoading(true);
    try {
      const response = await apiClient.get(`/diagnostic/${diagnosticId}/current-state`);
      return response.data as CurrentState;
    } finally {
      setIsLoading(false);
    }
  };
  
  /**
   * Inicia novo diagnóstico (abandonando anterior se houver).
   */
  const startNew = async (email: string, abandonPrevious: boolean = false) => {
    setIsLoading(true);
    try {
      if (abandonPrevious && existingDiagnostic?.diagnostic_id) {
        // Marcar anterior como abandonado
        await apiClient.post(`/diagnostic/${existingDiagnostic.diagnostic_id}/abandon`);
      }
      
      // Iniciar novo
      const response = await apiClient.post('/diagnostic/start', { email });
      return response.data;
    } finally {
      setIsLoading(false);
    }
  };
  
  return {
    existingDiagnostic,
    isChecking,
    isLoading,
    checkExisting,
    resumeDiagnostic,
    startNew
  };
}
