import time
import structlog
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.core.state import AgentState
from src.core.config import settings

logger = structlog.get_logger()

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.7
)

async def writer_node(state: AgentState) -> AgentState:
    """
    LangGraph node that synthesizes research data into a final response.
    
    Args:
        state: The current graph state.
        
    Returns:
        Updated state with the AI's final response and updated metadata.
    """
    start_time = time.time()
    
    # Extract data from state
    user_query = state["messages"][0].content if state["messages"] else "No query provided"
    research_context = "\n\n".join([
        f"Source: {res['title']} ({res['url']})\nContent: {res['content']}" 
        for res in state.get("research_data", [])
    ])
    
    log = logger.bind(node="writer", query=user_query)
    log.info("writer_node_started")

    # Construct the synthesis prompt
    system_prompt = (
        "You are an expert AI Assistant specializing in synthesizing information. "
        "Use the provided research data to answer the user's query. "
        "You MUST include citations in the form of URLs from the research data. "
        "If the research data is insufficient, be honest and state what you could not find. "
        "Format your response using professional Markdown."
    )
    
    context_prompt = f"### Research Data:\n{research_context}\n\n### User Query:\n{user_query}"

    try:
        # Generate response
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=context_prompt)
        ]
        
        response = await llm.ainvoke(messages)
        
        execution_time = time.time() - start_time
        
        log.info("writer_node_completed", execution_time=execution_time)
        
        # Update metadata
        new_metadata = state.get("metadata", {}).copy()
        new_metadata["execution_time"] = execution_time
        
        return {
            "messages": [response],
            "metadata": new_metadata
        }
        
    except Exception as e:
        log.error("writer_node_failed", error=str(e))
        error_msg = AIMessage(content="I encountered an error while synthesizing the research data.")
        return {"messages": [error_msg]}
