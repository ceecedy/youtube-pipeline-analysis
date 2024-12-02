# test_dag_load_to_gcs.py
from utils.airflow_tasks_runner import run_airflow_task_test

if __name__ == "__main__":
    # Define the DAG and tasks to test
    dag_id = "extract_trending_youtube_videos_weekly"
    execution_date = "2024-01-01"  # The execution date you want to test

    # Test the extract_and_save_to_local task
    run_airflow_task_test(dag_id, "extract_and_save_to_local", execution_date)

    # Test the upload_to_gcs task
    run_airflow_task_test(dag_id, "upload_to_gcs", execution_date)
    
    # Test the extract_and_save_to_local task
    run_airflow_task_test(dag_id, "create_youtube_dataset", execution_date)

    # Test the upload_to_gcs task
    run_airflow_task_test(dag_id, "get_most_recent_file", execution_date)
    
    # Test the extract_and_save_to_local task
    run_airflow_task_test(dag_id, "load_data_to_bq", execution_date)
