from fastapi import APIRouter, Depends
from storage.storage_base import StorageBase
from storage.connection import get_remote_state

router = APIRouter()

@router.get("/{id}")
async def get_tfstate(
    id: str,
    remote_state: StorageBase = Depends(get_remote_state)
):
    ...


@router.post("/{id}")
async def post_tfstate(
    id: str, tfstate: dict,
    remote_state: StorageBase = Depends(get_remote_state)
):
    ...
