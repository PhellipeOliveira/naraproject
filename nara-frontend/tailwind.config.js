/** @type {import('tailwindcss').Config} */
import tailwindcssAnimate from 'tailwindcss-animate';

export default {
  darkMode: ['class'],
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        // Nova paleta NARA - Violeta vibrante
        primary: {
          DEFAULT: '#7C3AED',
          foreground: '#ffffff',
          50: '#F5F3FF',
          100: '#EDE9FE',
          200: '#DDD6FE',
          300: '#C4B5FD',
          400: '#A78BFA',
          500: '#7C3AED',
          600: '#6D28D9',
          700: '#5B21B6',
          800: '#4C1D95',
          900: '#3B0764',
          950: '#2E1065',
        },
        // Cores de acento
        accent: {
          DEFAULT: '#06B6D4',
          foreground: '#ffffff',
          warm: '#F59E0B',
          fresh: '#10B981',
          cyan: '#06B6D4',
        },
        secondary: {
          DEFAULT: '#F4F4F5',
          foreground: '#18181B',
        },
        destructive: {
          DEFAULT: '#EF4444',
          foreground: '#ffffff',
        },
        success: {
          DEFAULT: '#22C55E',
          foreground: '#ffffff',
        },
        warning: {
          DEFAULT: '#F59E0B',
          foreground: '#000000',
        },
        info: {
          DEFAULT: '#3B82F6',
          foreground: '#ffffff',
        },
        muted: {
          DEFAULT: '#F4F4F5',
          foreground: '#71717A',
        },
        // Cores das 12 áreas - harmônicas
        area: {
          1: '#22C55E',  // Saúde Física - Verde vida
          2: '#8B5CF6',  // Saúde Mental - Roxo mente
          3: '#F59E0B',  // Saúde Espiritual - Âmbar luz
          4: '#EC4899',  // Vida Pessoal - Rosa identidade
          5: '#EF4444',  // Vida Amorosa - Vermelho paixão
          6: '#06B6D4',  // Vida Familiar - Ciano conexão
          7: '#3B82F6',  // Vida Social - Azul comunidade
          8: '#7C3AED',  // Vida Profissional - Violeta propósito
          9: '#10B981',  // Finanças - Esmeralda prosperidade
          10: '#F97316', // Educação - Laranja conhecimento
          11: '#A855F7', // Inovação - Fúcsia criatividade
          12: '#14B8A6', // Lazer - Teal equilíbrio
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Plus Jakarta Sans', 'Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.875rem' }],
      },
      spacing: {
        18: '4.5rem',
        22: '5.5rem',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%)',
        'gradient-warm': 'linear-gradient(135deg, #F59E0B 0%, #EF4444 100%)',
        'gradient-fresh': 'linear-gradient(135deg, #10B981 0%, #06B6D4 100%)',
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
      boxShadow: {
        'glow': '0 0 20px rgba(124, 58, 237, 0.3)',
        'glow-lg': '0 0 40px rgba(124, 58, 237, 0.4)',
        'card': '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05)',
        'card-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.05)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'fade-out': 'fadeOut 0.3s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'slide-out-left': 'slideOutLeft 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-fast': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-subtle': 'pulseSubtle 2s infinite',
        'bounce-subtle': 'bounceSubtle 1s infinite',
        'spin-slow': 'spin 3s linear infinite',
        'shake': 'shake 0.5s ease-in-out',
        'celebration': 'celebration 0.5s ease-out',
        'progress-fill': 'progressFill 0.5s ease-out',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeOut: {
          '0%': { opacity: '1' },
          '100%': { opacity: '0' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        slideOutLeft: {
          '0%': { opacity: '1', transform: 'translateX(0)' },
          '100%': { opacity: '0', transform: 'translateX(-20px)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        bounceSubtle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' },
        },
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '10%, 30%, 50%, 70%, 90%': { transform: 'translateX(-5px)' },
          '20%, 40%, 60%, 80%': { transform: 'translateX(5px)' },
        },
        celebration: {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.05)' },
          '100%': { transform: 'scale(1)' },
        },
        pulseSubtle: {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(124, 58, 237, 0.4)' },
          '50%': { boxShadow: '0 0 0 8px rgba(124, 58, 237, 0)' },
        },
        progressFill: {
          from: { width: '0' },
          to: { width: 'var(--progress-width)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(124, 58, 237, 0.2)' },
          '100%': { boxShadow: '0 0 20px rgba(124, 58, 237, 0.4)' },
        },
      },
      transitionDuration: {
        400: '400ms',
      },
    },
  },
  plugins: [tailwindcssAnimate],
};
