from fastapi import APIRouter
from api import *


api_router = APIRouter()

@api_router.get("/", tags=["Connection Check"])
async def status_check():
    return {"status": "Connected"}

api_router.include_router(terraform_state.router, prefix="/terraform_state", tags=["Terraform State"])
api_router.include_router(terraform_lock.router, prefix="/terraform_lock", tags=["Terraform Lock"])
