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
            "command": "binaryDownload",
            "rc": 0,
            "stdout": "Download Binary file",
        }

    except Exception as err:
        return {"command": "binaryDownload", "rc": 1, "stdout": err}


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
        return {
            "command": "copy_template",
            "rc": 0,
            "stdout": "템플릿 복사 성공",
        }

    except Exception as err:
        logger.info(f"템플릿 복사 실패: 이름({deploy_name}), 환경({environment})")
        raise err


def test_deploy(**context):
    t = Terraform(working_dir="/mcp_infra/test", terraform_bin_path="/mcp_infra/1.3.2/terraform")
    var_dict = {
        "aws_vpc_cidr": "10.0.0.0/16",
        "aws_vpc_name": "wow64",
        "aws_dns_support_flag": True,
        "aws_internet_gateway_name": "aws igw name",
        "aws_region": "ap-northeast-2"
    }


    t.init()

    logger.info("Terraform init 완료")
    try:
        t.plan(capture_output=True, out="plan.out", var=var_dict)
    except TerraformCommandError as e:
        print(e)

    t.apply("plan.out", capture_output=True)
    print("-"*80)

    t.destroy(capture_output=True, force=None)


def calc(**context):
    # context는 실행 시 넘겨준 파라미터를 받는다.

    print("calc 함수 호출됨")

    # context에는 다음과 같은 정보가 들어있다.
    # - dag: DAG 객체
    # - ds: 실행 날짜 (YYYY-MM-DD)
    # - ds_nodash: 실행 날짜 (YYYYMMDD)
    # - execution_date: 실행 시간 (UTC)
    # - params: 파라미터 (dict)
    # - task: Task 객체
    # - task_instance: TaskInstance 객체
    # - ti: TaskInstance 객체
    print(f"context['params']: {context['params']}")
    print(f"context['dag_run'].conf: {context['dag_run'].conf}")

    # 파라미터를 받아서 계산
    a = context['params'].get('a', 0)
    b = context['params'].get('b', 0)

    print("a:", a)
    print("b:", b)
    print("a + b:", a + b)

    context['ti'].xcom_push(key='result', value=a + b)  # xcom에 결과값 저장

    return a + b

def printResult(**context):
    print("printResult 함수 호출됨")

    # xcom에서 결과값 가져오기
    result = context['ti'].xcom_pull(key='result', task_ids='task_2')
    print("result:", result)

    return result

def sleep_seconds(seconds, **kwargs):
    # kwargs에서 파라미터를 받아서 sleep
    seconds = kwargs['params'].get('seconds', seconds)

    print('=' * 60)
    print('seconds:' + str(seconds))
    print('=' * 60)
    pprint(kwargs)
    print('=' * 60)
    print('sleeping...')
    time.sleep(seconds)
    return 'sleep well!!!'


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

# t2 = PythonOperator(
#     task_id='task_2',
#     provide_context=True,
#     python_callable=calc,
#     # op_kwargs={'a': 1, 'b': 2},  # 함수의 인자로 넣을 값들(이건 코드상에 고정?)
#     dag=dag
# )
# t3 = PythonOperator(
#     task_id='task_3',
#     provide_context=True,
#     python_callable=printResult,
#     dag=dag
# )
# t4 = PythonOperator(
#     task_id='task_4',
#     provide_context=True,
#     python_callable=sleep_seconds,
#     op_kwargs={'seconds': 2},
#     dag=dag
# )
# t5 = EmptyOperator(task_id='task_5', dag=dag)
# t6 = PythonOperator(
#     task_id='test_deploy',
#     provide_context=True,
#     python_callable=test_deploy,
#     dag=dag
# )


download >> copy_vpc

# download >> t2 >> t3 >> t4 >> t5
# download >> t6

# For Debugging
if __name__ == "__main__":
    dag.test()
