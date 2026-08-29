from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

class RootCausePredictionRequest(BaseModel):
    student_id: Optional[str] = "student_001"
    subject: str = "MATHEMATICS"
    question: Optional[str] = None
    correct_answer: Optional[str] = None
    student_answer: Optional[str] = None
    work_evidence: Optional[str] = None
    
    error_type: Optional[str] = "PROCEDURAL_ERROR"
    concept: Optional[str] = "Algebraic Manipulation"
    error_confidence: Optional[float] = 0.85
    concept_confidence: Optional[float] = 0.90
    
    concept_attempt_count: Optional[int] = 5
    concept_error_count: Optional[int] = 2
    concept_accuracy: Optional[float] = 0.60
    
    recent_error_count: Optional[int] = 3
    repeated_error_count: Optional[int] = 1
    recent_accuracy: Optional[float] = 0.50
    overall_accuracy: Optional[float] = 0.65
    recent_average_score: Optional[float] = 55.0
    score_trend: Optional[float] = -0.05
    
    concept_mastery: Optional[float] = 0.55
    prerequisite_mastery: Optional[float] = 0.60
    overall_mastery: Optional[float] = 0.62
    
    algebra_mastery: Optional[float] = 0.50
    calculation_mastery: Optional[float] = 0.70
    formula_mastery: Optional[float] = 0.65
    fraction_mastery: Optional[float] = 0.55
    
    algebra_error_count: Optional[int] = 2
    calculation_error_count: Optional[int] = 1
    sign_error_count: Optional[int] = 1
    formula_error_count: Optional[int] = 0
    fraction_error_count: Optional[int] = 0

class RootCausePredictionResponse(BaseModel):
    root_cause: str
    calibrated_probability: float
    raw_probability: float
    calibrated_probabilities: Dict[str, float]
    raw_probabilities: Dict[str, float]
    subject: str = "MATHEMATICS"
    calibration_method: str
