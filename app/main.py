"""
Main Application Entry Point

Responsibilities:
- Accept user query
- Call the retriever to fetch relevant documents from the vector database
- Pass retrieved context + user question to the LLM
- Return the generated answer

Pipeline Flow:
User Query
   ↓
Retriever
   ↓
Relevant Chunks from Vector DB
   ↓
LLM (OpenAI / other model)
   ↓
Generated Answer

This file orchestrates the full RAG pipeline.
"""