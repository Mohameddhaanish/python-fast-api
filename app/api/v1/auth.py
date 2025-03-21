from fastapi import FastAPI,APIRouter,Depends,HTTPException
from app.db.schemas import Token,UserCreate,LoginRequest
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import create_user,get_user_by_userName,authenticate_user
from app.core.config import settings
from datetime import timedelta
from app.core.security import create_access_token

router=APIRouter()

@router.post('/signup', response_model=Token)
async def signUp(user: UserCreate = Depends(), db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = get_user_by_userName(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User Already Registered")

    # Create user in the database and retrieve the created user
    created_user = create_user(db, user.__dict__)  # Ensure this function returns the new user

    # Generate JWT Token
    access_expire_time = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": created_user.id, "user_email": created_user.email, "role": created_user.role},
        expires_delta=access_expire_time
    )

    return {"access_token": access_token, "token_type": "bearer"}  # Or `created_user.id`


@router.post('/login',response_model=Token)
async def sign_in(form_data:LoginRequest,db:Session=Depends(get_db)):
   user=authenticate_user(db=db,username=form_data.email,password=form_data.password)
   if not user:
    raise HTTPException(status_code=404, detail="Incorrect username or password!")
   access_token_expire=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
   access_token=create_access_token(data={"user_id":user.id,"user_email":user.email},expires_delta=access_token_expire)
   return {"access_token":access_token,"token_type":"bearer","user":user.id}