from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    AIRFLOW_URL: str = os.getenv("AIRFLOW_URL", "localhost:7001")
    AIRFLOW_CREDS: str = os.getenv("AIRFLOW_CREDS", "admin:admin")

    class Config:
        env_file = "./config/.env"


settings = Settings()
