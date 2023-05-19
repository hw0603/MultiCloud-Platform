from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import HTTPException
from config.api_config import settings
from jose import jwt
from passlib.context import CryptContext

class TokenCreate:
    def __init__(self, subject: dict, expires_delta: timedelta = None):
        self.subject = subject                  # subject: Token의 정보 (key로 'sub'(Token이 대상하는 사용자를 식별하는 정보)를 꼭 포함해야 함)
        self.expires_delta = expires_delta      # 만료 시간

    def create_access_token(self) -> str:
        to_encode = self.subject.copy()
        if self.expires_delta:
            # 현재 기준 UTC에 Token 유효시간을 더한 시각을 만료 시각으로 함.
            expire = datetime.utcnow() + self.expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        # Token의 만료 시간 설정
        to_encode.update({"exp": expire})
        to_encode = {"exp": expire, "sub": str(self.subject)}

        # JWT 토큰 생성
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

class CheckPasswd:
    def __init__(self, password: str, hashed_password):
        self.password = password
        self.hashed_password = hashed_password
    
    def verify_password(self) -> bool:
        # 비밀번호 해싱 및 검증을 수행하는 인스턴스(CryptContext) 생성 (bycrypt 알고리즘 사용)
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(self.password, self.hashed_password)

class UserExist:
    def __init__(
        self,
        user_db,
        user: str,
        password: str,
        check_password=CheckPasswd, 
        token=TokenCreate
    ):
        self.user_db = user_db
        self.user = user
        self.password = password
        self.check_password = check_password
        self.token = token
    
    def validate_user(self):
        try:
            user = self.user_db              # DB에 저장된 user정보 저장
            hash_password = user.password    # DB에 저장된 password 저장
            config_check_password = self.check_password(self.password, hash_password)

            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            config_token = self.token(subject={"sub": user.id}, expires_delta=access_token_expires)
        
        except Exception as err:
            HTTPException(status_code=400, detail=str(err))
        
        if not config_check_password.verify_password():
            raise HTTPException(
                status_code=403, detail="사용자 이름이나 패스워드가 올바르지 않습니다."
            )
        # TODO: 추가 exception validation 필요

        # Token 반환
        return {
            "access_token": config_token.create_access_token(),
            "token_type": "brearer",
        }

