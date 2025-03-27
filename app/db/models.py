from sqlalchemy import Column, Float, Integer, String,ForeignKey,Text
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

    address=relationship("UserAddress",back_populates="user",cascade="all, delete-orphan")

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

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String(255), index=True,nullable=False)
    price = Column(Float,nullable=False)
    description = Column(Text,nullable=False)
    stock = Column(Integer, default=0)
    user_id=Column(Integer,ForeignKey('users.id'))
    category_id=Column(Integer,ForeignKey("categories.id"))


class Category(Base):
    __tablename__ = "categories"

    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    name=Column(String(255),index=True,nullable=False,unique=True)
    description=Column(Text,nullable=True)
    parent_id=Column(Integer,ForeignKey("categories.id"),nullable=True) #for sub category

    #for self referencng purpose
    parent=relationship("Category" ,remote_side=[id],backref="subcategories")




