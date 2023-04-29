from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    # for test
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "key_id")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "access_key")

    class Config:
        env_file = "./config/.env"


settings = Settings()
