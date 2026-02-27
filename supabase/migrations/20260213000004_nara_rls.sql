-- NARA: Row Level Security
-- Requer: 20260213000002_nara_tables.sql

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.diagnostics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.diagnostic_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.email_logs ENABLE ROW LEVEL SECURITY;

-- profiles: usuário vê/atualiza só o próprio; insert permitido (trigger ou service)
CREATE POLICY "Users can view own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

CREATE POLICY "Service can insert profiles"
    ON public.profiles FOR INSERT
    WITH CHECK (true);

-- diagnostics: anon com session_id ou user autenticado
CREATE POLICY "Users can view own diagnostics"
    ON public.diagnostics FOR SELECT
    USING (
        auth.uid() = user_id
        OR (user_id IS NULL AND anonymous_session_id = current_setting('app.session_id', true))
    );

CREATE POLICY "Users can create diagnostics"
    ON public.diagnostics FOR INSERT
    WITH CHECK (
        auth.uid() = user_id
        OR (auth.uid() IS NULL AND anonymous_session_id IS NOT NULL)
    );

CREATE POLICY "Users can update own diagnostics"
    ON public.diagnostics FOR UPDATE
    USING (
        auth.uid() = user_id
        OR (user_id IS NULL AND anonymous_session_id = current_setting('app.session_id', true))
    );

-- Acesso público ao resultado via token (backend seta app.result_token)
CREATE POLICY "Public access via result token"
    ON public.diagnostics FOR SELECT
    USING (
        result_token IS NOT NULL
        AND result_token = current_setting('app.result_token', true)
    );

-- answers: por diagnóstico do usuário/sessão
CREATE POLICY "Users can view own answers"
    ON public.answers FOR SELECT
    USING (
        diagnostic_id IN (
            SELECT id FROM public.diagnostics
            WHERE user_id = auth.uid()
               OR (user_id IS NULL AND anonymous_session_id = current_setting('app.session_id', true))
        )
    );

CREATE POLICY "Users can create answers"
    ON public.answers FOR INSERT
    WITH CHECK (
        diagnostic_id IN (
            SELECT id FROM public.diagnostics
            WHERE user_id = auth.uid()
               OR (user_id IS NULL AND anonymous_session_id = current_setting('app.session_id', true))
        )
    );

-- diagnostic_results: leitura por diagnóstico do usuário ou por result_token (via diagnostics)
CREATE POLICY "Users can view own diagnostic results"
    ON public.diagnostic_results FOR SELECT
    USING (
        diagnostic_id IN (
            SELECT id FROM public.diagnostics
            WHERE user_id = auth.uid()
               OR (user_id IS NULL AND anonymous_session_id = current_setting('app.session_id', true))
               OR (result_token IS NOT NULL AND result_token = current_setting('app.result_token', true))
        )
    );

-- feedback: usuário pode inserir/ver próprio
CREATE POLICY "Users can view own feedback"
    ON public.feedback FOR SELECT
    USING (
        user_id = auth.uid()
        OR diagnostic_id IN (
            SELECT id FROM public.diagnostics
            WHERE user_id = auth.uid() OR (user_id IS NULL AND anonymous_session_id = current_setting('app.session_id', true))
        )
    );

CREATE POLICY "Users can create feedback"
    ON public.feedback FOR INSERT
    WITH CHECK (true);

-- email_logs: sem política para anon/authenticated (apenas service_role acessa)
-- Nenhuma policy adicional; service_role bypassa RLS.
