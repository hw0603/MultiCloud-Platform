from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from db.model import (
    aws_model,
    azure_model,
    gcp_model,
    custom_provider_model,
    deploy_model,
    stack_model
)

router = APIRouter()

@router.get("/")
def get_status_count(db: Session = Depends(get_db)):
    # 서버에 등록된 프로바이더 수, 스택 개수, Deploy 수를 반환
    # 임시 API로, service 패키지를 사용하지 않고 라우터에서 직접 DB 접근하여 데이터를 가져옴. Needs Refactor

    # 프로바이더 수

    aws_count = db.query(aws_model.Aws_provider).count()
    azure_count = db.query(azure_model.Azure_provider).count()
    gcp_count = db.query(gcp_model.Gcloud_provider).count()
    custom_count = db.query(custom_provider_model.Custom_provider).count()

    # 스택 수
    stack_count = db.query(stack_model.Stack).count()

    # Deploy 수
    deploy_count = db.query(deploy_model.Deploy).count()
    
    # 프로바이더 수, 스택 개수, Deploy 수를 반환
    return {
        "aws_count": aws_count,
        "azure_count": azure_count,
        "gcp_count": gcp_count,
        "custom_count": custom_count,
        "stack_count": stack_count,
        "deploy_count": deploy_count,
    }
