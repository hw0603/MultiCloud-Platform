"""
의존성 관리 모듈
"""
from typing import Generator
from db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_active_user():
    # TODO: 현재 로그인한 사용자를 반환하는 함수. 현재는 테스트를 위해 임의의 값(시스템 관리자)을 반환하도록 구현
    from types import SimpleNamespace
    return SimpleNamespace(
        id=1,
        username="admin",
        team="team",
        is_master=True
    )
