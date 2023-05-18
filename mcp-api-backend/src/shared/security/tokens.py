from datetime import datetime, timedelta
from typing import Any, Union
from config.api_config import settings
from jose import jwt

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

