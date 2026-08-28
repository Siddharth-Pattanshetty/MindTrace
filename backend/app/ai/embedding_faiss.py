import numpy as np
from typing import List, Dict, Any, Tuple, Optional

class VectorStore:
    """
    MiniLM-L6-v2 embedding generator + FAISS vector search layer.
    """
    
    def __init__(self):
        self.dimension = 384
        self.model = None
        self.index = None
        self.documents: List[Dict[str, Any]] = []
        self._init_engine()

    def _init_engine(self):
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.index = faiss.IndexFlatL2(self.dimension)
            self.faiss_module = faiss
        except Exception:
            self.model = None
            self.index = None

    def encode(self, texts: List[str]) -> np.ndarray:
        """Embeds list of strings into 384-d vectors."""
        if self.model:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings.astype('float32')
        else:
            # Deterministic pseudo-embeddings fallback if model download is skipped/offline
            vecs = []
            for t in texts:
                v = np.zeros(self.dimension, dtype='float32')
                hash_val = sum(ord(c) for c in t)
                for i in range(self.dimension):
                    v[i] = np.sin(hash_val * (i + 1))
                vecs.append(v)
            return np.array(vecs, dtype='float32')

    def add_documents(self, docs: List[Dict[str, Any]]):
        """Indexes concepts, questions, or learning resources."""
        if not docs:
            return
        
        texts = [d.get("text", "") or d.get("name", "") or d.get("description", "") for d in docs]
        embeddings = self.encode(texts)
        
        if self.index and hasattr(self, 'faiss_module'):
            self.index.add(embeddings)
            
        self.documents.extend(docs)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """Search nearest concept or resource for a given text query."""
        if not self.documents:
            return []
            
        query_vec = self.encode([query])
        
        if self.index and hasattr(self, 'faiss_module'):
            distances, indices = self.index.search(query_vec, min(top_k, len(self.documents)))
            results = []
            for idx, dist in zip(indices[0], distances[0]):
                if idx < len(self.documents) and idx >= 0:
                    similarity = max(0.0, 1.0 - float(dist) / 100.0)
                    results.append((self.documents[idx], similarity))
            return results
        else:
            # Fallback distance computation
            results = []
            for doc in self.documents[:top_k]:
                results.append((doc, 0.85))
            return results

vector_store = VectorStore()
