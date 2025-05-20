from pydantic import BaseModel,EmailStr
from fastapi import Form,UploadFile,File
from typing import List,Literal,Optional
from datetime import date
from datetime import datetime

password_regex = r"^[A-Za-z\d!@#$%^&*()_+=-]{8,}$"

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False
    role: str = "customer"
 
    # class Config:
    #     extra = "forbid"

class UserCreate(UserBase):
    hashed_password: str
    # class Config:
    #     extra = "allow"

class VerificationResponse(BaseModel):
    message: str

class UserUpdate(UserBase):
    full_name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    is_verified: bool | None = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    verification_token:str

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    image_url:UploadFile=File(...)

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    title: str
    description: str
    image_url:str
    sku: str
    in_stock: bool 
    public_id:str
    price:float
    stock:int
    discounted_price:float
class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    title: str | None = None
    description: str | None = None
    in_stock: bool | None = None
    image_url:str |None =None

class AllProductsResponse(ProductBase):
    id:int
    class Config:
        from_attributes = True

class ProductResponse(ProductBase):
    id: int
    stock:int
    discounted_price:float
    variants: list["VariantResponse"] = []
    category: CategoryResponse | None = None 
    class Config:
        from_attributes = True

class VariantBase(BaseModel):
    name: str
    price: float
    stock: int = 0
    is_active: bool = True

class VariantCreate(VariantBase):
    product_id: int

class VariantUpdate(VariantBase):
    name: str | None = None
    price: float | None = None
    stock: int | None = None
    is_active: bool | None = None

class VariantResponse(VariantBase):
    id: int
    product_id: int
    images: List[str]  

    class Config:
        from_attributes = True

class InventoryItemBase(BaseModel):
    quantity: int

class InventoryItemCreate(InventoryItemBase):
    variant_id: int

class InventoryItemResponse(InventoryItemBase):
    id: int
    variant_id: int

    class Config:
        from_attributes = True

class OrderLineItemBase(BaseModel):
    quantity: int
    price: float

# Input schema
class OrderLineItemCreate(OrderLineItemBase):
    variant_id: int

# Output schema
class OrderLineItemResponse(OrderLineItemBase):
    id: int
    order_id: int
    variant_id: int

    class Config:
        from_attributes = True 

class OrderBase(BaseModel):
    total_amount: float

# Input schema (includes nested line items)
class OrderCreate(OrderBase):
    customer_id: int
    line_items: List[OrderLineItemCreate]

# Output schema
class OrderResponse(OrderBase):
    id: int
    customer_id: int
    order_date: datetime
    line_items: List[OrderLineItemResponse] = []

    class Config:
        from_attributes = True 

class CartBase(BaseModel):
    pass  # No extra fields, as it links to user

class CartCreate(CartBase):
    customer_id: int

class CartResponse(CartBase):
    id: int
    customer_id: int
    cart_items: list["CartItemResponse"] = []

    class Config:
        from_attributes = True
class CartItemBase(BaseModel):
    quantity: int

class CartItemCreate(CartItemBase):
    cart_id: int
    variant_id: int

class CartItemResponse(CartItemBase):
    id: int
    cart_id: int
    variant_id: int

    class Config:
        from_attributes = True
