from pydantic import BaseModel, constr


class CustomProviderBase(BaseModel):
    team: constr(strip_whitespace=True)
    environment: constr(strip_whitespace=True)
    configuration: dict


class CustomProvider(CustomProviderBase):
    id: int

    class Config:
        orm_mode = True
