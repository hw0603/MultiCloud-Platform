from typing import Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from requests import Session
from db.connection import get_db
from src.shared.security.tokens import UserExist
from repository import user_repository as crud_users
from repository import activity_logs_repository as crud_activity


def login_access_token(
    user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Any:
    user_db = crud_users.get_user_by_username(db, username=user.username)
    if not user_db:
        raise HTTPException(
                status_code=404,
                detail=f"존재하지 않는 사용자입니다."
            )
    validate = UserExist(user_db, user.username, user.password)

    crud_activity.create_activity_log(
        db=db,
        username=user_db.username,
        team=user_db.team,
        action=f"사용자 로그인",
    )
    return validate.validate_user()
