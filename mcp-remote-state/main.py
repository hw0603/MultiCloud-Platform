from fastapi import FastAPI
from config.storage_config import settings
from api.route import api_router
import logging

logger = logging.getLogger("uvicorn")
logger.warn(f"{settings.MCP_STORAGE_BACKEND} 원격 저장소를 사용합니다.")


app = FastAPI(
    title=f"Multi Cloud Platform Remote State API",
    description="퍼블릭 기반 멀티클라우드 플랫폼 Remote State API 서버",
    version=f"{settings.MCP_REMOTE_STATE_VER}",
)
app.include_router(api_router)
