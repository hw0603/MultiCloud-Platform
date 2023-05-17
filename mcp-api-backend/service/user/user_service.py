from multiprocessing import connection
import os
from re import U
from unittest import result
from fastapi import HTTPException, Depends
from entity.user_entity import UserUpdate

from config.api_config import settings
from repository import user_repository as crud_users
from sqlalchemy.orm import Session
from db.connection import get_db
from utils.utils import object_as_dict
from entity.user_entity import UserInit, UserCreate, User
from service.user import user_util
from src.shared.security import deps

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

async def create_user(
        user: UserCreate, 
        current_user: User = Depends(deps.get_current_active_user),
        db: Session = Depends(get_db)
):
    # TODO: user 권한 validation
    db_user = crud_users.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_util.validate_password(user.username, user.password)
    try:
        result = crud_users.create_user(db=db, user=user)
        # TODO: logging 추가
        return result
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

async def get_user_list(
        current_user: User = Depends(deps.get_current_active_user),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(deps.get_db)
):
    if not crud_users.is_superuser(db, current_user):  # superuser(team_manager)가 아닌 일반 user는 user list를 조회할 수 없음
        raise HTTPException(status_code=403, detail="접근할 수 없는 작업입니다.")
    try:
        if not crud_users.is_master(db, current_user):  # superuser(team_manager)는 자신이 속한 team의 user만 조회
            return crud_users.get_users_by_team(
                db=db, team=current_user.team, skip=skip, limit=limit
            )
        return crud_users.get_all_users(db=db, skip=skip, limit=limit)  # master(system_manager)는 모든 user 조회
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
    

async def update_user(
        user_id: str,
        user: UserUpdate,
        current_user: User = Depends(deps.get_current_active_user),
        db: Session = Depends(get_db)
):
    # TODO: user 권한 validation
    check_None = [None, "", "string"]
    if user.password not in check_None:
        user_util.validate_password(user.username, user.password)
    try:
        result = crud_users.update_user(db=db, user_id=user_id, user=user)
        # TODO: logging 추가
        return result
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
