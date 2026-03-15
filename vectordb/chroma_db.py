"""
Vector Database Management (Chroma)

Responsibilities:
- Generate embeddings for text chunks
- Store embeddings in the Chroma vector database
- Persist the vector database locally

Vector Database Purpose:
Stores numerical embeddings of text chunks so we can
perform similarity search when a user asks a question.

Pipeline Stage:
Chunks → Embeddings → Vector DB
"""