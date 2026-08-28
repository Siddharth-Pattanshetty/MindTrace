from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

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
