from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

# Auth Schemas
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: Optional[str] = "student"

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

    model_config = ConfigDict(from_attributes=True)

# Exam Schemas
class ExamCreate(BaseModel):
    title: str
    subject: Optional[str] = "Mathematics"
    raw_text: Optional[str] = None

class QuestionResponse(BaseModel):
    id: int
    question_number: str
    text: str
    expected_answer: str
    max_marks: float
    concept_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class StudentAnswerResponse(BaseModel):
    id: int
    question_id: int
    student_raw_text: str

    model_config = ConfigDict(from_attributes=True)

class EvaluationResponse(BaseModel):
    id: int
    question_id: int
    score: float
    max_score: float
    is_correct: bool
    sympy_verified: bool
    errors: List[Dict[str, Any]] = []

    model_config = ConfigDict(from_attributes=True)

class ExamResponse(BaseModel):
    id: int
    user_id: int
    title: str
    subject: str
    status: str
    score: float
    max_score: float
    created_at: datetime
    questions: List[QuestionResponse] = []

    model_config = ConfigDict(from_attributes=True)

# Diagnosis Schemas
class DiagnosisResponse(BaseModel):
    id: int
    exam_id: int
    user_id: int
    root_cause_title: str
    confidence: float
    evidence: List[str]
    affected_concepts: List[str]
    summary: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Practice Schemas
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

class PracticeSetResponse(BaseModel):
    id: int
    target_error_type: Optional[str] = None
    questions: List[PracticeQuestionResponse] = []

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

# Retest Schemas
class RetestSubmitRequest(BaseModel):
    retest_id: int
    answers: List[Dict[str, Any]] # [{"question_id": 1, "student_answer": "..."}]

class RetestResponse(BaseModel):
    id: int
    status: str
    score: float
    improvement_text: str

# Mastery & Progress Schemas
class MasteryItem(BaseModel):
    concept: str
    mastery: float

class StudentProfileResponse(BaseModel):
    student_id: int
    full_name: str
    overall_health: float
    concept_mastery: Dict[str, float]
    recent_exams_count: int
    resolved_weaknesses: List[str]
    active_root_causes: List[str]

class ProgressHistoryItem(BaseModel):
    exam_id: int
    exam_title: str
    score: float
    date: str
    root_cause: str
    algebra_mastery: float
