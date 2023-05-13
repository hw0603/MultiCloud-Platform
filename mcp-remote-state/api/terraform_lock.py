from fastapi import APIRouter

router = APIRouter()


@router.put("/{id}", tags=["Lock"])
async def put_tfstate(id: str, tfstate: dict):
    ...


@router.delete("/{id}", tags=["Lock"])
async def delete_tfstate(id: str):
    ...
