from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.domain import User
from app.schemas.auth import UserCreate, UserLogin, Token
from app.schemas.user import UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role or "student"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login_user(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = create_access_token(user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "full_name": user.full_name
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user
