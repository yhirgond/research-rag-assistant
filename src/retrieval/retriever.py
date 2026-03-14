from src.embeddings.embedder import Embedder
from src.retrieval.vector_store import VectorStore


class Retriever:
    def __init__(self, embedder: Embedder, vector_store: VectorStore):
        """Initialize retriever with embedder and vector store."""
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> list:
        """
        Given a query, embed it and retrieve top-k relevant chunks.
        """
        # Embed the query
        query_embedding = self.embedder.embed_query(query)

        # Search vector store
        results = self.vector_store.search(query_embedding, top_k=top_k)

        return results

    def format_results(self, results: list) -> str:
        """Format retrieved chunks for display."""
        formatted = ""
        for i, chunk in enumerate(results, 1):
            formatted += (
                f"\n[{i}] Source: {chunk['source']} | "
                f"Page: {chunk['page']} | "
                f"Score: {chunk['score']:.3f}\n"
                f"{chunk['text'][:300]}...\n"
                f"{'-' * 60}\n"
            )
        return formatted