import pytest
import numpy as np
from app.ai.mastery.service import MasteryService
from app.ai.mastery.schemas import MasteryPredictionRequest
from app.ai.mastery.model_loader import MasteryModelLoader

def test_mastery_model_loader():
    model, booster, metadata = MasteryModelLoader.load_mastery_model()
    assert model is not None
    assert booster is not None
    assert metadata.get("model_name") == "MindTrace Mastery Predictor"

def test_mastery_service_prediction():
    service = MasteryService()
    req = MasteryPredictionRequest(
        student_id="student_001",
        concept="Linear Equations",
        previous_accuracy=0.70,
        practice_accuracy=0.75,
        recent_accuracy=0.80
    )
    res = service.predict_mastery(req)

    assert res.concept == "Linear Equations"
    assert 0.0 <= res.mastery <= 1.0
    assert 0.0 <= res.probability_of_success <= 1.0
    assert res.trend in ["improving", "declining", "stable"]
    assert res.model_name == "MindTrace Mastery Predictor"
