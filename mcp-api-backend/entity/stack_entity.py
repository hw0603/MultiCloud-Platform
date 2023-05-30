from typing import List, Optional

from pydantic import BaseModel, Field, constr
import datetime


class StackBase(BaseModel):
    stack_name: constr(strip_whitespace=True)
    stack_type: constr(strip_whitespace=True)
    csp_type: constr(strip_whitespace=True)  # aws, azure, gcp
    description: constr(strip_whitespace=True)
    team_access: List[str] = ["*"]
    tf_version: constr(strip_whitespace=True) = "1.3.2"
    git_repo: Optional[constr(strip_whitespace=True)]
    branch: Optional[constr(strip_whitespace=True)] = "master"
    project_path: Optional[constr(strip_whitespace=True)] = Field("", example="")
    created_at: Optional[datetime.datetime]

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True  # remove trailing whitespace


class StackCreate(StackBase):
    pass

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True  # remove trailing whitespace


class Stack(StackBase):
    stack_id: int
    task_id: constr(strip_whitespace=True)
    user_id: int

    class Config:
        orm_mode = True
