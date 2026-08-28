from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.domain import User, Diagnosis, Exam
from app.schemas.diagnosis import DiagnosisResponse
from app.services.diagnosis_service import diagnosis_service

router = APIRouter()

@router.get("/{exam_id_or_diagnosis_id}", response_model=DiagnosisResponse)
def get_diagnosis(exam_id_or_diagnosis_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Query by diagnosis ID or exam ID
    diagnosis = db.query(Diagnosis).filter(Diagnosis.id == exam_id_or_diagnosis_id).first()
    if not diagnosis:
        diagnosis = db.query(Diagnosis).filter(Diagnosis.exam_id == exam_id_or_diagnosis_id).first()

    if not diagnosis:
        exam = db.query(Exam).filter(Exam.id == exam_id_or_diagnosis_id).first()
        if not exam:
            raise HTTPException(status_code=404, detail=f"No exam or diagnosis found for ID {exam_id_or_diagnosis_id}")
        
        # Execute real diagnosis pipeline
        diagnosis = diagnosis_service.diagnose_exam(db, exam, current_user)

    evidence_list = diagnosis.evidence_json if isinstance(diagnosis.evidence_json, list) else []

    return {
        "id": diagnosis.id,
        "exam_id": diagnosis.exam_id,
        "user_id": diagnosis.user_id,
        "root_cause_title": diagnosis.root_cause_title,
        "confidence": diagnosis.confidence,
        "evidence": evidence_list,
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
            f"Algebraic Expressions -> {diagnosis['root_cause_title']} (ROOT GAP) -> Higher Order Equations"
        ]
    }
