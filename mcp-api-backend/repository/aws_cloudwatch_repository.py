from sqlalchemy.orm import Session
from db.connection import get_db, get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from db.transactional import Transactional
from db.model.aws_cloudwatch_model import AwsCloudwatch
import db.model.aws_cloudwatch_model as models
from datetime import datetime

AwsCloudwatchModel = models.AwsCloudwatch


@Transactional()
async def createAwsCloudwatch(
    db: AsyncSession,
    instance_id: str, provider_id: int,
    metric: str, timestamp: datetime, value: float, unit: str,
):
    db_activity = AwsCloudwatch(
        instance_id=instance_id,
        provider_id=provider_id,
        metric=metric,
        timestamp=timestamp,
        value=value,
        unit=unit
    )
    db.add(db_activity)
