from config.database_config import SessionLocal
from pyparsing import Generator

"""
의존성 관리 모듈
"""

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
