/**
 * Botão para salvar progresso e sair do diagnóstico.
 * Envia email com link de retomada.
 */

import { useState } from 'react';
import { Button } from '../ui/button';
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogHeader, 
  DialogTitle 
} from '../ui/dialog';
import { LogOut, Mail, Loader2, CheckCircle } from 'lucide-react';
import { sendResumeLink } from '../../api/diagnostic';

interface SaveAndExitButtonProps {
  diagnosticId: string;
  email: string;
  totalAnswers: number;
  onExit?: () => void;
}

export function SaveAndExitButton({ 
  diagnosticId, 
  email, 
  totalAnswers,
  onExit 
}: SaveAndExitButtonProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);

  const handleSendEmail = async () => {
    setIsLoading(true);
    try {
      await sendResumeLink(diagnosticId);
      setEmailSent(true);
      
      // Aguardar 2 segundos e então redirecionar
      setTimeout(() => {
        if (onExit) {
          onExit();
        } else {
          window.location.href = '/';
        }
      }, 2000);
    } catch (error) {
      console.error('Erro ao enviar email:', error);
      alert('Erro ao enviar email. Mas seu progresso foi salvo!');
      // Mesmo com erro, permite sair
      if (onExit) {
        onExit();
      } else {
        window.location.href = '/';
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleExit = () => {
    // Sair sem enviar email
    if (onExit) {
      onExit();
    } else {
      window.location.href = '/';
    }
  };

  return (
    <>
      <Button
        variant="outline"
        onClick={() => setIsOpen(true)}
        className="gap-2"
      >
        <LogOut className="h-4 w-4" />
        Sair e Continuar Depois
      </Button>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="sm:max-w-md">
          {!emailSent ? (
            <>
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <LogOut className="h-5 w-5 text-primary" />
                  Salvar e Sair
                </DialogTitle>
                <DialogDescription>
                  Seu progresso será salvo automaticamente.
                </DialogDescription>
              </DialogHeader>

              <div className="py-4 space-y-4">
                <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
                  <p className="text-sm text-blue-900 dark:text-blue-100">
                    <strong>Progresso atual:</strong> {totalAnswers} respostas salvas
                  </p>
                  <p className="text-sm text-blue-700 dark:text-blue-200 mt-1">
                    Você pode retomar de onde parou usando o email: <strong>{email}</strong>
                  </p>
                </div>

                <div className="space-y-3">
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Deseja receber um email com o link para continuar?
                  </p>

                  <div className="flex gap-3">
                    <Button
                      variant="outline"
                      onClick={handleExit}
                      className="flex-1"
                      disabled={isLoading}
                    >
                      Não, só sair
                    </Button>
                    <Button
                      onClick={handleSendEmail}
                      className="flex-1 gap-2"
                      disabled={isLoading}
                    >
                      {isLoading ? (
                        <>
                          <Loader2 className="h-4 w-4 animate-spin" />
                          Enviando...
                        </>
                      ) : (
                        <>
                          <Mail className="h-4 w-4" />
                          Sim, enviar email
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="py-8 text-center space-y-4">
              <CheckCircle className="h-16 w-16 text-green-500 mx-auto" />
              <div>
                <h3 className="text-lg font-semibold text-green-800 dark:text-green-200">
                  Email Enviado!
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                  Verifique sua caixa de entrada em: <strong>{email}</strong>
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Redirecionando em 2 segundos...
                </p>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </>
  );
}
