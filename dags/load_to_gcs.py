# dags/load_to_gcs.py 
# this is where the extraction of the data is been scheduled.

# Python built-in imports
from datetime import datetime, timedelta
from plugins.youtube_api import extract_and_save

# helper functions
from utils.utilities import *

# Airflow DAG creator
from airflow import DAG
# Airflow Python operator
from airflow.operators.python import PythonOperator
# Uploading local data to data lake (GCS)
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
# Loading data from GCS to BigQuery using a built-in operator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator


# Default arguments for the DAG
default_args = {
    'owner': 'youtube-etl',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

# Define the DAG
with DAG('extract_trending_youtube_videos_weekly', 
         default_args=default_args, 
         schedule_interval='@weekly', 
         catchup=False) as dag:

    # Task to extract and save data to a local file (first step)
    extract_task = PythonOperator(
        task_id='extract_and_save_to_local',
        python_callable=extract_and_save,  # Calls the extract_and_save function from youtube_api.py
    )
    
    # Task to upload the most recent file to GCS (second step)
    def upload_files_to_gcs(**kwargs):
        directory_path = 'include/extracted_datasets'  # Path where the files are stored locally
        
        # Get and validate the most recent video and comment files
        recent_video_file, recent_comment_file = get_and_validate_recent_files(directory_path)
        
        # Ensure both files are NDJSON files (they should already be if the naming conventions are followed)
        if not recent_video_file.endswith('.ndjson'):
            raise ValueError(f"The file {recent_video_file} is not an NDJSON file.")
        
        if not recent_comment_file.endswith('.ndjson'):
            raise ValueError(f"The file {recent_comment_file} is not an NDJSON file.")

        # Now upload both files to GCS

        # Video file upload task
        upload_video_to_gcs_task = LocalFilesystemToGCSOperator(
            task_id='upload_video_to_gcs',
            src=recent_video_file,  # Provide the video file path
            dst=recent_video_file.split('/')[-1],  # Use the filename in the GCS path
            bucket='youtube-raw-data',
            gcp_conn_id='youtube-gcp-etl',
            mime_type='application/x-ndjson',  # MIME type for NDJSON
        )
        
        # Comment file upload task
        upload_comment_to_gcs_task = LocalFilesystemToGCSOperator(
            task_id='upload_comment_to_gcs',
            src=recent_comment_file,  # Provide the comment file path
            dst=recent_comment_file.split('/')[-1],  # Use the filename in the GCS path
            bucket='youtube-raw-data',
            gcp_conn_id='youtube-gcp-etl',
            mime_type='application/x-ndjson',  # MIME type for NDJSON
        )
        
        # Execute the upload tasks
        upload_video_to_gcs_task.execute(context=kwargs)  # Upload video file
        upload_comment_to_gcs_task.execute(context=kwargs)  # Upload comment file

    # PythonOperator to trigger the upload task
    upload_task = PythonOperator(
        task_id='upload_files_to_gcs',
        python_callable=upload_files_to_gcs,
        provide_context=True,
    )
    
    # Task to check if dataset exists and create if not
    check_and_create_youtube_dataset = PythonOperator(
        task_id='check_and_create_youtube_dataset',
        python_callable=check_and_create_bigquery_dataset,
        op_kwargs={'dataset_id': 'youtube', 'gcp_conn_id': 'youtube-gcp-etl'},
    )
    
    # Task to list the most recent file in GCS (from the GCS bucket)
    get_most_recent_file_gcs = PythonOperator(
        task_id='get_most_recent_file',
        python_callable=get_most_recent_file_from_gcs,
        provide_context=True,  # Ensures kwargs are passed to the function
        op_kwargs={
            'bucket': 'youtube-raw-data',  
            'video_prefix': 'youtube_trending_videos_',
            'comment_prefix': 'youtube_trending_comments_'
        }
    )
    
    # Task to load data from GCS to BigQuery using GoogleCloudStorageToBigQueryOperator
    def load_gcs_to_bq(**kwargs):
        # Retrieve the most recent video and comment files from XCom
        ti = kwargs['ti']
        most_recent_video_file = ti.xcom_pull(task_ids='get_most_recent_file', key='most_recent_video_file')
        most_recent_comment_file = ti.xcom_pull(task_ids='get_most_recent_file', key='most_recent_comment_file')
        
        # Define the destination table in BigQuery
        destination_table_video = 'yt-e2e-data-cycle-project.youtube.raw_youtube_video_data'
        destination_table_comment = 'yt-e2e-data-cycle-project.youtube.raw_youtube_comment_data'
        
        # Video file upload to BigQuery task
        gcs_to_bq_video_task = GCSToBigQueryOperator(
            task_id='gcs_to_bq_video',
            bucket='youtube-raw-data',  
            source_objects=[most_recent_video_file],  # The most recent video file in GCS
            destination_project_dataset_table=destination_table_video,  
            source_format='NEWLINE_DELIMITED_JSON',  
            write_disposition='WRITE_APPEND',  
            schema_update_options=['ALLOW_FIELD_ADDITION', 'ALLOW_FIELD_RELAXATION'],
            gcp_conn_id='youtube-gcp-etl',  
        )

        # Comment file upload to BigQuery task
        gcs_to_bq_comment_task = GCSToBigQueryOperator(
            task_id='gcs_to_bq_comment',
            bucket='youtube-raw-data',  
            source_objects=[most_recent_comment_file],  # The most recent comment file in GCS
            destination_project_dataset_table=destination_table_comment,  
            source_format='NEWLINE_DELIMITED_JSON',  
            write_disposition='WRITE_APPEND',  
            schema_update_options=['ALLOW_FIELD_ADDITION', 'ALLOW_FIELD_RELAXATION'],
            gcp_conn_id='youtube-gcp-etl',  
        )
        
        # Execute the upload tasks
        gcs_to_bq_video_task.execute(context=kwargs)  # Upload video file
        gcs_to_bq_comment_task.execute(context=kwargs)  # Upload comment file

    # PythonOperator to trigger the loading task
    load_data_to_bq = PythonOperator(
        task_id='load_data_to_bq',
        python_callable=load_gcs_to_bq,
        provide_context=True,
    )

    # Set task dependencies
    extract_task >> upload_task >> check_and_create_youtube_dataset >> get_most_recent_file_gcs >> load_data_to_bq
