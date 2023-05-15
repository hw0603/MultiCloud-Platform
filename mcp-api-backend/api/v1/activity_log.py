from fastapi import APIRouter, Depends

from entity import user_entity as schemas_users
from service import activity_log_service as service

router = APIRouter()


@router.get("/id/{username}")
async def get_activity_logs_by_username(
    get_activity: schemas_users.User = Depends(service.get_activity_logs_by_username)
):
    return get_activity


@router.get("/all")
async def get_all_activity_logs(
    get_all_activity: schemas_users.User = Depends(service.get_all_activity_logs)
):
    return get_all_activity
