from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    MONGODB_URL: str = os.getenv("MCP_MONGODB_URL", "mongodb:27017/")
    MONGODB_DB_NAME: str = os.getenv("MCP_MONGODB_DB_NAME", "mcp-remote-state")
    MONGODB_USER: str = os.getenv("MCP_MONGODB_USER", "admin")
    MONGODB_PASSWD: str = os.getenv("MCP_MONGODB_PASSWD", "admin")

    class Config:
        env_file = "./config/.env"


settings = Settings()
