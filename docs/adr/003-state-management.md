# ADR 003: Typed State Management in LangGraph

## Context
We need a robust way to pass data between agents (Researcher, Writer) while ensuring type safety and tracking metadata (PII masking status, token usage).

## Decision
Use `TypedDict` combined with `Annotated` from the `typing` module for the Graph State. Use `operator.add` for message history to allow incremental updates.

## Consequences
- Pros: Strict validation, better IDE support (Cursor/Claude), clear history tracking.
- Cons: Slightly more boilerplate code than a simple dictionary.
