from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # Move Base here
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    hashedPassword=Column(String(255))
    role=Column(String(255) ,default="user",nullable=False)

    products = relationship("Product", back_populates="user")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String(50), index=True)
    price = Column(Integer)
    description = Column(String(255))
    user_id=Column(Integer,ForeignKey('users.id'))

    user = relationship("User", back_populates="products")
