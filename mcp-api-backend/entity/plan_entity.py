from typing import Optional
from pydantic import BaseModel, Field, constr


class PlanCreate(BaseModel):
    deploy_name: constr(strip_whitespace=True)
    team: constr(strip_whitespace=True)
    environment: constr(strip_whitespace=True)
    start_time: Optional[constr(strip_whitespace=True)] = Field(
        None, example="30 7 * * 0-4"
    )
    destroy_time: Optional[constr(strip_whitespace=True)] = Field(
        None, example="30 8 * * 0-4"
    )
    