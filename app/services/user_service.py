from app.db.schemas import UserAddressSchema
from sqlalchemy.orm import Session,joinedload
from app.db.models import UserAddress,User


def create_user_address(db:Session,user_address_details:UserAddressSchema,current_user:int):
    user_address=UserAddress(user_id=current_user,**user_address_details.model_dump())
    db.add(user_address)
    db.commit()
    db.refresh(user_address)
    return user_address

def get_user_address(db:Session,current_user:int):
    # return db.query(UserAddress).options(joinedload(UserAddress.user)).filter(UserAddress.user_id == current_user).all()
    # return db.query(User,UserAddress).outerjoin(UserAddress,User.id==UserAddress.user_id).filter(User.id==current_user).all()
    return db.query(UserAddress).filter(UserAddress.user_id == current_user).all() 