import datetime

from db.session import Base
from sqlalchemy import JSON, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class DeployDetail(Base):
    __tablename__ = "deploy_detail"
    id = Column(Integer, primary_key=True, index=True)
    deploy_id = Column(Integer, ForeignKey("deploy.deploy_id"))
    stack_id = Column(Integer, ForeignKey("stack.stack_id"))
    tfvar_file = Column(String(50), nullable=True)
    variables = Column(JSON)

    # Relationships
    deploy_rel = relationship("Deploy", back_populates="deploy_detail_rel")
