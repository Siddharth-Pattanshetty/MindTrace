from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="student") # student, teacher, admin
    created_at = Column(DateTime, default=datetime.utcnow)

    exams = relationship("Exam", back_populates="user")
    mastery_history = relationship("MasteryHistory", back_populates="user")

class Concept(Base):
    __tablename__ = "concepts"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Mathematics")
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)

    parent = relationship("Concept", remote_side=[id], backref="children")

class ConceptRelationship(Base):
    __tablename__ = "concept_relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    source_concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    target_concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    relationship_type = Column(String(50), default="DEPENDS_ON") # DEPENDS_ON, PREREQUISITE_OF

class Exam(Base):
    __tablename__ = "exams"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    subject = Column(String(100), default="Mathematics")
    file_path = Column(String(512), nullable=True)
    status = Column(String(50), default="COMPLETED") # UPLOADED, PROCESSING, COMPLETED, FAILED
    score = Column(Float, default=0.0)
    max_score = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="exams")
    questions = relationship("Question", back_populates="exam", cascade="all, delete-orphan")
    diagnoses = relationship("Diagnosis", back_populates="exam")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    question_number = Column(String(20), nullable=False)
    text = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=False)
    max_marks = Column(Float, default=10.0)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)

    exam = relationship("Exam", back_populates="questions")
    answers = relationship("StudentAnswer", back_populates="question", cascade="all, delete-orphan")
    evaluations = relationship("Evaluation", back_populates="question")

class StudentAnswer(Base):
    __tablename__ = "student_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_raw_text = Column(Text, nullable=False)
    parsed_expression = Column(Text, nullable=True)

    question = relationship("Question", back_populates="answers")
    evaluation = relationship("Evaluation", back_populates="student_answer", uselist=False)

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    student_answer_id = Column(Integer, ForeignKey("student_answers.id"), nullable=False)
    score = Column(Float, default=0.0)
    max_score = Column(Float, default=10.0)
    is_correct = Column(Boolean, default=False)
    sympy_verified = Column(Boolean, default=False)
    divergence_point = Column(Text, nullable=True)

    question = relationship("Question", back_populates="evaluations")
    student_answer = relationship("StudentAnswer", back_populates="evaluation")
    errors = relationship("ErrorItem", back_populates="evaluation", cascade="all, delete-orphan")

class ErrorItem(Base):
    __tablename__ = "errors"
    
    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    error_type = Column(String(100), nullable=False) # SIGN_ERROR, FACTORIZATION_ERROR, etc.
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    explanation = Column(Text, nullable=False)
    confidence = Column(Float, default=0.9)
    evidence = Column(Text, nullable=True)

    evaluation = relationship("Evaluation", back_populates="errors")

class Diagnosis(Base):
    __tablename__ = "diagnoses"
    
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    root_cause_concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    root_cause_title = Column(String(255), nullable=False)
    confidence = Column(Float, default=0.9)
    evidence_json = Column(JSON, nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    exam = relationship("Exam", back_populates="diagnoses")
    interventions = relationship("Intervention", back_populates="diagnosis")

class Intervention(Base):
    __tablename__ = "interventions"
    
    id = Column(Integer, primary_key=True, index=True)
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    root_cause_title = Column(String(255), nullable=False)
    levels_json = Column(JSON, nullable=False)
    status = Column(String(50), default="IN_PROGRESS") # IN_PROGRESS, COMPLETED
    created_at = Column(DateTime, default=datetime.utcnow)

    diagnosis = relationship("Diagnosis", back_populates="interventions")

class PracticeSet(Base):
    __tablename__ = "practice_sets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.id"), nullable=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    target_error_type = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("PracticeQuestion", back_populates="practice_set")

class PracticeQuestion(Base):
    __tablename__ = "practice_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    practice_set_id = Column(Integer, ForeignKey("practice_sets.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    target_error_type = Column(String(100), nullable=True)
    difficulty = Column(Integer, default=1)
    explanation = Column(Text, nullable=True)

    practice_set = relationship("PracticeSet", back_populates="questions")
    attempts = relationship("PracticeAttempt", back_populates="question")

class PracticeAttempt(Base):
    __tablename__ = "practice_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    practice_question_id = Column(Integer, ForeignKey("practice_questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    error_detected = Column(String(100), nullable=True)
    score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    question = relationship("PracticeQuestion", back_populates="attempts")

class Retest(Base):
    __tablename__ = "retests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    practice_set_id = Column(Integer, ForeignKey("practice_sets.id"), nullable=True)
    status = Column(String(50), default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)

    attempts = relationship("RetestAttempt", back_populates="retest")

class RetestAttempt(Base):
    __tablename__ = "retest_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    retest_id = Column(Integer, ForeignKey("retests.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=False)
    student_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    retest = relationship("Retest", back_populates="attempts")

class MasteryHistory(Base):
    __tablename__ = "mastery_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    mastery_score = Column(Float, nullable=False) # 0 to 100 percentage
    change_reason = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="mastery_history")
