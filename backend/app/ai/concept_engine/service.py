import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from app.core.config import settings
from app.ai.concept_engine.retriever import ConceptRetriever
from app.ai.concept_engine.graph import KnowledgeGraphService
from app.ai.concept_engine.schemas import ConceptClassificationRequest, ConceptClassificationResponse

logger = logging.getLogger("mindtrace.concept_engine.service")

class ConceptEngineService:
    def __init__(self):
        self.similarity_threshold = getattr(settings, "CONCEPT_SIMILARITY_THRESHOLD", 0.45)
        self.top_k = getattr(settings, "CONCEPT_TOP_K", 5)
        self.graph_service = KnowledgeGraphService()
        self.retriever = self._init_retriever()

    def _init_retriever(self) -> ConceptRetriever:
        base_dir = Path(__file__).resolve().parents[3]
        concepts_file = base_dir / "knowledge_graph" / "concepts.json"
        
        if not concepts_file.exists():
            concepts_file = Path(__file__).resolve().parents[4] / "knowledge_graph" / "concepts.json"

        concepts = []
        if concepts_file.exists():
            with open(concepts_file, "r", encoding="utf-8") as f:
                concepts = json.load(f)
        else:
            logger.warning(f"concepts.json not found at {concepts_file}, using default fallback concept dataset")
            concepts = [
                {"name": "Quadratic Factorization", "description": "Factoring quadratic expressions", "subject": "Mathematics", "domain": "Algebra", "topic": "Polynomials"},
                {"name": "Linear Equations", "description": "Solving linear equations", "subject": "Mathematics", "domain": "Algebra", "topic": "Linear Equations"},
                {"name": "Fractions", "description": "Rational number operations", "subject": "Mathematics", "domain": "Arithmetic", "topic": "Fractions"},
                {"name": "Circles", "description": "Circle area and radius geometry", "subject": "Mathematics", "domain": "Geometry", "topic": "Circles"},
                {"name": "Mean", "description": "Arithmetic mean average", "subject": "Mathematics", "domain": "Statistics", "topic": "Mean"}
            ]

        return ConceptRetriever(concepts)

    def identify_concept(
        self,
        question: str,
        student_answer: str,
        work_evidence: str = "",
        error_type: str = None
    ) -> ConceptClassificationResponse:
        """
        Retrieves top candidate concepts via cosine similarity embedding, validates against Knowledge Graph,
        and returns concept hierarchy, prerequisites, and related concepts.
        """
        # Construct input context string
        query_parts = [f"[QUESTION]\n{question}"]
        if student_answer:
            query_parts.append(f"[STUDENT ANSWER]\n{student_answer}")
        if work_evidence:
            query_parts.append(f"[STUDENT WORK]\n{work_evidence}")
        
        query_text = "\n\n".join(query_parts)

        # Retrieve top embedding candidates
        candidates = self.retriever.retrieve_candidates(
            query_text=query_text,
            error_type=error_type,
            top_k=self.top_k
        )

        if not candidates:
            return self._unknown_concept_response()

        top_concept, sim_score = candidates[0]

        # Apply confidence threshold fallback
        if sim_score < self.similarity_threshold:
            logger.info(f"Top candidate '{top_concept.get('name')}' score {sim_score:.4f} below threshold {self.similarity_threshold}. Returning UNKNOWN.")
            return self._unknown_concept_response()

        concept_name = top_concept.get("name")

        # Knowledge Graph enrichment
        kg_context = self.graph_service.get_concept_context(concept_name)

        return ConceptClassificationResponse(
            concept=concept_name,
            confidence=round(float(sim_score), 4),
            hierarchy=kg_context.get("hierarchy", []),
            prerequisites=kg_context.get("prerequisites", []),
            related_concepts=kg_context.get("related_concepts", [])
        )

    def _unknown_concept_response(self) -> ConceptClassificationResponse:
        return ConceptClassificationResponse(
            concept="UNKNOWN",
            confidence=0.0,
            hierarchy=[],
            prerequisites=[],
            related_concepts=[]
        )

# Singleton instance for service reuse
_concept_engine_service = None

def get_concept_engine_service() -> ConceptEngineService:
    global _concept_engine_service
    if _concept_engine_service is None:
        _concept_engine_service = ConceptEngineService()
    return _concept_engine_service
