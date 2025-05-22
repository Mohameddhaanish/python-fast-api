from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.models import Cart, CartItem
from app.db.schemas import CartResponse,CartItemResponse,CartItemCreate,VariantResponse
from app.db.session import get_db
from app.utils.verifyToken import verify_token
from typing import List

router = APIRouter()

@router.get("/items", response_model=List[CartItemResponse])
def get_cart_items(db: Session = Depends(get_db), get_user: dict = Depends(verify_token)):
    if not get_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    customer_id = get_user["id"]
    
    cart = db.query(Cart).filter(Cart.customer_id == customer_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    response = []
    for item in cart_items:
        response.append(CartItemResponse(
            id=item.id,
            cart_id=item.cart_id,
            variant_id=item.variant_id,
            quantity=item.quantity if item.quantity is not None else 1,
            variant_items=[VariantResponse.from_orm(item.variant)] if item.variant else [] 
        ))

    return response


@router.post("/add", response_model=CartItemResponse)
def add_to_cart(
    cartItem: CartItemCreate,
    db: Session = Depends(get_db),
    get_user: dict = Depends(verify_token)
):
    if not get_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    customer_id = get_user['id']

    # Check if cart already exists
    cart = db.query(Cart).filter(Cart.customer_id == customer_id).first()
    if not cart:
        cart = Cart(customer_id=customer_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Check if variant already exists in the cart -> update quantity
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.variant_id == cartItem.variant_id
    ).first()

    if existing_item:
        existing_item.quantity += cartItem.quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            variant_id=cartItem.variant_id,
            quantity=cartItem.quantity
        )
        db.add(new_item)

    db.commit()

    return existing_item or new_item


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



