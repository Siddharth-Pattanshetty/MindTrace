from typing import List, Dict, Any
from app.concepts.concept_graph import concept_graph

class RootCauseEngine:
    """
    Proprietary Forensic Root-Cause Diagnostic Engine for MindTrace.
    Performs deterministic pattern detection & prerequisite graph traversal across student errors.
    """
    
    def diagnose_exam_errors(self, evaluation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes evaluation results to identify the underlying root learning gap.
        """
        error_counts: Dict[str, int] = {}
        affected_concepts = set()
        evidence_list = []
        
        incorrect_evals = [e for e in evaluation_results if not e.get("is_correct")]
        
        if not incorrect_evals:
            return {
                "root_cause": "No Significant Learning Gap Detected",
                "confidence": 0.99,
                "evidence": ["Student answered all questions correctly."],
                "affected_concepts": [],
                "summary": "Mastery of current exam material is strong."
            }
            
        for eval_item in incorrect_evals:
            error = eval_item.get("error")
            concept = eval_item.get("concept", "Algebraic Manipulation")
            affected_concepts.add(concept)
            
            if error:
                e_type = error.get("error_type", "PROCEDURAL_ERROR")
                error_counts[e_type] = error_counts.get(e_type, 0) + 1
        
        # Build evidence descriptions
        sign_errors = error_counts.get("SIGN_ERROR", 0)
        fact_errors = error_counts.get("FACTORIZATION_ERROR", 0)
        proc_errors = error_counts.get("PROCEDURAL_ERROR", 0) + error_counts.get("GENERAL_ERROR", 0)
        calc_errors = error_counts.get("CALCULATION_ERROR", 0)
        
        if sign_errors > 0:
            evidence_list.append(f"{sign_errors} sign errors")
        if fact_errors > 0:
            evidence_list.append(f"{fact_errors} factorization errors")
        if proc_errors > 0:
            evidence_list.append(f"{proc_errors} equation manipulation errors")
        if calc_errors > 0:
            evidence_list.append(f"{calc_errors} arithmetic/calculation errors")

        # Determine root cause concept via prerequisite graph analysis
        affected_concept_codes = []
        for c in affected_concepts:
            concept_obj = concept_graph.get_concept(c)
            if concept_obj:
                affected_concept_codes.append(concept_obj["code"])
                
        root_concept_name = concept_graph.find_lowest_common_prerequisite(affected_concept_codes)
        
        # Calculate diagnostic confidence score
        # Base confidence from error sample size & error consistency
        total_errors = len(incorrect_evals)
        base_confidence = min(0.95, 0.70 + (total_errors * 0.03))
        
        if sign_errors >= 2 and fact_errors >= 1:
            base_confidence = max(base_confidence, 0.91)
            
        root_cause_title = f"Weak {root_concept_name}"
        
        summary_text = (
            f"Your lost marks are primarily due to weak {root_concept_name.lower()}. "
            f"This caused repeated sign, factorization, and equation-solving errors across {total_errors} questions. "
            f"Addressing this foundational prerequisite will resolve surface errors in higher-order topics."
        )

        return {
            "root_cause": root_cause_title,
            "confidence": round(base_confidence, 2),
            "evidence": evidence_list,
            "affected_concepts": list(affected_concepts) or ["Expressions", "Factorization", "Equations", "Quadratics"],
            "summary": summary_text,
            "error_breakdown": {
                "concept_errors": fact_errors + proc_errors,
                "calculation_errors": calc_errors + sign_errors,
                "procedural_errors": proc_errors
            }
        }

root_cause_engine = RootCauseEngine()
