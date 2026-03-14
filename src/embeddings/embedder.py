from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Load the sentence transformer model."""
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list, batch_size: int = 32) -> np.ndarray:
        """Convert list of texts to embeddings."""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True  # normalize for cosine similarity
        )
        return np.array(embeddings, dtype="float32")

    def embed_query(self, query: str) -> np.ndarray:
        """Convert a single query string to embedding."""
        embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )
        return np.array(embedding, dtype="float32")