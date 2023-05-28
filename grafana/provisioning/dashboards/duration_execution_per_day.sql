SELECT
    dag_id,
    MIN(start_date) AS START,
    MAX(end_date) AS
end,
MAX(end_date) - MIN(start_date) AS duration,
AVG(duration),
AVG(duration) as avg2
FROM task_instance
WHERE
    dag_id in ($Dags)
    AND state = 'success'
GROUP BY start_date, dag_id