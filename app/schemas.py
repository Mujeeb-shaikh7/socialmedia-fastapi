from pydantic import BaseModel as Model
from pydantic import EmailStr
from datetime import datetime
from typing import Optional
class PostBase(Model):
    title:str
    content:str
    published:bool=True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id :int
    owner_id:int 
    created_at: datetime


    class Config:
        orm_mode=True

class UserCreate(Model):
    email:str
    password:str

class UserOut(Model):
    id:int
    email:EmailStr
    class Config:
        orm_mode=True

class UserLogin(Model):
    email:EmailStr
    password:str

class Token(Model):
    access_token:str
    token_type:str

class TokenData(Model):
    id: Optional[str]




