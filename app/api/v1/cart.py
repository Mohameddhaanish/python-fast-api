from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session,joinedload
from app.db.models import Cart, CartItem,VariantImages,Variant,Product
from app.db.schemas import CartResponse,CartItemResponse,CartItemCreate,VariantResponse,VariantImageResponse
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
        return []

    cart_items = (
      db.query(CartItem)
      .options( joinedload(CartItem.variant)
            .joinedload(Variant.product)
            .joinedload(Product.category),
            joinedload(CartItem.variant).joinedload(Variant.image_url))
      .filter(CartItem.cart_id == cart.id)
      .all()
    )    
    response = []
    for item in cart_items:
        response.append(CartItemResponse(
        id=item.id,
        cart_id=item.cart_id,
        category_id=item.variant.product.category.id if item.variant and item.variant.product else None,
        category_name=item.variant.product.category.name if item.variant and item.variant.product else None,
        variant_id=item.variant_id,
        quantity=item.quantity if item.quantity is not None else 1,
        sub_total=(item.variant.discounted_price if item.variant.discounted_price else item.variant.price) * item.quantity,
        variant=VariantResponse(
            id=item.variant.id,
            name=item.variant.name,
            price=item.variant.price,
            stock=item.variant.stock,
            is_active=item.variant.is_active,
            discounted_price=item.variant.discounted_price,
            is_default=item.variant.is_default,
            color=item.variant.color,
            in_stock=item.variant.product.in_stock,
            description=item.variant.product.description,
            images=[img.image_url for img in item.variant.image_url] if item.variant and item.variant.image_url else []  # ✅ Extract only URLs
        )
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


@router.put("/item/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(cart_item_id: int, quantity: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)

    return cart_item

@router.delete("/item/{cart_item_id}")
def remove_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()

    return {"message": "Item removed from cart"}



