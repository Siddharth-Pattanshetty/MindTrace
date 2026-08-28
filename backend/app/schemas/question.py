from pydantic import BaseModel, ConfigDict
from typing import Optional

class QuestionResponse(BaseModel):
    id: int
    question_number: str
    text: str
    expected_answer: str
    max_marks: float
    concept_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
