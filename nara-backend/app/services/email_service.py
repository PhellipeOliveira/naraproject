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
        diagnostic_id = diagnostic_result.get("diagnostic_id")
        summary_snippet = (summary[:300] + "...") if len(summary) > 300 else summary

        html = self._template_diagnostic_email(
            user_name=name,
            summary=summary_snippet,
            overall_score=overall_score,
            view_url=view_url,
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
    ) -> str:
        """Template HTML responsivo para email de resultado do diagnóstico."""
        score_block = ""
        if overall_score is not None:
            score_block = f"""
                <div style="width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 24px auto; text-align: center;">
                    <span style="font-size: 42px; font-weight: bold;">{overall_score:.1f}</span>
                    <span style="font-size: 12px; opacity: 0.9;">Score Geral</span>
                </div>
            """
        cta_block = ""
        if view_url:
            cta_block = f'<a href="{view_url}" style="display: block; background: #6366f1; color: white; text-decoration: none; padding: 14px 28px; border-radius: 8px; text-align: center; font-weight: 600; margin: 24px 0;">Ver Diagnóstico Completo →</a>'
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f9fafb;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; padding: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h1 style="color: #6366f1; font-size: 24px; margin: 0 0 24px 0;">Olá, {user_name}! 👋</h1>
                <p style="color: #374151; line-height: 1.6;">Seu Diagnóstico de Transformação Narrativa está pronto!</p>
                {score_block}
                <div style="background: #f3f4f6; border-radius: 8px; padding: 16px; margin: 24px 0;">
                    <strong>Resumo:</strong>
                    <p style="margin: 8px 0 0 0; color: #4b5563;">{summary}</p>
                </div>
                {cta_block}
                <p style="color: #6b7280; font-size: 14px; text-align: center; margin-top: 32px;">© {settings.APP_NAME}. Todos os direitos reservados.</p>
            </div>
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
    ) -> dict:
        """Envia link para retomar diagnóstico."""
        html = self._render_template(
            "resume_link",
            user_name=user_name or "Viajante",
            progress=progress,
            resume_url=f"{settings.FRONTEND_URL}/diagnostico/{diagnostic_id}/retomar",
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
    ) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f9fafb;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; padding: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h1 style="color: #6366f1; font-size: 24px;">Olá, {user_name}! 👋</h1>
                <p style="color: #374151; line-height: 1.6;">Continue seu Diagnóstico. Nara vai surpreender você!</p>
                <div style="background: #f3f4f6; border-radius: 8px; padding: 16px; margin: 24px 0;">
                    <p style="margin: 0;"><strong>Progresso:</strong> {progress}%</p>
                </div>
                <a href="{resume_url}" style="display: block; background: #6366f1; color: white; text-decoration: none; padding: 14px 28px; border-radius: 8px; text-align: center; font-weight: 600; margin: 24px 0;">Continuar Diagnóstico →</a>
                <p style="color: #6b7280; font-size: 14px; text-align: center; margin-top: 32px;">© NARA.</p>
            </div>
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
