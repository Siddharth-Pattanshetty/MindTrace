import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_classify_error_api():
    payload = {
        "question": "Solve 2x + 5 = 15",
        "correct_answer": "x = 5",
        "student_answer": "x = 10",
        "work_evidence": "Student subtracted 5 and then divided."
    }
    response = client.post("/api/ai/classify-error", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "error_type" in data
    assert "confidence" in data

def test_model_info_api():
    response = client.get("/api/ai/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_name"] == "MindTrace Error Classifier"
    assert "classes" in data

def test_classify_concept_api():
    payload = {
        "question": "Factorize x² - 5x + 6",
        "correct_answer": "(x-2)(x-3)",
        "student_answer": "(x-2)(x-4)",
        "work_evidence": "Student selected factors 2 and 4.",
        "error_type": "CONCEPT_ERROR"
    }
    response = client.post("/api/ai/classify-concept", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "concept" in data
    assert "hierarchy" in data
    assert "prerequisites" in data

def test_analyze_attempt_api():
    payload = {
        "question": "Factorize x² - 5x + 6",
        "correct_answer": "(x-2)(x-3)",
        "student_answer": "(x-2)(x-4)",
        "work_evidence": "Student selected factors 2 and 4."
    }
    response = client.post("/api/ai/analyze-attempt", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert "type" in data["error"]
    assert "confidence" in data["error"]
    assert "concept" in data
    assert "hierarchy" in data
    assert "prerequisites" in data
