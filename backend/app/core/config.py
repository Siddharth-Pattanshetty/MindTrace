from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "MindTrace"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "mindtrace-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    # Database (Defaults to SQLite for local development, configurable to PostgreSQL)
    DATABASE_URL: str = "sqlite:///./mindtrace.db"
    
    # AI / LLM configuration
    OPENAI_API_KEY: Optional[str] = None
    LATENTCODE_LLM_URL: Optional[str] = None
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()
