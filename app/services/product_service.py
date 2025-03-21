from sqlalchemy.orm import Session
from app.db.models import Product

def create_product_method(db:Session,product_details:dict,current_user:dict):
    db_product=Product(name=product_details.name,price=product_details.price,description=product_details.description,user_id=current_user['user_id'])
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products_with_users(db:Session,current_user_id:int):
    return db.query(Product).join(Product.user).filter(Product.user_id == current_user_id).all()