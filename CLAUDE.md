# AgenticFlow-Core: AI Assistant Context

## Project Overview
AgenticFlow-Core is a production-ready multi-agent orchestration system. It uses a graph-based approach to execute complex research and writing tasks autonomously.

## Tech Stack
- **Framework**: Python 3.11, FastAPI
- **Orchestration**: LangGraph (StateGraph)
- **Search**: Tavily API
- **LLM**: OpenAI GPT models
- **Logging**: Structlog (JSON)

## Development Standards
- **Conventional Commits**: `feat:`, `fix:`, `docs:`, `chore:`
- **Architecture**: Follow ADRs in `docs/adr/`
- **Typing**: Strict Pydantic v2 and Python Type Hints
- **Structure**:
    - `src/api`: FastAPI endpoints
    - `src/core`: Graph logic and nodes
    - `src/services`: External API clients
    - `src/utils`: Utilities (Logging, Masking)

## Key Commands
- `uvicorn src.api.main:app --reload`: Start dev server
- `pytest`: Run tests
- `docker compose up`: Run production environment
