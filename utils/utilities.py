# python built-in imports
import os
import glob
import json
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery


# Function to get the most recent JSON file from the directory
def get_and_validate_recent_files(directory_path: str):
    try:
        # Define the file patterns for NDJSON files (one for videos, one for comments)
        video_file_pattern = os.path.join(directory_path, "youtube_trending_videos_*.ndjson")
        comment_file_pattern = os.path.join(directory_path, "youtube_trending_comments_*.ndjson")

        # Get all files matching the patterns
        video_files = glob.glob(video_file_pattern)
        comment_files = glob.glob(comment_file_pattern)

        if not video_files:
            raise ValueError("No NDJSON video files found in the directory.")
        
        if not comment_files:
            raise ValueError("No NDJSON comment files found in the directory.")

        # Sort files by last modified time in descending order (newest first)
        video_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        comment_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        # Get the most recent video and comment files
        recent_video_file = video_files[0]
        recent_comment_file = comment_files[0]
        
        # Check if both files exist and can be accessed
        if not os.path.exists(recent_video_file):
            raise ValueError(f"The most recent video file {recent_video_file} does not exist or cannot be accessed.")
        
        if not os.path.exists(recent_comment_file):
            raise ValueError(f"The most recent comment file {recent_comment_file} does not exist or cannot be accessed.")
        
        return recent_video_file, recent_comment_file

    except Exception as e:
        raise ValueError(f"Error getting the most recent files: {e}")

# Main function for getting the most recent file in GCS.
def get_most_recent_file_from_gcs(**kwargs):
    # Retrieve the bucket name and prefix from kwargs
    bucket_name = kwargs['bucket']
    video_prefix = kwargs['video_prefix']
    comment_prefix = kwargs['comment_prefix']
    
    # Initialize the GCS client
    storage_client = storage.Client()
    
    # List all the blobs (files) with the given prefixes in the specified GCS bucket
    video_blobs = storage_client.list_blobs(bucket_name, prefix=video_prefix)
    comment_blobs = storage_client.list_blobs(bucket_name, prefix=comment_prefix)

    # If no blobs are found, raise an exception
    video_file_list = [blob.name for blob in video_blobs]
    comment_file_list = [blob.name for blob in comment_blobs]

    if not video_file_list:
        raise ValueError(f"No video NDJSON files found with prefix: {video_prefix}")
    
    if not comment_file_list:
        raise ValueError(f"No comment NDJSON files found with prefix: {comment_prefix}")
    
    # Find the most recent video and comment file based on the last modified timestamp
    most_recent_video_file = max(video_file_list, key=lambda x: storage_client.get_bucket(bucket_name).get_blob(x).updated)
    most_recent_comment_file = max(comment_file_list, key=lambda x: storage_client.get_bucket(bucket_name).get_blob(x).updated)

    # Push the most recent video and comment files to XCom for further use in other tasks if needed
    kwargs['ti'].xcom_push(key='most_recent_video_file', value=most_recent_video_file)
    kwargs['ti'].xcom_push(key='most_recent_comment_file', value=most_recent_comment_file)
    
    return most_recent_video_file, most_recent_comment_file

# Function to check if the dataset exists and create it if not
def check_and_create_bigquery_dataset(dataset_id: str, gcp_conn_id: str = 'youtube-gcp-etl'):
    client = bigquery.Client(project=gcp_conn_id)  # Initialize BigQuery client using the GCP connection ID

    try:
        # Try to get the dataset
        client.get_dataset(dataset_id)  # If the dataset exists, this will succeed
        print(f"Dataset {dataset_id} already exists.")
    except bigquery.exceptions.NotFound:
        # If the dataset doesn't exist, create it
        print(f"Dataset {dataset_id} does not exist. Creating dataset...")
        dataset = bigquery.Dataset(dataset_id)
        client.create_dataset(dataset)  # Create the dataset
        print(f"Dataset {dataset_id} created successfully.")