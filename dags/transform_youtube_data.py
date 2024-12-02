# main dag etl for youtube. 
import os
from datetime import datetime, timedelta
from airflow import DAG
from include.dbt.cosmos_config import *
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import RenderConfig


# Default args for the DAG
default_args = {
    'owner': 'youtube-etl',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

# Define the DAG
with DAG(
    'transform_youtube_data',
    default_args=default_args,
    description='Transform raw YouTube data to staging views and dimensional tables using DBT',
    schedule_interval='@weekly',
    catchup=False
) as dag:
    # Task to run DBT staging models
    run_staging_models = DbtTaskGroup(
        group_id='run_staging_models',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/youtube_data/staging']    
        ),
    )
    
    # Task to run DBT dimension models (dim_*, fact_*)
    run_dimension_fact_models = DbtTaskGroup(
        group_id='run_dimension_fact_models',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/youtube_data/marts']    
        ),
    )

    # Task dependencies
    run_staging_models >> run_dimension_fact_models 
