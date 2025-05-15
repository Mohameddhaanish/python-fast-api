from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.models import Cart, CartItem
from app.db.schemas import CartCreate, CartResponse
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=CartResponse)
def create_cart(cart: CartCreate, db: Session = Depends(get_db)):
    db_cart = Cart(**cart.dict())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

@router.get("/{cart_id}", response_model=CartResponse)
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    return db.query(Cart).filter(Cart.id == cart_id).first()

@router.delete("/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    db.query(Cart).filter(Cart.id == cart_id).delete()
    db.commit()
    return {"message": "Cart deleted"}
