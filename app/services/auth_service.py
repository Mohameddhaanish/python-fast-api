from fastapi import security,Depends,HTTPException
from jose import jwt,JWTError
from app.core.config import settings
from sqlalchemy.orm import Session
from app.db.models import User
from app.db.schemas import AdminTypeCreate
from app.db.models import AdminType
from app.db.session import get_db

oauth2_scheme=security.HTTPBearer()

def get_current_user(token: security.HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id:int=payload.get("user_id")
        role:str=payload.get("role")
        permission:str=payload.get("permission")
        email:str=payload.get("user_email")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        token_data = {"user_id": user_id,"role":role,"permission":permission,"email":email}
    except JWTError :
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return token_data

def check_verified_user(current_user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401,detail="Unauthorized access")
    user=db.query(User).filter(User.id == current_user["user_id"]).first()

    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Email not verified. Please verify your email to proceed."
        )
    return user

def check_admin_seller(role:str):
    def role_checker(user: User = Depends(check_verified_user)):
        if user.role != role:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to perform this action"
            )
        return user
    return role_checker

def append_admin_type(db:Session,admin_type_details:AdminTypeCreate):
    admin_type_detail=AdminType(**admin_type_details.__dict__)
    db.add(admin_type_detail)
    db.commit()
    db.refresh(admin_type_detail)
    return admin_type_detail
