from pydantic import BaseModel,EmailStr
from fastapi import Form,UploadFile,File
from typing import List,Literal,Optional
from datetime import date
from datetime import datetime

password_regex = r"^[A-Za-z\d!@#$%^&*()_+=-]{8,}$"

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str
# class UserCreate:
#     def __init__(
#         self,
#         username: str = Form(...),
#         email: EmailStr = Form(...),
#         hashed_password: str = Form(..., min_length=8, regex=password_regex),
#         role: Literal["User", "Admin","Vendor"] = Form("User"),
#         type_id:Optional[int]=Form(1),

#     ):
#         self.username = username
#         self.email = email
#         self.hashed_password = hashed_password
#         self.role = role
#         self.type_id=type_id

# class AdminTypeSchema(BaseModel):
#     id: int
#     admin_type: str
#     permission:str
#     model_config = ConfigDict(from_attributes=True)

# class UserResponse(BaseModel):
#     id: int
#     name: str
#     email: str
#     role: str
#     is_verified: bool
#     type_id: int
#     user_type: Optional[AdminTypeSchema]
#     model_config = ConfigDict(from_attributes=True)

# class Token(BaseModel):
#     access_token: str
#     token_type: str
#     model_config = ConfigDict(from_attributes=True)
# class UserAddressSchema(BaseModel): 
#     address_line1: str = Field(..., max_length=255, )
#     address_line2: Optional[str] = Field(None, max_length=255, )
#     city: str = Field(..., max_length=255,)
#     postal_code: str = Field(..., max_length=255, )
#     country: str = Field(..., max_length=255, )
#     telephone: Optional[str] = Field(None, max_length=255, )
#     mobile: Optional[str] = Field(None, max_length=255,)
# class UserAddressResponse(BaseModel):
#     address_line1: str
#     address_line2: Optional[str] = None
#     city: str
#     postal_code: str
#     country: str
#     telephone: Optional[str] = None
#     mobile: Optional[str] = None
#     user:UserResponse

#     model_config = ConfigDict(from_attributes=True)

# class UserAddressListResponse(BaseModel):
#     detail: List[UserAddressResponse]

# class UserPaymentDetails:
#     def __init__(
#         self,
#         payment_type:str=Form(...,max_length=255),
#         provider:str=Form(...,max_length=255),
#         account_no:str=Form(...,max_length=16),
#         expiry:date=Form(...)
#     ):
#        self.payment_type=payment_type
#        self.provider=provider
#        self.account_no=account_no
#        self.expiry=expiry 

# class UserPaymentDetailsResponse(BaseModel):
#      id: int
#      user_id: int
#      payment_type: str
#      provider: str
#      account_no: str
#      expiry: date
#      user:UserResponse
#      model_config = ConfigDict(from_attributes=True)

# class PaymentListResponse(BaseModel):
#     detail:List[UserPaymentDetailsResponse]
#     model_config = ConfigDict(from_attributes=True)

# class AdminTypeBase(BaseModel):
#     admin_type: str
#     permission: str

# class AdminTypeCreate(AdminTypeBase):
#     pass

# class AdminTypeResponse(AdminTypeBase):
#     id: int
#     created_at: Optional[datetime]
#     modified_at: Optional[datetime]
#     model_config = ConfigDict(from_attributes=True) 

# # ---------- Category Schema ----------
# class ProductCategoryBase(BaseModel):
#     name: constr(strip_whitespace=True, min_length=2, max_length=255)

# class ProductCategoryCreate(ProductCategoryBase):
#     pass

# class ProductCategoryResponse(ProductCategoryBase):
#     id: int
#     model_config = ConfigDict(from_attributes=True) 


# # ---------- Inventory Schema ----------
# class ProductInventoryBase(BaseModel):
#     quantity: conint(ge=0)  # Quantity must be non-negative

# class ProductInventoryCreate(ProductInventoryBase):
#     pass

# class ProductInventoryResponse(ProductInventoryBase):
#     id: int
#     model_config = ConfigDict(from_attributes=True) 


# # ---------- Discount Schema ----------
# class ProductDiscountBase(BaseModel):
#     name: constr(strip_whitespace=True, min_length=2, max_length=255)
#     description: constr(strip_whitespace=True)
#     discount_percent: confloat(ge=0, le=100)
#     active: bool

# class ProductDiscountCreate(ProductDiscountBase):
#     pass

# class ProductDiscountResponse(ProductDiscountBase):
#     id: int
#     model_config = ConfigDict(from_attributes=True) 


# # ---------- Product Schema ----------
# class ProductBase:
#     def __init__(
#         self,
#         name: str = Form(...),
#         description: str = Form(...),
#         sku: str = Form(...),
#         category_id: int = Form(...),
#         inventory_id: int = Form(...),
#         discount_id: Optional[int] = Form(None),
#         price: float = Form(...),
#         image_url: List[UploadFile] = File(...)
#     ):
#         self.name = name.strip()
#         self.description = description
#         self.sku = sku.strip()
#         self.category_id = category_id
#         self.inventory_id = inventory_id
#         self.discount_id = discount_id
#         self.price = price
#         self.image_url = image_url

# class ProductCreate(ProductBase):
#     pass

# class ProductResponse(BaseModel):
#     id: int
#     name: str 
#     description: str 
#     sku: str 
#     category_id: int 
#     inventory_id: int 
#     discount_id: Optional[int]
#     price: float 
#     image_url: List[str]
#     created_at: datetime
#     modified_at: datetime
#     deleted_at: Optional[datetime]
 
#     category: Optional[ProductCategoryResponse]
#     inventory: Optional[ProductInventoryResponse]
#     discount: Optional[ProductDiscountResponse]

#     model_config = ConfigDict(from_attributes=True) 

# class PaginatedProductResponse(BaseModel):
#      total: int
#      skip: int
#      limit: int
#      results: List[ProductResponse]

# NEW SCHEMAS

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

class ProductBase(BaseModel):
    title: str
    description: str
    sku: str
    in_stock: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    title: str | None = None
    description: str | None = None
    in_stock: bool | None = None

class ProductResponse(ProductBase):
    id: int
    variants: list["VariantResponse"] = []  # Nested relation

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

class OrderBase(BaseModel):
    total_amount: float

class OrderCreate(OrderBase):
    customer_id: int

class OrderResponse(OrderBase):
    id: int
    order_date: datetime
    customer_id: int
    line_items: list["OrderLineItemResponse"] = []

    class Config:
        from_attributes = True
class OrderLineItemBase(BaseModel):
    quantity: int
    price: float

class OrderLineItemCreate(OrderLineItemBase):
    order_id: int
    variant_id: int

class OrderLineItemResponse(OrderLineItemBase):
    id: int
    order_id: int
    variant_id: int

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
