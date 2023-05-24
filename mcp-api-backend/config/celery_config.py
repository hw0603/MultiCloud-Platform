from celery import Celery
import os


celery_app = None

# RabbitMQ 브로커 설정
BROKER_USER = os.getenv("BROKER_USER", "admin")
BROKER_PASSWD = os.getenv("BROKER_PASSWD", "admin")
BROKER_SERVER = os.getenv("BROKER_SERVER", "127.0.0.1")  # "rabbit" or "redis" 사용
BROKER_SERVER_PORT = os.getenv("BROKER_SERVER_PORT", "5672")  # redis:6379, RabbitMQ:5672
BROKER_TYPE = os.getenv("BROKER_TYPE", "amqp")  # use "amqp" for RabbitMQ or redis

# Redis backend 설정
BACKEND_TYPE = os.getenv("BACKEND_TYPE", "redis")
BACKEND_USER = os.getenv("BACKEND_USER", "")
BACKEND_PASSWD = os.getenv("BACKEND_PASSWD", "")
BACKEND_SERVER = os.getenv("BACKEND_SERVER", "127.0.0.1")  # "redis"
BACKEND_DB = os.getenv("BACKEND_DB", "0")

# Celery 설정
celery_app = Celery(
    "worker",
    backend=f"{BACKEND_TYPE}://{BACKEND_USER}:{BACKEND_PASSWD}@{BACKEND_SERVER}/{BACKEND_DB}",
    broker=f"{BROKER_TYPE}://{BROKER_USER}:{BROKER_PASSWD}@{BROKER_SERVER}:{BROKER_SERVER_PORT}//",
)
celery_app.conf.task_routes = {"app.worker.celery_worker.test_celery": "api-queue"}

celery_app.conf.update(task_track_started=True)
celery_app.conf.result_expires = os.getenv("MCP_RESULT_EXPIRE", "259200")
