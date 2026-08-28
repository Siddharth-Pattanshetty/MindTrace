from typing import List, Dict, Any
from app.ai.sympy_verifier import detect_detailed_error

class PracticeEngine:
    """
    Generates adaptive interventions, targeted practice sets, re-test problems, and computes estimated mastery.
    """
    
    def generate_intervention(self, root_cause_title: str) -> Dict[str, Any]:
        """
        Builds a 4-level adaptive intervention roadmap.
        """
        return {
            "root_cause": root_cause_title,
            "levels": [
                {
                    "level": 1,
                    "title": "Basic Algebraic Manipulation & Sign Rules",
                    "description": "Master bracket expansion and sign distribution (e.g. -(a - b) = -a + b).",
                    "status": "UNLOCKED"
                },
                {
                    "level": 2,
                    "title": "Factorization & Common Terms",
                    "description": "Extract common algebraic terms and group quadratic expressions.",
                    "status": "LOCKED"
                },
                {
                    "level": 3,
                    "title": "Quadratic Equations & Equation Solving",
                    "description": "Apply zero-product property and solve equations with negative coefficients.",
                    "status": "LOCKED"
                },
                {
                    "level": 4,
                    "title": "Exam-Level Multistep Problems",
                    "description": "Solve multi-variable complex algebraic exam problems with zero sign errors.",
                    "status": "LOCKED"
                }
            ]
        }

    def generate_practice_set(self, concept_name: str = "Factorization", count: int = 5) -> List[Dict[str, Any]]:
        """
        Generates targeted practice questions targeting specific root errors.
        """
        pool = [
            {
                "question": "Simplify the expression: 4(2x - 5) - 3(x - 2)",
                "expected_answer": "5x - 14",
                "concept": "Algebraic Manipulation",
                "target_error": "SIGN_ERROR",
                "difficulty": 1,
                "explanation": "Expand 4(2x-5)=8x-20 and -3(x-2)=-3x+6. Combine like terms: 8x-3x=5x, -20+6=-14."
            },
            {
                "question": "Factorize completely: x^2 + 8x + 15",
                "expected_answer": "(x + 3)(x + 5)",
                "concept": "Factorization",
                "target_error": "FACTORIZATION_ERROR",
                "difficulty": 2,
                "explanation": "Find two numbers that multiply to 15 and add up to 8: 3 and 5."
            },
            {
                "question": "Solve for x: 5(x - 3) = 2(x + 6)",
                "expected_answer": "x = 9",
                "concept": "Equations",
                "target_error": "PROCEDURAL_ERROR",
                "difficulty": 2,
                "explanation": "5x - 15 = 2x + 12 -> 3x = 27 -> x = 9."
            },
            {
                "question": "Factorize completely: 3x^2 + 8x + 4",
                "expected_answer": "(3x + 2)(x + 2)",
                "concept": "Factorization",
                "target_error": "FACTORIZATION_ERROR",
                "difficulty": 3,
                "explanation": "Split middle term 8x into 6x + 2x: 3x(x + 2) + 2(x + 2) = (3x + 2)(x + 2)."
            },
            {
                "question": "Solve the quadratic equation: x^2 - 7x + 12 = 0",
                "expected_answer": "x = 3, x = 4",
                "concept": "Quadratic Equations",
                "target_error": "SIGN_ERROR",
                "difficulty": 3,
                "explanation": "Factorize to (x - 3)(x - 4) = 0. Roots are x = 3 and x = 4."
            }
        ]
        return pool[:count]

    def generate_retest_set(self) -> List[Dict[str, Any]]:
        """
        Generates unseen re-test questions that are conceptually similar to original exam questions (Section 18).
        """
        return [
            {
                "question": "Expand and simplify: 4(3x - 2) - 3(2x - 5)",
                "expected_answer": "6x + 7",
                "concept": "Algebraic Manipulation"
            },
            {
                "question": "Factorize completely: 2x^2 + 9x + 4",
                "expected_answer": "(2x + 1)(x + 4)",
                "concept": "Factorization"
            },
            {
                "question": "Solve the quadratic equation: x^2 - 6x + 8 = 0",
                "expected_answer": "x = 2, x = 4",
                "concept": "Quadratic Equations"
            }
        ]

    def evaluate_attempt(self, student_answer: str, expected_answer: str, concept: str) -> Dict[str, Any]:
        """
        Evaluates a practice attempt.
        """
        return detect_detailed_error(student_answer, expected_answer, concept)

    def calculate_estimated_mastery(
        self,
        recent_perf: float,
        historical_perf: float,
        practice_perf: float,
        consistency: float = 80.0
    ) -> float:
        """
        Section 19 Transparent Mastery Calculation Formula:
        Mastery = 40% recent performance + 30% historical performance + 20% practice performance + 10% consistency
        """
        mastery = (0.40 * recent_perf) + (0.30 * historical_perf) + (0.20 * practice_perf) + (0.10 * consistency)
        return round(min(100.0, max(0.0, mastery)), 1)

practice_engine = PracticeEngine()
