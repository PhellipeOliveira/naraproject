"""
Testes de integração do pipeline RAG.
Conforme 07_DEPLOY_QUALIDADE.md - Seção 3
"""
import pytest
from app.rag.pipeline import NaraDiagnosticPipeline
from app.rag.retriever import retrieve_relevant_chunks


@pytest.mark.asyncio
class TestRAGPipeline:
    """Testes de integração do sistema RAG."""
    
    async def test_retrieve_chunks_with_query(self):
        """Testa busca de chunks relevantes."""
        query = "Como melhorar minha saúde física?"
        
        chunks = await retrieve_relevant_chunks(
            query=query,
            top_k=5,
            filter_version=1,
            filter_chunk_strategy="semantic"
        )
        
        # Deve retornar resultados
        assert isinstance(chunks, list)
        
        # Se houver chunks, validar estrutura
        if chunks:
            chunk = chunks[0]
            assert "content" in chunk
            assert "chapter" in chunk
            assert isinstance(chunk["content"], str)
    
    async def test_retrieve_chunks_empty_query(self):
        """Query vazia deve retornar lista vazia ou erro."""
        chunks = await retrieve_relevant_chunks(
            query="",
            top_k=5
        )
        
        assert isinstance(chunks, list)
    
    async def test_retrieve_chunks_with_filters(self):
        """Testa busca com filtros específicos."""
        chunks = await retrieve_relevant_chunks(
            query="Qual meu propósito?",
            top_k=3,
            filter_chapter="Metodologia",
            filter_version=1,
            filter_chunk_strategy="semantic"
        )
        
        assert isinstance(chunks, list)
        
        # Validar que filtros foram aplicados
        for chunk in chunks:
            if "chapter" in chunk:
                assert chunk["chapter"] == "Metodologia"


@pytest.mark.asyncio
class TestPipelineFlow:
    """Testes do fluxo completo do pipeline."""
    
    async def test_pipeline_initialization(self):
        """Testa inicialização do pipeline."""
        pipeline = NaraDiagnosticPipeline()
        
        assert pipeline is not None
        assert hasattr(pipeline, 'AREAS')
        assert len(pipeline.AREAS) == 12
    
    async def test_eligibility_check_structure(self):
        """Testa estrutura de resposta do check de elegibilidade."""
        pipeline = NaraDiagnosticPipeline()
        
        result = pipeline._check_eligibility(
            total_answers=40,
            total_words=3500,
            areas_covered=list(pipeline.AREAS)
        )
        
        assert hasattr(result, 'can_finish')
        assert hasattr(result, 'reasons')
        assert hasattr(result, 'missing_areas')
        assert isinstance(result.can_finish, bool)
        assert isinstance(result.reasons, list)
