from typing import List, Dict, Any

class ConfidenceEngine:
    """
    Calculates diagnostic confidence score based on error repetition frequency,
    evidence consistency across questions, and historical performance.
    """
    
    def calculate_diagnostic_confidence(self, error_breakdown: Dict[str, int], total_questions: int) -> float:
        if total_questions == 0:
            return 0.50
            
        sign_errors = error_breakdown.get("SIGN_ERROR", 0)
        fact_errors = error_breakdown.get("FACTORIZATION_ERROR", 0)
        total_errors = sum(error_breakdown.values())

        if total_errors == 0:
            return 0.99

        # Base confidence from sample size
        base_conf = 0.70 + min(0.20, (total_errors / max(1, total_questions)) * 0.25)

        # Boost confidence when specific repeating patterns emerge across multiple questions
        if sign_errors >= 2 and fact_errors >= 1:
            base_conf = max(base_conf, 0.91)
        elif sign_errors >= 3:
            base_conf = max(base_conf, 0.93)

        return round(min(0.99, max(0.50, base_conf)), 2)

confidence_engine = ConfidenceEngine()
