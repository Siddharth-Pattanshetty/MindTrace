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
    model_name: str
    version: str
    algorithm: str
    dataset: str
    classes: List[str]
    metadata: Optional[Dict[str, Any]] = None
