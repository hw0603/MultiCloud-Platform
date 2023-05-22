from typing import Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from requests import Session
from db.connection import get_db
from src.shared.security.tokens import UserExist
from repository import user_repository as crud_users


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
    return validate.validate_user()
