from typing import Dict, Any, Tuple
from app.ai.sympy_verifier import verify_answers, detect_detailed_error, parse_math_expression

class MathService:
    """
    Mathematical Verification & Parsing Service Abstraction powered by SymPy.
    """
    
    def parse_expression(self, expr_str: str):
        return parse_math_expression(expr_str)

    def verify_correctness(self, student_str: str, expected_str: str) -> Tuple[bool, bool, str]:
        return verify_answers(student_str, expected_str)

    def evaluate_and_classify(self, student_str: str, expected_str: str, concept: str = "Algebraic Manipulation") -> Dict[str, Any]:
        return detect_detailed_error(student_str, expected_str, concept)

math_service = MathService()
