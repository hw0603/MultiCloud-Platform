import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    INIT_USER = {
        "username": os.getenv("INIT_USER_NAME", "admin"),
        "fullname": os.getenv("INIT_FULL_NAME", "Master of the universe user"),
        "email": os.getenv("INIT_USER_EMAIL", "admin@example.com")
    }

    
    class Config:
        env_file = "./config/.env"

settings = Settings()
