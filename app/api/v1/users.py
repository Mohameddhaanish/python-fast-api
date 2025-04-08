from fastapi import APIRouter,Depends,HTTPException
from app.services.auth_service import get_current_user
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas import UserAddressSchema,UserAddressListResponse,UserPaymentDetails,PaymentListResponse,AdminTypeCreate
from app.services.user_service import create_user_address,get_user_address,add_payment_details,get_payment_details

router=APIRouter()

@router.get('/get_user')
async def get_user(current_user:dict=Depends(get_current_user)):
   return {"message":current_user}

@router.post('/create_user_address',response_model=UserAddressSchema)
async def post_user_address(current_user:dict=Depends(get_current_user),db:Session=Depends(get_db),user_address_details:UserAddressSchema=Depends()):
   if not current_user:
        raise HTTPException(status_code=401,detail="unauthorized access")
   user_address=create_user_address(db=db,user_address_details=user_address_details,current_user=current_user['user_id'])
   return user_address

@router.get('/get_user_address', response_model=UserAddressListResponse)
async def retrieve_user_address(
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    user_addresses = get_user_address(db=db, current_user=current_user["user_id"])

    if not user_addresses:
        raise HTTPException(status_code=404, detail="User address not found")

    return {"detail": user_addresses}

@router.post('/add_payment_details')
async def create_payment_details(current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db),
    payment_details:UserPaymentDetails=Depends()
):  
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    user_payment_details=add_payment_details(db=db,current_user=current_user["user_id"],payment_details=payment_details)
    return user_payment_details

@router.get('/get_payment_details',response_model=PaymentListResponse)
async def fetch_payment_details(current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    payment_details=get_payment_details(db=db,current_user=current_user["user_id"])
    return {"detail":payment_details}

