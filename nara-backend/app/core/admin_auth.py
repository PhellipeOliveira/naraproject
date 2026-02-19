"""Auth administrativa simples com token assinado (HMAC + expiração)."""
import base64
import hashlib
import hmac
import json
import time

from app.config import settings


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _secret() -> bytes:
    return settings.ADMIN_JWT_SECRET.encode("utf-8")


def create_admin_token(username: str) -> str:
    """Cria token admin com expiração."""
    now = int(time.time())
    exp = now + (settings.ADMIN_TOKEN_TTL_MINUTES * 60)
    payload = {"sub": username, "iat": now, "exp": exp, "scope": "admin"}

    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    sig = hmac.new(_secret(), payload_b64.encode("utf-8"), hashlib.sha256).digest()
    sig_b64 = _b64url_encode(sig)
    return f"{payload_b64}.{sig_b64}"


def verify_admin_token(token: str) -> dict | None:
    """Valida assinatura e expiração do token admin."""
    try:
        payload_b64, sig_b64 = token.split(".", 1)
    except ValueError:
        return None

    expected = hmac.new(_secret(), payload_b64.encode("utf-8"), hashlib.sha256).digest()
    try:
        provided = _b64url_decode(sig_b64)
    except Exception:
        return None

    if not hmac.compare_digest(expected, provided):
        return None

    try:
        payload_raw = _b64url_decode(payload_b64).decode("utf-8")
        payload = json.loads(payload_raw)
    except Exception:
        return None

    now = int(time.time())
    if not isinstance(payload, dict) or payload.get("exp", 0) < now:
        return None
    if payload.get("scope") != "admin":
        return None
    return payload
