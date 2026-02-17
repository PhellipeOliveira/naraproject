/**
 * Componentes com animações e transições suaves
 * para melhorar a experiência visual do resultado
 */

import { ReactNode, useEffect, useState } from "react";

interface FadeInProps {
  children: ReactNode;
  delay?: number;
  className?: string;
}

/**
 * Fade In com delay configurável
 */
export function FadeIn({ children, delay = 0, className = "" }: FadeInProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);

  return (
    <div
      className={`transition-all duration-700 ${
        isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
      } ${className}`}
    >
      {children}
    </div>
  );
}

interface SlideInProps {
  children: ReactNode;
  delay?: number;
  direction?: "left" | "right" | "up" | "down";
  className?: string;
}

/**
 * Slide In de qualquer direção
 */
export function SlideIn({ 
  children, 
  delay = 0, 
  direction = "up", 
  className = "" 
}: SlideInProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);

  const transforms = {
    left: "translate-x-8",
    right: "-translate-x-8",
    up: "translate-y-8",
    down: "-translate-y-8",
  };

  return (
    <div
      className={`transition-all duration-700 ease-out ${
        isVisible ? "opacity-100 translate-x-0 translate-y-0" : `opacity-0 ${transforms[direction]}`
      } ${className}`}
    >
      {children}
    </div>
  );
}

interface ScaleInProps {
  children: ReactNode;
  delay?: number;
  className?: string;
}

/**
 * Scale In (útil para cards importantes)
 */
export function ScaleIn({ children, delay = 0, className = "" }: ScaleInProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);

  return (
    <div
      className={`transition-all duration-500 ${
        isVisible ? "opacity-100 scale-100" : "opacity-0 scale-95"
      } ${className}`}
    >
      {children}
    </div>
  );
}

interface StaggerChildrenProps {
  children: ReactNode[];
  staggerDelay?: number;
  initialDelay?: number;
  className?: string;
}

/**
 * Anima children em sequência (stagger effect)
 */
export function StaggerChildren({ 
  children, 
  staggerDelay = 100, 
  initialDelay = 0,
  className = "" 
}: StaggerChildrenProps) {
  return (
    <div className={className}>
      {children.map((child, index) => (
        <FadeIn key={index} delay={initialDelay + index * staggerDelay}>
          {child}
        </FadeIn>
      ))}
    </div>
  );
}

interface PulseProps {
  children: ReactNode;
  intensity?: "low" | "medium" | "high";
  className?: string;
}

/**
 * Pulse animation (útil para destacar elementos importantes)
 */
export function Pulse({ children, intensity = "medium", className = "" }: PulseProps) {
  const animations = {
    low: "animate-pulse-slow",
    medium: "animate-pulse",
    high: "animate-pulse-fast",
  };

  return (
    <div className={`${animations[intensity]} ${className}`}>
      {children}
    </div>
  );
}

interface ProgressBarAnimatedProps {
  value: number;  // 0-100
  delay?: number;
  duration?: number;
  className?: string;
  color?: string;
}

/**
 * Progress bar com animação suave
 */
export function ProgressBarAnimated({ 
  value, 
  delay = 0, 
  duration = 1000,
  className = "",
  color = "bg-primary" 
}: ProgressBarAnimatedProps) {
  const [currentValue, setCurrentValue] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setCurrentValue(value);
    }, delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return (
    <div className={`h-2 bg-muted rounded-full overflow-hidden ${className}`}>
      <div 
        className={`h-full ${color} transition-all ease-out`}
        style={{ 
          width: `${currentValue}%`,
          transitionDuration: `${duration}ms`
        }}
      />
    </div>
  );
}

interface CountUpProps {
  value: number;
  duration?: number;
  suffix?: string;
  className?: string;
}

/**
 * Count up animation para números
 */
export function CountUp({ value, duration = 2000, suffix = "", className = "" }: CountUpProps) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTime: number;
    let animationFrame: number;

    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime;
      const progress = Math.min((currentTime - startTime) / duration, 1);
      
      setCount(Math.floor(progress * value));

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, [value, duration]);

  return (
    <span className={className}>
      {count}{suffix}
    </span>
  );
}

/**
 * Shake animation (para erros ou validações)
 */
export function Shake({ children, trigger, className = "" }: { 
  children: ReactNode; 
  trigger: boolean; 
  className?: string;
}) {
  return (
    <div className={`${trigger ? "animate-shake" : ""} ${className}`}>
      {children}
    </div>
  );
}
