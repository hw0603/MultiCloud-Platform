import datetime

from db.session import Base 
from sqlalchemy import JSON, Column, DateTime, Integer, String


class ActivityLogs(Base):
    __tablename__ = "activity_log"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    team = Column(JSON, nullable=False)
    action = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
