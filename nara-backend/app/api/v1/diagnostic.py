"""Endpoints de diagnóstico."""
import logging
from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import EmailStr

from app.models.diagnostic import (
    AnswerSubmitRequest,
    AnswerSubmitResponse,
    DiagnosticStartRequest,
    DiagnosticStartResponse,
    EligibilityResponse,
    DiagnosticResultResponse,
    NextQuestionsResponse,
    QuestionResponse,
)
from app.core.rate_limit import limiter
from app.services.diagnostic_service import DiagnosticService

router = APIRouter()
service = DiagnosticService()
logger = logging.getLogger(__name__)


@router.post("/start", response_model=DiagnosticStartResponse)
@limiter.limit("10/minute")
async def start_diagnostic(request: Request, payload: DiagnosticStartRequest):
    """
    Inicia um novo diagnóstico.
    Requer email e consentimento de privacidade.
    Retorna as 15 perguntas da Fase 1 (Baseline) e token para acesso ao resultado.
    """
    if not payload.consent_privacy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consentimento de privacidade é obrigatório",
        )

    result = await service.start_diagnostic(
        email=payload.email,
        full_name=payload.full_name,
        session_id=payload.session_id,
        consent_privacy=payload.consent_privacy,
        consent_marketing=payload.consent_marketing,
        device_info=payload.device_info,
        utm_source=payload.utm_source,
    )

    # Garantir que questions tenham o formato esperado pelo response model
    questions = [
        QuestionResponse(
            id=q.get("id", i),
            area=q.get("area", "Geral"),
            type=q.get("type", "open_long"),
            text=q.get("text", ""),
            scale_labels=q.get("scale_labels"),
            follow_up_hint=q.get("follow_up_hint"),
        )
        for i, q in enumerate(result["questions"], 1)
    ]

    return DiagnosticStartResponse(
        diagnostic_id=result["diagnostic_id"],
        status=result["status"],
        phase=result["phase"],
        questions=questions,
        total_questions=result["total_questions"],
        result_token=result["result_token"],
    )


@router.post("/{diagnostic_id}/answer", response_model=AnswerSubmitResponse)
@limiter.limit("120/minute")
async def submit_answer(request: Request, diagnostic_id: str, payload: AnswerSubmitRequest):
    """
    Submete uma resposta para uma pergunta.
    Atualiza contadores e scores parciais; retorna progresso e elegibilidade.
    """
    try:
        result = await service.submit_answer(
            diagnostic_id=diagnostic_id,
            question_id=payload.question_id,
            question_text=payload.question_text,
            question_area=payload.question_area,
            answer_text=payload.answer_text,
            answer_scale=payload.answer_scale,
            response_time_seconds=payload.response_time_seconds,
        )
        return AnswerSubmitResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.exception("submit_answer failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor. Tente novamente.",
        )


@router.get("/{diagnostic_id}/next-questions", response_model=NextQuestionsResponse)
@limiter.limit("20/minute")
async def get_next_questions(request: Request, diagnostic_id: str):
    """
    Gera perguntas para a próxima fase (RAG + LLM).
    Tempo típico de geração: 3-5 segundos (pode chegar a ~30s em carga).
    """
    try:
        result = await service.get_next_questions(diagnostic_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e) if str(e) else "Diagnóstico não encontrado",
        )
    except Exception as e:
        logger.exception("Erro ao gerar próximas perguntas: %s", e)
        msg = str(e) if str(e) else "Falha ao gerar perguntas (RAG/LLM). Tente novamente em instantes."
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=msg,
        )
    questions = [
        QuestionResponse(
            id=q.get("id", i),
            area=q.get("area", "Geral"),
            type=q.get("type", "open_long"),
            text=q.get("text", ""),
            scale_labels=q.get("scale_labels"),
            follow_up_hint=q.get("follow_up_hint"),
        )
        for i, q in enumerate(result["questions"], 1)
    ]
    return NextQuestionsResponse(
        phase=result["phase"],
        questions=questions,
        total_questions=result["total_questions"],
    )


