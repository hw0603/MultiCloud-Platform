from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import time
from pprint import pprint

args = {
    'owner': 'hw0603',
    'start_date': days_ago(n=1)
}

dag = DAG(
    dag_id='mcp_deploy_dag',
    default_args=args,
)

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


t1 = EmptyOperator(task_id='task_1', dag=dag)
t2 = PythonOperator(
    task_id='task_2',
    provide_context=True,
    python_callable=calc,
    # op_kwargs={'a': 1, 'b': 2},  # 함수의 인자로 넣을 값들(이건 코드상에 고정?)
    dag=dag
)
t3 = PythonOperator(
    task_id='task_3',
    provide_context=True,
    python_callable=printResult,
    dag=dag
)
t5 = EmptyOperator(task_id='task_5', dag=dag)
t4 = PythonOperator(
    task_id='task_4',
    provide_context=True,
    python_callable=sleep_seconds,
    op_kwargs={'seconds': 2},
    dag=dag
)


t1 >> t2 >> t3 >> t4 >> t5
