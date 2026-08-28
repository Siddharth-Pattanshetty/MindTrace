import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
from app.api.api import api_router
import app.models.domain # ensure models are registered

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("mindtrace")

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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Completed request: {request.method} {request.url.path} -> Status {response.status_code}")
    return response

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.warning(f"Validation error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc), "error_type": "VALIDATION_ERROR"}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred in MindTrace diagnostic pipeline.", "error_type": "INTERNAL_SERVER_ERROR"}
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
