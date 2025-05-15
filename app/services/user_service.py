from app.db.schemas import UserAddressSchema,UserPaymentDetails
from sqlalchemy.orm import Session,joinedload
from app.db.models import UserAddress,UserPayment


def create_user_address(db:Session,user_address_details:UserAddressSchema,current_user:int):
    user_address=UserAddress(user_id=current_user,**user_address_details.model_dump())
    db.add(user_address)
    db.commit()
    db.refresh(user_address)
    return user_address

def get_user_address(db:Session,current_user:int):
    return db.query(UserAddress).filter(UserAddress.user_id == current_user).all() 

def add_payment_details(db:Session,current_user:int,payment_details:UserPaymentDetails):
    payment_details=UserPayment(user_id=current_user,**payment_details.__dict__)
    db.add(payment_details)
    db.commit()
    db.refresh(payment_details)
    return payment_details

def get_payment_details(db:Session,current_user:int):
    return db.query(UserPayment).filter(UserPayment.user_id == current_user).all()


