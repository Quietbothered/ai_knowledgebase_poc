# Connectors and Indexing

## Data Sources

### Microsoft Teams
- Extract messages and attachments via Graph API
- Use delta queries for incremental updates

### Microsoft SharePoint
- Crawl documents and metadata
- Convert docx/pptx/pdf to text

### Jira
- Extract issues, comments, metadata
- Include status, labels, assignees

## Ingestion Strategy
- Initial full backfill
- Incremental updates via webhooks/delta APIs
- Store raw + processed data

## Metadata Model
- source_type
- document_id
- timestamp
- author
- project_key
- confidentiality

## Preprocessing
- Remove HTML
- Preserve structure (headings, code blocks)
- Normalize formatting

## Chunking Strategy
- 500–800 token chunks
- 50–100 token overlap
- Split by semantic boundaries

## Embeddings
- Use embedding model (OpenAI / sentence-transformers)
- Store vector + metadata

## Vector Database
Options:
- Qdrant
- Milvus
- Weaviate
- Pinecone

## Index Schema
- vector
- chunk_id
- document_id
- timestamp
- project
- text_snippet

## Incremental Indexing
- Track last_indexed_at
- Reindex only updated documents