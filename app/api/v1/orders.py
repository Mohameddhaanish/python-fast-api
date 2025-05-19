from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.models import Order, OrderLineItem
from app.db.schemas import OrderCreate, OrderResponse
from app.db.session import get_db
from datetime import datetime

router = APIRouter()

@router.post("/orders", response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    # Create the order
    new_order = Order(
        customer_id=order_data.customer_id,
        total_amount=order_data.total_amount,
        order_date=datetime.now()
    )
    db.add(new_order)
    db.flush()  # Get new_order.id without committing yet

    # Create line items
    for item in order_data.line_items:
        line_item = OrderLineItem(
            order_id=new_order.id,
            variant_id=item.variant_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(line_item)

    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.id == order_id).first()

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db.query(Order).filter(Order.id == order_id).delete()
    db.commit()
    return {"message": "Order deleted"}
