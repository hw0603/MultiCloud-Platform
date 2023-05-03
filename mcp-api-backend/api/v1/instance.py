from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from service import instance_service
from typing import Optional, List
from api.api_response import *
from db.connection import get_db, get_async_db
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from config.api_config import settings  # for testing

router = APIRouter()

EC2_Cloudwatch_Metrics = {
    "StatusCheckFailed_System", "StatusCheckFailed_Instance", "StatusCheckFailed",
    "CPUUtilization",
    "EBSReadBytes", "EBSWriteBytes", "EBSReadOps", "EBSWriteOps", "EBSByteBalance%", "EBSIOBalance%",
    "NetworkPacketsIn", "NetworkPacketsOut", "NetworkIn", "NetworkOut",
    "MetadataNoToken"
}


@router.get("/list")
def get_instance_list():
    # TODO: Authentication 추가 후에는 토큰에서 각 프로바이더의 인증 정보를 가져와서 사용할 것
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    AWS_DEFAULT_REGION = 'ap-northeast-2'

    instance_list = instance_service.get_instance_list(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION)
    return ApiResponse.with_data(ApiStatus.SUCCESS, "success", instance_list)


# @router.get("/test")
# async def test(db: AsyncSession = Depends(get_async_db)):
#     import random
#     await instance_service.addAwsCloudwatch(
#         db,
#         "i-0a0b0c0d0e0f0g0h0",
#         random.randint(0, 1000),
#         "CPUUtilization",
#         "2021-06-01 00:00:00",
#         1.1,
#         "Percent"
#     )

#     return ApiResponse.with_data(ApiStatus.SUCCESS, "success", "test")


@router.get("/{instance_id}")
async def get_instance_state(
    instance_id: str, metrics: Optional[List[str]] = Query(None),
    db: Session = Depends(get_async_db)
):
    ''' 사용자로부터 조회할 지표들을 받아서 조회 결과를 반환 '''

    # TODO: Authentication 추가 후에는 토큰에서 각 프로바이더의 인증 정보를 가져와서 사용할 것
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    AWS_DEFAULT_REGION = 'ap-northeast-2'

    # query param 리스트 validation
    if not metrics:
        return ApiResponse(ApiStatus.BAD_REQUEST, "조회할 Cloudwatch 지표가 전달되지 않았습니다.")
    if not (all(m in EC2_Cloudwatch_Metrics for m in metrics)):
        return ApiResponse(ApiStatus.BAD_REQUEST, "Cloudwatch 지표가 아닌 지표가 포함되어 있습니다.")

    state = await instance_service.get_instance_state(
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_DEFAULT_REGION,
        instance_id,
        metrics,
        db
    )
    return ApiResponse.with_data(ApiStatus.SUCCESS, "success", state)


