from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    BUCKET: str = os.getenv("MCP_BUCKET", "mcp-remote-state")
    REGION: str = os.getenv("AWS_DEFAULT_REGION", "ap-northeast-2")
    AWS_ACCESS_KEY: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")

    class Config:
        env_file = "./config/.env"


settings = Settings()
