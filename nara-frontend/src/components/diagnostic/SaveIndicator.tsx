/**
 * Indicador visual de status de salvamento.
 * Conforme 06_OPERACOES_EMAIL.md - Seção 2
 */

import { Cloud, CloudOff, Check, Loader2, AlertCircle, Wifi, WifiOff } from 'lucide-react';
import type { SaveStatus } from '../../hooks/useAutoSave';
import { useEffect, useState } from 'react';

interface SaveIndicatorProps {
  status: SaveStatus;
  className?: string;
}

export function SaveIndicator({ status, className = '' }: SaveIndicatorProps) {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const config = {
    idle: {
      icon: null,
      text: '',
      textColor: ''
    },
    saving: {
      icon: <Loader2 className="h-4 w-4 animate-spin" />,
      text: 'Salvando...',
      textColor: 'text-blue-600 dark:text-blue-400'
    },
    saved: {
      icon: <Check className="h-4 w-4" />,
      text: 'Salvo',
      textColor: 'text-green-600 dark:text-green-400'
    },
    error: {
      icon: <AlertCircle className="h-4 w-4" />,
      text: isOnline ? 'Erro ao salvar' : 'Salvo localmente',
      textColor: isOnline ? 'text-red-600 dark:text-red-400' : 'text-yellow-600 dark:text-yellow-400'
    }
  };

  const { icon, text, textColor } = config[status];

  // Mostrar status de conexão quando offline
  if (!isOnline && status === 'idle') {
    return (
      <div className={`flex items-center gap-1.5 text-sm text-yellow-600 dark:text-yellow-400 ${className}`}>
        <WifiOff className="h-4 w-4" />
        <span>Offline</span>
      </div>
    );
  }

  if (status === 'idle') return null;

  return (
    <div className={`flex items-center gap-1.5 text-sm ${textColor} ${className} transition-all`}>
      {icon}
      <span>{text}</span>
      {!isOnline && status === 'error' && (
        <CloudOff className="h-3 w-3 ml-1 opacity-70" />
      )}
    </div>
  );
}
