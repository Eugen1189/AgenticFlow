from langgraph.graph import StateGraph, START, END
from src.core.state import AgentState
from src.core.nodes.researcher import research_node
from src.core.nodes.writer import writer_node

def create_graph():
    """Assemble and compile the LangGraph workflow."""
    
    # Initialize the graph with our state schema
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("researcher", research_node)
    workflow.add_node("writer", writer_node)
    
    # Define edges (linear flow)
    workflow.add_edge(START, "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)
    
    # Compile the graph
    return workflow.compile()

# Export compiled graph
app_graph = create_graph()
