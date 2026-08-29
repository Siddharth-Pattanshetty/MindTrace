import pytest
from app.ai.concept_engine.service import ConceptEngineService
from app.ai.concept_engine.schemas import ConceptClassificationRequest

@pytest.fixture
def concept_service():
    return ConceptEngineService()

def test_quadratic_factorization_identified(concept_service):
    res = concept_service.identify_concept(
        question="Factorize x² - 5x + 6",
        student_answer="(x-2)(x-4)",
        work_evidence="Student chose factors 2 and 4.",
        error_type="CONCEPT_ERROR"
    )
    assert res.concept == "Quadratic Factorization"
    assert res.confidence > 0.45
    assert "Polynomials" in res.hierarchy
    assert "Factor Pairs" in res.prerequisites or "Polynomial Operations" in res.prerequisites

def test_linear_equations_identified(concept_service):
    res = concept_service.identify_concept(
        question="Solve single variable linear equation 3x + 7 = 22",
        student_answer="x = 4",
        work_evidence="Subtracted 7 and divided by 3.",
        error_type="CALCULATION_ERROR"
    )
    assert "Linear Equations" in res.concept or res.concept == "Linear Equations"

def test_mean_identified(concept_service):
    res = concept_service.identify_concept(
        question="Calculate the arithmetic mean average of numbers 10, 20, 30",
        student_answer="15",
        work_evidence="Added numbers",
        error_type="CONCEPT_ERROR"
    )
    assert res.concept == "Mean"

def test_circles_identified(concept_service):
    res = concept_service.identify_concept(
        question="Find the area and radius of a circle with diameter 14 cm",
        student_answer="154 cm2",
        work_evidence="Used pi * r^2 formula",
        error_type="FORMULA_ERROR"
    )
    assert res.concept == "Circles"

def test_unknown_question_fallback(concept_service):
    res = concept_service.identify_concept(
        question="qwerty random gibberish xyz123 nonmathematical",
        student_answer="abc",
        work_evidence="",
        error_type="UNKNOWN"
    )
    # Either UNKNOWN or low confidence
    if res.concept != "UNKNOWN":
        assert res.confidence < 0.60
