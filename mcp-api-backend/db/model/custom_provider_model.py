import datetime

from db.session import Base
from sqlalchemy import JSON, Column, DateTime, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship


class Custom_provider(Base):
    __tablename__ = "custom_provider"
    id = Column(Integer, primary_key=True, index=True)
    environment = Column(String(200), nullable=False)
    team = Column(String(50), ForeignKey("team.team_name"))
    configuration = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    __table_args__ = (UniqueConstraint("environment"),)

    # Relationships
    team_rel = relationship("Team", back_populates="custom_provider_rel")
