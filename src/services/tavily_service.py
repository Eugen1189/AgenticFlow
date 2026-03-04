import structlog
from typing import List, Dict, Any
from tavily import TavilyClient
from src.core.config import settings

logger = structlog.get_logger()

class TavilyService:
    """Service for interacting with the Tavily Search API."""
    
    def __init__(self, api_key: str = settings.TAVILY_TAVILY_API_KEY if hasattr(settings, 'TAVILY_TAVILY_API_KEY') else settings.TAVILY_API_KEY):
        self.client = TavilyClient(api_key=api_key)

    async def web_search(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform an asynchronous web search using Tavily.
        
        Args:
            query: The search query string.
            
        Returns:
            A list of search results containing title, url, and content.
        """
        log = logger.bind(query=query)
        log.info("tavily_search_started")
        
        try:
            # tavily-python's search is synchronous, we wrap it if needed or use as is 
            # for a true async experience we would use httpx, but for now we follow the SDK
            response = self.client.search(query=query, search_depth="smart")
            
            results = []
            for result in response.get("results", []):
                results.append({
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "content": result.get("content")
                })
            
            log.info("tavily_search_completed", count=len(results))
            return results
            
        except Exception as e:
            log.error("tavily_search_failed", error=str(e))
            return []
