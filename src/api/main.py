from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage
from src.api.schemas import HealthCheck, QueryRequest, QueryResponse
from src.core.graph import app_graph
from src.utils.pii_masker import mask_pii

app = FastAPI(
    title="AgenticFlow-Core API",
    description="Multi-agent workflow orchestrator for business automation",
    version="0.1.0",
)

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint to verify the API is running."""
    return HealthCheck(status="ok")

@app.post("/chat", response_model=QueryResponse)
async def chat_endpoint(request: QueryRequest):
    """
    Main entry point for multi-agent query processing.
    
    Runs the agentic workflow: Research -> Synthesis.
    """
    try:
        # Sanitize query (placeholder for now)
        sanitized_query = mask_pii(request.query)
        
        # Initialize graph state
        initial_state = {
            "messages": [HumanMessage(content=sanitized_query)],
            "research_data": [],
            "is_pii_masked": False, # Placeholder logic
            "metadata": {}
        }
        
        # Invoke LangGraph
        result = await app_graph.ainvoke(initial_state)
        
        # Extract the final AI message and sources
        final_message = result["messages"][-1].content
        sources = [res["url"] for res in result.get("research_data", [])]
        
        return QueryResponse(
            answer=final_message,
            sources=sources,
            pii_sanitized=False # Placeholder flag
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent workflow error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
