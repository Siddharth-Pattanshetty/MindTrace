from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
from app.api.api import api_router
from app.models import domain # ensure models are registered

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": "MindTrace AI Forensic Learning & Exam Diagnostic API",
        "tagline": "Don't just know what you got wrong. Discover why.",
        "status": "healthy",
        "version": settings.VERSION
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
