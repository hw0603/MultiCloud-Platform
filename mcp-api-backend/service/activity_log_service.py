from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from repository import activity_logs_repository as crud_activity
from src.shared.security import deps
from db.connection import get_db
from entity import user_entity as schemas_users
from repository import user_repository as crud_users


async def get_activity_logs_by_username(
    username: str,
    current_user: schemas_users.User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
):
    if not crud_users.is_superuser(db, current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not crud_users.is_master(db, current_user):
        team = current_user.team
        return crud_activity.get_activity_by_username_team(
            db=db, username=username, team=team
        )
    return crud_activity.get_activity_by_username(db, username=username)


async def get_all_activity_logs(
    current_user: schemas_users.User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if not crud_users.is_superuser(db, current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    try:
        if not crud_users.is_master(db, current_user):
            team = current_user.team
            result = crud_activity.get_all_activity_by_team(
                db=db, team=team, skip=skip, limit=limit
            )
            return result
        result = crud_activity.get_all_activity(db=db, skip=skip, limit=limit)
        return result
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"{err}")
