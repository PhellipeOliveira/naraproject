/**
 * Hook de auto-save para respostas do diagnóstico.
 * Conforme 06_OPERACOES_EMAIL.md - Seção 2
 * 
 * Features:
 * - Salva rascunho no localStorage a cada keystroke (debounced)
 * - Salva no servidor após delay (1s)
 * - Suporta modo offline com retry automático
 * - Indica status visual (saving, saved, error)
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { apiClient } from '../api/client';

const SAVE_DEBOUNCE_MS = 1000;
const LOCAL_DRAFT_KEY = 'nara_answer_draft';

export interface AnswerDraft {
  diagnosticId: string;
  questionId: number;
  questionText: string;
  questionArea: string;
  answerText?: string;
  timestamp: number;
}

export type SaveStatus = 'idle' | 'saving' | 'saved' | 'error';

export function useAutoSave(diagnosticId: string | null) {
  const [saveStatus, setSaveStatus] = useState<SaveStatus>('idle');
  const saveTimeoutRef = useRef<ReturnType<typeof setTimeout>>();
  const lastSavedRef = useRef<string>('');
  
  /**
   * Salva rascunho no localStorage (imediato).
   */
  const saveDraft = useCallback((draft: Omit<AnswerDraft, 'timestamp'>) => {
    const fullDraft: AnswerDraft = {
      ...draft,
      timestamp: Date.now()
    };
    localStorage.setItem(LOCAL_DRAFT_KEY, JSON.stringify(fullDraft));
  }, []);
  
  /**
   * Recupera rascunho do localStorage.
   */
  const getDraft = useCallback((): AnswerDraft | null => {
    const stored = localStorage.getItem(LOCAL_DRAFT_KEY);
    if (!stored) return null;
    
    try {
      const draft = JSON.parse(stored) as AnswerDraft;
      // Verificar se é do diagnóstico atual
      if (draft.diagnosticId === diagnosticId) {
        return draft;
      }
    } catch {
      // JSON inválido
      localStorage.removeItem(LOCAL_DRAFT_KEY);
    }
    return null;
  }, [diagnosticId]);
  
  /**
   * Limpa rascunho após salvar com sucesso.
   */
  const clearDraft = useCallback(() => {
    localStorage.removeItem(LOCAL_DRAFT_KEY);
    lastSavedRef.current = '';
  }, []);
  
  /**
   * Salva no servidor (com retry se offline).
   */
  const saveToServer = useCallback(async (answer: AnswerDraft): Promise<boolean> => {
    if (!diagnosticId) return false;
    
    // Evitar salvar duplicado
    const answerKey = `${answer.questionId}-${answer.answerText}`;
    if (answerKey === lastSavedRef.current) {
      return true;
    }
    
    setSaveStatus('saving');
    
    try {
      await apiClient.post(`/diagnostic/${diagnosticId}/answer`, {
        question_id: answer.questionId,
        question_text: answer.questionText,
        question_area: answer.questionArea,
        answer_text: answer.answerText,
      });
      
      lastSavedRef.current = answerKey;
      clearDraft();
      setSaveStatus('saved');
      
      // Reset status após 2 segundos
      setTimeout(() => setSaveStatus('idle'), 2000);
      
      return true;
      
    } catch {
      setSaveStatus('error');
      
      // Se offline, manter no localStorage para retry
      if (navigator.onLine) {
        // Reset status de erro após 5 segundos
        setTimeout(() => setSaveStatus('idle'), 5000);
      }
      
      return false;
    }
  }, [diagnosticId, clearDraft]);
  
  /**
   * Função principal de save (chamada pelo componente).
   */
  const save = useCallback((
    questionId: number,
    questionText: string,
    questionArea: string,
    answerText?: string
  ) => {
    if (!diagnosticId || !answerText?.trim()) return;
    
    const draft: AnswerDraft = {
      diagnosticId,
      questionId,
      questionText,
      questionArea,
      answerText,
      timestamp: Date.now()
    };
    
    // Salvar local imediatamente
    saveDraft(draft);
    
    // Debounce para servidor
    if (saveTimeoutRef.current) {
      clearTimeout(saveTimeoutRef.current);
    }
    
    setSaveStatus('saving');
    
    saveTimeoutRef.current = setTimeout(() => {
      saveToServer(draft);
    }, SAVE_DEBOUNCE_MS);
  }, [diagnosticId, saveDraft, saveToServer]);
  
  /**
   * Processar fila quando voltar online.
   */
  useEffect(() => {
    const handleOnline = async () => {
      const draft = getDraft();
      if (draft && draft.answerText) {
        await saveToServer(draft);
      }
    };
    
    window.addEventListener('online', handleOnline);
    return () => window.removeEventListener('online', handleOnline);
  }, [getDraft, saveToServer]);
  
  /**
   * Cleanup do timeout ao desmontar.
   */
  useEffect(() => {
    return () => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
    };
  }, []);
  
  return { 
    save, 
    saveStatus, 
    getDraft, 
    clearDraft,
    saveToServer 
  };
}
