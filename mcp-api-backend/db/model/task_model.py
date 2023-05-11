import datetime

from db.session import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey


class Task(Base):
    __tablename__ = "task"
    task_id = Column(String(300), primary_key=True)
    task_name = Column(String(100))
    user_id = Column(Integer)
    deploy_id = Column(Integer, ForeignKey("deploy.deploy_id"))
    username = Column(String(50), nullable=False)
    team = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
