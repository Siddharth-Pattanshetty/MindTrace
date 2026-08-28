from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any

class RetestSubmitRequest(BaseModel):
    retest_id: int
    answers: List[Dict[str, Any]]

class RetestResponse(BaseModel):
    id: int
    status: str
    score: float
    improvement_text: str

    model_config = ConfigDict(from_attributes=True)
