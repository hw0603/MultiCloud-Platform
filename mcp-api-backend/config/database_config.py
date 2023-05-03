import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "Key")
    DB_ENGINE: str = os.getenv("DB_ENGINE", "mysql")
    DB_ENGINE_ASYNC: str = os.getenv("DB_ENGINE_ASYNC", "mysql+aiomysql")
    DB_NAME: str = os.getenv("DB_NAME", "mcp")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = os.getenv("DB_PORT", 3306)
    DB_USERNAME: str = os.getenv("DB_USERNAME", "multicloud")
    DB_PASS: str = os.getenv("DB_PASS", "password")
    DEBUG: bool = os.getenv("DEBUG", True)
    
    class Config:
        env_file = "./config/.env"

settings = Settings()
