import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_headers():
    reg_payload = {
        "email": "testapi_user@mindtrace.ai",
        "password": "password123",
        "full_name": "API Test User",
        "role": "student"
    }
    client.post("/api/auth/register", json=reg_payload)
    login_res = client.post("/api/auth/login", json={
        "email": "testapi_user@mindtrace.ai",
        "password": "password123"
    })
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_root_and_health():
    res = client.get("/")
    assert res.status_code == 200
    assert "MindTrace" in res.json()["message"]
    
    h_res = client.get("/health")
    assert h_res.status_code == 200
    assert h_res.json()["status"] == "ok"

def test_auth_endpoints():
    headers = get_auth_headers()
    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "testapi_user@mindtrace.ai"

def test_exam_upload_and_processing():
    headers = get_auth_headers()
    upload_res = client.post("/api/exams/upload", data={"title": "Maths Diagnostic Benchmark"}, headers=headers)
    assert upload_res.status_code == 200
    exam_data = upload_res.json()
    assert exam_data["id"] > 0
    assert exam_data["status"] == "COMPLETED"
    
    exam_id = exam_data["id"]
    
    q_res = client.get(f"/api/exams/{exam_id}/questions", headers=headers)
    assert q_res.status_code == 200
    assert len(q_res.json()) == 10
    
    an_res = client.get(f"/api/exams/{exam_id}/analysis", headers=headers)
    assert an_res.status_code == 200
    analysis = an_res.json()
    assert analysis["root_cause"] == "Weak Algebraic Manipulation"
    assert analysis["confidence"] >= 0.90

def test_diagnosis_endpoints():
    headers = get_auth_headers()
    d_res = client.get("/api/diagnosis/1", headers=headers)
    assert d_res.status_code == 200
    diag = d_res.json()
    assert "Weak Algebraic Manipulation" in diag["root_cause_title"]
    assert diag["confidence"] >= 0.90

    rc_res = client.get("/api/diagnosis/1/root-causes", headers=headers)
    assert rc_res.status_code == 200
    assert "primary_root_cause" in rc_res.json()

def test_practice_flow():
    headers = get_auth_headers()
    gen_res = client.post("/api/practice/generate", json={"concept": "Factorization", "count": 5}, headers=headers)
    assert gen_res.status_code == 200
    pset = gen_res.json()
    assert len(pset["questions"]) == 5
    
    sub_res = client.post(f"/api/practice/{pset['id']}/submit", json={
        "question_id": pset["questions"][0]["id"],
        "student_answer": "5x - 14"
    }, headers=headers)
    assert sub_res.status_code == 200
    attempt = sub_res.json()
    assert attempt["is_correct"] is True
    assert attempt["updated_mastery"] > 0

def test_retest_and_progress_flow():
    headers = get_auth_headers()
    rt_gen = client.post("/api/retest/generate", headers=headers)
    assert rt_gen.status_code == 200
    retest_data = rt_gen.json()
    retest_id = retest_data["retest_id"]
    
    rt_sub = client.post(f"/api/retest/{retest_id}/submit", json={
        "answers": [
            {"student_answer": "6x + 7", "expected_answer": "6x + 7", "question_text": "Q1"},
            {"student_answer": "(2x + 1)(x + 4)", "expected_answer": "(2x + 1)(x + 4)", "question_text": "Q2"}
        ]
    }, headers=headers)
    assert rt_sub.status_code == 200
    sub_res = rt_sub.json()
    assert sub_res["score"] == 100.0
    
    prog_res = client.get("/api/progress", headers=headers)
    assert prog_res.status_code == 200
    prog = prog_res.json()
    assert "longitudinal_insight" in prog
