"""Utilitários de observabilidade (request ID e logs correlacionáveis)."""
import logging
from contextvars import ContextVar

_request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="-")


def set_request_id(request_id: str):
    """Define request_id no contexto corrente e retorna token para reset."""
    return _request_id_ctx_var.set(request_id)


def reset_request_id(token) -> None:
    """Restaura contexto anterior do request_id."""
    _request_id_ctx_var.reset(token)


def get_request_id() -> str:
    """Obtém request_id atual do contexto."""
    return _request_id_ctx_var.get("-")


class RequestContextFilter(logging.Filter):
    """Injeta request_id em todo LogRecord."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True


def configure_logging() -> None:
    """Configura logging JSON com campo de correlação request_id."""
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s",'
            '"request_id":"%(request_id)s","message":"%(message)s"}'
        ),
        datefmt="%Y-%m-%dT%H:%M:%S",
        force=True,
    )
    context_filter = RequestContextFilter()
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.addFilter(context_filter)
