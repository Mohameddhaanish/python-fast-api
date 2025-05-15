from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.models import User
from app.db.schemas import UserCreate, UserResponse,VerificationResponse
from app.db.session import get_db
from app.core.security import get_current_user
from app.api.v1 import auth
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
import os
router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME="mohameddhaanish@techmango.net" ,
    MAIL_PASSWORD=settings.GOOGLE_APP_KEY,
    MAIL_FROM="mohameddhaanish@techmango.net",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    USE_CREDENTIALS=True,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):

    db_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=auth.hash_password(user.hashed_password),
        is_active=user.is_active,
        is_verified=user.is_verified,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # return db_user
     # Send verification email
    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[db_user.email],
        body=f"Click to verify: http://localhost:8000/auth/verify/{db_user.verification_token}",
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)

    return db_user


@router.get("/verify/{token}", response_model=VerificationResponse)
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Invalid or expired token")

    user.is_verified = True
    user.is_active = True
    user.verification_token = None
    db.commit()

    return {"message": "Verification successful!"}



@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return {"message": "User deleted"}

@router.get("/me", response_model=UserResponse)
def get_current_user_data(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(User).filter(User.email == current_user["sub"]).first()