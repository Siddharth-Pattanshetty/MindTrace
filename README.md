# MindTrace — AI-Powered Forensic Learning & Exam Diagnostic System

> **“Don’t just know what you got wrong. Discover why.”**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Flutter](https://img.shields.io/badge/Flutter-3.24-02569B?logo=flutter)](https://flutter.dev)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://python.org)
[![SymPy](https://img.shields.io/badge/SymPy-1.12-3B5526)](https://www.sympy.org/)

---

## 1. What MindTrace Is

**MindTrace** is an AI-powered personalized learning diagnostic platform. Instead of simply calculating an exam score (e.g. *"You scored 62/100"*), MindTrace traces a student's mistakes back to their underlying root learning gaps, generates targeted remediation, evaluates practice improvement, and tracks concept mastery longitudinally.

---

## 2. Problem Statement

Traditional examination systems answer:
> *“You lost 38 marks on this test.”*

Students remain unaware of **why** they failed or which prerequisite concepts caused the cascade of errors across different questions.

---

## 3. Solution: Software Debugging for Learning

MindTrace treats learning gaps like software bugs:

```text
Software Debugging              MindTrace
------------------              ---------
Bug                         ──► Wrong Answer
Error                       ──► Error Type (e.g. SIGN_ERROR)
Root Cause                  ──► Prerequisite Learning Gap (e.g. Weak Algebraic Manipulation)
Fix                         ──► Targeted Adaptive Practice
Regression Test             ──► Concept Retest Verification
```

---

## 4. Architecture

```text
Exam Submission / Document Processing
                │
                ▼
  PaddleOCR / Qwen2.5-VL Vision
                │
                ▼
   Structured Questions & Answers
                │
                ▼
   SymPy Verification Engine (Deterministic Math Correctness)
                │
                ▼
  Structured Error Taxonomy Classifier (SIGN_ERROR, FACTORIZATION_ERROR, etc.)
                │
                ▼
    Prerequisite Concept Graph Traversal (MiniLM + FAISS Embeddings)
                │
                ▼
     Root Cause Analysis & Confidence Engine
                │
                ▼
 Adaptive Intervention & Practice Generator (LLM / Rule Bank)
                │
                ▼
     Concept Retest System (Unseen similar problems)
                │
                ▼
  Mastery Engine & SQLite Persistence Dashboard
```

---

## 5. Technology Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy ORM, Alembic Migrations, Pydantic Settings, PyJWT
- **Database**: SQLite (`mindtrace.db`)
- **AI & Deterministic Math**:
  - **SymPy**: Deterministic mathematical expression parsing, normalization, and divergence isolation
  - **PaddleOCR / Qwen2.5-VL**: Visual exam page & handwriting OCR abstraction
  - **all-MiniLM-L6-v2 & FAISS**: Concept & question embeddings and semantic vector retrieval
  - **LLMService**: Unified provider abstraction supporting LatentCode API, OpenAI, or rule-based fallback
- **Frontend**: Flutter / Dart cross-platform mobile application
- **DevOps**: Docker, Docker Compose, Alembic

---

## 6. Repository Structure

```text
MindTrace/
├── backend/
│   ├── alembic/              # Alembic database migration scripts
│   ├── app/
│   │   ├── ai/               # OCR, Vision, LLM, SymPy & Embedding services
│   │   ├── api/              # REST endpoints (auth, exams, diagnosis, practice, retest, progress)
│   │   ├── concepts/         # Prerequisite Concept Graph definitions
│   │   ├── core/             # Configuration, Database session & JWT Security
│   │   ├── diagnostics/      # Error taxonomy classifier, Root-Cause & Confidence engines
│   │   ├── db/               # SQLAlchemy session & Base
│   │   ├── models/           # Domain ORM models (User, Exam, Diagnosis, Mastery, etc.)
│   │   ├── practice/         # Practice generator & re-test engine
│   │   ├── schemas/          # Pydantic request/response contract schemas
│   │   └── services/         # Service layer business logic
│   ├── tests/                # Unit, API, and End-to-End test suites
│   ├── connect_sqlite.py     # SQLite direct management script
│   └── requirements.txt
├── mobile/
│   └── mindtrace_mobile/     # Flutter mobile application
├── skills/                   # SkillPatch skill definitions
├── docker/                   # Dockerfile for backend
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 7. Environment Variables

Create `.env` inside `backend/` or root based on `.env.example`:

```env
PROJECT_NAME=MindTrace
VERSION=1.0.0
API_V1_STR=/api

SECRET_KEY=mindtrace-secret-key-change-in-production-2026
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

DATABASE_URL=sqlite:///./mindtrace.db

OPENAI_API_KEY=
LATENTCODE_LLM_URL=
LATENTCODE_API_KEY=

EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
```

---

## 8. Local Setup & Installation

### 8.1 Backend Setup

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 8.2 Database Setup & Alembic Migrations

Run Alembic migration to build SQLite schema:

```bash
cd backend
alembic upgrade head
```

Verify SQLite DB connection:
```bash
python connect_sqlite.py
```

### 8.3 Running FastAPI

```bash
python -m uvicorn app.main:app --reload --port 8000
```

- API Root: `http://localhost:8000/`
- Interactive Swagger Specs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

---

## 9. Running the Flutter Mobile Application

```bash
cd mobile/mindtrace_mobile
flutter pub get

# Run on Chrome / Web
flutter run -d chrome

# Run on Mobile Emulator or Device
flutter run
```

---

## 10. Running with Docker

```bash
docker-compose up --build
```

---

## 11. API Endpoints

- **Auth**:
  - `POST /api/auth/register`
  - `POST /api/auth/login`
  - `GET /api/auth/me`
- **Exams**:
  - `POST /api/exams/upload`
  - `GET /api/exams`
  - `GET /api/exams/{exam_id}`
  - `POST /api/exams/{exam_id}/diagnose`
- **Diagnosis**:
  - `GET /api/diagnosis/{diagnosis_id}`
  - `GET /api/diagnosis/{exam_id}/root-causes`
- **Practice**:
  - `POST /api/practice/generate`
  - `GET /api/practice/{practice_id}`
  - `POST /api/practice/{practice_id}/submit`
- **Retest**:
  - `POST /api/retest/generate`
  - `GET /api/retest/{retest_id}`
  - `POST /api/retest/{retest_id}/submit`
- **Progress**:
  - `GET /api/progress`
  - `GET /api/progress/concepts`
  - `GET /api/progress/history`

---

## 12. Diagnostic Pipeline & Mastery Calculation

### Error Taxonomy
Classifies errors into: `SIGN_ERROR`, `FACTORIZATION_ERROR`, `CALCULATION_ERROR`, `PROCEDURAL_ERROR`, `CONCEPT_ERROR`, `FORMULA_ERROR`, `INCOMPLETE_ANSWER`, `QUESTION_MISINTERPRETATION`, `UNIT_ERROR`, `CARELESS_ERROR`.

### Transparent Mastery Formula
$$\text{Mastery} = 40\% \times \text{Recent Perf} + 30\% \times \text{Historical Perf} + 20\% \times \text{Practice Perf} + 10\% \times \text{Consistency}$$

---

## 13. Running Tests

Run full test suite (Unit, API, and End-to-End learning loop):

```bash
cd backend
python -m pytest tests/
```

Run Flutter widget tests:
```bash
cd mobile/mindtrace_mobile
flutter test
```

---

## 14. Known Limitations

- MVP focuses primarily on Mathematics (Algebra, Factorization, Equations, Quadratics). Concept Graph is expandable to Calculus, Physics, and Chemistry.
- PaddleOCR and Qwen2.5-VL use fallback OCR/rule parsing when local GPU weights or external cloud Vision keys are unconfigured.

---

## 15. License

MIT License.
