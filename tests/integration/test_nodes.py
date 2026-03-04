import pytest
from unittest.mock import AsyncMock, patch
from langchain_core.messages import HumanMessage
from src.core.nodes.researcher import research_node

@pytest.mark.asyncio
async def test_researcher_node_success():
    # Mock Tavily results
    mock_results = [
        {"title": "Test Title", "url": "https://test.com", "content": "Test content"}
    ]
    
    # State setup
    state = {
        "messages": [HumanMessage(content="What is AI?")],
        "research_data": [],
        "is_pii_masked": False,
        "metadata": {}
    }
    
    # Patch the web_search method of TavilyService instance used in researcher.py
    # Note: researcher.py has `tavily_service = TavilyService()` at module level
    with patch("src.core.nodes.researcher.tavily_service.web_search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = mock_results
        
        result = await research_node(state)
        
        assert "research_data" in result
        assert len(result["research_data"]) == 1
        assert result["research_data"][0]["title"] == "Test Title"
        assert "messages" in result
        assert "I found 1 sources" in result["messages"][0].content
