from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.models import Cart, CartItem
from app.db.schemas import CartCreate, CartResponse,CartItemResponse
from app.db.session import get_db
from app.utils.verifyToken import verify_token

router = APIRouter()

@router.get("/", response_model=CartResponse)
def get_cart(db: Session = Depends(get_db),get_user:dict=Depends(verify_token)):
    if not get_user:
        raise HTTPException(status_code=401,detail="Unauthorized")
    customer_id=get_user['id']
    cart = db.query(Cart).filter(Cart.customer_id == customer_id).first()
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart

@router.post("/add", response_model=CartItemResponse)
def add_to_cart( variant_id: int, quantity: int, db: Session = Depends(get_db),get_user:dict=Depends(verify_token)):
    if not get_user:
        raise HTTPException(status_code=401,detail="Unauthorized")
    
    customer_id=get_user['id']

    cart = db.query(Cart).filter(Cart.customer_id == customer_id).first()

    if not cart:
        cart = Cart(customer_id=customer_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    cart_item = CartItem(cart_id=cart.id, variant_id=variant_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item

@router.put("/cart/item/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(cart_item_id: int, quantity: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)

    return cart_item

@router.delete("/cart/item/{cart_item_id}")
def remove_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()

    return {"message": "Item removed from cart"}



