from fastapi import APIRouter, Depends,HTTPException,responses
from sqlalchemy.orm import Session
from app.db.models import User
from app.db.schemas import UserCreate, UserResponse,VerificationResponse
from app.db.session import get_db
from app.core.security import get_current_user
from app.api.v1 import auth
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
from app.utils.decryptPassword import decrypt_password
import secrets

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
        body=f"Click to verify: http://localhost:8000/api/v1/users/verify/{db_user.verification_token}",
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)

    return db_user


@router.get("/verify/{token}", include_in_schema=False)
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Invalid or expired token")

    user.is_verified = True
    user.is_active = True
    user.verification_token = None
    db.commit()

    return responses.RedirectResponse("http://localhost:3000/login")


@router.post("/checkuser",response_model=VerificationResponse)
async def check_user(email:str,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    user.verification_token=secrets.token_hex(16)
    db.commit()

    message=MessageSchema(
        subject="Request to Change Password",
        recipients=[user.email],
        body=f"Click to change the password:http://localhost:8000/api/v1/users/forgot-password/{user.verification_token}",
        subtype="html"
    )

    fm=FastMail(conf)
    await fm.send_message(message)

    return {"message":"Please check your mail"}

@router.get("/forgot-password/{token}")
def forgot_password(token:str,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.verification_token == token).first()

    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    return responses.RedirectResponse(f"http://localhost:3000/changePassword/{token}")


@router.post("/change-password/{token}")
def forgot_password(token:str,password:str,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.verification_token == token).first()

    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    decrypted_password = decrypt_password(password)
    
    user.hashed_password=auth.hash_password(decrypted_password)
    user.verification_token=None
    db.commit()
    db.refresh(user)

    return {"message":"Password changed successfully"} 

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