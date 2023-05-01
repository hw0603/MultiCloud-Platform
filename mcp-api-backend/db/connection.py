from db.session import SessionLocal
from pyparsing import Generator


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db  # DB 연결에 성공한 경우 세션 시작
    finally:
        db.close()  # DB 세션 시작된 후, API 호출 종료 시 세션 close
