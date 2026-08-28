from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "MindTrace"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    SECRET_KEY: str = "mindtrace-dev-secret-key-change-in-production-2026"
    JWT_ALGORITHM: str = "HS256"
    ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./mindtrace.db"
    
    # AI / LLM configuration
    OPENAI_API_KEY: Optional[str] = None
    LATENTCODE_LLM_URL: Optional[str] = None
    LATENTCODE_API_KEY: Optional[str] = None
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    QWEN_VISION_MODEL_PATH: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()
