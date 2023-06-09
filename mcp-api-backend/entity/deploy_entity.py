from typing import Optional
from pydantic import BaseModel, Field, constr
from entity.deploy_detail_entity import DeployDetailCreate, DeployDetailResponse


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
    deploy_detail: list[DeployDetailCreate]
    
    
class DeployCreateMaster(DeployCreate):
    team: constr(strip_whitespace=True)


class DeployDeleteMaster(BaseModel):
    team: constr(strip_whitespace=True)


class DeployUpdate(BaseModel):
    start_time: constr(strip_whitespace=True)
    destroy_time: constr(strip_whitespace=True)


class DeployResponsewithDetail(BaseModel):
    deploy_id: int
    deploy_name: constr(strip_whitespace=True)
    start_time: Optional[constr(strip_whitespace=True)] = Field(
        None, example="30 7 * * 0-4"
    )
    destroy_time: Optional[constr(strip_whitespace=True)] = Field(
        None, example="30 8 * * 0-4"
    )
    user_id: int
    username: constr(strip_whitespace=True)
    team: constr(strip_whitespace=True)
    environment: constr(strip_whitespace=True)
    detail_cnt: int
    csp_type: constr(strip_whitespace=True)  # aws, azure, gcp
    detail_data: list[DeployDetailResponse]


class DeployStatus(BaseModel):
    task_id: constr(strip_whitespace=True)
    status: constr(strip_whitespace=True)


class Deploy(DeployBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class DeployDestroy(BaseModel):
    deploy_name: str
    team: str
    stack_name: str
    environment: str