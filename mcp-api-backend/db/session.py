from config.database_config import settings
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from sqlalchemy.ext.asyncio import async_scoped_session

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from asyncio import current_task

logger = logging.getLogger("uvicorn")

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
)  # 동기 엔진
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL.replace(settings.DB_ENGINE, settings.DB_ENGINE_ASYNC),
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=200,
    max_overflow=-1,
    echo=settings.DEBUG  # 쿼리 로그 출력
)  # 비동기 엔진

logger.info(f"데이터베이스 URL: {SQLALCHEMY_DATABASE_URL}")
SessionLocal = scoped_session(
    session_factory=sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
AsyncSessionLocal = async_scoped_session(
    session_factory=sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession),
    scopefunc=current_task
)

Base = declarative_base()
