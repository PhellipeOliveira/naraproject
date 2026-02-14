"""Serviço de envio de emails via Resend."""
import asyncio
import logging
from typing import Optional

import resend

from app.config import settings
from app.database import supabase

logger = logging.getLogger(__name__)
resend.api_key = settings.RESEND_API_KEY


class EmailService:
    """Serviço de envio de emails via Resend."""

    FROM_EMAIL = settings.EMAIL_FROM
    FROM_NAME = "NARA Diagnóstico"

    async def send_email(
        self,
        to: str,
        subject: str,
        html: str,
        email_type: str,
        diagnostic_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> dict:
        """Envia um email e registra no log."""
        try:
            response = await asyncio.to_thread(
                resend.Emails.send,
                {
                    "from": f"{self.FROM_NAME} <{self.FROM_EMAIL}>",
                    "to": [to],
                    "subject": subject,
                    "html": html,
                },
            )
            resend_id = response.get("id")
            await self._log_email(
                recipient_email=to,
                diagnostic_id=diagnostic_id,
                user_id=user_id,
                email_type=email_type,
                subject=subject,
                status="sent",
                resend_id=resend_id,
            )
            logger.info("Email sent: %s to %s", email_type, to)
            return {"status": "sent", "resend_id": resend_id}
        except Exception as e:
            logger.exception("Error sending email: %s", e)
            await self._log_email(
                recipient_email=to,
                diagnostic_id=diagnostic_id,
                user_id=user_id,
                email_type=email_type,
                subject=subject,
                status="failed",
                error_message=str(e),
            )
            raise

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
        """Registra email na tabela de logs."""
        await asyncio.to_thread(
            lambda: supabase.table("email_logs").insert({
                "recipient_email": recipient_email,
                "diagnostic_id": diagnostic_id,
                "user_id": user_id,
                "email_type": email_type,
                "subject": subject,
                "status": status,
                "resend_id": resend_id,
                "error_message": error_message,
            }).execute()
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
        """Envia email com resultado do diagnóstico."""
        html = self._render_template(
            "diagnostic_result",
            user_name=user_name or "Viajante",
            overall_score=overall_score,
            summary=summary,
            view_url=f"{settings.FRONTEND_URL}/resultado/{result_token}",
        )
        return await self.send_email(
            to=to,
            subject="🎯 Seu Diagnóstico NARA está pronto!",
            html=html,
            email_type="diagnostic_result",
            diagnostic_id=diagnostic_id,
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
        """Renderiza template de email."""
        templates = {
            "diagnostic_result": self._template_diagnostic_result,
            "resume_link": self._template_resume_link,
            "waitlist_welcome": self._template_waitlist_welcome,
        }
        fn = templates.get(template_name)
        if not fn:
            raise ValueError(f"Template não encontrado: {template_name}")
        return fn(**kwargs)

    def _template_diagnostic_result(
        self,
        user_name: str,
        overall_score: float,
        summary: str,
        view_url: str,
    ) -> str:
        summary_snippet = (summary[:300] + "...") if len(summary) > 300 else summary
        return f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f9fafb;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; padding: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h1 style="color: #6366f1; font-size: 24px; margin: 0 0 24px 0;">Olá, {user_name}! 👋</h1>
                <p style="color: #374151; line-height: 1.6;">Seu Diagnóstico de Transformação Narrativa está pronto!</p>
                <div style="width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 24px auto; text-align: center;">
                    <span style="font-size: 42px; font-weight: bold;">{overall_score:.1f}</span>
                    <span style="font-size: 12px; opacity: 0.9;">Score Geral</span>
                </div>
                <div style="background: #f3f4f6; border-radius: 8px; padding: 16px; margin: 24px 0;">
                    <strong>Resumo:</strong>
                    <p style="margin: 8px 0 0 0; color: #4b5563;">{summary_snippet}</p>
                </div>
                <a href="{view_url}" style="display: block; background: #6366f1; color: white; text-decoration: none; padding: 14px 28px; border-radius: 8px; text-align: center; font-weight: 600; margin: 24px 0;">Ver Diagnóstico Completo →</a>
                <p style="color: #6b7280; font-size: 14px; text-align: center; margin-top: 32px;">© NARA. Todos os direitos reservados.</p>
            </div>
        </body>
        </html>
        """

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
                <p style="color: #374151; line-height: 1.6;">Continue seu Diagnóstico NARA de onde parou.</p>
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
