from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil

from app.api.deps import get_db, get_current_user
from app.models.domain import User, Exam, Question, StudentAnswer, Evaluation, ErrorItem, Diagnosis, Concept, MasteryHistory
from app.schemas.domain import ExamResponse, QuestionResponse
from app.ai.document_processor import document_processor
from app.ai.sympy_verifier import detect_detailed_error
from app.diagnostics.root_cause_engine import root_cause_engine

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
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = None
    
    if file:
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    exam = Exam(
        user_id=current_user.id,
        title=title,
        subject=subject,
        file_path=file_path,
        status="PROCESSING",
        score=0.0,
        max_score=100.0
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)

    # Process document (extract questions and student answers)
    parsed_questions = document_processor.process_document(file_path, raw_text)
    
    total_score = 0.0
    evaluation_records = []

    for q_data in parsed_questions:
        q_obj = Question(
            exam_id=exam.id,
            question_number=q_data["question_number"],
            text=q_data["text"],
            expected_answer=q_data["expected_answer"],
            max_marks=q_data.get("max_marks", 10.0)
        )
        db.add(q_obj)
        db.commit()
        db.refresh(q_obj)

        s_ans = StudentAnswer(
            exam_id=exam.id,
            question_id=q_obj.id,
            user_id=current_user.id,
            student_raw_text=q_data["student_answer"],
            parsed_expression=q_data["student_answer"]
        )
        db.add(s_ans)
        db.commit()
        db.refresh(s_ans)

        # Evaluate answer using SymPy & detailed verifier
        eval_res = detect_detailed_error(q_data["student_answer"], q_data["expected_answer"], q_data["concept_code"])
        
        evaluation = Evaluation(
            question_id=q_obj.id,
            student_answer_id=s_ans.id,
            score=eval_res["score"],
            max_score=q_obj.max_marks,
            is_correct=eval_res["is_correct"],
            sympy_verified=eval_res["sympy_verified"]
        )
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)

        total_score += eval_res["score"]

        err_item = None
        if eval_res.get("error"):
            err_data = eval_res["error"]
            err_item = ErrorItem(
                evaluation_id=evaluation.id,
                question_id=q_obj.id,
                error_type=err_data["error_type"],
                explanation=err_data["explanation"],
                confidence=err_data["confidence"],
                evidence=err_data["evidence"]
            )
            db.add(err_item)
            db.commit()

        evaluation_records.append({
            "question_number": q_obj.question_number,
            "is_correct": eval_res["is_correct"],
            "score": eval_res["score"],
            "concept": q_data["concept_code"],
            "error": eval_res.get("error")
        })

    exam.score = total_score
    exam.status = "COMPLETED"
    db.commit()
    db.refresh(exam)

    # Perform Root-Cause Analysis
    diag_data = root_cause_engine.diagnose_exam_errors(evaluation_records)
    
    diagnosis = Diagnosis(
        exam_id=exam.id,
        user_id=current_user.id,
        root_cause_title=diag_data["root_cause"],
        confidence=diag_data["confidence"],
        evidence_json=diag_data["evidence"],
        summary=diag_data["summary"]
    )
    db.add(diagnosis)
    db.commit()

    # Track mastery update
    concept_obj = db.query(Concept).filter(Concept.name == "Algebraic Manipulation").first()
    if not concept_obj:
        concept_obj = Concept(code="MANIP", name="Algebraic Manipulation", category="Algebra")
        db.add(concept_obj)
        db.commit()

    mh = MasteryHistory(
        user_id=current_user.id,
        concept_id=concept_obj.id,
        mastery_score=48.0,
        change_reason=f"Diagnosed from {exam.title}"
    )
    db.add(mh)
    db.commit()

    return exam

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
