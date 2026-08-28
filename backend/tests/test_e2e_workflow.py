import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_complete_end_to_end_learning_loop():
    # 1. Register Student
    email = "e2e_student@mindtrace.ai"
    reg_res = client.post("/api/auth/register", json={
        "email": email,
        "password": "password123",
        "full_name": "E2E Student",
        "role": "student"
    })
    assert reg_res.status_code in (200, 400) # Created or already exists

    # 2. Login
    login_res = client.post("/api/auth/login", json={
        "email": email,
        "password": "password123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Get Auth User Profile
    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == email

    # 4. Upload Real Exam / Raw Submission
    upload_res = client.post("/api/exams/upload", data={"title": "End-to-End Benchmark Exam", "subject": "Mathematics"}, headers=headers)
    assert upload_res.status_code == 200
    exam = upload_res.json()
    exam_id = exam["id"]
    assert exam["status"] == "COMPLETED"

    # 5. Extract Questions
    q_res = client.get(f"/api/exams/{exam_id}/questions", headers=headers)
    assert q_res.status_code == 200
    questions = q_res.json()
    assert len(questions) == 10

    # 6. Diagnose Exam & Identify Root Cause
    diag_res = client.post(f"/api/exams/{exam_id}/diagnose", headers=headers)
    assert diag_res.status_code == 200
    diag = diag_res.json()
    assert "Weak Algebraic Manipulation" in diag["root_cause_title"]
    assert diag["confidence"] >= 0.90

    # 7. Retrieve Diagnosis Details
    d_get = client.get(f"/api/diagnosis/{diag['id']}", headers=headers)
    assert d_get.status_code == 200
    assert len(d_get.json()["evidence"]) > 0

    # 8. Generate Targeted Practice
    prac_gen = client.post("/api/practice/generate", json={"diagnosis_id": diag["id"], "concept": "Factorization", "count": 5}, headers=headers)
    assert prac_gen.status_code == 200
    pset = prac_gen.json()
    assert len(pset["questions"]) == 5

    # 9. Submit Practice Attempt & Verify SymPy Evaluation
    pq_id = pset["questions"][0]["id"]
    sub_prac = client.post(f"/api/practice/{pset['id']}/submit", json={"question_id": pq_id, "student_answer": "5x - 14"}, headers=headers)
    assert sub_prac.status_code == 200
    attempt = sub_prac.json()
    assert attempt["is_correct"] is True
    assert attempt["updated_mastery"] > 0

    # 10. Generate Retest (Conceptually similar unseen problems)
    rt_gen = client.post("/api/retest/generate", headers=headers)
    assert rt_gen.status_code == 200
    retest_data = rt_gen.json()
    retest_id = retest_data["retest_id"]

    # 11. Submit Retest & Verify Mastery Recovery
    rt_sub = client.post(f"/api/retest/{retest_id}/submit", json={
        "answers": [
            {"student_answer": "6x + 7", "expected_answer": "6x + 7", "question_text": "Q1"},
            {"student_answer": "(2x + 1)(x + 4)", "expected_answer": "(2x + 1)(x + 4)", "question_text": "Q2"}
        ]
    }, headers=headers)
    assert rt_sub.status_code == 200
    sub_res = rt_sub.json()
    assert sub_res["score"] == 100.0

    # 12. Retrieve Longitudinal Progress Dashboard
    prog_res = client.get("/api/progress", headers=headers)
    assert prog_res.status_code == 200
    prog = prog_res.json()
    assert "algebra_mastery" in str(prog)
