# Prompt and RAG Design

## RAG Workflow
1. User query
2. Retrieve relevant chunks
3. Assemble context
4. Generate response using LLM

## Prompt Template

SYSTEM:
You are a knowledge assistant. Use only provided sources.
If unsure, say "I don't know".

USER:
{query}

CONTEXT:
[1] {source} | excerpt
[2] {source} | excerpt

TASK:
- Provide summary
- Provide detailed explanation
- Cite sources

## Hallucination Prevention
- Strict "use only context" instruction
- Return "I don't know" if no evidence

## Citation Format
- Inline references: [1], [2]
- Source list at end

## Response Structure
1. Summary (2–4 lines)
2. Detailed explanation
3. Sources

## Conversational Context
- Include previous queries
- Enable follow-up questions