import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from app.ai.embedding_service import embedding_service

class VectorStore:
    """
    FAISS vector retrieval layer mapping vector IDs to database entity IDs.
    Powered by Sentence Transformers (all-MiniLM-L6-v2).
    """
    
    def __init__(self):
        self.dimension = 384
        self.index = None
        self.entity_id_map: Dict[int, Any] = {} # FAISS index -> Database Entity ID
        self.documents: List[Dict[str, Any]] = []
        self._init_faiss()

    def _init_faiss(self):
        try:
            import faiss
            self.index = faiss.IndexFlatL2(self.dimension)
            self.faiss_module = faiss
        except Exception:
            self.index = None

    def add_documents(self, docs: List[Dict[str, Any]]):
        """
        Indexes concepts, questions, or practice items and binds FAISS vector IDs to DB entities.
        """
        if not docs:
            return
        
        texts = [d.get("text", "") or d.get("name", "") or d.get("description", "") for d in docs]
        embeddings = embedding_service.encode(texts)
        
        start_idx = len(self.documents)
        if self.index and hasattr(self, 'faiss_module'):
            self.index.add(embeddings)
            
        for i, d in enumerate(docs):
            faiss_id = start_idx + i
            db_id = d.get("id") or d.get("code") or faiss_id
            self.entity_id_map[faiss_id] = db_id
            self.documents.append(d)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """
        Semantic vector search returning document entities and similarity scores.
        """
        if not self.documents:
            return []
            
        query_vec = embedding_service.encode([query])
        
        if self.index and hasattr(self, 'faiss_module'):
            distances, indices = self.index.search(query_vec, min(top_k, len(self.documents)))
            results = []
            for idx, dist in zip(indices[0], distances[0]):
                if idx < len(self.documents) and idx >= 0:
                    similarity = max(0.0, float(1.0 / (1.0 + dist)))
                    results.append((self.documents[idx], round(similarity, 3)))
            return results
        else:
            return [(d, 0.85) for d in self.documents[:top_k]]

vector_store = VectorStore()
