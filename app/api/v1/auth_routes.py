from fastapi import APIRouter, Depends, HTTPException,Response,Request
from sqlalchemy.orm import Session
from app.db.models import User
from app.db.schemas import UserLogin
from app.db.session import get_db
from app.api.v1.auth import verify_password, create_access_token
from datetime import timedelta
from app.utils.decryptPassword import decrypt_password
from app.utils.verifyToken import verify_token
router = APIRouter()

@router.post("/login")
def login(response:Response,user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()

    decrypted_password = decrypt_password(user_data.password)

    if not user or not verify_password(decrypted_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email")
    
    access_token = create_access_token({"sub": user.email,"id":user.id}, timedelta(minutes=30))
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        # domain="127.0.0.1"
    )
    return {"message":"Logged in successfully"}

@router.post("/logout")
def logout(response: Response):
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=0,
        domain="127.0.0.1"
    )

    return {"message": "Logged out successfully"}

@router.get("/checkauth")
def check_authentication(get_token:dict=Depends(verify_token)):
   if not get_token:
       raise HTTPException(status_code=401,detail="Unauthorised")
   return {"message":"User logged in"}

