"""Geração de PDF do diagnóstico do usuário."""
from __future__ import annotations

from io import BytesIO
from typing import Any


def _safe_text(value: Any) -> str:
    return str(value) if value is not None else ""


def build_diagnostic_pdf(result_data: dict[str, Any]) -> bytes:
    """
    Gera PDF em memória a partir do resultado do diagnóstico.
    Requer reportlab instalado no ambiente.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except ImportError as exc:  # pragma: no cover - depende do ambiente
        raise RuntimeError("Dependência 'reportlab' não instalada.") from exc

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="Diagnóstico NARA")
    styles = getSampleStyleSheet()
    story = []

    vetor = result_data.get("vetor_estado") or {}
    memorias = result_data.get("memorias_vermelhas") or []
    ancoras = result_data.get("ancoras_sugeridas") or []
    recommendations = result_data.get("recommendations") or []

    story.append(Paragraph("Diagnóstico NARA", styles["Title"]))
    story.append(Paragraph("Transformação Narrativa · Metodologia Phellipe Oliveira", styles["Normal"]))
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Resumo Executivo</b>", styles["Heading2"]))
    story.append(Paragraph(_safe_text(result_data.get("executive_summary")), styles["BodyText"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Vetor de Estado</b>", styles["Heading2"]))
    story.append(Paragraph(f"Motor dominante: {_safe_text(vetor.get('motor_dominante'))}", styles["BodyText"]))
    story.append(Paragraph(f"Estágio: {_safe_text(vetor.get('estagio_jornada'))}", styles["BodyText"]))
    story.append(Paragraph(f"Crise raiz: {_safe_text(vetor.get('crise_raiz'))}", styles["BodyText"]))
    story.append(Paragraph(f"Ponto de entrada: {_safe_text(vetor.get('ponto_entrada_ideal'))}", styles["BodyText"]))
    story.append(Spacer(1, 10))

    if memorias:
        story.append(Paragraph("<b>Frases que revelam conflitos</b>", styles["Heading2"]))
        for memoria in memorias[:10]:
            story.append(Paragraph(f"- {_safe_text(memoria)}", styles["BodyText"]))
        story.append(Spacer(1, 10))

    if ancoras:
        story.append(Paragraph("<b>Práticas sugeridas</b>", styles["Heading2"]))
        for ancor in ancoras[:10]:
            story.append(Paragraph(f"- {_safe_text(ancor)}", styles["BodyText"]))
        story.append(Spacer(1, 10))

    if recommendations:
        story.append(Paragraph("<b>Próximos passos</b>", styles["Heading2"]))
        for rec in recommendations[:10]:
            action = _safe_text(rec.get("action"))
            timeframe = _safe_text(rec.get("timeframe"))
            story.append(Paragraph(f"- {action} ({timeframe})", styles["BodyText"]))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def build_micro_diagnostic_pdf(area: str, result_data: dict[str, Any]) -> bytes:
    """
    Gera PDF em memória para o resultado do microdiagnóstico.
    Requer reportlab instalado no ambiente.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except ImportError as exc:  # pragma: no cover - depende do ambiente
        raise RuntimeError("Dependência 'reportlab' não instalada.") from exc

    buffer = BytesIO()
    title_area = _safe_text(area) or "Área não informada"
    doc = SimpleDocTemplate(buffer, pagesize=A4, title=f"Microdiagnóstico NARA - {title_area}")
    styles = getSampleStyleSheet()
    story = []

    ancoras = result_data.get("ancoras") or []

    story.append(Paragraph("Microdiagnóstico NARA", styles["Title"]))
    story.append(Paragraph(f"Área: {title_area}", styles["Heading2"]))
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Resumo do microdiagnóstico</b>", styles["Heading2"]))
    story.append(Paragraph(_safe_text(result_data.get("micro_summary")), styles["BodyText"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Técnica TCC</b>", styles["Heading2"]))
    story.append(Paragraph(_safe_text(result_data.get("foco_tcc")), styles["BodyText"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Ação para 7 dias</b>", styles["Heading2"]))
    story.append(Paragraph(_safe_text(result_data.get("proxima_acao_7_dias")), styles["BodyText"]))
    story.append(Spacer(1, 10))

    if ancoras:
        story.append(Paragraph("<b>Âncoras sugeridas</b>", styles["Heading2"]))
        for ancora in ancoras[:10]:
            story.append(Paragraph(f"- {_safe_text(ancora)}", styles["BodyText"]))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
