from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.domain import User
from app.services.mastery_service import mastery_service

router = APIRouter()

@router.get("")
def get_longitudinal_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    analysis = mastery_service.get_longitudinal_analysis(db, current_user.id)
    return {
        "student_name": current_user.full_name,
        "overall_health": analysis["overall_health"],
        "longitudinal_insight": analysis["longitudinal_insight"],
        "concept_trends": analysis["concept_trends"],
        "history": analysis["history"]
    }

@router.get("/concepts")
def get_concept_mastery_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    mastery_map = mastery_service.get_user_concept_mastery(db, current_user.id)
    return {
        "user_id": current_user.id,
        "concepts": mastery_map
    }

@router.get("/history")
def get_assessment_history_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    analysis = mastery_service.get_longitudinal_analysis(db, current_user.id)
    return analysis["history"]
