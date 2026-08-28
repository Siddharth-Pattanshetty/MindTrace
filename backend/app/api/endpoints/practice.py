from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.models.domain import User, PracticeSet, PracticeQuestion, PracticeAttempt, MasteryHistory, Concept
from app.schemas.domain import PracticeGenerateRequest, PracticeSetResponse, PracticeSubmitRequest, PracticeAttemptResponse
from app.practice.practice_engine import practice_engine

router = APIRouter()

@router.post("/generate", response_model=PracticeSetResponse)
def generate_practice(
    req: PracticeGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pset = PracticeSet(
        user_id=current_user.id,
        diagnosis_id=req.diagnosis_id,
        target_error_type="SIGN_ERROR"
    )
    db.add(pset)
    db.commit()
    db.refresh(pset)

    generated_q_list = practice_engine.generate_practice_set(req.concept or "Factorization", req.count or 5)
    
    questions_out = []
    for q_data in generated_q_list:
        pq = PracticeQuestion(
            practice_set_id=pset.id,
            question_text=q_data["question"],
            expected_answer=q_data["expected_answer"],
            target_error_type=q_data["target_error"],
            difficulty=q_data["difficulty"],
            explanation=q_data["explanation"]
        )
        db.add(pq)
        db.commit()
        db.refresh(pq)
        questions_out.append(pq)

    return {
        "id": pset.id,
        "target_error_type": pset.target_error_type,
        "questions": questions_out
    }

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

    # Calculate updated estimated mastery (Section 19 formula)
    new_mastery = practice_engine.calculate_estimated_mastery(
        recent_perf=62.0,
        historical_perf=48.0,
        practice_perf=80.0 if eval_res["is_correct"] else 50.0,
        consistency=85.0
    )

    concept_obj = db.query(Concept).filter(Concept.name == "Algebraic Manipulation").first()
    if concept_obj:
        mh = MasteryHistory(
            user_id=current_user.id,
            concept_id=concept_obj.id,
            mastery_score=new_mastery,
            change_reason="Updated after targeted practice attempt"
        )
        db.add(mh)
        db.commit()

    return {
        "attempt_id": attempt.id,
        "question_id": pq.id,
        "is_correct": eval_res["is_correct"],
        "score": eval_res["score"],
        "error_detected": attempt.error_detected,
        "updated_mastery": new_mastery,
        "explanation": pq.explanation or "Practice complete."
    }
