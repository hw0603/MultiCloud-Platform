from fastapi import APIRouter
from api.v1 import *


api_router = APIRouter()


api_router.include_router(health.router, tags=["Connection Check"])
api_router.include_router(adminInfo.router, prefix="/adminInfo", tags=["AdminInfo"])
api_router.include_router(instance.router, prefix="/instance", tags=["Instance"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(stack.router, prefix="/stacks", tags=["Stack"])
api_router.include_router(variable.router, prefix="/variable", tags=["Variable"])
api_router.include_router(activity_log.router, prefix="/activity_log", tags=["ActivityLog"])
api_router.include_router(aws.router, prefix="/aws", tags=["Aws"])
api_router.include_router(gcp.router, prefix="/gcp", tags=["Gcp"])
api_router.include_router(azure.router, prefix="/azure", tags=["Azure"])
api_router.include_router(custom_provider.router, prefix="/custom_provider", tags=["CustomProvider"])
api_router.include_router(deploy.router, prefix="/deploy", tags=["Deploy"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(status.router, prefix="/status", tags=["Status"])

# api_router.include_router(testapi.router, prefix="/test", tags=["Test"])
