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

t = Terraform()

args = {
    'owner': 'multicloud-platform',
    'start_date': days_ago(n=1)
}

with DAG(
    dag_id='mcp_destroy_dag',
    default_args=args,
    schedule_interval=None
) as dag:
    
    def destroy(**context):
        context_data = context['params']
        target_stack = context_data.get('stack')
        environment = context_data.get('environment')
        team = context_data.get('team')
        deploy_name = context_data.get('deploy_name')

        dest_dir = f"/mcp_infra/{target_stack.get('csp_type')}_{target_stack.get('stack_name')}/{environment}/{team}/{deploy_name}/{target_stack.get('stack_type')}"
        print(dest_dir)
        tf_version = target_stack.get('tf_version')
        t = Terraform(working_dir=dest_dir, terraform_bin_path=f"/mcp_infra/{tf_version}/terraform")
        
        # Destroy
        result = ""
        try:
            result = t.destroy("plan.out", capture_output=True)
        except TerraformCommandError as e:
            logger.warn(e)
        
        logger.info("-"*80)
        logger.info("Terraform Destroy 완료")
        logger.info(f"result: {result}")
        logger.info("-"*80)

    destroy = PythonOperator(
        task_id='destroy',
        provide_context=True,
        python_callable=destroy,
        dag=dag
    )

    destroy



# For Debugging
if __name__ == "__main__":
    dag.test()
