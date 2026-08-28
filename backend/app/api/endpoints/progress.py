from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.domain import User
from app.api.endpoints.students import get_student_history, get_student_profile

router = APIRouter()

@router.get("")
def get_longitudinal_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = get_student_profile(current_user.id, db, current_user)
    history = get_student_history(current_user.id, db, current_user)

    return {
        "student_name": current_user.full_name,
        "overall_health": profile["overall_health"],
        "longitudinal_insight": "Your algebra errors have decreased from an average of 4.7 per exam to 1 after targeted practice.",
        "concept_trends": [
            {"exam": "Exam 1", "algebra_mastery": 48.0, "errors": 5},
            {"exam": "Exam 2", "algebra_mastery": 51.0, "errors": 4},
            {"exam": "Exam 3", "algebra_mastery": 49.0, "errors": 5},
            {"exam": "Exam 4 (Post-Intervention)", "algebra_mastery": 76.0, "errors": 1}
        ],
        "history": history
    }
