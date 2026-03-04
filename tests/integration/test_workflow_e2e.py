import pytest
import httpx
from unittest.mock import AsyncMock, patch
from langchain_core.messages import AIMessage
from src.api.main import app

@pytest.mark.asyncio
async def test_workflow_e2e_complex_query():
    """
    Integration test for the end-to-end workflow using a complex query.
    Mocks external services (Tavily and OpenAI) to ensure deterministic behavior.
    """
    # 1. Mock Tavily search results
    mock_research_data = [
        {
            "url": "https://tech-trends.eu/ai-2025", 
            "title": "AI Trends in EU 2025", 
            "content": "European Union focuses heavily on AI Act compliance and ethical AI frameworks in 2025."
        },
        {
            "url": "https://innovation-us.com/future-ai", 
            "title": "AI Trends in USA 2025", 
            "content": "The USA maintains its lead in large-scale foundation models and private sector AI investment."
        }
    ]
    
    # 2. Mock LLM response
    mock_llm_content = (
        "In 2025, AI trends show a clear divergence between the EU and the USA. "
        "The EU is primarily focused on regulatory frameworks like the AI Act, "
        "while the USA leads in compute-intensive foundation models. "
        "Sources: https://tech-trends.eu/ai-2025, https://innovation-us.com/future-ai"
    )
    mock_llm_response = AIMessage(content=mock_llm_content)

    # 3. Patch external service calls
    with patch("src.core.nodes.researcher.tavily_service.web_search", new_callable=AsyncMock) as mock_search, \
         patch("src.core.nodes.writer.llm", new_callable=AsyncMock) as mock_ll:
        
        mock_search.return_value = mock_research_data
        mock_ll.ainvoke.return_value = mock_llm_response
        
        # 4. Execute request via httpx.AsyncClient
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/chat",
                json={"query": "Compare 2025 AI trends in EU vs USA"}
            )
            
        # 5. Assertions
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "answer" in data
        assert "sources" in data
        assert isinstance(data["sources"], list)
        
        # Verify sources are not empty (should have 2 from our mock)
        assert len(data["sources"]) > 0
        assert "https://tech-trends.eu/ai-2025" in data["sources"]
        assert "https://innovation-us.com/future-ai" in data["sources"]
        
        # Verify metadata and execution time
        assert "metadata" in data
        assert "execution_time" in data["metadata"]
        assert isinstance(data["metadata"]["execution_time"], (int, float))
        assert data["metadata"]["execution_time"] >= 0
