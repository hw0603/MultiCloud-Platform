from fastapi import APIRouter, Depends, HTTPException
from storage.storage_base import StorageBase
from storage.connection import get_remote_state
import json

router = APIRouter()

@router.get("/{id}")
async def get_tfstate(
    id: str,
    remote_state: StorageBase = Depends(get_remote_state)
):
    result = remote_state.get(id)
    if not (result):
        raise HTTPException(status_code=404)
    return result


@router.post("/{id}")
async def post_tfstate(
    id: str, tfstate: dict,
    remote_state: StorageBase = Depends(get_remote_state)
):
    json.dumps(remote_state.put(id, tfstate))
    return {}
