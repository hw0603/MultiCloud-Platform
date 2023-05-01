import datetime

from db.session import Base
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    fullname = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(JSON, nullable=False)
    team = Column(JSON, nullable=False)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime)
