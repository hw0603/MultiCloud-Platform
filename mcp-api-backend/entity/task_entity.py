from typing import Optional
from pydantic import BaseModel, EmailStr, Field, constr


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


class PlanCreate(BaseModel):
    name: constr(strip_whitespace=True)
    team: constr(strip_whitespace=True)
    environment: constr(strip_whitespace=True)
    start_time: Optional[constr(strip_whitespace=True)] = Field(
        None, example="30 7 * * 0-4"
    )
    destroy_time: Optional[constr(strip_whitespace=True)] = Field(
        None, example="30 8 * * 0-4"
    )
