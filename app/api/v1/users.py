from fastapi import APIRouter,Depends
from app.services.auth_service import get_current_user

router=APIRouter()

@router.get('/get_user')
async def get_user(current_user:dict=Depends(get_current_user)):
   return {"message":current_user}
   