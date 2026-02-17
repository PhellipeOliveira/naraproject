/**
 * Modal para retomar ou reiniciar diagnóstico.
 * Conforme 06_OPERACOES_EMAIL.md - Seção 7
 */

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../ui/dialog';
import { Button } from '../ui/button';
import { formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Clock, RefreshCw, Play } from 'lucide-react';

interface ResumeModalProps {
  open: boolean;
  onClose: () => void;
  diagnostic: {
    diagnostic_id: string;
    total_answers: number;
    started_at: string;
  };
  onResume: () => void;
  onStartNew: () => void;
}

export function ResumeModal({ 
  open, 
  onClose, 
  diagnostic, 
  onResume, 
  onStartNew 
}: ResumeModalProps) {
  const ESTIMATED_TOTAL_QUESTIONS = 40;
  const progress = Math.round((diagnostic.total_answers / ESTIMATED_TOTAL_QUESTIONS) * 100);
  
  const startedAgo = formatDistanceToNow(new Date(diagnostic.started_at), {
    addSuffix: true,
    locale: ptBR
  });
  
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5 text-primary" />
            Diagnóstico em Andamento
          </DialogTitle>
          <DialogDescription>
            Encontramos um diagnóstico que você iniciou {startedAgo}.
          </DialogDescription>
        </DialogHeader>
        
        <div className="py-4 space-y-4">
          <div className="bg-gradient-to-br from-primary/10 to-primary/5 rounded-lg p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Progresso Atual
              </span>
              <span className="text-lg font-bold text-primary">
                {diagnostic.total_answers} respostas
              </span>
            </div>
            
            <div className="relative w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
              <div 
                className="absolute top-0 left-0 h-full bg-gradient-to-r from-primary to-primary-600 rounded-full transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
              <span className="absolute inset-0 flex items-center justify-center text-xs font-semibold text-white">
                {progress}%
              </span>
            </div>
          </div>
          
          <div className="text-sm text-gray-600 dark:text-gray-400 text-center">
            Suas respostas estão salvas. O que você gostaria de fazer?
          </div>
        </div>
        
        <div className="flex gap-3">
          <Button 
            variant="outline" 
            onClick={onStartNew} 
            className="flex-1 gap-2"
          >
            <RefreshCw className="h-4 w-4" />
            Começar Novo
          </Button>
          <Button 
            onClick={onResume} 
            className="flex-1 gap-2"
          >
            <Play className="h-4 w-4" />
            Continuar
          </Button>
        </div>
        
        <p className="text-xs text-center text-gray-500 dark:text-gray-400">
          Se começar um novo, o diagnóstico anterior será arquivado.
        </p>
      </DialogContent>
    </Dialog>
  );
}
