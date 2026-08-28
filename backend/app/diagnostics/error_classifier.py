from typing import Dict, Any, Optional
from app.ai.math_service import math_service

TAXONOMY_TYPES = [
    "SIGN_ERROR",
    "FACTORIZATION_ERROR",
    "CALCULATION_ERROR",
    "PROCEDURAL_ERROR",
    "CONCEPT_ERROR",
    "FORMULA_ERROR",
    "INCOMPLETE_ANSWER",
    "QUESTION_MISINTERPRETATION",
    "UNIT_ERROR",
    "CARELESS_ERROR"
]

class ErrorClassifier:
    """
    Classifies student mistakes into the MindTrace structured Error Taxonomy.
    """
    
    def classify(self, student_answer: str, expected_answer: str, concept: str = "Algebraic Manipulation") -> Dict[str, Any]:
        eval_res = math_service.evaluate_and_classify(student_answer, expected_answer, concept)
        
        if eval_res.get("is_correct"):
            return {
                "is_correct": True,
                "error_type": None,
                "confidence": 1.0,
                "evidence": "Answer matches expected mathematical solution.",
                "explanation": "Correct answer."
            }
            
        err = eval_res.get("error", {})
        e_type = err.get("error_type", "PROCEDURAL_ERROR")
        if e_type not in TAXONOMY_TYPES:
            e_type = "PROCEDURAL_ERROR"

        return {
            "is_correct": False,
            "error_type": e_type,
            "confidence": err.get("confidence", 0.90),
            "evidence": err.get("evidence", f"Student answered '{student_answer}', expected '{expected_answer}'"),
            "explanation": err.get("explanation", "Mathematical solution diverged.")
        }

error_classifier = ErrorClassifier()
