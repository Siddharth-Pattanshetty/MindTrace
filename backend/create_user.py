import sys
from app.db.session import SessionLocal
from app.models.domain import User
from app.core.security import get_password_hash

def create_new_user(email, password, full_name):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                hashed_password=get_password_hash(password),
                full_name=full_name,
                role="student"
            )
            db.add(user)
            db.commit()
            print(f"User created: {email} / {password}")
        else:
            print(f"User already exists: {email}")
    finally:
        db.close()

if __name__ == "__main__":
    create_new_user("hello@mindtrace.ai", "hello1234", "Hello User")
