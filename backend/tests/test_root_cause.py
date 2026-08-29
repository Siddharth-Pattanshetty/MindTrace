import pytest
import numpy as np
from app.ai.root_cause.service import RootCauseService
from app.ai.root_cause.schemas import RootCausePredictionRequest
from app.ai.root_cause.calibrator import ConfidenceCalibrator
from app.ai.root_cause.model_loader import RootCauseModelLoader

def test_root_cause_model_loader():
    model, classes, metadata = RootCauseModelLoader.load_root_cause_model()
    assert model is not None
    assert len(classes) == 10
    assert "ALGEBRAIC_MANIPULATION_WEAKNESS" in classes

def test_calibrator_model_loader():
    calib_model, calib_meta = RootCauseModelLoader.load_calibrator_model()
    assert calib_model is not None
    assert calib_meta.get("model_name") == "MindTrace Confidence Calibration"

def test_calibration_execution():
    calib_model, calib_meta = RootCauseModelLoader.load_calibrator_model()
    calibrator = ConfidenceCalibrator(calib_model, calib_meta)
    
    # Dummy raw probability vector across 10 classes
    raw_probs = np.array([0.5, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.03, 0.02])
    base_classes = [
        "ALGEBRAIC_MANIPULATION_WEAKNESS", "CALCULATION_WEAKNESS",
        "FORMULA_RECALL_WEAKNESS", "FRACTION_MANIPULATION_WEAKNESS",
        "INCONSISTENT_MASTERY", "INSUFFICIENT_EVIDENCE",
        "PROCEDURAL_MISUNDERSTANDING", "SIGN_ERROR_PATTERN",
        "WEAK_CONCEPT_UNDERSTANDING", "WEAK_PREREQUISITE"
    ]
    predicted_class = "ALGEBRAIC_MANIPULATION_WEAKNESS"
    
    calibrated_dict, calib_confidence = calibrator.calibrate(raw_probs, base_classes, predicted_class)
    
    assert isinstance(calibrated_dict, dict)
    assert len(calibrated_dict) == 10
    assert 0.0 <= calib_confidence <= 1.0
    assert not np.isnan(calib_confidence)
    assert not np.isinf(calib_confidence)
    # Check probability sum
    prob_sum = sum(calibrated_dict.values())
    assert abs(prob_sum - 1.0) < 1e-3

def test_root_cause_service_prediction():
    service = RootCauseService()
    req = RootCausePredictionRequest(
        student_id="student_001",
        subject="MATHEMATICS",
        error_type="SIGN_ERROR",
        concept="Quadratic Factorization",
        error_confidence=0.85,
        concept_confidence=0.90
    )
    res = service.predict_root_cause(req)
    
    assert res.root_cause in res.calibrated_probabilities
    assert 0.0 <= res.calibrated_probability <= 1.0
    assert 0.0 <= res.raw_probability <= 1.0
    assert res.subject == "MATHEMATICS"
    assert "Platt" in res.calibration_method or "Logistic" in res.calibration_method
