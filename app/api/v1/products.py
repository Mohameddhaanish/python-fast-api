from fastapi import APIRouter,Depends,HTTPException
from app.db.schemas import CreateProduct,ProductResponse
from app.db.session import get_db
from app.services.auth_service import get_current_user
from app.services.product_service import create_product_method,get_products_with_users
from sqlalchemy.orm import Session

router=APIRouter()

@router.post('/create-product')
async def create_product(product_details:CreateProduct,current_user:dict=Depends(get_current_user),db: Session = Depends(get_db)):
     
   product=create_product_method(db,product_details=product_details,current_user=current_user) 
   if product:
     return {"message":"Product created successfully"}
   else:
     return {"message":"Product creation failed"}  
   
@router.get("/getproducts", response_model=list[ProductResponse])
def fetch_products(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    current_user_id = current_user.get("user_id")
    
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    products = get_products_with_users(db, current_user_id)
    return products 
   