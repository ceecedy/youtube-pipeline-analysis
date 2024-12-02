from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

# Default arguments for the orchestrator DAG
default_args = {
    'owner': 'youtube-etl',
    'start_date': datetime(2023, 11, 1),
    'catchup': False,
}

# Define the Orchestrator DAG
with DAG('orchestrator_dag', 
         default_args=default_args, 
         schedule_interval='@weekly',
         catchup=False) as dag:

    # Task to trigger 'load_to_gcs' DAG
    trigger_load_to_gcs = TriggerDagRunOperator(
        task_id='trigger_load_to_gcs',
        trigger_dag_id='extract_trending_youtube_videos_weekly',  # The ID of the DAG you want to trigger
        conf={"message": "Starting GCS load process"}  # Optional configuration to pass to the triggered DAG
    )

    # Task to trigger 'transform_youtube_data' DAG after 'load_to_gcs'
    trigger_transform_youtube_data = TriggerDagRunOperator(
        task_id='trigger_transform_youtube_data',
        trigger_dag_id='transform_youtube_data',  # Trigger the transformation DAG
        conf={"message": "Starting YouTube data transformation"}
    )

    # Setting the execution order: Load -> Transform -> Test
    trigger_load_to_gcs >> trigger_transform_youtube_data
