from typing import Annotated, TypedDict, List, Dict, Any, Union
from langchain_core.messages import BaseMessage, add_messages

class AgentState(TypedDict):
    """
    State of the multi-agent graph.
    
    Attributes:
        messages: Ongoing conversation history, updated incrementally.
        research_data: Collected information from external search (Tavily).
        is_pii_masked: GDPR compliance flag tracking if data was sanitized.
        metadata: Execution metrics like token usage and processing time.
    """
    messages: Annotated[List[BaseMessage], add_messages]
    research_data: List[Union[str, Dict[str, Any]]]
    is_pii_masked: bool
    metadata: Dict[str, Any]
