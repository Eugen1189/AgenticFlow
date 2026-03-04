# ADR 005: Graph Orchestration and LLM Synthesis

## Context
We need to synthesize research data into a coherent response and define the execution flow between research and writing.

## Decision
Use `langchain-openai` (specifically GPT-4o or GPT-4o-mini) for synthesis. The graph will follow a linear path for the MVP: Start -> Researcher -> Writer -> End. 

## Consequences
- Pros: Simple, predictable flow, easy to debug.
- Cons: Lacks conditional routing (e.g., "if research is insufficient, search again"), which can be added in later iterations.
