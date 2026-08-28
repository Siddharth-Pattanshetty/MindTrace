from typing import List, Dict, Any, Optional

MATH_CONCEPT_GRAPH = {
    "MATH": {
        "code": "MATH",
        "name": "Mathematics",
        "category": "Root",
        "description": "Mathematics root discipline",
        "parent": None
    },
    "ALG": {
        "code": "ALG",
        "name": "Algebra",
        "category": "Mathematics",
        "description": "Algebraic principles, variables, and transformations",
        "parent": "MATH"
    },
    "EXPR": {
        "code": "EXPR",
        "name": "Expressions",
        "category": "Algebra",
        "description": "Simplification, term expansion, and basic algebraic expressions",
        "parent": "ALG"
    },
    "MANIP": {
        "code": "MANIP",
        "name": "Algebraic Manipulation",
        "category": "Algebra",
        "description": "Sign handling, expanding brackets, and distributive laws",
        "parent": "ALG",
        "depends_on": ["EXPR"]
    },
    "EQN": {
        "code": "EQN",
        "name": "Equations",
        "category": "Algebra",
        "description": "Linear equation solving, variable isolation, and transposition",
        "parent": "ALG",
        "depends_on": ["MANIP"]
    },
    "FACT": {
        "code": "FACT",
        "name": "Factorization",
        "category": "Algebra",
        "description": "Common factor extraction, quadratic grouping, and root factorization",
        "parent": "ALG",
        "depends_on": ["MANIP"]
    },
    "QUAD": {
        "code": "QUAD",
        "name": "Quadratic Equations",
        "category": "Algebra",
        "description": "Solving second-degree polynomial equations and zero-product rule",
        "parent": "ALG",
        "depends_on": ["FACT", "EQN"]
    }
}

class ConceptGraph:
    """
    Manages concept hierarchy and prerequisite dependency graphs.
    """
    def __init__(self):
        self.nodes = MATH_CONCEPT_GRAPH

    def get_concept(self, code_or_name: str) -> Optional[Dict[str, Any]]:
        code_or_name_upper = code_or_name.upper()
        for k, v in self.nodes.items():
            if k == code_or_name_upper or v["name"].upper() == code_or_name_upper or v["code"].upper() == code_or_name_upper:
                return v
        return self.nodes.get("MANIP")

    def get_prerequisites(self, concept_code: str) -> List[str]:
        concept = self.get_concept(concept_code)
        if not concept:
            return []
        
        prereqs = concept.get("depends_on", [])
        all_prereqs = list(prereqs)
        for p in prereqs:
            all_prereqs.extend(self.get_prerequisites(p))
        return list(set(all_prereqs))

    def find_lowest_common_prerequisite(self, concept_codes: List[str]) -> str:
        """
        Given a list of affected concepts, finds the foundational root concept in the dependency tree.
        """
        prereq_counts: Dict[str, int] = {}
        for c in concept_codes:
            deps = self.get_prerequisites(c) + [c]
            for dep in deps:
                prereq_counts[dep] = prereq_counts.get(dep, 0) + 1
                
        # "MANIP" (Algebraic Manipulation) is the core prerequisite for Factorization, Equations, and Quadratics
        if prereq_counts.get("MANIP", 0) > 0:
            return "Algebraic Manipulation"
        
        # Sort by frequency of occurrence in dependency tree
        sorted_prereqs = sorted(prereq_counts.items(), key=lambda x: x[1], reverse=True)
        if sorted_prereqs:
            code = sorted_prereqs[0][0]
            concept = self.nodes.get(code)
            return concept["name"] if concept else "Algebraic Manipulation"

        return "Algebraic Manipulation"

concept_graph = ConceptGraph()
