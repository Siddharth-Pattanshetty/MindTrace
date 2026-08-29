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
    
    # Neo4j Graph Database
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "mindtrace_password"
    NEO4J_DATABASE: str = "neo4j"
    
    # Concept Engine Configuration
    CONCEPT_TOP_K: int = 5
    CONCEPT_SIMILARITY_THRESHOLD: float = 0.45
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    
    # Error Classifier Path
    ERROR_CLASSIFIER_PATH: str = "backend/models/mindtrace_error_classifier.joblib"
    
    # AI / LLM configuration
    OPENAI_API_KEY: Optional[str] = None
    LATENTCODE_LLM_URL: Optional[str] = None
    LATENTCODE_API_KEY: Optional[str] = None
    QWEN_VISION_MODEL_PATH: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()
