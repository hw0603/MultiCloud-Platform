import datetime

from db.session import Base
from sqlalchemy import JSON, Column, DateTime, Integer, String


class DeployDetail(Base):
    __tablename__ = "deploy_detail"
    id = Column(Integer, primary_key=True, index=True)
    tfvar_file = Column(String(50), nullable=True)
    variables = Column(JSON)
