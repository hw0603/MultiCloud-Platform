from fastapi import APIRouter, Depends
import service.azure_service as azureService
import entity.azure_entity as schemas_azure
import logging


router = APIRouter()
logger = logging.getLogger("uvicorn")


@router.post("/", status_code=200)
async def create_new_azure_profile(
    create_azure_account: schemas_azure.AzureBase = Depends(
        azureService.create_new_azure_profile
    ),
):
    return create_azure_account


@router.get("/")
async def get_all_azure_accounts(
    get_azure_account: schemas_azure.AzureBase = Depends(
    azureService.get_all_azure_accounts
    ),
):
    return get_azure_account


@router.delete("/{azure_account_id}")
async def delete_azure_account_by_id(
    delete_azure_account: schemas_azure.AzureBase = Depends(
        azureService.azure_account_by_id
    ),
):
    return delete_azure_account
