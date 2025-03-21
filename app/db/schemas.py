from pydantic import BaseModel,ConfigDict,Field,EmailStr
from fastapi import Form
from typing import List

password_regex = r"^[A-Za-z\d!@#$%^&*()_+=-]{8,}$"


class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str=Field(...,min_length=8,pattern=password_regex)
    role:str|None=None

    # Token schema
class Token(BaseModel):
    access_token: str
    token_type: str
    user:int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str
    user: UserResponse
      
    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class CreateProduct(BaseModel):
    name: str=Field(...,max_length=50,min_length=5)
    price: int=Field(...,gt=0)
    description: str=Field(...,max_length=200,min_length=5)