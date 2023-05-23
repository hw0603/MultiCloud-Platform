from fastapi import APIRouter, Depends
import service.gcp_service as gcpService
import entity.gcp_entity as schemas_gcp
import logging


router = APIRouter()
logger = logging.getLogger("uvicorn")


@router.post("/", status_code=200)
async def create_new_gcloud_profile(
    create_gcp_account: schemas_gcp.GcloudBase = Depends(gcpService.new_gcloud_profile),
):
    return create_gcp_account


@router.get("/")
async def get_all_gcloud_accounts(
    get_gcp_account: schemas_gcp.GcloudBase = Depends(gcpService.all_gcloud_accounts),
):
    return get_gcp_account


@router.delete("/{gcloud_account_id}")
async def delete_gcloud_account_by_id(
    get_gcp_account: schemas_gcp.GcloudBase = Depends(gcpService.gcloud_account_by_id),
):
    return get_gcp_account

