import numpy as np
import logging
from typing import List, Dict, Any, Tuple
from app.ai.concept_engine.embeddings import EmbeddingModelLoader

logger = logging.getLogger("mindtrace.concept_engine.retriever")

class ConceptRetriever:
    def __init__(self, concepts_data: List[Dict[str, Any]]):
        self.model = EmbeddingModelLoader.get_model()
        self.concepts = concepts_data
        self.concept_embeddings = None
        self._build_concept_embeddings()

    def _build_concept_embeddings(self):
        texts = []
        for c in self.concepts:
            # Construct rich text: Subject > Domain > Topic > Concept. Description
            subject = c.get("subject", "Mathematics")
            domain = c.get("domain", "")
            topic = c.get("topic", "")
            name = c.get("name", "")
            desc = c.get("description", "")
            
            rich_text = f"{subject} > {domain} > {topic} > {name}. {desc}"
            texts.append(rich_text)

        logger.info(f"Generating embeddings for {len(texts)} concepts...")
        encoded = self.model.encode(texts, convert_to_numpy=True)
        # Normalize for cosine similarity
        if isinstance(encoded, list):
            encoded = np.array(encoded)
        norms = np.linalg.norm(encoded, axis=1, keepdims=True)
        norms[norms == 0] = 1e-10
        self.concept_embeddings = encoded / norms

    def retrieve_candidates(self, query_text: str, error_type: str = None, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        # Append contextual error details if present
        full_query = query_text
        if error_type:
            full_query += f"\n[ERROR CONTEXT] {error_type}"

        query_vec = self.model.encode(full_query, convert_to_numpy=True)
        if isinstance(query_vec, list):
            query_vec = np.array(query_vec)
        
        norm = np.linalg.norm(query_vec)
        if norm == 0:
            norm = 1e-10
        query_vec = query_vec / norm

        # Compute cosine similarity
        similarities = np.dot(self.concept_embeddings, query_vec)
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            concept = self.concepts[idx]
            sim_score = float(similarities[idx])
            results.append((concept, sim_score))

        return results
