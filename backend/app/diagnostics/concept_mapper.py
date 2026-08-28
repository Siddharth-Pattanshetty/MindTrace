from typing import List, Dict, Any
from app.concepts.concept_graph import concept_graph

class ConceptMapper:
    """
    Maps detected errors and questions to concept graph nodes and prerequisite dependency chains.
    """
    
    def map_question_concept(self, question_text: str, concept_code_hint: str = "MANIP") -> Dict[str, Any]:
        concept = concept_graph.get_concept(concept_code_hint)
        prereqs = concept_graph.get_prerequisites(concept["code"]) if concept else []
        
        return {
            "concept_code": concept["code"] if concept else "MANIP",
            "concept_name": concept["name"] if concept else "Algebraic Manipulation",
            "category": concept["category"] if concept else "Algebra",
            "prerequisites": prereqs
        }

    def find_root_prerequisite(self, concept_codes: List[str]) -> str:
        return concept_graph.find_lowest_common_prerequisite(concept_codes)

concept_mapper = ConceptMapper()
