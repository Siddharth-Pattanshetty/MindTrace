from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.api.deps import get_db, get_current_user
from app.models.domain import User, Retest, RetestAttempt
from app.schemas.retest import RetestResponse
from app.practice.practice_engine import practice_engine
from app.services.mastery_service import mastery_service

router = APIRouter()

@router.post("/generate")
def generate_retest(
    practice_set_id: int = 1,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    retest = Retest(
        user_id=current_user.id,
        practice_set_id=practice_set_id,
        status="PENDING"
    )
    db.add(retest)
    db.commit()
    db.refresh(retest)

    retest_q_list = practice_engine.generate_retest_set()
    return {
        "retest_id": retest.id,
        "status": retest.status,
        "questions": retest_q_list
    }

@router.get("/{retest_id}")
def get_retest(
    retest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    retest = db.query(Retest).filter(Retest.id == retest_id).first()
    if not retest:
        raise HTTPException(status_code=404, detail="Retest not found")
    return retest

@router.post("/{retest_id}/submit", response_model=RetestResponse)
def submit_retest(
    retest_id: int,
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    retest = db.query(Retest).filter(Retest.id == retest_id).first()
    if not retest:
        raise HTTPException(status_code=404, detail="Retest not found")

    answers = payload.get("answers", [])
    correct_count = 0
    total = len(answers) or 1

    for a in answers:
        s_ans = a.get("student_answer", "")
        exp_ans = a.get("expected_answer", "")
        eval_res = practice_engine.evaluate_attempt(s_ans, exp_ans, "Algebra")
        
        attempt = RetestAttempt(
            retest_id=retest.id,
            user_id=current_user.id,
            question_text=a.get("question_text", ""),
            expected_answer=exp_ans,
            student_answer=s_ans,
            is_correct=eval_res["is_correct"]
        )
        db.add(attempt)
        if eval_res["is_correct"]:
            correct_count += 1

    score_pct = (correct_count / total) * 100.0
    retest.status = "COMPLETED"
    db.commit()

    updated_mastery = mastery_service.update_mastery_from_history(
        db, current_user.id, "Algebraic Manipulation", reason="Re-test submission verified fix"
    )

    return {
        "id": retest.id,
        "status": "COMPLETED",
        "score": score_pct,
        "improvement_text": f"MindTrace verified your weakness resolution! Estimated mastery updated to {updated_mastery}%."
    }
