"""
MindTrace SQLite Database Connection & Management Script
Connects to mindtrace.db using SQLAlchemy, verifies tables, and displays contents.
"""

import os
import sys
from sqlalchemy import inspect
from app.db.session import engine, SessionLocal, Base
from app.models.domain import (
    User, Exam, Question, StudentAnswer, Evaluation,
    ErrorItem, Diagnosis, Concept, MasteryHistory
)
from app.core.security import get_password_hash

def init_db():
    print("=" * 60)
    print("Connecting to SQLite database at: mindtrace.db")
    print("=" * 60)
    
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\nSuccessfully connected! Found {len(tables)} tables in SQLite database:")
    for t in sorted(tables):
        print(f"  - {t}")
        
    db = SessionLocal()
    try:
        # Check demo user
        demo_user = db.query(User).filter(User.email == "demo@mindtrace.ai").first()
        if not demo_user:
            demo_user = User(
                email="demo@mindtrace.ai",
                hashed_password=get_password_hash("demo1234"),
                full_name="Rahul Verma",
                role="student"
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print(f"\n[+] Created demo user: {demo_user.full_name} ({demo_user.email})")
        else:
            print(f"\n[+] Demo user exists: {demo_user.full_name} ({demo_user.email})")

        # Summary statistics
        user_count = db.query(User).count()
        exam_count = db.query(Exam).count()
        question_count = db.query(Question).count()
        diagnosis_count = db.query(Diagnosis).count()

        print("\nDatabase Statistics:")
        print(f"  • Users:      {user_count}")
        print(f"  • Exams:      {exam_count}")
        print(f"  • Questions:  {question_count}")
        print(f"  • Diagnoses:  {diagnosis_count}")
        
        # Display recent exams
        if exam_count > 0:
            print("\nRecent Exams in SQLite:")
            for e in db.query(Exam).limit(5).all():
                diag = db.query(Diagnosis).filter(Diagnosis.exam_id == e.id).first()
                rc = diag.root_cause_title if diag else "N/A"
                print(f"  [ID {e.id}] '{e.title}' | Score: {e.score}/{e.max_score} | Root Cause: {rc}")
        
        print("\nSQLite Database connection is fully operational and healthy!")
        print("=" * 60)

    except Exception as ex:
        print(f"[-] Database error: {ex}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
