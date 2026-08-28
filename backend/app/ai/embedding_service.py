import logging
import numpy as np
from typing import List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Sentence Transformers Embedding Service Abstraction for MindTrace.
    Provides singleton caching for all-MiniLM-L6-v2 embeddings.
    """
    
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        model_name = getattr(settings, "EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(model_name)
            logger.info(f"[EmbeddingService] Successfully loaded model '{model_name}'.")
        except Exception as e:
            logger.warning(f"[EmbeddingService] Failed to load SentenceTransformer '{model_name}': {e}. Using deterministic fallback encoder.")
            self._model = None

    def encode(self, texts: List[str]) -> np.ndarray:
        if self._model:
            embeddings = self._model.encode(texts, convert_to_numpy=True)
            return embeddings.astype('float32')
        else:
            # Deterministic fallback vectors if model download offline
            dim = 384
            vecs = []
            for t in texts:
                v = np.zeros(dim, dtype='float32')
                hash_val = sum(ord(c) for c in t)
                for i in range(dim):
                    v[i] = np.sin(hash_val * (i + 1))
                vecs.append(v)
            return np.array(vecs, dtype='float32')

embedding_service = EmbeddingService()
