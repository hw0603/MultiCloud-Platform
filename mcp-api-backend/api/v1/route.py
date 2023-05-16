from fastapi import APIRouter
from api.v1 import *


api_router = APIRouter()

@api_router.get("/", tags=["Connection Check"])
async def status_check():
    return {"status": "Connected"}

api_router.include_router(testapi.router, prefix="/test", tags=["Test"])
api_router.include_router(adminInfo.router, prefix="/adminInfo", tags=["AdminInfo"])
api_router.include_router(instance.router, prefix="/instance", tags=["Instance"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(stack.router, prefix="/stacks", tags=["Stack"])
api_router.include_router(variable.router, prefix="/variable", tags=["Variable"])
api_router.include_router(activity_log.router, prefix="/activity_log", tags=["ActivityLog"])
