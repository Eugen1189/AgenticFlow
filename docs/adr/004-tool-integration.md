# ADR 004: Tool Integration for External Research

## Context
The agent needs to access real-time web data to provide accurate answers. 

## Decision
Use Tavily API as the primary search engine due to its AI-optimized output (cleaner content compared to Google/Bing). Tools will be invoked via a dedicated 'Researcher' node in LangGraph.

## Consequences
- Pros: Reduced noise in LLM context, faster development.
- Cons: Dependency on a third-party API (Tavily).
