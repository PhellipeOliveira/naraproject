"""Exceções HTTP customizadas para a API."""
from fastapi import HTTPException, status


def not_found(detail: str = "Recurso não encontrado") -> HTTPException:
    """404 Not Found."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def bad_request(detail: str = "Requisição inválida") -> HTTPException:
    """400 Bad Request."""
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def validation_error(detail: str = "Erro de validação") -> HTTPException:
    """422 Unprocessable Entity."""
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


def forbidden(detail: str = "Acesso negado") -> HTTPException:
    """403 Forbidden."""
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def unauthorized(detail: str = "Não autenticado") -> HTTPException:
    """401 Unauthorized."""
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
