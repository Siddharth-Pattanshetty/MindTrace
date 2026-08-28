import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from typing import Dict, Any, Tuple, Optional

transformations = (standard_transformations + (implicit_multiplication_application,))

def parse_math_expression(expr_str: str) -> Optional[sp.Expr]:
    """Parse a math expression string into a SymPy expression safely."""
    if not expr_str or not expr_str.strip():
        return None
    
    cleaned = expr_str.strip().replace("^", "**").replace("=", "-(").replace(";", "")
    # Handle equation format if '=' present
    if "=" in expr_str:
        parts = expr_str.split("=")
        if len(parts) == 2:
            cleaned = f"({parts[0].strip()}) - ({parts[1].strip()})"

    try:
        return parse_expr(cleaned, transformations=transformations)
    except Exception:
        try:
            return sp.sympify(cleaned)
        except Exception:
            return None

def verify_answers(student_str: str, expected_str: str) -> Tuple[bool, bool, Optional[str]]:
    """
    Deterministic mathematical verification using SymPy.
    Returns: (is_correct, sympy_verified, error_type)
    """
    s_expr = parse_math_expression(student_str)
    e_expr = parse_math_expression(expected_str)
    
    if s_expr is None or e_expr is None:
        # Fallback to string equality comparison
        is_exact = student_str.strip().lower() == expected_str.strip().lower()
        return is_exact, False, None if is_exact else "GENERAL_ERROR"
    
    try:
        diff = sp.simplify(s_expr - e_expr)
        if diff == 0:
            return True, True, None
        
        # Check if difference is purely sign reversal (e.g. -(a - b) vs (a - b))
        sign_diff = sp.simplify(s_expr + e_expr)
        if sign_diff == 0:
            return False, True, "SIGN_ERROR"

        # Check sub-expression / term sign flip (e.g., constant or single variable term sign inversion)
        # If diff is an even multiple of a constant or term present in the expression, it indicates a sign error in expansion
        if diff.is_number or (hasattr(diff, "free_symbols") and len(diff.free_symbols) == 1):
            # Check if student expression matches after changing a term's sign or expanding with flipped sign
            return False, True, "SIGN_ERROR"
        
        # Check if student answer is off by a constant factor
        if s_expr != 0 and e_expr != 0:
            ratio = sp.simplify(s_expr / e_expr)
            if ratio.is_number and ratio != 1:
                if ratio == -1:
                    return False, True, "SIGN_ERROR"
                return False, True, "CALCULATION_ERROR"
        
        # Check factorization error: expand both and check if expanded form matches
        s_expanded = sp.expand(s_expr)
        e_expanded = sp.expand(e_expr)
        if sp.simplify(s_expanded - e_expanded) == 0:
            # Structurally mathematically equivalent, but factorization might be incomplete
            return False, True, "INCOMPLETE_ANSWER"
        
        # Check sign error on expanded
        if sp.simplify(s_expanded + e_expanded) == 0:
            return False, True, "SIGN_ERROR"
            
        return False, True, "PROCEDURAL_ERROR"
        
    except Exception:
        is_exact = student_str.strip().lower() == expected_str.strip().lower()
        return is_exact, False, None if is_exact else "GENERAL_ERROR"

def detect_detailed_error(student_str: str, expected_str: str, concept_code: str = "Algebraic Manipulation") -> Dict[str, Any]:
    """
    Evaluates mathematical answer and returns structured error details.
    """
    is_correct, sympy_verified, error_type = verify_answers(student_str, expected_str)
    
    if is_correct:
        return {
            "is_correct": True,
            "score": 10.0,
            "max_score": 10.0,
            "sympy_verified": sympy_verified,
            "error": None
        }
    
    # Map error type to specific taxonomy
    e_type = error_type or "PROCEDURAL_ERROR"
    
    explanation = "The student's answer does not mathematically match the expected solution."
    confidence = 0.95 if sympy_verified else 0.85
    
    if e_type == "SIGN_ERROR":
        explanation = "Sign error detected: A positive/negative sign was inverted during expansion or transposition."
        confidence = 0.96
    elif e_type == "CALCULATION_ERROR":
        explanation = "Arithmetic/coefficient calculation error detected in algebraic steps."
        confidence = 0.92
    elif e_type == "FACTORIZATION_ERROR" or "factor" in concept_code.lower():
        e_type = "FACTORIZATION_ERROR"
        explanation = "Incorrect factorization or invalid roots produced during expression expansion."
        confidence = 0.94
    elif e_type == "INCOMPLETE_ANSWER":
        explanation = "The expression is algebraically correct but incompletely factored or simplified."
        confidence = 0.90

    return {
        "is_correct": False,
        "score": 4.0 if e_type == "SIGN_ERROR" else (2.0 if e_type == "FACTORIZATION_ERROR" else 0.0),
        "max_score": 10.0,
        "sympy_verified": sympy_verified,
        "error": {
            "error_type": e_type,
            "concept": concept_code,
            "explanation": explanation,
            "confidence": confidence,
            "evidence": f"Student answered '{student_str}', expected '{expected_str}'"
        }
    }
