import structlog
from langchain_core.messages import SystemMessage
from src.core.state import AgentState
from src.services.tavily_service import TavilyService

logger = structlog.get_logger()
tavily_service = TavilyService()

async def research_node(state: AgentState) -> AgentState:
    """
    LangGraph node that performs web research based on the user's query.
    
    Args:
        state: The current graph state.
        
    Returns:
        Updated state with research results and a system update message.
    """
    # Get the last message which should be the user query
    user_query = state["messages"][-1].content
    
    log = logger.bind(node="researcher", query=user_query)
    log.info("research_node_started")
    
    # Perform search
    results = await tavily_service.web_search(user_query)
    
    if not results:
        summary_message = "I performed a search but found no relevant information."
    else:
        summary_message = f"I found {len(results)} sources relevant to the query."
        
    log.info("research_node_completed", result_count=len(results))
    
    # Return updates to the state
    return {
        "research_data": results,
        "messages": [SystemMessage(content=summary_message)]
    }
