import pytest
from app.ai.sympy_verifier import verify_answers, detect_detailed_error
from app.ai.document_processor import document_processor
from app.concepts.concept_graph import concept_graph
from app.diagnostics.root_cause_engine import root_cause_engine
from app.practice.practice_engine import practice_engine

def test_sympy_verifier():
    # Correct algebraic expansion
    is_correct, sympy_verified, error = verify_answers("x + 14", "x + 14")
    assert is_correct is True
    assert sympy_verified is True
    
    # Sign error detection
    is_correct, sympy_verified, error = verify_answers("6x - 23", "6x - 7")
    assert is_correct is False
    assert error == "SIGN_ERROR"

def test_document_processor():
    exam = document_processor.process_document("")
    assert len(exam) == 10
    assert exam[0]["question_number"] == "Q1"

def test_concept_graph():
    concept = concept_graph.get_concept("Factorization")
    assert concept["name"] == "Factorization"
    prereqs = concept_graph.get_prerequisites("FACT")
    assert "MANIP" in prereqs

def test_root_cause_engine():
    # Process standard exam
    exam_questions = document_processor.get_sample_math_exam()
    evaluations = []
    
    for q in exam_questions:
        res = detect_detailed_error(q["student_answer"], q["expected_answer"], q["concept_code"])
        evaluations.append({
            "question_number": q["question_number"],
            "is_correct": res["is_correct"],
            "score": res["score"],
            "concept": q["concept_code"],
            "error": res.get("error")
        })
        
    diagnosis = root_cause_engine.diagnose_exam_errors(evaluations)
    assert "Weak Algebraic Manipulation" in diagnosis["root_cause"]
    assert diagnosis["confidence"] >= 0.90
    assert len(diagnosis["evidence"]) > 0

def test_mastery_calculation():
    m = practice_engine.calculate_estimated_mastery(
        recent_perf=62.0,
        historical_perf=48.0,
        practice_perf=80.0,
        consistency=75.0
    )
    # 0.40*62 + 0.30*48 + 0.20*80 + 0.10*75 = 24.8 + 14.4 + 16.0 + 7.5 = 62.7
    assert m == 62.7
