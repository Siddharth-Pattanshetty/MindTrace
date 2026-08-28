from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.domain import User, MasteryHistory, Concept, Exam, Question, Evaluation, ErrorItem, PracticeAttempt, RetestAttempt, Diagnosis
from app.practice.practice_engine import practice_engine

class MasteryService:
    """
    Handles persistent student mastery score calculation and progress tracking.
    Computes all statistics dynamically from database records.
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

    def get_user_concept_mastery(self, db: Session, user_id: int) -> Dict[str, float]:
        """
        Dynamically calculates concept mastery scores from persisted DB records.
        """
        concepts = db.query(Concept).all()
        mastery_map: Dict[str, float] = {}

        # Get overall exam average
        exams = db.query(Exam).filter(Exam.user_id == user_id).all()
        if not exams:
            return {"Algebra": 0.0, "Algebraic Manipulation": 0.0, "Factorization": 0.0, "Equations": 0.0, "Quadratic Equations": 0.0}

        recent_exam = exams[-1]
        recent_perf = (recent_exam.score / max(1.0, recent_exam.max_score)) * 100.0 if recent_exam.max_score else 0.0
        
        hist_scores = [(e.score / max(1.0, e.max_score)) * 100.0 for e in exams]
        historical_perf = sum(hist_scores) / len(hist_scores) if hist_scores else 0.0

        # Get practice accuracy
        practice_attempts = db.query(PracticeAttempt).filter(PracticeAttempt.user_id == user_id).all()
        if practice_attempts:
            correct_p = sum(1 for p in practice_attempts if p.is_correct)
            practice_perf = (correct_p / len(practice_attempts)) * 100.0
        else:
            practice_perf = historical_perf

        # Compute calculated mastery
        overall_mastery = practice_engine.calculate_estimated_mastery(
            recent_perf=recent_perf,
            historical_perf=historical_perf,
            practice_perf=practice_perf,
            consistency=85.0 if len(exams) > 1 else 60.0
        )

        for c in concepts:
            # Query recent MasteryHistory for concept
            mh = db.query(MasteryHistory).filter(
                MasteryHistory.user_id == user_id,
                MasteryHistory.concept_id == c.id
            ).order_by(MasteryHistory.created_at.desc()).first()

            if mh:
                mastery_map[c.name] = mh.mastery_score
            else:
                mastery_map[c.name] = overall_mastery

        if "Algebra" not in mastery_map:
            mastery_map["Algebra"] = overall_mastery
        if "Algebraic Manipulation" not in mastery_map:
            mastery_map["Algebraic Manipulation"] = overall_mastery

        return mastery_map

    def get_longitudinal_analysis(self, db: Session, user_id: int) -> Dict[str, Any]:
        """
        Builds longitudinal progress trends and error reduction insights from persisted DB data.
        """
        exams = db.query(Exam).filter(Exam.user_id == user_id).order_by(Exam.created_at.asc()).all()
        
        concept_trends = []
        history = []
        
        for idx, e in enumerate(exams):
            q_ids = [q.id for q in e.questions]
            error_count = db.query(ErrorItem).filter(ErrorItem.question_id.in_(q_ids)).count() if q_ids else 0
            
            pct = (e.score / max(1.0, e.max_score)) * 100.0
            diag = db.query(Diagnosis).filter(Diagnosis.exam_id == e.id).first()
            
            title = f"Exam {idx + 1}"
            if idx == len(exams) - 1 and idx > 0:
                title = f"Exam {idx + 1} (Post-Intervention)"

            concept_trends.append({
                "exam": title,
                "algebra_mastery": round(pct, 1),
                "errors": error_count
            })

            history.append({
                "exam_id": e.id,
                "title": e.title,
                "score": e.score,
                "max_score": e.max_score,
                "date": e.created_at.strftime("%Y-%m-%d"),
                "root_cause": diag.root_cause_title if diag else "Weak Algebraic Manipulation"
            })

        # Calculate insight string dynamically
        if len(concept_trends) >= 2:
            first_errs = concept_trends[0]["errors"]
            latest_errs = concept_trends[-1]["errors"]
            insight = f"Your algebra errors have decreased from {first_errs} in early assessments to {latest_errs} in recent practice."
        elif len(concept_trends) == 1:
            errs = concept_trends[0]["errors"]
            insight = f"Diagnostic assessment completed: {errs} learning errors identified requiring targeted practice."
        else:
            insight = "No exam history recorded yet. Upload an exam paper to begin forensic diagnosis."

        mastery_map = self.get_user_concept_mastery(db, user_id)
        overall_health = mastery_map.get("Algebra", 0.0)

        return {
            "overall_health": overall_health,
            "longitudinal_insight": insight,
            "concept_trends": concept_trends,
            "history": history
        }

mastery_service = MasteryService()
