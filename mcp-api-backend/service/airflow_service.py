from config.airflow_config import settings as airflow_settings
import requests
import base64
import json


webserver_url = f"http://{airflow_settings.AIRFLOW_URL}"
airflow_creds = base64.b64encode(airflow_settings.AIRFLOW_CREDS.encode("utf-8")).decode("utf-8")
headers = {
    "Authorization": f"Basic {airflow_creds}",
    "Content-Type": "application/json"
}
s = requests.Session()
s.headers.update(headers)


# Airflow에 등록된 DAG 목록 정보 조회
def get_dag_list(
    limit: int = 100,
    offset: int = 0,
    tags: str = None,
    only_active: bool = True,
    dag_id_pattern: str = None,
) -> dict:
    API_PATH = "/api/v1/dags"
    params = {
        "limit": limit,
        "offset": offset,
        "tags": tags,
        "only_active": only_active,
        "dag_id_pattern": dag_id_pattern,
    }
    response = s.get(f"{webserver_url}{API_PATH}", params=params)

    return response.json()


# DAG Trigger
def trigger_dag(dag_id: str, conf: dict = {}) -> dict:
    API_PATH = f"/api/v1/dags/{dag_id}/dagRuns"
    data = {"conf": conf}
    response = s.post(f"{webserver_url}{API_PATH}", json=data)

    return response.json()


# DAGRun 내에 있는 Task들의 Status 조회
def get_task_status(dag_id: str, dag_run_id: str) -> dict:
    API_PATH = f"/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances"
    response = s.get(f"{webserver_url}{API_PATH}")

    return response.json()


# Task 별 XCOM 키 값 조회
def get_task_xcom(dag_id: str, dag_run_id: str, task_id: str) -> dict:
    API_PATH = f"/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries"
    response = s.get(f"{webserver_url}{API_PATH}")

    return response.json()

# Task 별 로그 조회
def get_task_log(dag_id: str, dag_run_id: str, task_id: str, task_try_number: int = 1) -> str:
    API_PATH = f"/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{task_try_number}"
    response = s.get(f"{webserver_url}{API_PATH}")

    return response.text
