import datetime

from db.session import Base
from sqlalchemy import JSON, Column, DateTime, Integer, String, Text


class Stack(Base):
    __tablename__ = "stack"
    id = Column(Integer, primary_key=True, index=True)
    stack_name = Column(String(50), unique=True)
    stack_type = Column(String(50), nullable=False)
    description = Column(Text())
    var_list = Column(JSON)
    var_json = Column(JSON)
    team_access = Column(JSON)
    tf_version = Column(String(30))
    user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now())
