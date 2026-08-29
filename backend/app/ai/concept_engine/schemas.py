from pydantic import BaseModel, Field
from typing import List, Optional

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

class AttemptAnalysisResponse(BaseModel):
    error: ErrorDetail
    concept: ConceptDetail
    hierarchy: List[str]
    prerequisites: List[str]
    related_concepts: List[str]
