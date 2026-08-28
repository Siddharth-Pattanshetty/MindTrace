from pydantic import BaseModel, ConfigDict
from typing import List, Dict

class StudentProfileResponse(BaseModel):
    student_id: int
    full_name: str
    email: str
    overall_health: float
    concept_mastery: Dict[str, float]
    recent_exams_count: int
    resolved_weaknesses: List[str]
    active_root_causes: List[str]

    model_config = ConfigDict(from_attributes=True)

class ProgressHistoryItem(BaseModel):
    exam_id: int
    exam_title: str
    score: float
    date: str
    root_cause: str

    model_config = ConfigDict(from_attributes=True)
