"""
source venv/bin/activate # Activate the virtual environment
Document Ingestion and Chunking Module

Responsibilities:
- Load raw documents from the data directory
- Split large documents into smaller chunks
- Prepare text chunks for embedding generation

Why Chunking?
Large documents exceed the token limits of embedding models.
Chunking breaks documents into smaller pieces so each piece can
be embedded and stored in the vector database.

Pipeline Stage:
Documents → Chunking → Embeddings
"""