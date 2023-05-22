from typing import Optional
from pydantic import BaseModel, Field, constr


class DeployDetailBase(BaseModel):
    variables: constr(strip_whitespace=True)


class DeployDetailCreate(BaseModel):
    stack_name: constr(strip_whitespace=True)
    tfvar_file: Optional[constr(strip_whitespace=True)] = Field(
        "", example="terraform.tfvars"
    )
    variables: dict


class DeployDetail(DeployDetailBase):
    id: int
    deploy_id: constr(strip_whitespace=True)
    stack_id: constr(strip_whitespace=True)

    class Config:
        orm_mode = True
