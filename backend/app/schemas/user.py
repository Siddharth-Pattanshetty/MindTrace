from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

    model_config = ConfigDict(from_attributes=True)
