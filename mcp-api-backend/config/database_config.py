import os
import logging
from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "Key")
    DB_ENGINE: str = os.getenv("DB_ENGINE", "mysql")
    DB_NAME: str = os.getenv("DB_NAME", "mcp")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = os.getenv("DB_PORT", 3306)
    DB_USERNAME: str = os.getenv("DB_USERNAME", "multicloud")
    DB_PASS: str = os.getenv("DB_PASS", "password")
    DEBUG: bool = os.getenv("DEBUG", True)
    
    class Config:
        env_file = "./config/.env"

settings = Settings()

SQLALCHEMY_DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(
    settings.DB_ENGINE,
    settings.DB_USERNAME,
    settings.DB_PASS,
    settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_NAME,
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=200,
    max_overflow=-1,
    echo=settings.DEBUG  # 쿼리 로그 출력
)


logger = logging.getLogger("uvicorn")
logger.info(f"데이터베이스 URL: {SQLALCHEMY_DATABASE_URL}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
