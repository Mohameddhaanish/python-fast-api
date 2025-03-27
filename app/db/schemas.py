from pydantic import BaseModel,ConfigDict,Field,EmailStr
from fastapi import Form
from typing import List,Literal,Optional

password_regex = r"^[A-Za-z\d!@#$%^&*()_+=-]{8,}$"

class Token(BaseModel):
    access_token: str
    token_type: str
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class UserCreate:
    def __init__(
        self,
        username: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(..., min_length=8, regex=password_regex),
        role: Literal["User", "Admin"] = Form("User")
    ):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

class UserResponse(BaseModel):
    name: str
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
class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str
    user: UserResponse
      
    model_config = ConfigDict(from_attributes=True)

class CreateProduct(BaseModel):
    name: str=Field(...,max_length=50,min_length=5)
    price: int=Field(...,gt=0)
    description: str=Field(...,max_length=200,min_length=5)