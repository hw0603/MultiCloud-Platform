from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    # for test
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "key_id")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "access_key")

    INIT_USER: dict = {
        "username": os.getenv("INIT_USER_NAME", "admin"),
        "fullname": os.getenv("INIT_FULL_NAME", "Master of the universe user"),
        "email": os.getenv("INIT_USER_EMAIL", "admin@example.com")
    }

    USE_TEST_API: bool = os.getenv("USE_TEST_API", False)

    API_V1_URL: str = "/api/v1"
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALL_ROLE: list = ["user", "system_manager", "team_manager"]

    class Config:
        env_file = "./config/.env"


settings = Settings()
