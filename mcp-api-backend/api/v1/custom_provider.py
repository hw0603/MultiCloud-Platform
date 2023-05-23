from fastapi import APIRouter, Depends
import service.custom_provider_service as customProviderService
import entity.custom_provider_entity as schemas_custom_provider
import logging


router = APIRouter()
logger = logging.getLogger("uvicorn")


@router.post("/", status_code=200)
async def create_custom_provider_account(
    create_custom_provider_account: schemas_custom_provider.CustomProviderBase = Depends(
        customProviderService.create_custom_provider_profile
    ),
):
    return create_custom_provider_account


@router.get("/")
async def get_all_custom_providers_accounts(
    get_custom_provider_account: schemas_custom_provider.CustomProviderBase = Depends(
        customProviderService.all_custom_providers_accounts
    ),
):
    return get_custom_provider_account


@router.delete("/{custom_provider_id}")
async def delete_custom_provider_account_by_id(
    delete_custom_provider_account: schemas_custom_provider.CustomProviderBase = Depends(
        customProviderService.custom_provider_account_by_id
    ),
):
    return delete_custom_provider_account

