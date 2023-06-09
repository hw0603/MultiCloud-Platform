from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    username: constr(strip_whitespace=True)
    team: constr(strip_whitespace=True)


class UserCreate(UserBase):
    fullname: constr(strip_whitespace=True)
    password: str
    email: EmailStr = None
    is_active: bool = True
    team: str
    role: List[str] = []


class UserCreateMaster(UserCreate):
    pass 


class UserUpdate(UserBase):
    fullname: constr(strip_whitespace=True)
    password: str
    email: str = None
    is_active: bool = True
    team: str
    role: List[str] = []


class UserAuthenticate(UserBase):
    password: str


class UserInit(BaseModel):
    password: str


class PasswordReset(BaseModel):
    passwd: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    token_type: str
    access_token: str
    role: List


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class TokenData(BaseModel):
    user_id: int = None
