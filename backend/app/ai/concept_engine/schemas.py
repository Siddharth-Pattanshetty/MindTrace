from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ConceptClassificationRequest(BaseModel):
    question: str = Field(..., description="The mathematical question prompt")
    correct_answer: Optional[str] = Field(None, description="The correct answer")
    student_answer: str = Field(..., description="The student's submitted answer")
    work_evidence: Optional[str] = Field("", description="Student work evidence or explanation")
    error_type: Optional[str] = Field(None, description="Error type output from Error Classifier")

class ConceptClassificationResponse(BaseModel):
    concept: str = Field(..., description="Identified mathematical concept or UNKNOWN")
    confidence: float = Field(..., description="Cosine similarity retrieval confidence (0.0 to 1.0)")
    hierarchy: List[str] = Field(default_factory=list, description="Subject > Domain > Topic > Subtopic > Concept hierarchy")
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisite concepts")
    related_concepts: List[str] = Field(default_factory=list, description="Related mathematical concepts")

class AttemptAnalysisRequest(BaseModel):
    student_id: Optional[str] = Field("student_001", description="Student ID")
    subject: str = Field("MATHEMATICS", description="Subject name")
    question: str = Field(..., description="The mathematical question prompt")
    correct_answer: Optional[str] = Field(None, description="The correct answer")
    student_answer: str = Field(..., description="The student's submitted answer")
    work_evidence: Optional[str] = Field("", description="Student work evidence or explanation")

class ErrorDetail(BaseModel):
    type: str
    confidence: float

class ConceptDetail(BaseModel):
    name: str
    confidence: float

class RootCauseDetail(BaseModel):
    root_cause: str
    calibrated_probability: float
    raw_probability: float
    calibration_method: str

class RecommendationDetail(BaseModel):
    action: str
    target_concept: str
    reasoning: str
    suggested_practice_topics: List[str]

class AttemptAnalysisResponse(BaseModel):
    subject: str = "MATHEMATICS"
    error_type: str
    error_confidence: float
    concept: str
    concept_confidence: float
    root_cause: str
    root_cause_probability: float
    raw_root_cause_probability: Optional[float] = None
    calibration_method: Optional[str] = None
    error_detail: Optional[ErrorDetail] = None
    concept_detail: Optional[ConceptDetail] = None
    root_cause_detail: Optional[RootCauseDetail] = None
    recommendation: Optional[RecommendationDetail] = None
    hierarchy: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    related_concepts: List[str] = Field(default_factory=list)
