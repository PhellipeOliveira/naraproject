-- NARA: Tabelas principais
-- Requer: 20260213000001_nara_extensions.sql

-- ==== areas (referência das 12 áreas) ====
CREATE TABLE public.areas (
    id SMALLINT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    color TEXT,
    display_order SMALLINT
);

INSERT INTO public.areas (id, name, description, icon, color, display_order) VALUES
(1, 'Saúde Física', 'Manutenção da constituição física e disposição corporal', '💪', '#22c55e', 1),
(2, 'Saúde Mental', 'Equilíbrio das funções cognitivas e gestão das emoções', '🧠', '#8b5cf6', 2),
(3, 'Saúde Espiritual', 'Força da fé e convicção interior', '✨', '#f59e0b', 3),
(4, 'Vida Pessoal', 'Autoconhecimento e descoberta da própria essência', '🪞', '#ec4899', 4),
(5, 'Vida Amorosa', 'Relacionamentos íntimos e dedicação entre parceiros', '❤️', '#ef4444', 5),
(6, 'Vida Familiar', 'Vínculos de parentesco e valores morais', '👨‍👩‍👧‍👦', '#06b6d4', 6),
(7, 'Vida Social', 'Interações comunitárias e prestígio social', '👥', '#3b82f6', 7),
(8, 'Vida Profissional', 'Atuação produtiva e desenvolvimento da carreira', '💼', '#6366f1', 8),
(9, 'Finanças', 'Gestão do capital econômico e recursos materiais', '💰', '#10b981', 9),
(10, 'Educação', 'Busca contínua por conhecimento e aperfeiçoamento', '📚', '#f97316', 10),
(11, 'Inovação', 'Criatividade e desenvolvimento de novas ideias', '💡', '#a855f7', 11),
(12, 'Lazer', 'Entretenimento, hobbies e recuperação de energia', '🎮', '#14b8a6', 12);

-- ==== profiles (extensão de auth.users) ====
CREATE TABLE public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    phone TEXT,
    accepted_terms BOOLEAN DEFAULT FALSE,
    accepted_privacy BOOLEAN DEFAULT FALSE,
    marketing_consent BOOLEAN DEFAULT FALSE,
    preferences JSONB DEFAULT '{"emailNotifications": true, "shareData": true, "language": "pt-BR"}'::JSONB,
    acquisition_channel TEXT DEFAULT 'organic',
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT,
    referrer_code TEXT,
    referred_by UUID REFERENCES public.profiles(id),
    total_diagnostics INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    CONSTRAINT profiles_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_profiles_email ON public.profiles(email);
CREATE INDEX idx_profiles_created_at ON public.profiles(created_at);
CREATE INDEX idx_profiles_referrer ON public.profiles(referrer_code);

-- ==== diagnostics ====
CREATE TABLE public.diagnostics (
    id UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    anonymous_session_id TEXT,
    email TEXT NOT NULL,
    full_name TEXT,
    status TEXT NOT NULL DEFAULT 'in_progress'
        CHECK (status IN ('in_progress', 'eligible', 'processing', 'completed', 'abandoned', 'failed')),
    current_phase INTEGER DEFAULT 1 CHECK (current_phase BETWEEN 1 AND 4),
    current_question INTEGER DEFAULT 0,
    total_answers INTEGER DEFAULT 0,
    total_words INTEGER DEFAULT 0,
    areas_covered SMALLINT[] DEFAULT ARRAY[]::SMALLINT[],
    result_token TEXT UNIQUE,
    consent_privacy BOOLEAN DEFAULT FALSE,
    consent_marketing BOOLEAN DEFAULT FALSE,
    overall_score DECIMAL(3,1),
    scores_by_area JSONB DEFAULT '{}',
    crisis_areas JSONB DEFAULT '[]',
    insights TEXT,
    radar_chart_url TEXT,
    pdf_url TEXT,
    ip_address INET,
    user_agent TEXT,
    referrer TEXT,
    utm_source TEXT,
    utm_campaign TEXT,
    device_info JSONB DEFAULT '{}',
    started_at TIMESTAMPTZ DEFAULT NOW(),
    last_activity_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_progress CHECK (total_answers >= 0 AND total_words >= 0 AND current_question >= 0),
    CONSTRAINT session_or_user CHECK (user_id IS NOT NULL OR anonymous_session_id IS NOT NULL OR email IS NOT NULL)
);

