from typing import Optional

from pydantic import BaseModel, Field, constr


class DeployBase(BaseModel):
    deploy_name: constr(strip_whitespace=True)
    username: constr(strip_whitespace=True)
    team: constr(strip_whitespace=True)
    environment: constr(strip_whitespace=True)
    

class DeployCreate(BaseModel):
    deploy_name: constr(strip_whitespace=True)
    team: constr(strip_whitespace=True)
    environment: constr(strip_whitespace=True)
    start_time: Optional[constr(strip_whitespace=True)] = Field(
        None, example="30 7 * * 0-4"
    )
    destroy_time: Optional[constr(strip_whitespace=True)] = Field(
        None, example="30 8 * * 0-4"
    )
    
    
class DeployCreateMaster(DeployCreate):
    team: constr(strip_whitespace=True)


class DeployDeleteMaster(BaseModel):
    team: constr(strip_whitespace=True)


class DeployUpdate(BaseModel):
    start_time: constr(strip_whitespace=True)
    destroy_time: constr(strip_whitespace=True)


class Deploy(DeployBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
