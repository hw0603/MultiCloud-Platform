import datetime

from db.session import Base
from sqlalchemy import JSON, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship


class Stack(Base):
    __tablename__ = "stack"
    stack_id = Column(Integer, primary_key=True, index=True)
    stack_name = Column(String(50), unique=True)
    stack_type = Column(String(50))
    description = Column(Text())
    var_list = Column(JSON)
    var_json = Column(JSON)
    team_access = Column(JSON)
    tf_version = Column(String(30))
    user_id = Column(Integer)
    git_repo = Column(String(200))
    branch = Column(String(50))
    task_id = Column(String(200))
    project_path = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.now())
    # deploy = relationship("Deploy")
