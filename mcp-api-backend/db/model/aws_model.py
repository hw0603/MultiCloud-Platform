import datetime

from db.session import Base
from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

class Aws_provider(Base):
    __tablename__ = "aws_provider"
    id = Column(Integer, primary_key=True, index=True)
    environment = Column(String(200), nullable=False)
    team = Column(String(50), ForeignKey("team.team_name"))
    access_key_id = Column(String(200), nullable=False)
    secret_access_key = Column(String(200), nullable=False)
    default_region = Column(String(200))
    profile_name = Column(String(200), nullable=False)
    role_arn = Column(String(200), nullable=True)
    source_profile = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    __table_args__ = (UniqueConstraint("environment"),)
