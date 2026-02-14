"""Endpoints de diagnóstico."""
from fastapi import APIRouter, HTTPException, status

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
from app.services.diagnostic_service import DiagnosticService

router = APIRouter()
service = DiagnosticService()


@router.post("/start", response_model=DiagnosticStartResponse)
async def start_diagnostic(request: DiagnosticStartRequest):
    """
    Inicia um novo diagnóstico.
    Requer email e consentimento de privacidade.
    Retorna as 15 perguntas da Fase 1 (Baseline) e token para acesso ao resultado.
    """
    if not request.consent_privacy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consentimento de privacidade é obrigatório",
        )

    result = await service.start_diagnostic(
        email=request.email,
        full_name=request.full_name,
        session_id=request.session_id,
        consent_privacy=request.consent_privacy,
        consent_marketing=request.consent_marketing,
        device_info=request.device_info,
        utm_source=request.utm_source,
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
async def submit_answer(diagnostic_id: str, request: AnswerSubmitRequest):
    """
    Submete uma resposta para uma pergunta.
    Atualiza contadores e scores parciais; retorna progresso e elegibilidade.
    """
    result = await service.submit_answer(
        diagnostic_id=diagnostic_id,
        question_id=request.question_id,
        question_text=request.question_text,
        question_area=request.question_area,
        answer_text=request.answer_text,
        answer_scale=request.answer_scale,
        response_time_seconds=request.response_time_seconds,
    )
    return AnswerSubmitResponse(**result)


@router.get("/{diagnostic_id}/next-questions", response_model=NextQuestionsResponse)
async def get_next_questions(diagnostic_id: str):
    """
    Gera perguntas para a próxima fase (RAG + LLM).
    Tempo típico de geração: 3-5 segundos.
    """
    result = await service.get_next_questions(diagnostic_id)
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
async def check_eligibility(diagnostic_id: str):
    """
    Verifica se o diagnóstico pode ser finalizado.
    Critérios: ≥40 perguntas OU ≥3500 palavras e ≥12 áreas cobertas.
    """
    result = await service.check_eligibility(diagnostic_id)
    return EligibilityResponse(**result)


@router.post("/{diagnostic_id}/finish", response_model=DiagnosticResultResponse)
async def finish_diagnostic(diagnostic_id: str):
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
async def check_existing_diagnostic(email: str):
    """
    Verifica se existe diagnóstico em andamento para o email.
    Usado na tela de início para oferecer retomada.
    """
    return await service.check_existing_diagnostic(email)


@router.get("/{diagnostic_id}/current-state")
async def get_current_state(diagnostic_id: str):
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
async def get_result_by_token(token: str):
    """Obtém resultado pelo token público (sem autenticação)."""
    result = await service.get_result_by_token(token)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultado não encontrado ou token inválido.",
        )
    return DiagnosticResultResponse(**result)


@router.get("/{diagnostic_id}/result", response_model=DiagnosticResultResponse)
async def get_result(diagnostic_id: str):
    """Obtém o resultado de um diagnóstico finalizado."""
    result = await service.get_result(diagnostic_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultado não encontrado. Diagnóstico pode não ter sido finalizado.",
        )
    return DiagnosticResultResponse(**result)
