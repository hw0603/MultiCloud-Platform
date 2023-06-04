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
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import BranchPythonOperator

# TODO: 인프라 별로 매 번 params를 파싱하기보다 파싱하는 Task를 우선 수행하고, Xcom에서 데이터 가져오는 것이 효율적일 것 같음

t = Terraform()

args = {
    'owner': 'multicloud-platform',
    'start_date': days_ago(n=1)
}

with DAG(
    dag_id='mcp_deploy_dag',
    default_args=args,
    schedule_interval=None
) as dag:
    


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


    def check_available(current_infra: str, **context):
        context_data = context['params']
        infra_data = context_data.get('infra_data')

        logger.info(f"현재 인프라: {current_infra}")
        logger.info(f"인프라 데이터: {infra_data}")

        for infra in infra_data:
            assert type(infra_data[infra]) == dict
            target_stack_data = infra_data.get(infra)

            if (target_stack_data.get("stack_type") == current_infra):
                return f"{current_infra}.copy"
        return f"{current_infra}.skip"
        


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


    def set_storage_and_creds(stack_type: str, **context):
        working_dir = context['ti'].xcom_pull(key='working_dir', task_ids=f'{stack_type}.copy')

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
        provider_data = context['ti'].xcom_pull(key='stack_provider', task_ids=f'{stack_type}.copy')

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
        working_dir = context['ti'].xcom_pull(key='working_dir', task_ids=f'{stack_type}.copy')
        tf_version = context["ti"].xcom_pull(key='tf_version', task_ids='terraform_download')
        var_dict = context['ti'].xcom_pull(key='stack_vars', task_ids=f'{stack_type}.copy')

        # 테라폼 인스턴스 할당
        t = Terraform(working_dir=working_dir, terraform_bin_path=f"/mcp_infra/{tf_version}/terraform")
        logger.info(f"테라폼 working_dir={working_dir}")

        # Init
        result = ""
        try:
            result = t.init(capture_output=True)
        except TerraformCommandError as e:
            logger.warn(e)
            raise e
        logger.info("-"*80)
        logger.info("Terraform Init 성공")
        logger.info(f"result: {result}")
        logger.info("-"*80)

        # Plan
        try:
            result = t.plan(capture_output=True, out="plan.out", var=var_dict)
        except TerraformCommandError as e:
            logger.warn(e)
        logger.info("-"*80)
        logger.info(f"Terraform Plan 성공")
        logger.info(f"result: {result}")
        logger.info("-"*80)


    def apply(stack_type: str, **context):
        # XCOM에서 사용할 정보 pull
        working_dir = context['ti'].xcom_pull(key='working_dir', task_ids=f'{stack_type}.copy')
        tf_version = context["ti"].xcom_pull(key='tf_version', task_ids='terraform_download')
        t = Terraform(working_dir=working_dir, terraform_bin_path=f"/mcp_infra/{tf_version}/terraform")

        # Apply
        result = ""
        try:
            result = t.apply("plan.out", capture_output=True)
        except TerraformCommandError as e:
            logger.warn(e)
        logger.info("-"*80)
        logger.info("Terraform Apply 완료")
        logger.info(f"result: {result}")
        logger.info("-"*80)

        # logger.info("10초 대기...")
        # time.sleep(10)
        # return_code, stdout, stderr = t.destroy(capture_output=True, force=None)
        # logger.info("-"*80)
        # logger.info("Terraform Destroy 완료")
        # logger.info(f"return_code: {return_code}")
        # logger.info(f"stdout: {stdout}")
        # logger.info(f"stderr: {stderr}")
        # logger.info("-"*80)

    
    download = PythonOperator(
        task_id='terraform_download',
        provide_context=True,
        python_callable=terraform_download,
        dag=dag
    )

    infra_types = [
        "vpc", "subnet", "security_group",
        "nat_gateway", "route_table", "route_rule", "route_table_association",
        "key_pair", "bastion", "alb"
    ]

    groups = {}

    for g_id in infra_types:
        with TaskGroup(group_id=g_id) as tg:
            check_task = BranchPythonOperator(
                task_id='check',
                provide_context=True,
                python_callable=check_available,
                op_kwargs={'current_infra': g_id},
                trigger_rule='one_success',
                dag=dag
            )
            copy_task = PythonOperator(
                task_id='copy',
                provide_context=True,
                python_callable=copy_template,
                op_kwargs={'stack_type': g_id},
                dag=dag
            )
            storage_task = PythonOperator(
                task_id='storage_and_creds',
                provide_context=True,
                python_callable=set_storage_and_creds,
                op_kwargs={'stack_type': g_id},
                dag=dag
            )
            plan_task = PythonOperator(
                task_id='plan',
                provide_context=True,
                python_callable=plan,
                op_kwargs={'stack_type': g_id},
                dag=dag
            )
            apply_task = PythonOperator(
                task_id='apply',
                provide_context=True,
                python_callable=apply,
                op_kwargs={'stack_type': g_id},
                dag=dag
            )
            skip_task = EmptyOperator(
                task_id='skip',
                dag=dag
            )
            check_task >> [copy_task, skip_task]
            copy_task >> storage_task >> plan_task >> apply_task
            
            groups[g_id] = tg

    # TODO: Stack 간 의존성 설정
    def iter_task_group():
        for gid in infra_types:
            yield groups[gid]


    download >> groups["vpc"] >> groups["subnet"] >> groups["security_group"] >> groups["nat_gateway"] >> groups["route_table"] >> groups["route_rule"] >> groups["route_table_association"] >> groups["key_pair"] >> groups["bastion"] >> groups["alb"]
    
    # 병렬처리 (의존관계 XCOM으로 관리해 주어야 함)
    # for gid in infra_types:
    #     download >> groups[gid]



# For Debugging
if __name__ == "__main__":
    dag.test()
