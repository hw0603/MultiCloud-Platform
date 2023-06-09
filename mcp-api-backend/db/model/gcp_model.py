import datetime

from db.session import Base
from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

class Gcloud_provider(Base):
    __tablename__ = "gcloud_provider"
    id = Column(Integer, primary_key=True, index=True)
    environment = Column(String(200), nullable=False)
    team = Column(String(50), ForeignKey("team.team_name"))
    gcloud_keyfile_json = Column(String(5000), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    __table_args__ = (UniqueConstraint("team", "environment"),)
