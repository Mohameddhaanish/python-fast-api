from fastapi import FastAPI,APIRouter,Depends,HTTPException
from app.db.schemas import Token,UserCreate,LoginRequest
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import create_user,get_user_by_userName,authenticate_user
from app.core.config import settings
from datetime import timedelta
from app.core.security import create_access_token
from app.db.schemas import AdminTypeCreate
from app.services.auth_service import append_admin_type
from app.services.auth_service import get_current_user
from app.utils.email import simple_send

router=APIRouter()

@router.post('/signup', response_model=Token)
async def signUp(user: UserCreate = Depends(), db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = get_user_by_userName(db, user.username,user.role)
    if db_user:
        raise HTTPException(status_code=400, detail="User Already Registered")

    # Create user in the database and retrieve the created user
    created_user = create_user(db, user)  

    # Generate JWT Token
    access_expire_time = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": created_user.id, "user_email": created_user.email, "role": created_user.role},
        expires_delta=access_expire_time
    )

    return {"access_token": access_token, "token_type": "bearer"}  # Or `created_user.id`

#User Login
@router.post('/user/login',response_model=Token)
async def sign_in(form_data:LoginRequest,db:Session=Depends(get_db)):
   user=authenticate_user(db=db,username=form_data.email,password=form_data.password,role="User")
   if not user:
    raise HTTPException(status_code=404, detail="Incorrect username or password!")
   access_token_expire=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
   access_token=create_access_token(data={"user_id":user.id,"user_email":user.email, "role": user.role,"permission":user.user_type.permission},expires_delta=access_token_expire)
   return {"access_token":access_token,"token_type":"bearer"}

#Admin Login
@router.post('/admin/login',response_model=Token)
async def sign_in(form_data:LoginRequest,db:Session=Depends(get_db)):
   user=authenticate_user(db=db,username=form_data.email,password=form_data.password,role="Admin")
   if not user:
    raise HTTPException(status_code=404, detail="Incorrect username or password!")
   access_token_expire=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
   access_token=create_access_token(data={"user_id":user.id,"user_email":user.email, "role": user.role,"permission":user.user_type.permission},expires_delta=access_token_expire)
   return {"access_token":access_token,"token_type":"bearer"}

@router.post("/create_admin_type")
def create_admin_type( 
    db: Session = Depends(get_db),admin_type_details:AdminTypeCreate=Depends()):
    admin_type=append_admin_type(db=db,admin_type_details=admin_type_details)
    return admin_type

@router.post("/verify_email")
async def verify_email(current_user:dict=Depends(get_current_user)):
   if not current_user:
      raise HTTPException(status_code=401,detail="Unauthorized access")
   email=current_user['user_email']
   send_email=simple_send(email=email)
   return send_email
