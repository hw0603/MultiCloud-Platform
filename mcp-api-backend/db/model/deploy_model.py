import datetime

from db.session import Base
from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)


class Deploy(Base):
    __tablename__ = "deploy"
    deploy_id = Column(Integer, primary_key=True, index=True)
    deploy_name = Column(String(100))
    start_time = Column(String(100))
    destroy_time = Column(String(100))
    user_id = Column(Integer)
    username = Column(String(50), nullable=False)
    team = Column(String(50), nullable=False)
    environment = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime)
    detail_cnt = Column(Integer)
