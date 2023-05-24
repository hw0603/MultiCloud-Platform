from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    GRAFANA_URL: str = os.getenv("GRAFANA_URL", "localhost:3001")
    GRAFANA_CREDS: str = os.getenv("GRAFANA_CREDS", "admin")

    class Config:
        env_file = "./config/.env"


settings = Settings()
