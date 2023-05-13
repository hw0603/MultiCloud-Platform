from fastapi import APIRouter

router = APIRouter()

@router.get("/{id}")
async def get_tfstate(id: str):
    ...


@router.post("/{id}")
async def post_tfstate(id: str, tfstate: dict):
    ...
