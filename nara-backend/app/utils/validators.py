"""Validações customizadas (email, limites)."""
import re


def validate_email_domain(email: str, allowed_domains: list[str] | None = None) -> bool:
    """Valida formato de email; opcionalmente restringe a domínios."""
    if not email or "@" not in email:
        return False
    if allowed_domains is None:
        return True
    domain = email.split("@")[-1].lower()
    return domain in allowed_domains


def validate_word_count(text: str | None, max_words: int = 5000) -> bool:
    """Retorna True se o texto tiver no máximo max_words palavras."""
    if not text:
        return True
    return len(text.split()) <= max_words
