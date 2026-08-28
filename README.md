# MindTrace — AI-Powered Forensic Learning & Exam Diagnostic System

> **“Don’t just know what you got wrong. Discover why.”**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Flutter](https://img.shields.io/badge/Flutter-3.38-02569B?logo=flutter)](https://flutter.dev)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://python.org)
[![SymPy](https://img.shields.io/badge/SymPy-1.14-3B5526)](https://www.sympy.org/)

---

## 1. Overview

**MindTrace** is an AI-powered learning diagnostic platform that analyzes a student's examination performance to identify the **underlying root cause of their mistakes**, rather than simply calculating a score.

### Core Philosophy: Software Debugging for Learning

```text
Software Debugging              MindTrace
------------------              ---------
Bug                         ──► Wrong Answer
Error                       ──► Error Type
Root Cause                  ──► Learning Root Cause
Fix                         ──► Targeted Intervention
Regression Test             ──► Re-Test Verification
```

Traditional exam systems report:
> *“You scored 62/100.”*

MindTrace reports:
> *“You lost marks primarily because of weak algebraic manipulation. This caused repeated sign, factorization, and equation-solving errors across multiple questions. Your mastery of the underlying concept is estimated at 48%. Here are targeted problems designed to address this weakness.”*

---

## 2. Architecture & Pipeline

```text
                         STUDENT
                            │
                            ▼
                     ┌───────────────┐
                     │ Exam Upload   │
                     └───────┬───────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ Document Processing   │
                 └───────────┬───────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
             Qwen2.5-VL            PaddleOCR
                  │                     │
                  └──────────┬──────────┘
                             ▼
                    Structured Document
                             │
                             ▼
                    Question/Answer Pair
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
         General Evaluation        Mathematics
                                      │
                                      ▼
                                    SymPy
                                      │
                                      ▼
                            Mathematical Verification
                │                         │
                └────────────┬────────────┘
                             ▼
                    Error Classification
                             │
                             ▼
                    Concept Identification
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
           MiniLM Embeddings        Concept Graph
                │                         │
                └────────────┬────────────┘
                             ▼
                       FAISS Retrieval
                             │
                             ▼
                    Root-Cause Engine
                             │
                             ▼
                     Student Profile
                             │
                             ▼
                     LatentCode Agent
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
         Practice       Explanation      Study Plan
             │
             ▼
          Re-test
             │
             ▼
       Mastery Update
```

---

## 3. Technology Stack

- **Frontend**: Flutter (Dart) — Cross-platform mobile application
- **Backend**: FastAPI (Python 3.12)
- **Database**: SQLAlchemy ORM with SQLite (development) & PostgreSQL support
- **AI & Deterministic Diagnostics**:
  - **SymPy**: Deterministic mathematical expression parsing, normalization, and divergence isolation
  - **Qwen2.5-VL / PaddleOCR**: Visual exam document understanding & handwriting OCR
  - **all-MiniLM-L6-v2**: Semantic embeddings for concepts, error explanations, and questions
  - **FAISS**: Vector search retrieval layer
  - **Root-Cause Diagnostic Engine**: Prerequisite graph traversal & pattern detection

---

## 4. Key Components

### 4.1 Structured Error Taxonomy
Supports minimum 10 error classifications:
- `SIGN_ERROR`
- `FACTORIZATION_ERROR`
- `CALCULATION_ERROR`
- `PROCEDURAL_ERROR`
- `CONCEPT_ERROR`
- `FORMULA_ERROR`
- `INCOMPLETE_ANSWER`
- `QUESTION_MISINTERPRETATION`
- `UNIT_ERROR`
- `CARELESS_ERROR`

### 4.2 Prerequisite Concept Graph
Mathematics core hierarchy:
```text
Algebraic Expressions
       │
       ▼ (depends on)
Algebraic Manipulation  <── [FOUNDATIONAL GAP]
       │
       ├──────────────┐
       ▼              ▼ (depends on)
Equations       Factorization
       │              │
       └──────┬───────┘
              ▼ (depends on)
      Quadratic Equations
```

### 4.3 MindTrace Estimated Mastery Formula
$$\text{Mastery} = 40\% \times \text{Recent Perf} + 30\% \times \text{Historical Perf} + 20\% \times \text{Practice Perf} + 10\% \times \text{Consistency}$$

---

## 5. SkillPatch & LatentCode Integration

- **SkillPatch Skill**: Located at `skills/mindtrace-exam-diagnosis/SKILL.md`
- **LatentCode Agent Orchestration**: Configured at `.latentcode/agents/mindtrace-agent.json`

---

## 6. Quick Start & Setup

### 6.1 Backend API Server

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Run test suite:
```bash
python -m pytest tests/
```

### 6.2 Flutter Mobile Application

```bash
cd mobile/mindtrace_mobile
flutter pub get
flutter run
```

Run widget tests:
```bash
flutter test
```

### 6.3 Docker Deployment

```bash
docker-compose up --build
```

---

## 7. Demo Walkthrough

1. **Home Screen**: View student learning health (72%) and active root cause.
2. **Upload Exam**: Upload math midterm paper or sample text. Watch real-time OCR and SymPy parsing.
3. **Exam Autopsy**: Observe score (62/100), error breakdown (18 concept, 8 calc, 7 procedural), and root cause banner.
4. **Root-Cause Explanation**: Examine evidence (3 sign errors, 2 factorization errors) and interactive Prerequisite Graph.
5. **Targeted Practice**: Complete 5 adaptive practice questions. Watch live mastery updates (52% → 61%).
6. **Re-Test & Progress**: Execute concept re-test with unseen, similar problems (`3x² + 8x + 4 = 0`) to verify mastery recovery (48% → 83%).

---

## 8. License

MIT License.
