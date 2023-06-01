from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import time
from pprint import pprint
import os
import logging
import shutil
logger = logging.getLogger(__name__)
import json
from dda_python_terraform import *
from jinja2 import Template

"""
TODO:
Stack 들의 연산은 트랜잭션 처리되어야 함.
XCOM 같은 기법을 사용하여 이전 스택이 성공적으로 생성되었는지 확인 후 다음 스택을 생성해야 함.

인프라 별로 매 번 params를 파싱하기보다 파싱하는 Task를 우선 수행하고, Xcom에서 데이터 가져오는 것이 효율적일 것 같음

작업 별로 로깅 자세히 하기, terraform output을 로깅에 포함시키기

Task Group과 Skip를 적절히 사용하고, Dynamic Workflow를 구현하여 작업을 효율적으로 수행할 수 있도록 하기
"""

t = Terraform()

args = {
    'owner': 'multicloud-platform',
    'start_date': days_ago(n=1)
}

dag = DAG(
    dag_id='mcp_deploy_dag',
    default_args=args,
    schedule_interval=None
)


def terraform_download(**context):
    from io import BytesIO
    import os, stat, zipfile, requests, sys, platform

    context_data = context['params']
    version = context_data.get('tf_version', '1.3.2')
    # XCOM에 테라폼 버전 push
    context['ti'].xcom_push(key='tf_version', value=version)

    # 플랫폼에 맞게 다운로드
    arch = 'arm64' if platform.machine() in {'arm64', 'aarch64'} else 'amd64'
    match (sys.platform):
        case 'win32':
            platform = f'windows_{arch}'
        case 'linux':
            platform = f'linux_{arch}'
        case 'darwin':
            platform = f'darwin_{arch}'

    # 테라폼 바이너리 다운로드
    binary = f"https://releases.hashicorp.com/terraform/{version}/terraform_{version}_{platform}.zip"
    logger.info(f"Download Binary file: {binary}")
    try:
        if not os.path.exists(f"/mcp_infra/{version}"):
            os.mkdir(f"/mcp_infra/{version}")
        if not os.path.isfile(f"/mcp_infra/{version}/terraform"):
            req = requests.get(binary, verify=False)
            _zipfile = zipfile.ZipFile(BytesIO(req.content))
            _zipfile.extractall(f"/mcp_infra/{version}")
            st = os.stat(f"/mcp_infra/{version}/terraform")
            os.chmod(f"/mcp_infra/{version}/terraform", st.st_mode | stat.S_IEXEC)
        return {
            "command": "terraform_download",
            "rc": 0,
            "stdout": "테라폼 바이너리 다운로드 성공",
        }

    except Exception as err:
        return {"command": "terraform_download", "rc": 1, "stdout": str(err)}


# /mcp_infra 에 있는 스택(env=default, name=default)을 Deploy 이름과 환경에 맞는 경로로 복사
def copy_template(stack_type: str, **context):
    context_data = context['params']
    deploy_name = context_data.get('deploy_name', 'default')
    environment = context_data.get('environment', 'default')
    team = context_data.get('team', 'default')
    
    infra_data = context_data.get('infra_data')
    target_stack_name = ""
    target_stack_data = {}
    # infra_data에서 stack_type에 맞는 스택을 찾아서 target_stack_name, target_stack_data에 저장
    for infra in infra_data:
        if (infra_data[infra]['stack_type'] == stack_type):
            target_stack_name = infra
            target_stack_data = infra_data.get(infra)
            break
    logger.info(f"타겟 스택을 찾았습니다. ({target_stack_name})")

    # XCOM에 타겟 스택의 변수 push
    context['ti'].xcom_push(key="stack_vars", value=target_stack_data.get("variables"))
    # XCOM에 타켓 스택의 Provider 정보 push
    context['ti'].xcom_push(key="stack_provider", value=target_stack_data.get("provider"))


    try:
        source_dir = f"/mcp_infra/{target_stack_data.get('csp_type')}_{target_stack_name}/default/{team}/default/{stack_type}"
        dest_dir = f"/mcp_infra/{target_stack_data.get('csp_type')}_{target_stack_name}/{environment}/{team}/{deploy_name}/{stack_type}"
        
        # 디렉토리 복사
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            logger.info(f"디렉토리 생성: {dest_dir}")
        else:
            logger.info(f"디렉토리 존재: {dest_dir}")

        # 파일 복사
        logger.info(f"파일 복사: {source_dir} -> {dest_dir}")
        logger.info(f"파일 목록: {os.listdir(source_dir)}")
        for file in os.listdir(source_dir):
            if os.path.isfile(os.path.join(source_dir, file)):
                shutil.copy(os.path.join(source_dir, file), dest_dir)
                logger.info(f"파일 복사: {file}")
            else:
                logger.info(f"파일 복사: {file} (실패)")

        logger.info(f"템플릿 복사 성공: 이름({deploy_name}), 환경({environment})")

        # XCOM에 dest_dir 푸시
        context['ti'].xcom_push(key='working_dir', value=dest_dir)
        return {
            "command": "copy_template",
            "rc": 0,
            "stdout": "템플릿 복사 성공",
        }

    except Exception as err:
        logger.info(f"템플릿 복사 실패: 이름({deploy_name}), 환경({environment})")
        raise err


