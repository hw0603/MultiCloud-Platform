from pydantic import BaseModel, constr


class TeamBase(BaseModel):
    team_name: constr(strip_whitespace=True)


class TeamCreate(TeamBase):
    pass 


class TeamCreateMaster(TeamCreate):
    pass 


class TeamUpdate(TeamCreate):
    pass 


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True
