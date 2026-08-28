from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.domain import Exam, Diagnosis, Question, Evaluation, ErrorItem, User, Intervention
from app.diagnostics.root_cause_engine import root_cause_engine
from app.practice.practice_engine import practice_engine

class DiagnosisService:
    """
    Orchestrates exam diagnosis, root cause inference, confidence calculation, and intervention planning.
    """
    
    def diagnose_exam(self, db: Session, exam: Exam, user: User) -> Diagnosis:
        existing = db.query(Diagnosis).filter(Diagnosis.exam_id == exam.id).first()
        if existing:
            return existing

        questions = db.query(Question).filter(Question.exam_id == exam.id).all()
        q_ids = [q.id for q in questions]

        evaluations = db.query(Evaluation).filter(Evaluation.question_id.in_(q_ids)).all() if q_ids else []
        
        evaluation_records = []
        for ev in evaluations:
            err = db.query(ErrorItem).filter(ErrorItem.evaluation_id == ev.id).first()
            evaluation_records.append({
                "question_number": f"Q{ev.question_id}",
                "is_correct": ev.is_correct,
                "score": ev.score,
                "concept": "Algebraic Manipulation",
                "error": {
                    "error_type": err.error_type if err else "PROCEDURAL_ERROR",
                    "explanation": err.explanation if err else "Error detected",
                    "confidence": err.confidence if err else 0.90,
                    "evidence": err.evidence if err else ""
                } if err else None
            })

        diag_data = root_cause_engine.diagnose_exam_errors(evaluation_records)

        diagnosis = Diagnosis(
            exam_id=exam.id,
            user_id=user.id,
            root_cause_title=diag_data["root_cause"],
            confidence=diag_data["confidence"],
            evidence_json=diag_data["evidence"],
            summary=diag_data["summary"]
        )
        db.add(diagnosis)
        db.commit()
        db.refresh(diagnosis)

        # Generate intervention
        intervention_plan = practice_engine.generate_intervention(diag_data["root_cause"])
        intervention = Intervention(
            diagnosis_id=diagnosis.id,
            user_id=user.id,
            root_cause_title=diag_data["root_cause"],
            levels_json=intervention_plan["levels"],
            status="IN_PROGRESS"
        )
        db.add(intervention)
        db.commit()

        return diagnosis

diagnosis_service = DiagnosisService()
