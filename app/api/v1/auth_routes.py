from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models import User
from app.db.schemas import UserLogin, UserResponse
from app.db.session import get_db
from app.api.v1.auth import verify_password, create_access_token
from datetime import timedelta
from app.utils.decryptPassword import decrypt_password
router = APIRouter()

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()

    decrypted_password = decrypt_password(user_data.password)

    if not user or not verify_password(decrypted_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email")
    
    access_token = create_access_token({"sub": user.email}, timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

