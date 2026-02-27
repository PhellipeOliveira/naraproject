"""Serviço de envio de emails transacionais via Resend API."""
import asyncio
import logging
from typing import Any, Dict, Optional

import resend
from email_validator import EmailNotValidError, validate_email

from app.config import settings
from app.database import supabase

logger = logging.getLogger(__name__)

# Retry
RESEND_MAX_RETRIES = 3
RESEND_RETRY_DELAY_SECONDS = 2
PHASE_NAMES = {
    1: "Diagnóstico Base",
    2: "Aprofundamento",
    3: "Integração",
    4: "Síntese Final",
}


def _validate_email_address(email: str) -> str:
    """
    Valida formato do email e retorna o endereço normalizado.
    Raises ValueError se inválido.
    """
    try:
        validated = validate_email(email, check_deliverability=False)
        return validated.normalized
    except EmailNotValidError as e:
        raise ValueError(f"Email inválido: {email}") from e


class EmailService:
    """
    Serviço de envio de emails via Resend (resend-python).
    From: diagnostic.nara@phellipeoliveira.org
    Reply-to: contato@phellipeoliveira.org
    """

    FROM_EMAIL: str = settings.EMAIL_FROM
    FROM_NAME: str = "Nara - Diagnóstico"
    REPLY_TO: str = settings.RESEND_REPLY_TO

    def _ensure_api_key(self) -> None:
        """Verifica se RESEND_API_KEY está configurada. Raises ValueError se não."""
        if not (settings.RESEND_API_KEY or "").strip():
            raise ValueError("RESEND_API_KEY não está configurada. Configure a variável de ambiente.")

    async def send_email(
        self,
        to: str,
        subject: str,
        html: str,
        email_type: str,
        diagnostic_id: Optional[str] = None,
        user_id: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> dict:
        """
        Envia um email via Resend com retry (3 tentativas) e registra no log.

        Returns:
            dict: {"status": "sent", "resend_id": "..."} ou
                  {"status": "failed", "error": "..."}
        """
        self._ensure_api_key()
        try:
            to_normalized = _validate_email_address(to)
        except ValueError as e:
            logger.warning("Validação de email falhou: %s", e)
            await self._log_email(
                recipient_email=to,
                diagnostic_id=diagnostic_id,
                user_id=user_id,
                email_type=email_type,
                subject=subject,
                status="failed",
                error_message=str(e),
            )
            return {"status": "failed", "error": str(e)}

        last_error: Optional[Exception] = None
        payload: Dict[str, Any] = {
            "from": f"{self.FROM_NAME} <{self.FROM_EMAIL}>",
            "to": [to_normalized],
            "subject": subject,
            "html": html,
        }
        if reply_to or self.REPLY_TO:
            payload["reply_to"] = reply_to or self.REPLY_TO

        for attempt in range(1, RESEND_MAX_RETRIES + 1):
            try:
                resend.api_key = settings.RESEND_API_KEY
                response = await asyncio.to_thread(
                    resend.Emails.send,
                    payload,
                )
                resend_id = response.get("id")
                logger.info(
                    "Email enviado com sucesso: type=%s to=%s attempt=%d resend_id=%s",
                    email_type,
                    to_normalized,
                    attempt,
                    resend_id,
                )
                await self._log_email(
                    recipient_email=to_normalized,
                    diagnostic_id=diagnostic_id,
                    user_id=user_id,
                    email_type=email_type,
                    subject=subject,
                    status="sent",
                    resend_id=resend_id,
                )
                return {"status": "sent", "resend_id": resend_id}
            except Exception as e:
                last_error = e
                logger.warning(
                    "Tentativa %d/%d de envio de email falhou: type=%s to=%s error=%s",
                    attempt,
                    RESEND_MAX_RETRIES,
                    email_type,
                    to_normalized,
                    e,
                )
                if attempt < RESEND_MAX_RETRIES:
                    await asyncio.sleep(RESEND_RETRY_DELAY_SECONDS)

        logger.error(
            "Falha definitiva após %d tentativas: type=%s to=%s error=%s",
            RESEND_MAX_RETRIES,
            email_type,
            to_normalized,
            last_error,
        )
        error_msg = str(last_error) if last_error else "unknown"
        await self._log_email(
            recipient_email=to_normalized,
            diagnostic_id=diagnostic_id,
            user_id=user_id,
            email_type=email_type,
            subject=subject,
            status="failed",
            error_message=error_msg,
        )
        return {"status": "failed", "error": error_msg}

    async def send_diagnostic_email(
        self,
        user_email: str,
        user_name: Optional[str],
        diagnostic_result: Dict[str, Any],
    ) -> dict:
        """
        Envia email formatado com o resultado do diagnóstico.

        Parâmetros:
            user_email: Email do destinatário (validado antes do envio).
            user_name: Nome do usuário (opcional).
            diagnostic_result: Dict com 'summary'; opcionalmente
                'overall_score' (float), 'view_url' (str), 'diagnostic_id' (str).

        Returns:
            dict: {"status": "sent", "resend_id": "..."} ou
                  {"status": "failed", "error": "..."}
        """
        self._ensure_api_key()
        try:
            _validate_email_address(user_email)
        except ValueError as e:
            logger.warning("Validação de email em send_diagnostic_email: %s", e)
            return {"status": "failed", "error": str(e)}

        name = user_name or "Viajante"
        summary = diagnostic_result.get("summary") or ""
        overall_score = diagnostic_result.get("overall_score")
        view_url = diagnostic_result.get("view_url") or ""
        dashboard_url = diagnostic_result.get("dashboard_url") or ""
        start_url = diagnostic_result.get("start_url") or ""
        diagnostic_id = diagnostic_result.get("diagnostic_id")
        summary_snippet = (summary[:300] + "...") if len(summary) > 300 else summary

        html = self._template_diagnostic_email(
            user_name=name,
            summary=summary_snippet,
            overall_score=overall_score,
            view_url=view_url,
            dashboard_url=dashboard_url,
            start_url=start_url,
        )
        return await self.send_email(
            to=user_email,
            subject="🎯 Seu Diagnóstico NARA está pronto!",
            html=html,
            email_type="diagnostic_result",
            diagnostic_id=diagnostic_id,
        )

    def _template_diagnostic_email(
        self,
        user_name: str,
        summary: str,
        overall_score: Optional[float] = None,
        view_url: str = "",
        dashboard_url: str = "",
        start_url: str = "",
    ) -> str:
        """Template HTML responsivo para email de resultado do diagnóstico."""
        primary = "#7C3AED"
        primary_light = "#A78BFA"
        primary_dark = "#6D28D9"
        accent_cyan = "#06B6D4"
        accent_emerald = "#10B981"
        neutral_50 = "#F9FAFB"
        neutral_200 = "#E5E7EB"
        neutral_500 = "#6B7280"
        neutral_900 = "#1F2937"
        gradient = f"linear-gradient(135deg, {primary} 0%, {accent_cyan} 100%)"

        score_block = ""
        if overall_score is not None:
            score_block = f"""
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 20px 0 0 0;">
                    <tr>
                        <td align="center">
                            <div style="width: 120px; height: 120px; border-radius: 999px; background: {primary}; background: {gradient}; color: #ffffff; display: inline-flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; box-shadow: 0 8px 18px rgba(124, 58, 237, 0.25);">
                                <span style="font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 42px; line-height: 1; font-weight: 700;">{overall_score:.1f}</span>
                                <span style="font-size: 12px; opacity: 0.95; margin-top: 6px;">Score Geral</span>
                            </div>
                        </td>
                    </tr>
                </table>
            """

        dashboard_button = ""
        if dashboard_url:
            dashboard_button = f"""
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 0;">
                    <tr>
                        <td align="center">
                            <a href="{dashboard_url}" style="display: block; background: {primary}; background: {gradient}; color: #ffffff; text-decoration: none; padding: 15px 24px; border-radius: 10px; text-align: center; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; font-size: 15px; box-shadow: 0 8px 18px rgba(124, 58, 237, 0.20);">
                                Acessar o dashboard →
                            </a>
                        </td>
                    </tr>
                </table>
            """

        result_button = ""
        if view_url:
            result_button = f"""
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top: 12px;">
                    <tr>
                        <td align="center">
                            <a href="{view_url}" style="display: block; background: transparent; color: {primary}; text-decoration: none; padding: 13px 24px; border-radius: 10px; text-align: center; border: 2px solid {primary}; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; font-size: 15px;">
                                Ver resultado
                            </a>
                        </td>
                    </tr>
                </table>
            """

        invite_block = ""
        if start_url:
            invite_block = f"""
                <tr>
                    <td style="padding: 24px 32px 0 32px;">
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-top: 1px solid {neutral_200};">
                            <tr>
                                <td style="padding-top: 24px; text-align: center;">
                                    <p style="margin: 0 0 8px 0; color: {neutral_500}; font-size: 14px; line-height: 1.6;">👥 Conhece alguém que também pode se beneficiar?</p>
                                    <a href="{start_url}" style="color: {primary}; font-size: 15px; font-weight: 700; text-decoration: underline; text-underline-offset: 2px;">
                                        Convidar alguém a fazer o diagnóstico
                                    </a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            """

        return f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
            <title>Diagnóstico NARA concluído</title>
        </head>
        <body style="margin: 0; padding: 20px; background-color: {neutral_50}; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 14px; border: 1px solid {neutral_200}; box-shadow: 0 2px 8px rgba(31, 41, 55, 0.06);">
                <tr>
                    <td style="padding: 32px 32px 12px 32px;">
                        <h1 style="margin: 0; color: {primary}; font-size: 28px; line-height: 1.25; font-weight: 700; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                            Olá, {user_name}! 👋
                        </h1>
                        <p style="margin: 10px 0 0 0; color: {neutral_500}; font-size: 15px; line-height: 1.6;">
                            Seu Diagnóstico de Transformação Narrativa está pronto.
                        </p>
                    </td>
                </tr>

                <tr>
                    <td style="padding: 12px 32px 0 32px;">
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background: #F3F0FF; border: 1px solid #DDD6FE; border-radius: 12px; box-shadow: 0 8px 18px rgba(124, 58, 237, 0.08);">
                            <tr>
                                <td align="center" style="padding: 32px;">
                                    <p style="margin: 0; font-size: 34px; line-height: 1;">🎉</p>
                                    <h2 style="margin: 12px 0 8px 0; color: {primary_dark}; font-size: 24px; line-height: 1.3; font-weight: 700; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                                        Parabéns! Seu diagnóstico está completo!
                                    </h2>
                                    <p style="margin: 0; color: {neutral_500}; font-size: 14px; line-height: 1.7;">
                                        Agora você tem insights poderosos sobre sua jornada de transformação.
                                    </p>
                                    <span style="display: inline-block; margin-top: 14px; background: {accent_emerald}; color: #ffffff; font-size: 12px; line-height: 1; font-weight: 700; padding: 8px 12px; border-radius: 999px;">
                                        ✓ Diagnóstico Completo
                                    </span>
                                    {score_block}
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>

                <tr>
                    <td style="padding: 18px 32px 0 32px;">
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background: #F3F0FF; border: 1px solid #DDD6FE; border-radius: 12px;">
                            <tr>
                                <td style="padding: 24px;">
                                    <h3 style="margin: 0 0 8px 0; color: {primary_dark}; font-size: 20px; line-height: 1.3; font-weight: 700; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                                        Pronto para descobrir seus resultados?
                                    </h3>
                                    <p style="margin: 0 0 18px 0; color: {neutral_500}; font-size: 14px; line-height: 1.6;">
                                        Explore insights detalhados e recomendações personalizadas.
                                    </p>
                                    {dashboard_button}
                                    {result_button}
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>

                <tr>
                    <td style="padding: 18px 32px 0 32px;">
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background: {neutral_50}; border: 1px solid {neutral_200}; border-radius: 12px;">
                            <tr>
                                <td style="padding: 20px;">
                                    <h3 style="margin: 0 0 8px 0; color: {neutral_900}; font-size: 18px; line-height: 1.3; font-weight: 700; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                                        📊 Resumo
                                    </h3>
                                    <p style="margin: 0; color: {neutral_500}; font-size: 14px; line-height: 1.7;">
                                        {summary}
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>

                <tr>
                    <td style="padding: 18px 32px 0 32px;">
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background: #ffffff; border: 1px solid {neutral_200}; border-radius: 12px;">
                            <tr>
                                <td style="padding: 20px;">
                                    <h3 style="margin: 0 0 12px 0; color: {neutral_900}; font-size: 18px; line-height: 1.3; font-weight: 700; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                                        Próximos passos
                                    </h3>
                                    <p style="margin: 0 0 8px 0; color: {neutral_500}; font-size: 14px; line-height: 1.7;">
                                        <span style="color: {primary}; font-weight: 700;">📊</span> Analise seus resultados detalhados
                                    </p>
                                    <p style="margin: 0 0 8px 0; color: {neutral_500}; font-size: 14px; line-height: 1.7;">
                                        <span style="color: {primary}; font-weight: 700;">💡</span> Receba recomendações personalizadas
                                    </p>
                                    <p style="margin: 0; color: {neutral_500}; font-size: 14px; line-height: 1.7;">
                                        <span style="color: {primary}; font-weight: 700;">📈</span> Acompanhe sua evolução
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>

                {invite_block}

                <tr>
                    <td style="padding: 28px 32px 32px 32px; text-align: center;">
                        <p style="margin: 0; color: {neutral_500}; font-size: 13px; line-height: 1.6;">
                            © {settings.APP_NAME}. Todos os direitos reservados.
                        </p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    async def _log_email(
        self,
        recipient_email: str,
        email_type: str,
        subject: str,
        status: str,
        diagnostic_id: Optional[str] = None,
        user_id: Optional[str] = None,
        resend_id: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> None:
        """Registra envio na tabela email_logs."""
        await asyncio.to_thread(
            lambda: supabase.table("email_logs").insert(
                {
                    "recipient_email": recipient_email,
                    "diagnostic_id": diagnostic_id,
                    "user_id": user_id,
                    "email_type": email_type,
                    "subject": subject,
                    "status": status,
                    "resend_id": resend_id,
                    "error_message": error_message,
                }
            ).execute()
        )

    async def send_diagnostic_result(
        self,
        to: str,
        user_name: Optional[str],
        diagnostic_id: str,
        result_token: str,
        overall_score: float,
        summary: str,
    ) -> dict:
        """Envia email com resultado do diagnóstico (compatível com fluxo existente)."""
        diagnostic_result = {
            "diagnostic_id": diagnostic_id,
            "overall_score": overall_score,
            "summary": summary,
            "view_url": f"{settings.FRONTEND_URL}/resultado/{result_token}",
            "dashboard_url": f"{settings.FRONTEND_URL}/meu-diagnostico/{result_token}",
            "start_url": f"{settings.FRONTEND_URL}/diagnostico/iniciar?compartilhar=1",
        }
        return await self.send_diagnostic_email(
            user_email=to,
            user_name=user_name,
            diagnostic_result=diagnostic_result,
        )

    async def send_resume_link(
        self,
        to: str,
        user_name: Optional[str],
        diagnostic_id: str,
        progress: int,
        phase: Optional[int] = None,
        total_answers: Optional[int] = None,
        areas_covered: Optional[int] = None,
        can_finish: bool = False,
    ) -> dict:
        """Envia link para retomar diagnóstico."""
        html = self._render_template(
            "resume_link",
            user_name=user_name or "Viajante",
            progress=progress,
            phase=phase,
            total_answers=total_answers,
            areas_covered=areas_covered,
            can_finish=can_finish,
            resume_url=f"{settings.FRONTEND_URL}/diagnostico/{diagnostic_id}/retomar",
            start_url=f"{settings.FRONTEND_URL}/diagnostico/iniciar?compartilhar=1",
        )
        return await self.send_email(
            to=to,
            subject="📝 Continue seu Diagnóstico NARA",
            html=html,
            email_type="resume_link",
            diagnostic_id=diagnostic_id,
        )

    async def send_waitlist_welcome(
        self,
        to: str,
        user_name: Optional[str] = None,
    ) -> dict:
        """Envia email de boas-vindas à lista de espera."""
        html = self._render_template(
            "waitlist_welcome",
            user_name=user_name or "Viajante",
        )
        return await self.send_email(
            to=to,
            subject="🚀 Você está na lista de espera da NARA!",
            html=html,
            email_type="waitlist_welcome",
        )

    def _render_template(self, template_name: str, **kwargs: object) -> str:
        """Renderiza template de email por nome."""
        templates = {
            "resume_link": self._template_resume_link,
            "waitlist_welcome": self._template_waitlist_welcome,
        }
        fn = templates.get(template_name)
        if not fn:
            raise ValueError(f"Template não encontrado: {template_name}")
        return fn(**kwargs)

    def _template_resume_link(
        self,
        user_name: str,
        progress: int,
        resume_url: str,
        phase: Optional[int] = None,
        total_answers: Optional[int] = None,
        areas_covered: Optional[int] = None,
        can_finish: bool = False,
        start_url: str = "",
    ) -> str:
        primary = "#7C3AED"
        primary_dark = "#6D28D9"
        accent_cyan = "#06B6D4"
        accent_amber = "#F59E0B"
        accent_emerald = "#10B981"
        neutral_50 = "#F9FAFB"
        neutral_200 = "#E5E7EB"
        neutral_500 = "#6B7280"
        neutral_900 = "#1F2937"
        gradient = f"linear-gradient(135deg, {primary} 0%, {accent_cyan} 100%)"

        phase_name = PHASE_NAMES.get(phase or 1, "Diagnóstico Base")
        answered = max(0, int(total_answers or 0))
        covered = max(0, int(areas_covered or 0))
        remaining_questions = max(0, 40 - answered)
        progress_value = max(0, min(100, int(progress or 0)))
        progress_remaining = 100 - progress_value
        finish_line = (
            "✓ Você já atingiu os critérios mínimos para finalizar"
            if can_finish
            else f"→ Faltam ~{remaining_questions} perguntas para poder finalizar"
        )

        finish_icon = "✅" if can_finish else "⏳"
        finish_color = accent_emerald if can_finish else accent_amber
        invite_block = ""
        if start_url:
            invite_block = f"""
                <tr>
                    <td style="padding: 24px 32px 0 32px;">
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-top: 1px solid {neutral_200};">
                            <tr>
                                <td style="padding-top: 24px; text-align: center;">
                                    <p style="margin: 0 0 8px 0; color: {neutral_500}; font-size: 14px; line-height: 1.6;">
                                        👥 Conhece alguém que também pode se beneficiar?
                                    </p>
                                    <a href="{start_url}" style="color: {primary}; font-size: 15px; font-weight: 700; text-decoration: underline; text-underline-offset: 2px;">
                                        Convidar alguém a fazer o diagnóstico
                                    </a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            """

        return f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
            <title>Continue seu Diagnóstico NARA</title>
        </head>
        <body style="margin: 0; padding: 20px; background-color: {neutral_50}; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 14px; border: 1px solid {neutral_200}; box-shadow: 0 2px 8px rgba(31, 41, 55, 0.06);">
                <tr>
                    <td style="padding: 32px 32px 12px 32px;">
                        <h1 style="margin: 0; color: {primary}; font-size: 28px; line-height: 1.25; font-weight: 700; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                            Olá, {user_name}! 👋
                        </h1>
                        <p style="margin: 10px 0 0 0; color: {neutral_500}; font-size: 15px; line-height: 1.6;">
                            Continue seu Diagnóstico. Nara vai surpreender você!
                        </p>
                    </td>
                </tr>

                <tr>
                    <td style="padding: 12px 32px 0 32px;">
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background: {neutral_50}; border: 1px solid {primary}; border-radius: 12px;">
                            <tr>
                                <td style="padding: 24px;">
                                    <p style="margin: 0 0 8px 0; color: {neutral_900}; font-size: 16px; font-weight: 700; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                                        🎯 Seu progresso
                                    </p>
                                    <p style="margin: 0; color: {primary}; font-size: 34px; line-height: 1.1; font-weight: 700; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                                        {progress_value}%
                                    </p>

                                    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 12px 0 14px 0;">
                                        <tr>
                                            <td width="{progress_value}%" style="height: 10px; border-radius: 999px 0 0 999px; background: {primary}; background: {gradient};"></td>
                                            <td width="{progress_remaining}%" style="height: 10px; border-radius: 0 999px 999px 0; background: {neutral_200};"></td>
                                        </tr>
                                    </table>

                                    <span style="display: inline-block; margin-bottom: 12px; background: #F3F0FF; color: {primary_dark}; font-size: 12px; line-height: 1; font-weight: 700; padding: 8px 12px; border-radius: 999px;">
                                        Fase {phase or 1} — {phase_name}
                                    </span>

                                    <p style="margin: 0 0 8px 0; color: {neutral_500}; font-size: 14px; line-height: 1.7;">
                                        <span style="color: {accent_emerald}; font-weight: 700;">✅</span>
                                        <strong>{answered}</strong> perguntas respondidas de <strong>40</strong> necessárias
                                    </p>
                                    <p style="margin: 0 0 8px 0; color: {neutral_500}; font-size: 14px; line-height: 1.7;">
                                        <span style="color: {accent_cyan}; font-weight: 700;">📋</span>
                                        <strong>{covered}</strong> de <strong>12</strong> áreas cobertas
                                    </p>
                                    <p style="margin: 0; color: {neutral_500}; font-size: 14px; line-height: 1.7;">
                                        <span style="color: {finish_color}; font-weight: 700;">{finish_icon}</span>
                                        {finish_line}
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>

                <tr>
                    <td style="padding: 18px 32px 0 32px;">
                        <p style="margin: 0 0 12px 0; color: {neutral_500}; font-size: 14px; line-height: 1.6; text-align: center;">
                            💪 Você está quase lá! Continue de onde parou.
                        </p>
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                            <tr>
                                <td align="center">
                                    <a href="{resume_url}" style="display: block; background: {primary}; background: {gradient}; color: #ffffff; text-decoration: none; padding: 15px 24px; border-radius: 10px; text-align: center; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; font-size: 15px; box-shadow: 0 8px 18px rgba(124, 58, 237, 0.20);">
                                        Continuar Diagnóstico →
                                    </a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>

                {invite_block}

                <tr>
                    <td style="padding: 28px 32px 32px 32px; text-align: center;">
                        <p style="margin: 0; color: {neutral_500}; font-size: 13px; line-height: 1.6;">
                            © {settings.APP_NAME}. Todos os direitos reservados.
                        </p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    def _template_waitlist_welcome(self, user_name: str) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f9fafb;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; padding: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h1 style="color: #6366f1; font-size: 24px;">🎉 Você está na lista!</h1>
                <p style="color: #374151; line-height: 1.6;">Olá, {user_name}! Você agora faz parte da lista de espera da NARA.</p>
                <p style="color: #6b7280; font-size: 14px; text-align: center; margin-top: 32px;">© NARA.</p>
            </div>
        </body>
        </html>
        """


email_service = EmailService()
