# MindTrace — Run & Setup Guide

This guide provides complete instructions to set up, configure API keys, and run the **MindTrace** AI-powered learning diagnostic system (Backend API, AI Diagnostic Pipeline, and Flutter Mobile Application).

---

## 1. Environment & API Key Configuration

Copy the example environment file `.env.example` to `.env` in the `backend/` directory or root:

```bash
cp .env.example backend/.env
```

### Environment Variables & API Key Reference

| Variable | Required? | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `SECRET_KEY` | **Required** | `mindtrace-secret-key-change-in-production-2026` | Secret key used for signing JWT authentication tokens. |
| `DATABASE_URL` | **Required** | `sqlite:///./mindtrace.db` | Database connection string. Supports SQLite locally or PostgreSQL (`postgresql://user:pass@localhost:5432/mindtrace`). |
| `OPENAI_API_KEY` | *Optional* | `""` | API key for OpenAI / LLM fallback interpretation and question generation. MindTrace runs deterministically with SymPy even without this key. |
| `LATENTCODE_LLM_URL` | *Optional* | `""` | Endpoint for LatentCode LLM agent service if running inside LatentCode environment. |
| `MATHPIX_APP_ID` | *Optional* | `""` | Mathpix OCR App ID for math image parsing. If omitted, built-in PaddleOCR & document processor are used. |
| `MATHPIX_APP_KEY` | *Optional* | `""` | Mathpix OCR App Key. |
| `EMBEDDING_MODEL_NAME` | **Required** | `all-MiniLM-L6-v2` | SentenceTransformer model name for FAISS concept & question embeddings. |

> **Note on AI Models:** MindTrace is designed to run locally out-of-the-box using **SymPy** for deterministic math verification, **all-MiniLM-L6-v2** for embeddings, and local rule engines for root-cause analysis. External API keys (`OPENAI_API_KEY` or `MATHPIX_APP_ID`) are completely optional and only needed if you want to extend LLM response generation or cloud OCR.

---

## 2. Running the Backend API (FastAPI)

### Prerequisites
- Python 3.12+

### Step-by-Step Backend Launch

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Start the FastAPI server using Uvicorn:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Verify Backend Status:**
   - Open your browser at `http://localhost:8000/`
   - Interactive Swagger API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

5. **Run Backend Test Suite:**
   ```bash
   python -m pytest tests/
   ```

---

## 3. Running the Mobile Application (Flutter)

### Prerequisites
- Flutter SDK (3.24+)
- Dart 3.5+
- Android Studio / VS Code / iOS Simulator / Web browser

### Step-by-Step Mobile Launch

1. **Navigate to the Flutter app directory:**
   ```bash
   cd mobile/mindtrace_mobile
   ```

2. **Fetch Flutter package dependencies:**
   ```bash
   flutter pub get
   ```

3. **Configure API Base Endpoint (if testing on device/emulator):**
   - For Android Emulator: API runs at `http://10.0.2.2:8000/api`
   - For Desktop / Web / Local testing: API runs at `http://127.0.0.1:8000/api`
   - Configured in `mobile/mindtrace_mobile/lib/services/api_service.dart`.

4. **Run the Flutter Mobile App:**
   ```bash
   # Run on Chrome / Web
   flutter run -d chrome

   # Run on connected Android / iOS device or emulator
   flutter run
   ```

5. **Run Flutter Widget Tests:**
   ```bash
   flutter test
   ```

---

## 4. Running via Docker Compose

To launch the complete MindTrace environment in Docker containers:

```bash
docker-compose up --build
```

This starts:
- **MindTrace FastAPI Backend**: Exposed at `http://localhost:8000`

To stop containers:
```bash
docker-compose down
```

---

## 5. End-to-End Hackathon Demo Flow

1. Start the FastAPI backend server (`http://localhost:8000`).
2. Launch the Flutter mobile app (`flutter run`).
3. **Home Screen**: Observe student overall learning health gauge (72%) and active root cause (*Weak Algebraic Manipulation*).
4. **Analyze Exam**: Tap `[ Analyze Exam ]` -> Upload or paste exam text -> Observe real-time progress steps (Document Processing -> SymPy Verification -> Root-Cause Traversal).
5. **Exam Autopsy Report**: View exam score (`62/100`), error breakdown (18 concept errors, 8 calculation errors, 7 procedural errors), and root cause banner with 91% diagnostic confidence.
6. **Root Cause Explanation**: View specific evidence (3 sign errors, 2 factorization errors, 2 equation manipulation errors) and the interactive **Prerequisite Dependency Graph**.
7. **Targeted Practice**: Solve 5 adaptive practice problems -> Get immediate feedback with sign error pattern checks -> Watch live estimated mastery updates (`52% → 61%`).
8. **Re-Test Verification**: Execute re-test with unseen, similar problems (`3x² + 8x + 4 = 0`) -> Verify conceptual mastery recovery (`48% → 83%`).
