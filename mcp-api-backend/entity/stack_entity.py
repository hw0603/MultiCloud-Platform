from typing import List, Optional

from pydantic import BaseModel, Field, constr


class StackBase(BaseModel):
    stack_name: constr(strip_whitespace=True)
    team_access: List[str] = ["*"]
    tf_version: constr(strip_whitespace=True) = "1.0.0"
    description: constr(strip_whitespace=True)

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True  # remove trailing whitespace


class StackCreate(StackBase):
    pass 

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True  # remove trailing whitespace


class Stack(StackBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
