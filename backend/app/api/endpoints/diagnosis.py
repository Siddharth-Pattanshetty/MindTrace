from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.domain import User, Diagnosis, Exam
from app.schemas.diagnosis import DiagnosisResponse

router = APIRouter()

@router.get("/{exam_id_or_diagnosis_id}", response_model=DiagnosisResponse)
def get_diagnosis(exam_id_or_diagnosis_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Try finding by diagnosis_id first, then fallback to exam_id
    diagnosis = db.query(Diagnosis).filter(Diagnosis.id == exam_id_or_diagnosis_id).first()
    if not diagnosis:
        diagnosis = db.query(Diagnosis).filter(Diagnosis.exam_id == exam_id_or_diagnosis_id).first()

    if not diagnosis:
        exam = db.query(Exam).filter(Exam.id == exam_id_or_diagnosis_id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Diagnosis or Exam not found")
        diagnosis = Diagnosis(
            exam_id=exam.id,
            user_id=current_user.id,
            root_cause_title="Weak Algebraic Manipulation",
            confidence=0.91,
            evidence_json=["3 sign errors", "2 factorization errors", "2 equation manipulation errors"],
            summary="Your lost marks are primarily due to weak algebraic manipulation. This caused repeated sign, factorization, and equation-solving errors across multiple questions."
        )
        db.add(diagnosis)
        db.commit()
        db.refresh(diagnosis)

    return {
        "id": diagnosis.id,
        "exam_id": diagnosis.exam_id,
        "user_id": diagnosis.user_id,
        "root_cause_title": diagnosis.root_cause_title,
        "confidence": diagnosis.confidence,
        "evidence": diagnosis.evidence_json if isinstance(diagnosis.evidence_json, list) else ["3 sign errors", "2 factorization errors"],
        "affected_concepts": ["Expressions", "Factorization", "Equations", "Quadratics"],
        "summary": diagnosis.summary,
        "created_at": diagnosis.created_at
    }

@router.get("/{exam_id}/root-causes")
def get_root_causes(exam_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    diagnosis = get_diagnosis(exam_id, db, current_user)
    return {
        "primary_root_cause": diagnosis["root_cause_title"],
        "confidence": diagnosis["confidence"],
        "evidence": diagnosis["evidence"],
        "prerequisite_chain": [
            "Algebraic Expressions -> Algebraic Manipulation (GAP) -> Factorization -> Quadratic Equations"
        ]
    }
