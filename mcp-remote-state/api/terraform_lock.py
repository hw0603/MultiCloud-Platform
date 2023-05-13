from fastapi import APIRouter, Depends, HTTPException
from storage.storage_base import StorageBase
from storage.connection import get_remote_state

router = APIRouter()


@router.put("/{id}", tags=["Lock"])
async def put_tfstate(
    id: str, tfstate: dict,
    remote_state: StorageBase = Depends(get_remote_state)
):
    success, info = remote_state.lock(id, tfstate)
    if not (success):
        raise HTTPException(status_code=423)
    return info


@router.delete("/{id}", tags=["Lock"])
async def delete_tfstate(
    id: str,
    remote_state: StorageBase = Depends(get_remote_state)
):
    tfstate = {}
    if not (remote_state.unlock(id, tfstate)):
        raise HTTPException(status_code=404)
    return {}
