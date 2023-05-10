from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    username: constr(strip_whitespace=True)


class UserCreate(UserBase):
    fullname: constr(strip_whitespace=True)
    password: str
    email: EmailStr = None
    is_active: bool = True
    team: List[str] = []
    role: List[str] = []


class UserCreateMaster(UserCreate):
    pass 


class UserUpdate(UserCreate):
    pass


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

