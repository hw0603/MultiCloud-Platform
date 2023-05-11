import datetime

from db.session import Base
from sqlalchemy import JSON, Column, DateTime, Integer, String, ForeignKey


class DeployDetail(Base):
    __tablename__ = "deploy_detail"
    id = Column(Integer, primary_key=True, index=True)
    deploy_id = Column(Integer, ForeignKey("deploy.deploy_id"))
    stack_id = Column(Integer, ForeignKey("stack.stack_id"))
    tfvar_file = Column(String(50), nullable=True)
    variables = Column(JSON)
