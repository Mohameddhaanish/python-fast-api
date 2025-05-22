from sqlalchemy import Column, Float, Integer, String,ForeignKey,Text,Date,DateTime,func,Boolean,JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from datetime import datetime
import secrets

Base = declarative_base() 
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

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    image_url=Column(String(255), nullable=True)
    public_id=Column(String(255),nullable=True)
    # One-to-many relationship with Product
    products = relationship("Product", back_populates="category", cascade="all, delete")
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text)
    sku = Column(String(255), unique=True, index=True)
    in_stock = Column(Boolean, default=True)
    image_url=Column(String(255),nullable=True)
    public_id=Column(String(255),nullable=True)
    price = Column(Float, nullable=False) 
    stock=Column(Integer,nullable=True)
    discounted_price= Column(Float, nullable=False) 
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    category = relationship("Category", back_populates="products")
    variants = relationship("Variant", back_populates="product", cascade="all, delete")


class Variant(Base):
    __tablename__ = 'variants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    color = Column(String(255),nullable=True)
    discounted_price=Column(Integer,nullable=True)
    is_default=Column(Boolean,nullable=True)
    
    product = relationship("Product", back_populates="variants")
    inventory_item = relationship("InventoryItem", back_populates="variant", uselist=False, cascade="all, delete")
    order_items = relationship("OrderLineItem", back_populates="variant", cascade="all, delete")
    image_url = relationship("VariantImages", back_populates="variant", cascade="all, delete-orphan")
    cart_items=relationship("CartItem",back_populates="variant", cascade="all, delete-orphan")

class VariantImages(Base):
    __tablename__ = "variant_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(Integer, ForeignKey("variants.id"), nullable=False)
    image_url = Column(String(500), nullable=False)

    variant = relationship("Variant", back_populates="image_url")


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
    variant = relationship("Variant" ,back_populates="cart_items")








