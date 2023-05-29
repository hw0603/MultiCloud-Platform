from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from service import instance_service, grafana_service
from typing import Optional, List
from api.api_response import *
from db.connection import get_db, get_async_db
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from config.api_config import settings as api_settings  # for testing
from config.grafana_config import settings as grafana_settings
from entity import user_entity as schemas_users
from src.shared.security.deps import get_current_user
from repository import aws_repository as crud_aws
from src.shared.security.vault import vault_encrypt, vault_decrypt


@vault_encrypt
def encrypt(secreto):
    try:
        return secreto
    except Exception as err:
        raise err


@vault_decrypt
def decrypt(secreto):
    try:
        return secreto
    except Exception as err:
        raise err

router = APIRouter()

EC2_Cloudwatch_Metrics = {
    "StatusCheckFailed_System", "StatusCheckFailed_Instance", "StatusCheckFailed",
    "CPUUtilization",
    "EBSReadBytes", "EBSWriteBytes", "EBSReadOps", "EBSWriteOps", "EBSByteBalance%", "EBSIOBalance%",
    "NetworkPacketsIn", "NetworkPacketsOut", "NetworkIn", "NetworkOut",
    "MetadataNoToken"
}


@router.get("/list")
def get_instance_list(
    current_user: schemas_users.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 현재 사용자의 프로바이더 정보를 가져옴
    csp_providers = crud_aws.get_team_aws_profile(
        db=db, team=current_user.team, environment=None
    )

    aws_account = next(iter(csp_providers), None)
    AWS_ACCESS_KEY_ID = decrypt(aws_account.access_key_id)
    AWS_SECRET_ACCESS_KEY = decrypt(aws_account.secret_access_key)
    AWS_DEFAULT_REGION = aws_account.default_region

    instance_list = instance_service.get_instance_list(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
    )
    return ApiResponse.with_data(ApiStatus.SUCCESS, "success", instance_list)



@router.get("/{instance_id}")
async def get_instance_state(
    instance_id: str, metrics: Optional[List[str]] = Query(None),
    current_user: schemas_users.User = Depends(get_current_user),
    db: Session = Depends(get_async_db),
    syncdb: Session = Depends(get_db)
):
    '''
    사용자로부터 조회할 지표들을 받아서 DB 업데이트 후,
    그라파나 대시보드를 생성하고 각 패널에 접근할 수 있는 iframe url 반환
    '''

    # 현재 사용자의 프로바이더 정보를 가져옴
    csp_providers = crud_aws.get_team_aws_profile(
        db=syncdb, team=current_user.team, environment=None
    )

    aws_account = next(iter(csp_providers), None)
    AWS_ACCESS_KEY_ID = decrypt(aws_account.access_key_id)
    AWS_SECRET_ACCESS_KEY = decrypt(aws_account.secret_access_key)
    AWS_DEFAULT_REGION = aws_account.default_region

    # query param 리스트 validation
    if not metrics:
        return ApiResponse(ApiStatus.BAD_REQUEST, "조회할 Cloudwatch 지표가 전달되지 않았습니다.")
    if not (all(m in EC2_Cloudwatch_Metrics for m in metrics)):
        return ApiResponse(ApiStatus.BAD_REQUEST, "Cloudwatch 지표가 아닌 지표가 포함되어 있습니다.")

    # 지표 별 데이터 조회 후 DB 업데이트
    state = await instance_service.get_instance_state(
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_DEFAULT_REGION,
        instance_id,
        metrics,
        db
    )

    # 그라파나 대시보드 생성
    GRAFANA_URL = grafana_settings.GRAFANA_URL
    GRAFANA_CREDS = grafana_settings.GRAFANA_CREDS
    dashboard_data = await grafana_service.create_dashboard(
        instance_id=instance_id,
        provider_id=12345,
        grafana_url=GRAFANA_URL,
        grafana_creds=GRAFANA_CREDS
    )

    return ApiResponse.with_data(ApiStatus.SUCCESS, "success", dashboard_data)
