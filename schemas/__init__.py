from pydantic import BaseModel, EmailStr
from models.util import PrivacyType
from typing import Union, List
from fastapi import UploadFile




class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    firstname: Union[str, None] = None
    lastname: Union[str, None] = None


class UserUpdatePassword(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

class ImageCreate(BaseModel):
    img: List[UploadFile]

class PostCreate(BaseModel):
    content: str
    is_anonymous: bool
    privacy_type: PrivacyType