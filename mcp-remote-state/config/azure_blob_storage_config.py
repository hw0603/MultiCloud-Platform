from pydantic import BaseSettings
import os

# DOCS: https://docs.microsoft.com/ko-kr/azure/storage/blobs/storage-quickstart-blobs-python

class Settings(BaseSettings):
    CONTAINER: str = os.getenv("MCP_CONTAINER", "mcp-remote-state")
    AZURE_ACCOUNT: str = os.getenv("AZURE_ACCOUNT")
    AZURE_ACCESS_KEY: str = os.getenv("AZURE_ACCESS_KEY")


settings = Settings()
