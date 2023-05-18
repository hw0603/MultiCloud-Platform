from fastapi import APIRouter, Depends
import service.aws_service as awsService
import entity.aws_entity as schemas_aws
import logging


router = APIRouter()
logger = logging.getLogger("uvicorn")


@router.post("/", response_model=schemas_aws.Aws)
async def create_new_aws_profile(
    create_aws_profile: schemas_aws.AwsAsumeProfile = Depends(
        awsService.create_new_aws_profile
    ),
):
    return create_aws_profile


@router.get("/")
async def get_all_aws_accounts(
    get_aws_profile: schemas_aws.AwsAsumeProfile = Depends(
        awsService.get_all_aws_accounts
    ),
):
    return get_aws_profile


@router.delete("/{aws_account_id}")
async def delete_aws_account_by_id(
    delete_aws_profile: schemas_aws.AwsAsumeProfile = Depends(
        awsService.aws_account_by_id
    ),
):
    return delete_aws_profile

