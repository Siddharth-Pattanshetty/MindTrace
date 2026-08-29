import pytest
from pathlib import Path
from app.ai.error_classifier.model_loader import ErrorClassifierModelLoader
from app.ai.error_classifier.predictor import ErrorClassifierPredictor
from app.ai.error_classifier.service import ErrorClassifierService
from app.ai.error_classifier.schemas import ErrorClassificationRequest

def test_model_loader_success():
    vectorizer, classifier, classes, metadata = ErrorClassifierModelLoader.load_model()
    assert classifier is not None
    assert metadata["model_name"] == "MindTrace Error Classifier"
    assert metadata["dataset"] == "MAP"

def test_predictor_format_input():
    predictor = ErrorClassifierPredictor()
    formatted = predictor.format_input("Solve 2x + 5 = 15", "x = 10", "Subtracted 5 then divided")
    assert "[QUESTION]\nSolve 2x + 5 = 15" in formatted
    assert "[STUDENT ANSWER]\nx = 10" in formatted
    assert "[STUDENT EXPLANATION]\nSubtracted 5 then divided" in formatted

def test_prediction_output():
    service = ErrorClassifierService()
    req = ErrorClassificationRequest(
        question="Solve 2x + 5 = 15",
        correct_answer="x = 5",
        student_answer="x = 10",
        work_evidence="Student subtracted 5 and then divided."
    )
    res = service.classify_error(req)
    assert res.error_type is not None
    assert isinstance(res.confidence, float)
    assert 0.0 <= res.confidence <= 1.0

def test_model_info():
    service = ErrorClassifierService()
    info = service.get_model_info()
    assert info.model_name == "MindTrace Error Classifier"
    assert len(info.classes) > 0