@router.get("/{diagnostic_id}/eligibility", response_model=EligibilityResponse)
@limiter.limit("60/minute")
async def check_eligibility(request: Request, diagnostic_id: str):
    """
    Verifica se o diagnóstico pode ser finalizado.
    Critérios: ≥40 perguntas OU ≥3500 palavras e ≥12 áreas cobertas.
    """
    result = await service.check_eligibility(diagnostic_id)
    return EligibilityResponse(**result)


@router.post("/{diagnostic_id}/finish", response_model=DiagnosticResultResponse)
@limiter.limit("10/minute")
async def finish_diagnostic(request: Request, diagnostic_id: str):
    """
    Finaliza o diagnóstico e gera o relatório.
    Valida elegibilidade antes; geração via RAG + LLM (5-10 s).
    """
    eligibility = await service.check_eligibility(diagnostic_id)
    if not eligibility["can_finish"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Diagnóstico não atende aos critérios. Progresso: {eligibility['overall_progress']:.1f}%",
        )
    result = await service.finish_diagnostic(diagnostic_id)
    return DiagnosticResultResponse(**result)


@router.get("/check-existing")
@limiter.limit("30/minute")
async def check_existing_diagnostic(
    request: Request,
    email: EmailStr = Query(..., description="Email do titular"),
):
    """
    Verifica se existe diagnóstico em andamento para o email.
    Usado na tela de início para oferecer retomada.
    """
    return await service.check_existing_diagnostic(email)


@router.get("/{diagnostic_id}/current-state")
@limiter.limit("60/minute")
async def get_current_state(request: Request, diagnostic_id: str):
    """
    Retorna o estado atual do diagnóstico para retomada (perguntas restantes, progresso).
    """
    try:
        return await service.get_current_state(diagnostic_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# Declarar antes de /{diagnostic_id}/result para que /result/{token} não seja capturado como diagnostic_id
@router.get("/result/{token}", response_model=DiagnosticResultResponse)
@limiter.limit("30/minute")
async def get_result_by_token(request: Request, token: str):
    """Obtém resultado pelo token público (sem autenticação)."""
    result = await service.get_result_by_token(token)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultado não encontrado ou token inválido.",
        )
    return DiagnosticResultResponse(**result)


@router.get("/{diagnostic_id}/result", response_model=DiagnosticResultResponse)
@limiter.limit("30/minute")
async def get_result(request: Request, diagnostic_id: str):
    """Obtém o resultado de um diagnóstico finalizado."""
    result = await service.get_result(diagnostic_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultado não encontrado. Diagnóstico pode não ter sido finalizado.",
        )
    return DiagnosticResultResponse(**result)


@router.post("/{diagnostic_id}/send-resume-link")
@limiter.limit("5/minute")
async def send_resume_link(request: Request, diagnostic_id: str):
    """
    Envia email com link para retomar o diagnóstico.
    Usado quando o usuário clica em "Sair e continuar depois".
    """
    from app.services.email_service import email_service
    from app.database import supabase
    
    # Buscar diagnóstico
    diag_result = supabase.table("diagnostics").select("*").eq(
        "id", diagnostic_id
    ).single().execute()
    
    if not diag_result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnóstico não encontrado"
        )
    
    diagnostic = diag_result.data
    
    # Calcular progresso
    total_answers = diagnostic.get("total_answers", 0)
    progress = min(100, int((total_answers / 40) * 100))
    
    # Enviar email
    try:
        await email_service.send_resume_link(
            to=diagnostic["email"],
            user_name=diagnostic.get("full_name"),
            diagnostic_id=diagnostic_id,
            progress=progress
        )
        
        return {
            "status": "sent",
            "message": f"Email enviado para {diagnostic['email']}"
        }
    except Exception as e:
        logger.exception("send_resume_link failed for diagnostic_id=%s: %s", diagnostic_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao enviar email de retomada. Tente novamente."
        )
