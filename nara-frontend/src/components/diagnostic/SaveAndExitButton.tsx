/**
 * Botão para salvar progresso e sair do diagnóstico.
 * Envia email com link de retomada.
 */

import { useState } from 'react';
import { Button } from '../ui/button';
import { LogOut, Mail, Loader2, CheckCircle, X } from 'lucide-react';
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

      {/* Modal simples sem shadcn/ui Dialog */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6 relative">
            {/* Botão fechar */}
            <button
              onClick={() => setIsOpen(false)}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
            >
              <X className="h-5 w-5" />
            </button>

            {!emailSent ? (
              <>
                <div className="mb-4">
                  <h2 className="text-xl font-semibold flex items-center gap-2 text-gray-900 dark:text-white">
                    <LogOut className="h-5 w-5 text-primary" />
                    Salvar e Sair
                  </h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    Seu progresso será salvo automaticamente.
                  </p>
                </div>

                <div className="space-y-4 mb-6">
                  <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
                    <p className="text-sm text-blue-900 dark:text-blue-100">
                      <strong>Progresso atual:</strong> {totalAnswers} respostas salvas
                    </p>
                    <p className="text-sm text-blue-700 dark:text-blue-200 mt-1">
                      Você pode retomar de onde parou usando o email: <strong>{email}</strong>
                    </p>
                  </div>

                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Deseja receber um email com o link para continuar?
                  </p>
                </div>

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
          </div>
        </div>
      )}
    </>
  );
}
