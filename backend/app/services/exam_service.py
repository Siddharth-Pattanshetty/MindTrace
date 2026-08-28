import os
import shutil
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.models.domain import Exam, Question, StudentAnswer, Evaluation, ErrorItem, User
from app.ai.document_processor import document_processor
from app.diagnostics.error_classifier import error_classifier

class ExamService:
    """
    Handles exam file upload, validation, document processing, and question extraction.
    """
    
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf", ".txt"}
    MAX_FILE_SIZE_MB = 10

    def validate_file(self, file: UploadFile) -> None:
        if not file or not file.filename:
            return
            
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file format '{ext}'. Allowed: JPG, PNG, PDF, TXT")

    def create_and_process_exam(
        self,
        db: Session,
        user: User,
        title: str,
        subject: str,
        file: Optional[UploadFile] = None,
        raw_text: Optional[str] = None
    ) -> Exam:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = None

        if file:
            self.validate_file(file)
            safe_filename = f"user_{user.id}_{os.path.basename(file.filename)}"
            file_path = os.path.join(upload_dir, safe_filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        exam = Exam(
            user_id=user.id,
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

        parsed_q_list = document_processor.process_document(file_path, raw_text)
        
        total_score = 0.0

        for q_data in parsed_q_list:
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
                user_id=user.id,
                student_raw_text=q_data["student_answer"],
                parsed_expression=q_data["student_answer"]
            )
            db.add(s_ans)
            db.commit()
            db.refresh(s_ans)

            eval_res = error_classifier.classify(q_data["student_answer"], q_data["expected_answer"], q_data.get("concept_code", "MANIP"))
            
            score = 10.0 if eval_res["is_correct"] else (4.0 if eval_res["error_type"] == "SIGN_ERROR" else 2.0)
            total_score += score

            evaluation = Evaluation(
                question_id=q_obj.id,
                student_answer_id=s_ans.id,
                score=score,
                max_score=q_obj.max_marks,
                is_correct=eval_res["is_correct"],
                sympy_verified=True
            )
            db.add(evaluation)
            db.commit()
            db.refresh(evaluation)

            if not eval_res["is_correct"]:
                err_item = ErrorItem(
                    evaluation_id=evaluation.id,
                    question_id=q_obj.id,
                    error_type=eval_res["error_type"],
                    explanation=eval_res["explanation"],
                    confidence=eval_res["confidence"],
                    evidence=eval_res["evidence"]
                )
                db.add(err_item)
                db.commit()

        exam.score = total_score
        exam.status = "COMPLETED"
        db.commit()
        db.refresh(exam)

        return exam

exam_service = ExamService()
