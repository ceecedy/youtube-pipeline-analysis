# test_dag_orchestrator.py
from utils.airflow_tasks_runner import run_airflow_task_test

if __name__ == "__main__":
    # Define the DAG and tasks to test
    dag_id = "orchestrator_dag"
    execution_date = "2024-01-01"  # The execution date you want to test

    # Test the staging transformation task
    run_airflow_task_test(dag_id, "trigger_load_to_gcs", execution_date)

    # Test the dim's and fact transformation task
    run_airflow_task_test(dag_id, "trigger_transform_youtube_data", execution_date)

