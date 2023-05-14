from fastapi import APIRouter
from . import hello, adminInfo, instance, user


api_router = APIRouter()
api_router.include_router(hello.router, prefix="/hello", tags=["Hello"])
api_router.include_router(adminInfo.router, prefix="/adminInfo", tags=["AdminInfo"])
api_router.include_router(instance.router, prefix="/instance", tags=["Instance"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
