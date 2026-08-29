import logging
import pandas as pd
from typing import Dict, Any, List
from app.ai.root_cause.schemas import RootCausePredictionRequest

logger = logging.getLogger("mindtrace.ai.root_cause.feature_builder")

# Exact feature names expected by mindtrace_root_cause_model.joblib Pipeline
EXACT_FEATURE_NAMES = [
    "error_type",
    "concept",
    "error_confidence",
    "concept_confidence",
    "concept_attempt_count",
    "concept_error_count",
    "concept_accuracy",
    "recent_error_count",
    "repeated_error_count",
    "recent_accuracy",
    "overall_accuracy",
    "recent_average_score",
    "score_trend",
    "concept_mastery",
    "prerequisite_mastery",
    "overall_mastery",
    "algebra_mastery",
    "calculation_mastery",
    "formula_mastery",
    "fraction_mastery",
    "algebra_error_count",
    "calculation_error_count",
    "sign_error_count",
    "formula_error_count",
    "fraction_error_count"
]

VALID_ERROR_TYPES = [
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

class RootCauseFeatureBuilder:
    """
    Constructs a 1-row pandas DataFrame matching the exact schema expected
    by the trained Root Cause pipeline model.
    """
    def build_features(self, request: RootCausePredictionRequest) -> pd.DataFrame:
        error_type = request.error_type if request.error_type in VALID_ERROR_TYPES else "PROCEDURAL_ERROR"
        concept = request.concept or "Algebraic Manipulation"

        # Construct single-row dictionary with strict schema types
        row = {
            "error_type": str(error_type),
            "concept": str(concept),
            "error_confidence": float(request.error_confidence if request.error_confidence is not None else 0.85),
            "concept_confidence": float(request.concept_confidence if request.concept_confidence is not None else 0.90),
            "concept_attempt_count": int(request.concept_attempt_count if request.concept_attempt_count is not None else 5),
            "concept_error_count": int(request.concept_error_count if request.concept_error_count is not None else 2),
            "concept_accuracy": float(request.concept_accuracy if request.concept_accuracy is not None else 0.60),
            "recent_error_count": int(request.recent_error_count if request.recent_error_count is not None else 3),
            "repeated_error_count": int(request.repeated_error_count if request.repeated_error_count is not None else 1),
            "recent_accuracy": float(request.recent_accuracy if request.recent_accuracy is not None else 0.50),
            "overall_accuracy": float(request.overall_accuracy if request.overall_accuracy is not None else 0.65),
            "recent_average_score": float(request.recent_average_score if request.recent_average_score is not None else 55.0),
            "score_trend": float(request.score_trend if request.score_trend is not None else -0.05),
            "concept_mastery": float(request.concept_mastery if request.concept_mastery is not None else 0.55),
            "prerequisite_mastery": float(request.prerequisite_mastery if request.prerequisite_mastery is not None else 0.60),
            "overall_mastery": float(request.overall_mastery if request.overall_mastery is not None else 0.62),
            "algebra_mastery": float(request.algebra_mastery if request.algebra_mastery is not None else 0.50),
            "calculation_mastery": float(request.calculation_mastery if request.calculation_mastery is not None else 0.70),
            "formula_mastery": float(request.formula_mastery if request.formula_mastery is not None else 0.65),
            "fraction_mastery": float(request.fraction_mastery if request.fraction_mastery is not None else 0.55),
            "algebra_error_count": int(request.algebra_error_count if request.algebra_error_count is not None else 2),
            "calculation_error_count": int(request.calculation_error_count if request.calculation_error_count is not None else 1),
            "sign_error_count": int(request.sign_error_count if request.sign_error_count is not None else 1),
            "formula_error_count": int(request.formula_error_count if request.formula_error_count is not None else 0),
            "fraction_error_count": int(request.fraction_error_count if request.fraction_error_count is not None else 0)
        }

        df = pd.DataFrame([row], columns=EXACT_FEATURE_NAMES)
        return df
