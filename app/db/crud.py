from sqlalchemy.orm import Session
from app.db.models import User
from app.db.schemas import UserCreate
from app.core.security import get_hashed_pwd,verify_password
from fastapi import Depends

def get_user_by_userName(db:Session,user_name:str,role:str):
    return db.query(User).filter(User.email == user_name,User.role == role).first()

def create_user(db:Session, user:UserCreate=Depends()):
   hashed_password=get_hashed_pwd(user.password)
   db_user = User(name=user.username,email=user.email,hashed_password=hashed_password,role=user.role)
   db.add(db_user)
   db.commit()
   db.refresh(db_user)
   return db_user

def authenticate_user(db: Session, username: str, password: str,role:str):
    user = get_user_by_userName(db, username,role)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user