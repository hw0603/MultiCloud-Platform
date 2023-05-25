from fastapi import APIRouter
from config.api_config import settings as api_settings
from config import celery_config as celery_settings
from config.database_config import settings as db_settings
from config.grafana_config import settings as grafana_settings
from config.airflow_config import settings as airflow_settings
import logging
import requests
import redis


router = APIRouter()
logger = logging.getLogger("uvicorn")


def check_airflow(s: requests.Session, name: str = "airflow-webserver"):
    # Airflow webserver 연결 확인
    try:
        req = s.get(f"http://{airflow_settings.AIRFLOW_URL}/health")
        logger.info(f"{name} 연결 확인: {req.status_code}")
        return {name: True}
    except Exception as e:
        logger.error(f"{name} 연결 실패: {e}")
        return {name: False}

def check_grafana(s: requests.Session, name: str = "grafana"):
    # Grafana 연결 확인
    try:
        req = s.get(f"http://{grafana_settings.GRAFANA_URL}")
        logger.info(f"{name} 연결 확인: {req.status_code}")
        return {name: True}
    except Exception as e:
        logger.error(f"{name} 연결 실패: {e}")
        return {name: False}

def check_redis(name: str = "redis"):
    # Redis 연결 확인
    try:
        r = redis.Redis(
            host=celery_settings.BACKEND_SERVER,
            port=6379
        )
        r.set("conn check", "true")
        logger.info(f"{name} 연결 확인: {r.get('conn check')}")
        return {name: True}
    except Exception as e:
        logger.error(f"{name} 연결 실패: {e}")
        return {name: False}

def check_rabbitmq(name: str = "rabbit"):
    # TODO: RabbitMQ 연결 확인
    raise NotImplementedError


@router.get("/")
async def check_connection():
    s = requests.Session()

    data = [
        check_airflow(s),
        check_grafana(s),
        check_redis(),
    ]

    result = {"api-backend": True}

    for di in data:
        result.update(di)


    return result