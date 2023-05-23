"""
의존성 관리 모듈
"""
from typing import Generator
from db.session import SessionLocal

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError
from pydantic import ValidationError
from requests import Session
from config.api_config import settings
from db.connection import get_db
from src.shared.security.tokens import decode_access_token
from db.model import user_model
from entity import user_entity as schemas
from repository import user_repository as crud_users

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_URL}/authenticate/access"
)

Usermodel = user_model.User

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="권한을 검증할 수 없습니다",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # JWT 토큰의 유효성을 검사, 토큰의 페이로드(claims) 추출
        payload = decode_access_token(token=token)
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except (JWTError):
        raise credentials_exception
    user = crud_users.get_user_by_id(db, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user

def get_current_active_user(
    db: Session = Depends(get_db),
    current_user: Usermodel = Depends(get_current_user)
):
    if not crud_users.is_active(db, current_user):
        raise HTTPException(status_code=400, detail="비활성화된 사용자입니다.")
    return current_user

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

