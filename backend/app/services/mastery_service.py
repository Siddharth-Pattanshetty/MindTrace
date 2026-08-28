from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.domain import User, MasteryHistory, Concept
from app.practice.practice_engine import practice_engine

class MasteryService:
    """
    Handles persistent student mastery score calculation and progress tracking.
    """
    
    def calculate_and_save_mastery(
        self,
        db: Session,
        user: User,
        concept_name: str,
        recent_perf: float,
        historical_perf: float,
        practice_perf: float,
        reason: str = "Updated assessment"
    ) -> float:
        mastery = practice_engine.calculate_estimated_mastery(
            recent_perf=recent_perf,
            historical_perf=historical_perf,
            practice_perf=practice_perf,
            consistency=80.0
        )

        concept_obj = db.query(Concept).filter(Concept.name == concept_name).first()
        if not concept_obj:
            concept_obj = Concept(code="MANIP", name=concept_name, category="Algebra")
            db.add(concept_obj)
            db.commit()
            db.refresh(concept_obj)

        mh = MasteryHistory(
            user_id=user.id,
            concept_id=concept_obj.id,
            mastery_score=mastery,
            change_reason=reason
        )
        db.add(mh)
        db.commit()

        return mastery

mastery_service = MasteryService()