CREATE INDEX idx_diagnostics_user ON public.diagnostics(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_diagnostics_anonymous ON public.diagnostics(anonymous_session_id) WHERE anonymous_session_id IS NOT NULL;
CREATE INDEX idx_diagnostics_email ON public.diagnostics(email);
CREATE INDEX idx_diagnostics_status ON public.diagnostics(status);
CREATE INDEX idx_diagnostics_token ON public.diagnostics(result_token) WHERE result_token IS NOT NULL;
CREATE INDEX idx_diagnostics_created ON public.diagnostics(created_at);
CREATE INDEX idx_diagnostics_activity ON public.diagnostics(last_activity_at);

-- ==== answers ====
CREATE TABLE public.answers (
    id UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
    diagnostic_id UUID NOT NULL REFERENCES public.diagnostics(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_area TEXT NOT NULL,
    question_phase INTEGER NOT NULL,
    answer_value JSONB NOT NULL,
    word_count INTEGER DEFAULT 0,
    response_time_seconds INTEGER,
    sentiment_score DECIMAL(3,2),
    key_themes TEXT[],
    answered_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_answer_per_question UNIQUE (diagnostic_id, question_id)
);

CREATE INDEX idx_answers_diagnostic ON public.answers(diagnostic_id);
CREATE INDEX idx_answers_area ON public.answers(question_area);
CREATE INDEX idx_answers_phase ON public.answers(question_phase);
CREATE INDEX idx_answers_answered ON public.answers(answered_at);

CREATE OR REPLACE FUNCTION public.calculate_word_count()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.answer_value->>'text' IS NOT NULL AND trim(NEW.answer_value->>'text') != '' THEN
        NEW.word_count := array_length(regexp_split_to_array(trim(NEW.answer_value->>'text'), '\s+'), 1);
    ELSE
        NEW.word_count := 0;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calculate_answer_word_count
    BEFORE INSERT OR UPDATE ON public.answers
    FOR EACH ROW EXECUTE FUNCTION public.calculate_word_count();

-- ==== knowledge_chunks ====
CREATE TABLE public.knowledge_chunks (
    id UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
    chapter TEXT NOT NULL,
    section TEXT,
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}'::JSONB,
    motor_motivacional TEXT[],
    estagio_jornada TEXT[],
    tipo_crise TEXT[],
    ponto_entrada TEXT,
    sintomas TEXT[],
    tom_emocional TEXT,
    token_count INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_chunks_chapter ON public.knowledge_chunks(chapter);
CREATE INDEX idx_chunks_active ON public.knowledge_chunks(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_chunks_motor ON public.knowledge_chunks USING GIN (motor_motivacional);
CREATE INDEX idx_chunks_estagio ON public.knowledge_chunks USING GIN (estagio_jornada);
CREATE INDEX idx_chunks_crise ON public.knowledge_chunks USING GIN (tipo_crise);
CREATE INDEX idx_chunks_metadata ON public.knowledge_chunks USING GIN (metadata);
-- Índice vetorial ivfflat: criado em migração posterior após popular knowledge_chunks (ver 20260213000005)

-- ==== diagnostic_results ====
CREATE TABLE public.diagnostic_results (
    id UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
    diagnostic_id UUID UNIQUE NOT NULL REFERENCES public.diagnostics(id) ON DELETE CASCADE,
    overall_score DECIMAL(3,1),
    area_scores JSONB NOT NULL DEFAULT '{}',
    motor_scores JSONB NOT NULL DEFAULT '{}',
    phase_identified TEXT,
    motor_dominante TEXT,
    motor_secundario TEXT,
    crise_raiz TEXT,
    crises_derivadas TEXT[],
    ponto_entrada_ideal TEXT,
    dominios_alavanca TEXT[],
    executive_summary TEXT NOT NULL,
    detailed_analysis JSONB NOT NULL DEFAULT '{}',
    recommendations JSONB NOT NULL DEFAULT '[]',
    strengths TEXT[] DEFAULT '{}',
    opportunities TEXT[] DEFAULT '{}',
    model_used TEXT DEFAULT 'gpt-4o',
    tokens_used INTEGER,
    generation_time_ms INTEGER,
    generated_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_results_diagnostic ON public.diagnostic_results(diagnostic_id);
CREATE INDEX idx_results_generated ON public.diagnostic_results(generated_at);

-- ==== feedback ====
CREATE TABLE public.feedback (
    id UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
    diagnostic_id UUID REFERENCES public.diagnostics(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    nps_score INTEGER CHECK (nps_score BETWEEN 0 AND 10),
    feedback_text TEXT,
    feedback_type TEXT CHECK (feedback_type IN ('public', 'private')),
    accuracy_rating INTEGER CHECK (accuracy_rating BETWEEN 1 AND 5),
    relevance_rating INTEGER CHECK (relevance_rating BETWEEN 1 AND 5),
    clarity_rating INTEGER CHECK (clarity_rating BETWEEN 1 AND 5),
    tags TEXT[] DEFAULT '{}',
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_feedback_diagnostic ON public.feedback(diagnostic_id);
CREATE INDEX idx_feedback_nps ON public.feedback(nps_score);
CREATE INDEX idx_feedback_created ON public.feedback(created_at);

-- ==== waitlist ====
CREATE TABLE public.waitlist (
    id UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    diagnostic_id UUID REFERENCES public.diagnostics(id) ON DELETE SET NULL,
    source TEXT DEFAULT 'diagnostic',
    referrer TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'invited', 'converted')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    invited_at TIMESTAMPTZ,
    converted_at TIMESTAMPTZ,
    utm_source TEXT,
    CONSTRAINT waitlist_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_waitlist_email ON public.waitlist(email);
CREATE INDEX idx_waitlist_status ON public.waitlist(status);
CREATE INDEX idx_waitlist_created ON public.waitlist(created_at);

-- ==== email_logs ====
CREATE TABLE public.email_logs (
    id UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
    recipient_email TEXT NOT NULL,
    diagnostic_id UUID REFERENCES public.diagnostics(id) ON DELETE SET NULL,
    user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    email_type TEXT NOT NULL,
    subject TEXT NOT NULL,
    template_id TEXT,
    status TEXT DEFAULT 'queued'
        CHECK (status IN ('queued', 'sent', 'delivered', 'opened', 'clicked', 'bounced', 'failed')),
    provider TEXT DEFAULT 'resend',
    resend_id TEXT,
    sent_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    opened_at TIMESTAMPTZ,
    clicked_at TIMESTAMPTZ,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_email_logs_recipient ON public.email_logs(recipient_email);
CREATE INDEX idx_email_logs_diagnostic ON public.email_logs(diagnostic_id);
CREATE INDEX idx_email_logs_type ON public.email_logs(email_type);
CREATE INDEX idx_email_logs_status ON public.email_logs(status);
CREATE INDEX idx_email_logs_created ON public.email_logs(created_at);

-- ==== Trigger updated_at ====
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_diagnostics_updated_at
    BEFORE UPDATE ON public.diagnostics
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_knowledge_chunks_updated_at
    BEFORE UPDATE ON public.knowledge_chunks
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_email_logs_updated_at
    BEFORE UPDATE ON public.email_logs
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
