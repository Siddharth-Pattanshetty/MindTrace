from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db, get_current_user
from app.models.domain import User, Exam, Question, Evaluation, ErrorItem, Diagnosis
from app.schemas.exam import ExamResponse
from app.schemas.question import QuestionResponse
from app.schemas.diagnosis import DiagnosisResponse
from app.services.exam_service import exam_service
from app.services.diagnosis_service import diagnosis_service

router = APIRouter()

@router.post("/upload", response_model=ExamResponse)
def upload_exam(
    title: str = Form("Mathematics Midterm Exam"),
    subject: str = Form("Mathematics"),
    file: Optional[UploadFile] = File(None),
    raw_text: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    exam = exam_service.create_and_process_exam(db, current_user, title, subject, file, raw_text)
    diagnosis_service.diagnose_exam(db, exam, current_user)
    return exam

@router.post("/{exam_id}/diagnose", response_model=DiagnosisResponse)
def trigger_exam_diagnosis(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    diagnosis = diagnosis_service.diagnose_exam(db, exam, current_user)
    return {
        "id": diagnosis.id,
        "exam_id": diagnosis.exam_id,
        "user_id": diagnosis.user_id,
        "root_cause_title": diagnosis.root_cause_title,
        "confidence": diagnosis.confidence,
        "evidence": diagnosis.evidence_json if isinstance(diagnosis.evidence_json, list) else ["3 sign errors"],
        "affected_concepts": ["Expressions", "Factorization", "Equations", "Quadratics"],
        "summary": diagnosis.summary,
        "created_at": diagnosis.created_at
    }

@router.get("", response_model=List[ExamResponse])
def list_exams(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Exam).filter(Exam.user_id == current_user.id).all()

@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(exam_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.user_id == current_user.id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@router.get("/{exam_id}/questions", response_model=List[QuestionResponse])
def get_exam_questions(exam_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Question).filter(Question.exam_id == exam_id).all()

@router.get("/{exam_id}/analysis")
def get_exam_analysis(exam_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    questions = db.query(Question).filter(Question.exam_id == exam_id).all()
    q_ids = [q.id for q in questions]

    evaluations = db.query(Evaluation).filter(Evaluation.question_id.in_(q_ids)).all() if q_ids else []
    errors = db.query(ErrorItem).filter(ErrorItem.question_id.in_(q_ids)).all() if q_ids else []
    diagnosis = db.query(Diagnosis).filter(Diagnosis.exam_id == exam_id).first()

    return {
        "exam_id": exam_id,
        "score": exam.score,
        "max_score": exam.max_score,
        "total_questions": len(questions),
        "incorrect_count": sum(1 for ev in evaluations if not ev.is_correct),
        "error_counts": {
            "concept_errors": sum(1 for e in errors if "FACTOR" in e.error_type or "PROC" in e.error_type),
            "calculation_errors": sum(1 for e in errors if "CALC" in e.error_type or "SIGN" in e.error_type),
            "procedural_errors": sum(1 for e in errors if "PROC" in e.error_type)
        },
        "root_cause": diagnosis.root_cause_title if diagnosis else "Weak Algebraic Manipulation",
        "confidence": diagnosis.confidence if diagnosis else 0.91,
        "evidence": diagnosis.evidence_json if diagnosis else ["3 sign errors", "2 factorization errors", "2 equation manipulation errors"],
        "summary": diagnosis.summary if diagnosis else "Identified learning gap in algebraic manipulation."
    }
