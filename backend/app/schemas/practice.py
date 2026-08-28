from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class PracticeGenerateRequest(BaseModel):
    diagnosis_id: Optional[int] = None
    concept: Optional[str] = "Factorization"
    count: Optional[int] = 5

class PracticeQuestionResponse(BaseModel):
    id: int
    practice_set_id: int
    question_text: str
    expected_answer: str
    concept_id: Optional[int] = None
    difficulty: int
    explanation: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PracticeSetResponse(BaseModel):
    id: int
    target_error_type: Optional[str] = None
    questions: List[PracticeQuestionResponse] = []

    model_config = ConfigDict(from_attributes=True)

class PracticeSubmitRequest(BaseModel):
    question_id: int
    student_answer: str

class PracticeAttemptResponse(BaseModel):
    attempt_id: int
    question_id: int
    is_correct: bool
    score: float
    error_detected: Optional[str] = None
    updated_mastery: float
    explanation: str
