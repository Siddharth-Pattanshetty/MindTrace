import logging
import numpy as np
from typing import List, Union
from app.core.config import settings

logger = logging.getLogger("mindtrace.concept_engine.embeddings")

class EmbeddingModelLoader:
    _instance = None
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            model_name = getattr(settings, "EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading SentenceTransformer embedding model '{model_name}'...")
                cls._model = SentenceTransformer(model_name)
                logger.info("SentenceTransformer model loaded successfully.")
            except Exception as e:
                logger.warning(f"Failed to load sentence-transformers '{model_name}': {e}. Using fallback TF-IDF vectorizer.")
                cls._model = FallbackEmbeddingModel()
        return cls._model

class FallbackEmbeddingModel:
    def __init__(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vectorizer = TfidfVectorizer()
        self.is_fitted = False

    def encode(self, sentences: Union[str, List[str]], convert_to_numpy: bool = True) -> np.ndarray:
        if isinstance(sentences, str):
            sentences = [sentences]
        if not self.is_fitted:
            vecs = self.vectorizer.fit_transform(sentences).toarray()
            self.is_fitted = True
            return vecs[0] if len(sentences) == 1 else vecs
        else:
            try:
                vecs = self.vectorizer.transform(sentences).toarray()
                return vecs[0] if len(sentences) == 1 else vecs
            except Exception:
                vecs = self.vectorizer.fit_transform(sentences).toarray()
                return vecs[0] if len(sentences) == 1 else vecs
