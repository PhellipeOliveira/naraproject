"""Cálculo de scores por área (lógica extraída do pipeline se necessário)."""
# O cálculo principal está em rag/pipeline._calculate_area_scores.
# Este módulo pode conter funções auxiliares reutilizáveis.


def scale_to_score(scale_1_5: float) -> float:
    """Converte escala 1-5 para score 0-10."""
    if scale_1_5 is None:
        return 5.0
    return round(scale_1_5 * 2, 1)
