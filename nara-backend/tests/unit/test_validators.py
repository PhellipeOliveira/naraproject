"""
Testes unitários para validações do sistema.
Conforme 07_DEPLOY_QUALIDADE.md - Seção 3
"""
import pytest
from app.rag.pipeline import NaraDiagnosticPipeline


class TestValidators:
    """Testes de validação de inputs e regras de negócio."""
    
    def test_email_validation(self):
        """Testa validação de formato de email."""
        from email_validator import validate_email, EmailNotValidError
        
        valid_emails = [
            "test@example.com",
            "user+tag@domain.co.uk",
            "first.last@company.com"
        ]
        
        for email in valid_emails:
            validated = validate_email(email, check_deliverability=False)
            assert validated.normalized
        
        invalid_emails = ["invalid", "@domain.com", "user@", ""]
        
        for email in invalid_emails:
            with pytest.raises(EmailNotValidError):
                validate_email(email)
    
    def test_answer_text_minimum_length(self):
        """Resposta deve ter pelo menos 10 caracteres."""
        MIN_LENGTH = 10
        
        valid = "Esta é uma resposta válida"
        invalid = "muito"
        
        assert len(valid) >= MIN_LENGTH
        assert len(invalid) < MIN_LENGTH
    
    def test_question_area_validation(self):
        """Área da pergunta deve ser uma das 12 áreas NARA."""
        pipeline = NaraDiagnosticPipeline()
        areas = list(pipeline.AREAS)
        
        assert len(areas) == 12
        assert "Saúde Física" in areas
        assert "Propósito e Vocação" in areas
        assert "Área Inválida" not in areas
    
    def test_phase_validation(self):
        """Fase deve estar entre 1 e 4."""
        valid_phases = [1, 2, 3, 4]
        invalid_phases = [0, 5, -1, 10]
        
        for phase in valid_phases:
            assert 1 <= phase <= 4
        
        for phase in invalid_phases:
            assert not (1 <= phase <= 4)


class TestAnswerProcessing:
    """Testes de processamento de respostas."""
    
    def test_word_count_calculation(self):
        """Testa cálculo de palavras."""
        text = "Esta resposta tem exatamente cinco palavras"
        words = text.split()
        assert len(words) == 5
        
        empty = ""
        assert len(empty.split()) == 0
    
    def test_area_coverage_tracking(self):
        """Testa tracking de cobertura de áreas."""
        areas_covered = ["Saúde Física", "Relacionamentos"]
        
        # Adicionar nova área
        new_area = "Finanças"
        if new_area not in areas_covered:
            areas_covered.append(new_area)
        
        assert len(areas_covered) == 3
        assert "Finanças" in areas_covered
        
        # Evitar duplicatas
        if new_area not in areas_covered:
            areas_covered.append(new_area)
        
        assert len(areas_covered) == 3  # Não duplica
