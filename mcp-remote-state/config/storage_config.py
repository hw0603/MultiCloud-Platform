from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    MCP_STORAGE_BACKEND: str = os.getenv("MCP_STORAGE_BACKEND", "local")
    MCP_REMOTE_STATE_VER: str = os.getenv("MCP_REMOTE_STATE_VER", "1.0.0")

    class Config:
        env_file = "./config/.env"


settings = Settings()
