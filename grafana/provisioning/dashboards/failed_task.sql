SELECT
    dr.dag_id as NAME_DAG,
    LEFT(RIGHT(dr.run_id, 25), 10) AS DATA,
    LEFT(RIGHT(dr.run_id, 14), 8) AS _time,
    ti.task_id as NAME_TASK_AIRFLOW -- ,ti.state as STATUS_JOB
,
    case
        when ti.state = 'failed' then 1
        else 0
    end STATUS_JOB,
    concat(
        'http://localhost:7001/admin/taskinstance/?flt0_task_id_contains='
    ) as log
FROM dag_run as dr
    INNER JOIN (
        SELECT
            dag_id,
            task_id,
            state,
            start_date
        FROM task_instance
        WHERE
            state = 'failed'
            and dag_id in ($Dags) --and start_date > now() - interval '7 day'
    ) as ti ON dr.dag_id = ti.dag_id --AND dr.start_date = ti.start_date
order by dr.dag_id, dr.start_date