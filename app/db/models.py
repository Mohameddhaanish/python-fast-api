from sqlalchemy import Column, Float, Integer, String,ForeignKey,Text,Date,DateTime,func,Boolean,JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from datetime import datetime
import secrets

Base = declarative_base() 


# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True,autoincrement=True)
#     name = Column(String(50))
#     email = Column(String(100), unique=True, index=True)
#     hashed_password=Column(String(255))
#     role=Column(String(255) ,default="user",nullable=False)
#     is_verified=Column(Boolean,default=False,nullable=False)
#     type_id=Column(Integer, ForeignKey("admin_type.id",ondelete="CASCADE"),nullable=False)
     
#     user_type=relationship("AdminType",back_populates="users")
#     address=relationship("UserAddress",back_populates="user",cascade="all, delete-orphan")
#     payment=relationship("UserPayment",back_populates="user",cascade="all, delete-orphan")

# class UserAddress(Base):
#     __tablename__="user_address"

#     id = Column(Integer, primary_key=True, index=True,autoincrement=True)
#     user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),index=True)
#     address_line1=Column(String(255))
#     address_line2=Column(String(255))
#     city=Column(String(255))
#     postal_code=Column(String(255))
#     country=Column(String(255))
#     telephone=Column(String(255))
#     mobile=Column(String(255))

#     user=relationship("User",back_populates="address")

# class UserPayment(Base):
#     __tablename__="user_payment"

#     id=Column(Integer,primary_key=True,index=True,autoincrement=True)
#     user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),index=True)
#     payment_type=Column(String(255),nullable=False)
#     provider=Column(String(255),nullable=False)
#     account_no=Column(String(16),nullable=False)
#     expiry=Column(Date,nullable=False)

#     user=relationship("User",back_populates="payment")

# class AdminType(Base):
#     __tablename__="admin_type"

#     id=Column(Integer,primary_key=True,index=True,autoincrement=True)
#     admin_type=Column(String(255),nullable=False)
#     permission=Column(String(255),nullable=False)
#     created_at=Column(DateTime(timezone=True), server_default=func.now())
#     modified_at=Column(DateTime(timezone=True), server_default=func.now())

#     users=relationship("User",back_populates="user_type")

# class Product(Base):
#     __tablename__="product"

#     id=Column(Integer,primary_key=True,index=True,autoincrement=True)
#     name=Column(String(255),unique=True,index=True,nullable=False)
#     description=Column(Text,nullable=False)
#     sku=Column(String(255),unique=True,nullable=False,index=True)
#     category_id=Column(Integer,ForeignKey("category.id"))
#     inventory_id=Column(Integer,ForeignKey("inventory.id"))
#     discount_id=Column(Integer,ForeignKey("discount.id"))
#     price=Column(Float,nullable=False)
#     image_url=Column(JSON,nullable=False)
#     created_at=Column(DateTime(timezone=True), server_default=func.now())
#     modified_at=Column(DateTime(timezone=True), server_default=func.now())
#     deleted_at=Column(DateTime(timezone=True), server_default=func.now())

#     category = relationship("ProductCategory", back_populates="products")
#     inventory = relationship("ProductInventory", back_populates="products")
#     discount = relationship("ProductDiscount", back_populates="products")

# class ProductCategory(Base):
#     __tablename__="category"
    
#     id=Column(Integer,primary_key=True,index=True,autoincrement=True)
#     name=Column(String(255),unique=True,index=True,nullable=False)
#     created_at=Column(DateTime(timezone=True), server_default=func.now())
#     modified_at=Column(DateTime(timezone=True), server_default=func.now())
#     deleted_at=Column(DateTime(timezone=True), server_default=func.now())

#     products = relationship("Product", back_populates="category")


# class ProductInventory(Base):
#     __tablename__="inventory"
    
#     id=Column(Integer,primary_key=True,index=True,autoincrement=True)
#     quantity=Column(Integer,nullable=False)
#     created_at=Column(DateTime(timezone=True), server_default=func.now())
#     modified_at=Column(DateTime(timezone=True), server_default=func.now())
#     deleted_at=Column(DateTime(timezone=True), server_default=func.now())

#     products = relationship("Product", back_populates="inventory")

# class ProductDiscount(Base):
#     __tablename__="discount"
    
#     id=Column(Integer,primary_key=True,index=True,autoincrement=True)
#     name=Column(String(255),unique=True,index=True,nullable=False)
#     description=Column(Text,nullable=False)
#     discount_percent=Column(Float,nullable=False)
#     active=Column(Boolean,nullable=False,index=True)
#     created_at=Column(DateTime(timezone=True), server_default=func.now())
#     modified_at=Column(DateTime(timezone=True), server_default=func.now())
#     deleted_at=Column(DateTime(timezone=True), server_default=func.now())

#     products = relationship("Product", back_populates="discount")

#  NEW STORE MODELS

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(20), default="customer")  # Roles: admin, vendor, customer
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    verification_token = Column(String(32), unique=True, default=lambda: secrets.token_hex(16))

    orders = relationship("Order", back_populates="customer", cascade="all, delete")
    cart = relationship("Cart", back_populates="customer", uselist=False, cascade="all, delete")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text)
    sku = Column(String(255), unique=True, index=True)
    in_stock = Column(Boolean, default=True)

    variants = relationship("Variant", back_populates="product", cascade="all, delete")


class Variant(Base):
    __tablename__ = 'variants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    product = relationship("Product", back_populates="variants")
    inventory_item = relationship("InventoryItem", back_populates="variant", uselist=False, cascade="all, delete")
    order_items = relationship("OrderLineItem", back_populates="variant", cascade="all, delete")


class InventoryItem(Base):
    __tablename__ = 'inventory_items'

    id = Column(Integer, primary_key=True, index=True)
    variant_id = Column(Integer, ForeignKey('variants.id', ondelete="CASCADE"))
    quantity = Column(Integer)

    variant = relationship("Variant", back_populates="inventory_item")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    order_date = Column(DateTime, default=datetime.now)
    total_amount = Column(Float)

    customer = relationship("User", back_populates="orders")
    line_items = relationship("OrderLineItem", back_populates="order", cascade="all, delete")


class OrderLineItem(Base):
    __tablename__ = 'order_line_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"))
    variant_id = Column(Integer, ForeignKey('variants.id', ondelete="CASCADE"))
    quantity = Column(Integer)
    price = Column(Float)

    order = relationship("Order", back_populates="line_items")
    variant = relationship("Variant", back_populates="order_items")


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    
    customer = relationship("User", back_populates="cart")
    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete")


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id', ondelete="CASCADE"))
    variant_id = Column(Integer, ForeignKey('variants.id', ondelete="CASCADE"))
    quantity = Column(Integer)

    cart = relationship("Cart", back_populates="cart_items")
    variant = relationship("Variant")








