from fastapi import APIRouter
from app.api.endpoints import auth, exams, diagnosis, practice, retest, students, progress, ai

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(exams.router, prefix="/exams", tags=["exams"])
api_router.include_router(diagnosis.router, prefix="/diagnosis", tags=["diagnosis"])
api_router.include_router(practice.router, prefix="/practice", tags=["practice"])
api_router.include_router(retest.router, prefix="/retest", tags=["retest"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
