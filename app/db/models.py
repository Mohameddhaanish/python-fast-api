from sqlalchemy import Column, Float, Integer, String,ForeignKey,Text,Date,DateTime,func,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List
Base = declarative_base()  # Move Base here
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    hashed_password=Column(String(255))
    role=Column(String(255) ,default="user",nullable=False)
    is_verified=Column(Boolean,default=False,nullable=False)
    type_id=Column(Integer, ForeignKey("admin_type.id",ondelete="CASCADE"),nullable=False)
     
    user_type=relationship("AdminType",back_populates="users")
    address=relationship("UserAddress",back_populates="user",cascade="all, delete-orphan")
    payment=relationship("UserPayment",back_populates="user",cascade="all, delete-orphan")

class UserAddress(Base):
    __tablename__="user_address"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),index=True)
    address_line1=Column(String(255))
    address_line2=Column(String(255))
    city=Column(String(255))
    postal_code=Column(String(255))
    country=Column(String(255))
    telephone=Column(String(255))
    mobile=Column(String(255))

    user=relationship("User",back_populates="address")

class UserPayment(Base):
    __tablename__="user_payment"

    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),index=True)
    payment_type=Column(String(255),nullable=False)
    provider=Column(String(255),nullable=False)
    account_no=Column(String(16),nullable=False)
    expiry=Column(Date,nullable=False)

    user=relationship("User",back_populates="payment")

class AdminType(Base):
    __tablename__="admin_type"

    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    admin_type=Column(String(255),nullable=False)
    permission=Column(String(255),nullable=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    modified_at=Column(DateTime(timezone=True), server_default=func.now())

    users=relationship("User",back_populates="user_type")





