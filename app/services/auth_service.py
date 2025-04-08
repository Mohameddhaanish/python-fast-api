from fastapi import security,Depends,HTTPException
from jose import jwt,JWTError
from app.core.config import settings
from sqlalchemy.orm import Session
from app.db.models import User
from app.db.schemas import AdminTypeCreate
from app.db.models import AdminType

oauth2_scheme=security.HTTPBearer()

def get_current_user(token: security.HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id:int=payload.get("user_id")
        role:str=payload.get("role")
        permission:str=payload.get("permission")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        token_data = {"user_id": user_id,"role":role,"permission":permission}
    except JWTError :
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return token_data

async def verify_email(token: str,db:Session):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.is_verified = True
        db.commit()
        return {"message": "Email verified successfully"}

    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
def append_admin_type(db:Session,admin_type_details:AdminTypeCreate):
    admin_type_detail=AdminType(**admin_type_details.__dict__)
    db.add(admin_type_detail)
    db.commit()
    db.refresh(admin_type_detail)
    return admin_type_detail
