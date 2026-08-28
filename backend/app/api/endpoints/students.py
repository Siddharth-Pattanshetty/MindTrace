from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.api.deps import get_db, get_current_user
from app.models.domain import User, Exam, Diagnosis
from app.services.mastery_service import mastery_service

router = APIRouter()

@router.get("/{student_id}/profile")
def get_student_profile(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == student_id).first()
    if not user:
        user = current_user

    concept_mastery = mastery_service.get_user_concept_mastery(db, user.id)
    overall_health = concept_mastery.get("Algebra", 0.0)

    exams_count = db.query(Exam).filter(Exam.user_id == user.id).count()

    latest_exam = db.query(Exam).filter(Exam.user_id == user.id).order_by(Exam.created_at.desc()).first()
    active_root_causes = []
    if latest_exam:
        diag = db.query(Diagnosis).filter(Diagnosis.exam_id == latest_exam.id).first()
        if diag and "No Significant" not in diag.root_cause_title:
            active_root_causes.append(diag.root_cause_title)

    resolved_weaknesses = []
    for concept_name, score in concept_mastery.items():
        if score >= 75.0:
            resolved_weaknesses.append(concept_name)

    return {
        "student_id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "overall_health": overall_health,
        "trend": "Improving" if overall_health >= 60 else ("Assessment Pending" if exams_count == 0 else "Requires Focus"),
        "concept_mastery": concept_mastery,
        "recent_exams_count": exams_count,
        "resolved_weaknesses": resolved_weaknesses,
        "active_root_causes": active_root_causes
    }

@router.get("/{student_id}/mastery")
def get_student_mastery(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == student_id).first() or current_user
    return mastery_service.get_user_concept_mastery(db, user.id)

@router.get("/{student_id}/history")
def get_student_history(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == student_id).first() or current_user
    analysis = mastery_service.get_longitudinal_analysis(db, user.id)
    return analysis["history"]
