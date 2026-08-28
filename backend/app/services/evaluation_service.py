from typing import Dict, Any
from app.ai.math_service import math_service
from app.diagnostics.error_classifier import error_classifier

class EvaluationService:
    """
    Handles mathematical evaluation and error classification for student answers.
    """
    
    def evaluate_student_answer(self, student_answer: str, expected_answer: str, concept: str = "Algebraic Manipulation") -> Dict[str, Any]:
        return error_classifier.classify(student_answer, expected_answer, concept)

evaluation_service = EvaluationService()
