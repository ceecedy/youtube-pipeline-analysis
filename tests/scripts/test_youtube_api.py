# testing for plugin youtube_api
import unittest
from unittest.mock import MagicMock, patch
import json
from datetime import datetime
import pytz

from plugins.youtube_api import (
    get_trending_videos,
    get_video_comments,
    get_video_category,
    get_channel_details,
    get_video_category_details,
    save_data_locally,
    extract_and_save
)

class TestYouTubeAPIFunctions(unittest.TestCase):
    
    @patch('plugins.youtube_api.create_youtube_client')
    def setUp(self, mock_create_youtube_client):
        # Mock the YouTube API client creation
        self.mock_youtube = MagicMock()
        mock_create_youtube_client.return_value = self.mock_youtube

        # Mock YouTube API responses for different functions
        self.mock_trending_response = {
            'items': [
                {
                    'id': 'video_1',
                    'snippet': {
                        'title': 'Trending Video 1',
                        'description': 'Description of trending video 1',
                        'channelId': 'channel_1',
                        'channelTitle': 'Channel 1',
                        'publishedAt': '2024-11-12T00:00:00Z'
                    },
                    'statistics': {
                        'viewCount': 1000,
                        'likeCount': 100,
                        'commentCount': 50
                    }
                }
            ]
        }

        self.mock_comments_response = {
            'items': [
                {
                    'id': 'comment_1',
                    'snippet': {
                        'topLevelComment': {
                            'snippet': {
                                'authorDisplayName': 'User 1',
                                'textDisplay': 'Great video!',
                                'likeCount': 10,
                                'publishedAt': '2024-11-12T00:00:00Z'
                            }
                        }
                    }
                }
            ]
        }

        self.mock_category_response = {
            'items': [
                {
                    'snippet': {
                        'title': 'Music',
                        'description': 'All music related videos'
                    }
                }
            ]
        }

        self.mock_channel_response = {
            'items': [
                {
                    'snippet': {
                        'description': 'This is a channel about music.',
                        'publishedAt': '2020-01-01T00:00:00Z'
                    }
                }
            ]
        }
        
    @patch('plugins.youtube_api.get_trending_videos')
    def test_get_trending_videos(self, mock_get_trending_videos):
        self.mock_youtube.videos().list().execute.return_value = self.mock_trending_response
        
        region = 'US'
        videos = get_trending_videos(self.mock_youtube, region)
        
        self.assertEqual(len(videos), 1)
        self.assertEqual(videos[0]['id'], 'video_1')
        self.assertEqual(videos[0]['snippet']['title'], 'Trending Video 1')
    
    @patch('plugins.youtube_api.get_video_comments')
    def test_get_video_comments(self, mock_get_video_comments):
        # Create a mock youtube client object
        mock_youtube = MagicMock()
        # Mock the response from youtube.commentThreads().list().execute()
        mock_execute = MagicMock(return_value={
            'items': [
                {
                    'id': 'comment_1',
                    'snippet': {
                        'topLevelComment': {
                            'snippet': {
                                'authorDisplayName': 'User 1',
                                'textDisplay': 'Great video!',
                                'likeCount': 10,
                                'publishedAt': '2024-01-01T00:00:00Z'
                            }
                        }
                    }
                }
            ]
        })
        
        # Mock the method chain: youtube.commentThreads().list().execute()
        mock_youtube.commentThreads().list().execute = mock_execute

        comments = get_video_comments(mock_youtube, 'video_1')

        # Assertions
        self.assertEqual(comments[0]['snippet']['topLevelComment']['snippet']['authorDisplayName'], 'User 1')
        self.assertEqual(comments[0]['snippet']['topLevelComment']['snippet']['textDisplay'], 'Great video!')
    
    @patch('plugins.youtube_api.get_video_category')
    def test_get_video_category(self, mock_get_video_category):
        self.mock_youtube.videos().list().execute.return_value = {
            'items': [{'snippet': {'categoryId': '10'}}]
        }
        
        category_id = get_video_category(self.mock_youtube, 'video_1')
        
        self.assertEqual(category_id, '10')
    
    @patch('plugins.youtube_api.get_video_category_details')
    def test_get_video_category_details(self, mock_get_video_category_details):
        self.mock_youtube.videoCategories().list().execute.return_value = self.mock_category_response
        
        category_id = '10'
        category_name, category_description = get_video_category_details(self.mock_youtube, category_id)
        
        self.assertEqual(category_name, 'Music')
        self.assertEqual(category_description, 'All music related videos')
    
    @patch('plugins.youtube_api.create_youtube_client')  # Mock the client creation
    def test_get_channel_details(self, mock_create_youtube_client):
        mock_youtube = MagicMock()
        mock_create_youtube_client.return_value = mock_youtube
        mock_response = {
            'items': [{
                'snippet': {
                    'description': 'This is a channel about music.',
                    'publishedAt': '2020-01-01T00:00:00Z'
                }
            }]
        }
        mock_youtube.channels().list().execute.return_value = mock_response
        
        # Channel ID to test
        channel_id = 'channel_1'
        # Call the function you're testing
        channel_details = get_channel_details(mock_youtube, channel_id)
        # Assertions to check the returned channel details
        self.assertEqual(channel_details['description'], 'This is a channel about music.')
        self.assertEqual(channel_details['publishedAt'], '2020-01-01T00:00:00Z')
    
    @patch('plugins.youtube_api.save_data_locally')
    @patch('plugins.youtube_api.get_trending_videos')
    @patch('plugins.youtube_api.get_video_comments')
    @patch('plugins.youtube_api.get_video_category')
    @patch('plugins.youtube_api.get_video_category_details')
    @patch('plugins.youtube_api.get_channel_details')
    def test_extract_and_save(self, mock_channel_details, mock_category_details, mock_video_category, 
                               mock_video_comments, mock_trending_videos, mock_save_data_locally):
        # Set up the mock responses
        mock_trending_videos.return_value = self.mock_trending_response['items']
        mock_video_comments.return_value = self.mock_comments_response['items']
        mock_video_category.return_value = '10'
        mock_category_details.return_value = ('Music', 'All music related videos')
        mock_channel_details.return_value = {
            'description': 'This is a channel about music.',
            'publishedAt': '2020-01-01T00:00:00Z'
        }

        # Call the extract_and_save function
        extract_and_save()

        # Check if the save function was called
        mock_save_data_locally.assert_called_once()
        args, kwargs = mock_save_data_locally.call_args
        saved_data = args[0]
        
        # Check if saved data matches the expected structure
        self.assertIsInstance(saved_data, list)
        self.assertGreater(len(saved_data), 0) 

if __name__ == '__main__':
    unittest.main()