def set_storage(stack_type: str, **context):
    working_dir = context['ti'].xcom_pull(key='working_dir', task_ids=f'copy_{stack_type}')

    storage_data = '''
    terraform {
        backend "http" {
            address = "http://remote-state:8080/terraform_state/{{deploy_state}}"
            lock_address = "http://remote-state:8080/terraform_lock/{{deploy_state}}"
            lock_method = "PUT"
            unlock_address = "http://remote-state:8080/terraform_lock/{{deploy_state}}"
            unlock_method = "DELETE"
        }
    }
    '''
    tm = Template(storage_data)
    provider_backend = tm.render(
        deploy_state=f"{working_dir.replace('/', '-').replace(' ', '_')}"  # Deploy의 UID
    )

    logger.info(provider_backend)

    with open(f"{working_dir}/remote-state.tf", "w+") as f:
        f.write(provider_backend)
    logger.info("원격 저장소 설정 완료")

    # Provider 설정
    provider_data = context['ti'].xcom_pull(key='stack_provider', task_ids=f'copy_{stack_type}')

    cred_data = '''
    variable "aws_access_key" {
        type = string
        default = "{{aws_access_key}}"
    }
    variable "aws_secret_key" {
        type = string
        default = "{{aws_secret_key}}"
    }
    '''
    tm = Template(cred_data)
    creds = tm.render(
        aws_access_key=provider_data.get("access_key_id"),
        aws_secret_key=provider_data.get("secret_access_key")
    )
    logger.info(creds)

    with open(f"{working_dir}/credential.tf", "w+") as f:
        f.write(creds)
    logger.info("인증 정보 설정 완료")


def plan(stack_type: str, **context):
    # XCOM에서 사용할 정보 pull
    working_dir = context['ti'].xcom_pull(key='working_dir', task_ids=f'copy_{stack_type}')
    tf_version = context["ti"].xcom_pull(key='tf_version', task_ids='terraform_download')
    var_dict = context['ti'].xcom_pull(key='stack_vars', task_ids=f'copy_{stack_type}')

    # 테라폼 인스턴스 할당
    t = Terraform(working_dir=working_dir, terraform_bin_path=f"/mcp_infra/{tf_version}/terraform")
    logger.info(f"테라폼 working_dir={working_dir}")

    # Init
    try:
        return_code, stdout, stderr = t.init(capture_output=True)  # TODO: 출력 캡처
    except TerraformCommandError as e:
        logger.warn(e)
        raise e
    logger.info("-"*80)
    logger.info("Terraform Init 성공")
    logger.info(f"stdout: {stdout}")
    logger.info("-"*80)

    # Plan
    try:
        return_code, stdout, stderr = t.plan(capture_output=True, out="plan.out", var=var_dict)  # TODO: 출력 캡처
    except TerraformCommandError as e:
        logger.warn(e)
    logger.info("-"*80)
    logger.info(f"Terraform Plan 성공")
    logger.info(f"stdout: {stdout}")
    logger.info("-"*80)


def apply(stack_type: str, **context):
    # XCOM에서 사용할 정보 pull
    working_dir = context['ti'].xcom_pull(key='working_dir', task_ids=f'copy_{stack_type}')
    tf_version = context["ti"].xcom_pull(key='tf_version', task_ids='terraform_download')
    t = Terraform(working_dir=working_dir, terraform_bin_path=f"/mcp_infra/{tf_version}/terraform")

    # Apply
    try:
        return_code, stdout, stderr = t.apply("plan.out", capture_output=True)
    except TerraformCommandError as e:
        logger.warn(e)
    logger.info("-"*80)
    logger.info("Terraform Apply 완료")
    logger.info(f"stdout: {stdout}")
    logger.info("-"*80)

    logger.info("10초 대기...")
    time.sleep(10)
    return_code, stdout, stderr = t.destroy(capture_output=True, force=None)
    logger.info("-"*80)
    logger.info("Terraform Destroy 완료")
    logger.info(f"stdout: {stdout}")
    logger.info("-"*80)


download = PythonOperator(
    task_id='terraform_download',
    provide_context=True,
    python_callable=terraform_download,
    dag=dag
)
copy_vpc = PythonOperator(
    task_id='copy_vpc',
    provide_context=True,
    python_callable=copy_template,
    op_kwargs={'stack_type': 'vpc'},
    dag=dag
)
storage_vpc = PythonOperator(
    task_id='storage_vpc',
    provide_context=True,
    python_callable=set_storage,
    op_kwargs={'stack_type': 'vpc'},
    dag=dag
)
plan_vpc = PythonOperator(
    task_id='plan_vpc',
    provide_context=True,
    python_callable=plan,
    op_kwargs={'stack_type': 'vpc'},
    dag=dag
)
apply_vpc = PythonOperator(
    task_id='apply_vpc',
    provide_context=True,
    python_callable=apply,
    op_kwargs={'stack_type': 'vpc'},
    dag=dag
)


download >> copy_vpc >> storage_vpc >> plan_vpc >> apply_vpc


# For Debugging
if __name__ == "__main__":
    dag.test()
