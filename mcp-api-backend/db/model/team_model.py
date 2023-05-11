import datetime

from db.session import Base
from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint


class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    __table_args__ = (UniqueConstraint("team_name"),)
    