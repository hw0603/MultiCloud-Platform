from db.session import Base
from sqlalchemy import Column, DateTime, Integer, Float, String, PrimaryKeyConstraint, UniqueConstraint


class AwsCloudwatch(Base):
    __tablename__ = "aws_cloudwatch"
    __table_args__ = (PrimaryKeyConstraint('instance_id', 'provider_id', 'metric', 'timestamp'), )  # 복합키

    instance_id = Column(String(50), index=True, nullable=False)
    provider_id = Column(Integer, index=True, nullable=False)  # TODO: FK 지정해야 함
    metric = Column(String(50), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(10), nullable=False)
