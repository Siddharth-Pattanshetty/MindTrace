from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.schemas.question import QuestionResponse

class ExamCreate(BaseModel):
    title: str
    subject: Optional[str] = "Mathematics"
    raw_text: Optional[str] = None

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
