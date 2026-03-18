# RAG System Architecture

## High-Level Flow
1. Ingestion from external systems
2. Preprocessing and chunking
3. Embedding and indexing
4. Retrieval (hybrid search)
5. LLM-based answer generation
6. UI with citations

## Architecture Overview
- Connectors → Extract data
- Preprocessor → Normalize + chunk
- Vector DB → Store embeddings
- Retriever → Fetch relevant chunks
- LLM → Generate response
- UI → Display answer + sources

## Data Flow
User Query → Retrieval → Context Assembly → LLM → Answer + Citations

## Components

### 1. Connectors
- Teams API
- SharePoint API
- Jira API

### 2. Preprocessing
- HTML cleanup
- Text normalization
- Chunking (500–800 tokens)
- Metadata tagging

### 3. Embedding Layer
- Convert chunks into vectors
- Store in vector database

### 4. Retrieval Layer
- Semantic search (vector similarity)
- Keyword search (exact match)
- Metadata filtering (ACLs)

### 5. Reranking
- Recency-based scoring
- Source trust weighting
- Deduplication

### 6. LLM Layer
- Context-aware generation
- Citation-based answering
- Hallucination control

## Retrieval Strategy
Final Score:
final_score = α * semantic + β * keyword + γ * recency + δ * trust

## Output Format
- Summary
- Detailed explanation
- Source citations