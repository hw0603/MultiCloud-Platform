SELECT
    start_date,
    task_id,
    MIN(start_date) AS start,
    MAX(end_date) AS
end,
MAX(end_date) - MIN(start_date) AS duration
FROM task_instance
WHERE
    dag_id in ($Dags)
    AND state = 'success'
GROUP BY start_date, TASK_ID
ORDER BY start_date DESC