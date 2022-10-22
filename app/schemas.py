from datetime import datetime
from dis import code_info
from lib2to3.pgen2 import token
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class CreateUser(BaseModel):
    user_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    created_at: datetime
    user_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(BasePost):
    pass


class PostResponse(BasePost):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    # votes: int

    class Config:
        orm_mode = True


class VoteOut(BaseModel):
    Post: PostResponse
    votes: int
    


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional['str']


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
