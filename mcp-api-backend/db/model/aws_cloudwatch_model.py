from db.session import Base
from sqlalchemy import Column, DateTime, Integer, Float, String


class AwsCloudwatch(Base):
    __tablename__ = "aws_cloudwatch"
    instance_id = Column(String(50), primary_key=True, index=True)
    provider_id = Column(Integer, nullable=False)  # TODO: FK 지정해야 함
    metric = Column(String(50), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(10), nullable=False)
