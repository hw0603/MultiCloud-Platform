from pydantic import BaseSettings
import os

# DOCS: https://cloud.google.com/storage/docs/reference/libraries#create-service-account-console

class Settings(BaseSettings):
    BUCKET: str = os.getenv("MCP_BUCKET", "mcp-remote-state")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    class Config:
        env_file = "./config/.env"


settings = Settings()
