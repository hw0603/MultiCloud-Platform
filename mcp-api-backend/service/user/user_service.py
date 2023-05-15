import os
from fastapi import HTTPException, Depends

from config.api_config import settings
from repository import user_repository as crud_users
from sqlalchemy.orm import Session
from db.connection import get_db
from utils.utils import object_as_dict
from entity.user_entity import UserInit
from service.user import user_util

def get_admin_info(db: Session):
    user = crud_users.get_user_by_username(db, "admin")
    return object_as_dict(user)


async def create_init_user(passwd: UserInit, db: Session = Depends(get_db)):
    init_user = settings.INIT_USER
    user_util.validate_password(init_user.get("username"), passwd.password)
    db_user = crud_users.get_user_by_username(db, username=init_user.get("username"))
    if db_user:
        raise HTTPException(status_code=409, detail="Username already registered")
    else:
        try:
            return crud_users.create_init_user(db=db, password=passwd.password)
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))