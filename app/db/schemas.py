from pydantic import BaseModel,ConfigDict,Field,EmailStr
from fastapi import Form
from typing import List,Literal,Optional
from datetime import date
from datetime import datetime

password_regex = r"^[A-Za-z\d!@#$%^&*()_+=-]{8,}$"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class UserCreate:
    def __init__(
        self,
        username: str = Form(...),
        email: EmailStr = Form(...),
        hashed_password: str = Form(..., min_length=8, regex=password_regex),
        role: Literal["User", "Admin"] = Form("User"),
        type_id:Optional[int]=Form(1),

    ):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.type_id=type_id

class AdminTypeSchema(BaseModel):
    id: int
    admin_type: str
    permission:str
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_verified: bool
    type_id: int
    user_type: Optional[AdminTypeSchema]
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
    model_config = ConfigDict(from_attributes=True)
class UserAddressSchema(BaseModel): 
    address_line1: str = Field(..., max_length=255, )
    address_line2: Optional[str] = Field(None, max_length=255, )
    city: str = Field(..., max_length=255,)
    postal_code: str = Field(..., max_length=255, )
    country: str = Field(..., max_length=255, )
    telephone: Optional[str] = Field(None, max_length=255, )
    mobile: Optional[str] = Field(None, max_length=255,)
class UserAddressResponse(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    postal_code: str
    country: str
    telephone: Optional[str] = None
    mobile: Optional[str] = None
    user:UserResponse

    model_config = ConfigDict(from_attributes=True)

class UserAddressListResponse(BaseModel):
    detail: List[UserAddressResponse]

class UserPaymentDetails:
    def __init__(
        self,
        payment_type:str=Form(...,max_length=255),
        provider:str=Form(...,max_length=255),
        account_no:str=Form(...,max_length=16),
        expiry:date=Form(...)
    ):
       self.payment_type=payment_type
       self.provider=provider
       self.account_no=account_no
       self.expiry=expiry 

class UserPaymentDetailsResponse(BaseModel):
     id: int
     user_id: int
     payment_type: str
     provider: str
     account_no: str
     expiry: date
     user:UserResponse
     model_config = ConfigDict(from_attributes=True)

class PaymentListResponse(BaseModel):
    detail:List[UserPaymentDetailsResponse]
    model_config = ConfigDict(from_attributes=True)

class AdminTypeBase(BaseModel):
    admin_type: str
    permission: str

class AdminTypeCreate(AdminTypeBase):
    pass

class AdminTypeResponse(AdminTypeBase):
    id: int
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True) 