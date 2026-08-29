from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class ErrorClassificationRequest(BaseModel):
    question: str = Field(..., description="The mathematical question prompt")
    correct_answer: Optional[str] = Field(None, description="The correct answer to the question")
    student_answer: str = Field(..., description="The student's submitted answer")
    work_evidence: Optional[str] = Field("", description="Explanation or work evidence provided by student")

class ErrorClassificationResponse(BaseModel):
    error_type: str = Field(..., description="Predicted error category")
    confidence: float = Field(..., description="Probability confidence of the prediction")

class ModelInfoResponse(BaseModel):
    error_classifier: Optional[Dict[str, Any]] = None
    mastery_model: Optional[Dict[str, Any]] = None
    root_cause_model: Optional[Dict[str, Any]] = None
    confidence_calibration: Optional[Dict[str, Any]] = None
    model_name: Optional[str] = "MindTrace Complete AI Diagnostic Suite"
    version: Optional[str] = "1.0.0"
    algorithm: Optional[str] = None
    dataset: Optional[str] = None
    classes: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

