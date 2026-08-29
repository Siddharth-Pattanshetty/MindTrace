from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class MasteryPredictionRequest(BaseModel):
    student_id: Optional[str] = "student_001"
    concept: Optional[str] = "Linear Equations"
    previous_accuracy: Optional[float] = 0.70
    practice_accuracy: Optional[float] = 0.75
    retest_accuracy: Optional[float] = 0.70
    recent_accuracy: Optional[float] = 0.72
    previous_error_rate: Optional[float] = 0.28
    error_recurrence: Optional[float] = 0.10
    question_difficulty: Optional[float] = 0.50
    concept_difficulty: Optional[float] = 0.50
    time_between_attempts_log: Optional[float] = 0.0
    previous_attempts: Optional[int] = 3
    prerequisite_mastery: Optional[float] = 0.75

class MasteryPredictionResponse(BaseModel):
    concept: str
    mastery: float
    probability_of_success: float
    trend: str
    model_name: str = "MindTrace Mastery Predictor"
