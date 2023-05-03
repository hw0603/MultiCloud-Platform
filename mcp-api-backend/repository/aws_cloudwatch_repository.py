from sqlalchemy.orm import Session
from db.connection import get_db, get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from db.transactional import Transactional
from db.model.aws_cloudwatch_model import AwsCloudwatch
import db.model.aws_cloudwatch_model as models
import datetime
from sqlalchemy import select


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


async def getLastUpdatedTime(
    db: AsyncSession, instance_id: str
) -> datetime.datetime | None:
    query = (
        select(AwsCloudwatchModel.timestamp)
        .where(AwsCloudwatchModel.instance_id == instance_id)
        .order_by(AwsCloudwatchModel.timestamp.desc())
        .limit(1)
    )
    result = await db.execute(query)

    # KST 기준으로 DB에 저장하므로, UTC로 변환하여 반환
    return r[0] - datetime.timedelta(hours=9) if (r := result.fetchone()) is not None else None


async def getAwsCloudwatch(
    db: AsyncSession, instance_id: str, provider_id: int,
    metric: str, timestamp: datetime
) -> AwsCloudwatch | None:
    # query = (
    #     select(AwsCloudwatchModel)
    #     .where(AwsCloudwatchModel.instance_id == instance_id)
    #     .where(AwsCloudwatchModel.provider_id == provider_id)
    #     .where(AwsCloudwatchModel.metric == metric)
    #     .where(AwsCloudwatchModel.timestamp == timestamp)
    # )
    # result = await db.execute(query)
    # return result.fetchone()

    id = (instance_id, provider_id, metric, timestamp)
    return await db.get(AwsCloudwatchModel, id)