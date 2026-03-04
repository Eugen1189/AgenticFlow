from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    """Schema for the user query request."""
    query: str = Field(..., description="The user's query or instruction.")
    max_rounds: int = Field(default=5, description="Maximum number of agent iterations.")

class QueryResponse(BaseModel):
    """Schema for the final agent response."""
    answer: str = Field(..., description="The generated answer from the multi-agent system.")
    sources: List[str] = Field(default_factory=list, description="List of URLs or source names used.")
    pii_sanitized: bool = Field(..., description="Whether the response was checked for PII.")
