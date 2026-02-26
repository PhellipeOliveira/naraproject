/**
 * Indicador visual de status de salvamento.
 * Redesenhado para nova UI/UX NARA
 */

import { CloudOff, Check, Loader2, AlertCircle, WifiOff } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import type { SaveStatus } from '../../hooks/useAutoSave';
import { useEffect, useState } from 'react';
import { cn } from '../../lib/utils';

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
      bgColor: '',
      textColor: '',
      borderColor: '',
    },
    saving: {
      icon: <Loader2 className="h-4 w-4 animate-spin" />,
      text: 'Salvando...',
      bgColor: 'bg-primary/10',
      textColor: 'text-primary',
      borderColor: 'border-primary/20',
    },
    saved: {
      icon: <Check className="h-4 w-4" />,
      text: 'Salvo',
      bgColor: 'bg-success/10',
      textColor: 'text-success',
      borderColor: 'border-success/20',
    },
    error: {
      icon: <AlertCircle className="h-4 w-4" />,
      text: isOnline ? 'Erro ao salvar' : 'Salvo localmente',
      bgColor: isOnline ? 'bg-destructive/10' : 'bg-warning/10',
      textColor: isOnline ? 'text-destructive' : 'text-warning',
      borderColor: isOnline ? 'border-destructive/20' : 'border-warning/20',
    },
  };

  const { icon, text, bgColor, textColor, borderColor } = config[status];

  // Mostrar status de conexão quando offline
  if (!isOnline && status === 'idle') {
    return (
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 20 }}
        className={cn(
          'flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium',
          'bg-warning/10 text-warning border border-warning/20',
          className
        )}
      >
        <WifiOff className="h-4 w-4" />
        <span>Offline</span>
      </motion.div>
    );
  }

  return (
    <AnimatePresence mode="wait">
      {status !== 'idle' && (
        <motion.div
          key={status}
          initial={{ opacity: 0, x: 20, scale: 0.9 }}
          animate={{ opacity: 1, x: 0, scale: 1 }}
          exit={{ opacity: 0, x: 20, scale: 0.9 }}
          transition={{ duration: 0.2 }}
          className={cn(
            'flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium border',
            bgColor,
            textColor,
            borderColor,
            className
          )}
        >
          {icon}
          <span>{text}</span>
          {!isOnline && status === 'error' && (
            <CloudOff className="h-3 w-3 ml-1 opacity-70" />
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
