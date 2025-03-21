from sqlalchemy.orm import Session
from app.db.models import User
from app.db.schemas import UserCreate
from datetime import timedelta,datetime
from app.core.security import get_hashed_pwd,verify_password

def get_user_by_userName(db:Session,user_name:str):
    return db.query(User).filter(User.email == user_name).first()

def create_user(db:Session, user=UserCreate):
   hashed_password=get_hashed_pwd(user.password)
   db_user = User(name=user.username,email=user.email,hashedPassword=hashed_password,role=user.role)
   db.add(db_user)
   db.commit()
   db.refresh(db_user)
   return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_userName(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashedPassword):
        return False
    return user