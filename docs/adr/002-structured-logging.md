# ADR 002: Structured Logging for AI Workflows

## Context
AI workflows (especially multi-agent) are notoriously hard to debug. Traditional `print()` statements are insufficient for production monitoring and audit trails.

## Decision
Implement structured JSON logging using `structlog`.

## Context
Every node entry, exit, and external API call must be logged with context (e.g., query ID, execution time, token usage).

## Consequences
- Pros: Logs can be easily ingested by ELK, Datadog, or Loki. Clear visibility into agent "thought processes".
- Cons: Minor performance overhead (negligible for LLM-based apps).
