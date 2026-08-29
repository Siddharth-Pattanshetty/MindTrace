import pandas as pd
from typing import Dict, Any
from app.ai.mastery.schemas import MasteryPredictionRequest

EXACT_MASTERY_FEATURE_NAMES = [
    "previous_accuracy",
    "practice_accuracy",
    "retest_accuracy",
    "recent_accuracy",
    "previous_error_rate",
    "question_difficulty",
    "concept_difficulty",
    "time_between_attempts_log",
    "previous_attempts",
    "prerequisite_mastery"
]

class MasteryFeatureBuilder:
    """
    Constructs a 1-row pandas DataFrame matching the exact 10-feature schema
    expected by mindtrace_mastery_model.joblib.
    """
    def build_features(self, request: MasteryPredictionRequest) -> pd.DataFrame:
        row = {
            "previous_accuracy": float(request.previous_accuracy if request.previous_accuracy is not None else 0.70),
            "practice_accuracy": float(request.practice_accuracy if request.practice_accuracy is not None else 0.75),
            "retest_accuracy": float(request.retest_accuracy if request.retest_accuracy is not None else 0.70),
            "recent_accuracy": float(request.recent_accuracy if request.recent_accuracy is not None else 0.72),
            "previous_error_rate": float(request.previous_error_rate if request.previous_error_rate is not None else 0.28),
            "question_difficulty": float(request.question_difficulty if request.question_difficulty is not None else 0.50),
            "concept_difficulty": float(request.concept_difficulty if request.concept_difficulty is not None else 0.50),
            "time_between_attempts_log": float(request.time_between_attempts_log if request.time_between_attempts_log is not None else 0.0),
            "previous_attempts": int(request.previous_attempts if request.previous_attempts is not None else 3),
            "prerequisite_mastery": float(request.prerequisite_mastery if request.prerequisite_mastery is not None else 0.75)
        }

        df = pd.DataFrame([row], columns=EXACT_MASTERY_FEATURE_NAMES)
        return df
