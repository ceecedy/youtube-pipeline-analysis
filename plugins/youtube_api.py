# plugins/youtube_api.py 
# this is where code for the extraction of the raw data in the youtube is located. 
import os
import googleapiclient.discovery
import json
import pytz
from dotenv import load_dotenv
from datetime import datetime
import time

# Load API key from environment variables
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Directory path where the data will be saved locally
LOCAL_SAVE_PATH = 'include/extracted_datasets/'

# Set a delay to avoid hitting API rate limits too quickly
TIME_DELAY = 1  # Delay in seconds between API calls to avoid rate limiting

# Helper function to create YouTube API client
def create_youtube_client():
    return googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

# Function to fetch trending videos
def get_trending_videos(youtube, region_code):
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=50
        )
        response = request.execute()
        return response['items']
    except Exception as e:
        print(f"Error fetching trending videos for region {region_code}: {e}")
        return []

# Function to fetch video comments
def get_video_comments(youtube, video_id):
    try:
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            maxResults=50
        )
        response = request.execute()
        return response['items']
    except Exception as e:
        print(f"Error fetching comments for video {video_id}: {e}")
        return []

# Function to fetch video categories
def get_video_category(youtube, video_id):
    try:
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()
        return response['items'][0]['snippet']['categoryId'] if response['items'] else None
    except Exception as e:
        print(f"Error fetching category for video {video_id}: {e}")
        return None

# Function to fetch channel details
def get_channel_details(youtube, channel_id):
    try:
        request = youtube.channels().list(
            part="snippet",
            id=channel_id
        )
        response = request.execute()
        return response['items'][0]['snippet'] if response['items'] else {}
    except Exception as e:
        print(f"Error fetching channel details for {channel_id}: {e}")
        return {}

# Function to fetch multiple video category details
def get_video_category_details(youtube, category_id):
    try:
        request = youtube.videoCategories().list(
            part="snippet",
            id=category_id
        )
        response = request.execute()
        if response['items']:
            category = response['items'][0]['snippet']
            return category['title'], category.get('description', 'No description available')
        return None, None
    except Exception as e:
        print(f"Error fetching category details for category ID {category_id}: {e}")
        return None, None

# Function to save data locally in NDJSON format
def save_data_as_ndjson(data, filename):
    os.makedirs(LOCAL_SAVE_PATH, exist_ok=True)
    file_path = os.path.join(LOCAL_SAVE_PATH, filename)
    
    with open(file_path, 'w') as ndjson_file:
        for record in data:
            ndjson_file.write(json.dumps(record) + '\n')  # Write each record as a new line in the file
    print(f"Data saved as NDJSON to {file_path}")

# Main function to extract and save data for videos and comments
def extract_and_save():
    regions = ['PH', 'US']  # List of regions to fetch data from
    all_video_data = []
    all_comment_data = []

    youtube = create_youtube_client()  # Create API client once for reuse

    for region in regions:
        trending_videos = get_trending_videos(youtube, region)

        # Iterate over the trending videos and flatten each one
        for video in trending_videos:
            video_id = video['id']

            # Flatten video data into a single dictionary
            video_data = {
                "video_id": video_id,
                "title": video['snippet']['title'],
                "description": video['snippet']['description'],
                "channel_id": video['snippet']['channelId'],
                "channel_title": video['snippet']['channelTitle'],
                "published_at": video['snippet']['publishedAt'],
                "view_count": video['statistics'].get('viewCount', 0),
                "like_count": video['statistics'].get('likeCount', 0),
                "comment_count": video['statistics'].get('commentCount', 0),
                "region_code": region,
            }

            # Fetch category and category details
            category_id = get_video_category(youtube, video_id)
            video_data['category_id'] = category_id
            category_name, category_description = get_video_category_details(youtube, category_id)
            video_data['category_name'] = category_name
            video_data['category_description'] = category_description

            # Fetch channel details
            channel_details = get_channel_details(youtube, video_data['channel_id'])
            video_data['channel_description'] = channel_details.get('description', '')
            video_data['channel_published_at'] = channel_details.get('publishedAt', '')

            # Add video data to the list
            all_video_data.append(video_data)

            # Flatten and collect comments for each video
            video_comments = get_video_comments(youtube, video_id)
            for comment in video_comments:
                comment_data = {
                    "comment_id": comment['id'],
                    "video_id": video_id,
                    "comment_author": comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    "comment_text": comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                    "like_count": comment['snippet']['topLevelComment']['snippet'].get('likeCount', 0),
                    "published_at": comment['snippet']['topLevelComment']['snippet']['publishedAt'],
                }
                # Add comment data to the list
                all_comment_data.append(comment_data)

            # To avoid hitting the API rate limits, add a small delay between API calls
            time.sleep(TIME_DELAY)

    # Define filenames based on current date (for weekly extraction)
    today = datetime.now(pytz.timezone('Asia/Manila'))
    video_filename = f"youtube_trending_videos_{today.strftime('%Y%m%d')}.ndjson"
    comment_filename = f"youtube_trending_comments_{today.strftime('%Y%m%d')}.ndjson"

    # Save all video data as NDJSON
    save_data_as_ndjson(all_video_data, video_filename)
    
    # Save all comment data as NDJSON
    save_data_as_ndjson(all_comment_data, comment_filename)


