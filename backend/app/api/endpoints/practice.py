from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.domain import User, PracticeSet, PracticeQuestion, PracticeAttempt
from app.schemas.practice import PracticeGenerateRequest, PracticeSetResponse, PracticeSubmitRequest, PracticeAttemptResponse
from app.practice.practice_engine import practice_engine
from app.services.practice_service import practice_service
from app.services.mastery_service import mastery_service

router = APIRouter()

@router.post("/generate", response_model=PracticeSetResponse)
def generate_practice(
    req: PracticeGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return practice_service.generate_practice_set(db, current_user, req.diagnosis_id, req.concept or "Factorization", req.count or 5)

@router.get("/{practice_id}", response_model=PracticeSetResponse)
def get_practice_set(
    practice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pset = db.query(PracticeSet).filter(PracticeSet.id == practice_id).first()
    if not pset:
        raise HTTPException(status_code=404, detail="Practice set not found")
    return pset

@router.post("/{practice_id}/submit", response_model=PracticeAttemptResponse)
def submit_practice(
    practice_id: int,
    sub: PracticeSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pq = db.query(PracticeQuestion).filter(PracticeQuestion.id == sub.question_id).first()
    if not pq:
        raise HTTPException(status_code=404, detail="Practice question not found")

    eval_res = practice_engine.evaluate_attempt(sub.student_answer, pq.expected_answer, "Factorization")
    
    attempt = PracticeAttempt(
        practice_question_id=pq.id,
        user_id=current_user.id,
        student_answer=sub.student_answer,
        is_correct=eval_res["is_correct"],
        error_detected=eval_res["error"]["error_type"] if eval_res.get("error") else None,
        score=eval_res["score"]
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    new_mastery = mastery_service.update_mastery_from_history(
        db, current_user.id, "Algebraic Manipulation", reason="Targeted practice attempt submitted"
    )

    return {
        "attempt_id": attempt.id,
        "question_id": pq.id,
        "is_correct": eval_res["is_correct"],
        "score": eval_res["score"],
        "error_detected": attempt.error_detected,
        "updated_mastery": new_mastery,
        "explanation": pq.explanation or "Practice evaluation complete."
    }
