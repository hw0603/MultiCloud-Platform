from fastapi import APIRouter, Depends
from storage.storage_base import StorageBase
from storage.connection import get_remote_state

router = APIRouter()


@router.put("/{id}", tags=["Lock"])
async def put_tfstate(
    id: str, tfstate: dict,
    remote_state: StorageBase = Depends(get_remote_state)
):
    ...


@router.delete("/{id}", tags=["Lock"])
async def delete_tfstate(
    id: str,
    remote_state: StorageBase = Depends(get_remote_state)
):
    ...
