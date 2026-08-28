from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.domain import User, PracticeSet, PracticeQuestion, PracticeAttempt
from app.practice.practice_engine import practice_engine

class PracticeService:
    """
    Handles practice question generation, attempt submission, and re-test workflows.
    """
    
    def generate_practice_set(self, db: Session, user: User, diagnosis_id: Optional[int] = None, concept: str = "Factorization", count: int = 5) -> PracticeSet:
        pset = PracticeSet(
            user_id=user.id,
            diagnosis_id=diagnosis_id,
            target_error_type="SIGN_ERROR"
        )
        db.add(pset)
        db.commit()
        db.refresh(pset)

        q_list = practice_engine.generate_practice_set(concept, count)
        for q_data in q_list:
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

        db.refresh(pset)
        return pset

practice_service = PracticeService()
