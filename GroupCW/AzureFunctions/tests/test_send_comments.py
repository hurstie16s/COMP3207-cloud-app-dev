import unittest
import requests
import uuid
import json
from unittest.mock import patch
# Azure Imports
# Code base Imports
import AzureData
from shared_code import auth

class TestSendCommentsFunction(unittest.TestCase):
    TEST_URL = "http://localhost:7071/send/comments"

    def setUp(self):
        self.interview_id = "generated-unique-id"
        self.new_interview_data = {
            "username": "TestUser",
            "industry": "Test Industry",
            "questionId": "generated-unique-id-for-question", 
            "interviewTitle": "Test Interview Title",
            "interviewQuestion": "Test Interview Question?",
            "interviewBlobURL": "https://example.com/test-interview-blob-url.webm",
            "audioUuid": "generated-unique-audio-uuid",  
            "interviewLanguage": "en",
            "transcript": {
                "English": "Test transcript in English.",
                "Welsh": "Test transcript in Welsh.",
                "Irish": "Test transcript in Irish.",
                "French": "Test transcript in French.",
                "Polish": "Test transcript in Polish."
            },
            "comments": [],  
            "ratings": [],   
            "tips": {
                "goodTips": {
                    "English": ["Good tip in English."],
                    "Welsh": ["Good tip in Welsh."],
                    "Irish": ["Good tip in Irish."],
                    "French": ["Good tip in French."],
                    "Polish": ["Good tip in Polish."]
                },
                "improvementTips": {
                    "English": ["Improvement tip in English."],
                    "Welsh": ["Improvement tip in Welsh."],
                    "Irish": ["Improvement tip in Irish."],
                    "French": ["Improvement tip in French."],
                    "Polish": ["Improvement tip in Polish."]
                }
            },
            "private": False,
            "timestamp": "2024-01-06T13:21:46.435486",  
            "id": self.interview_id 
        }
        existing_data = list(AzureData.containerInterviewData.query_items(
            query="SELECT * FROM c WHERE c.id = @id",
            parameters=[{"name": "@id", "value": self.interview_id}],
            enable_cross_partition_query=True
        ))
        if existing_data:
            AzureData.containerInterviewData.delete_item(item=existing_data[0]['id'], partition_key=existing_data[0]['id'])

        AzureData.containerInterviewData.create_item(body=self.new_interview_data)

    def test_add_comment(self):
        token = auth.signJwt("TestUser")
        headers = {'Authorization': token}

        comment_data = {
            "id": self.interview_id,
            "comment": "This is a test comment."
        }
        response = requests.put(self.TEST_URL, json=comment_data, headers=headers)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data.get('result'))
        self.assertEqual(response_data.get('msg'), "Comment added successfully")
    
    def test_invalid_interview_id(self):
        token = auth.signJwt("TestUser")
        headers = {'Authorization': token}
        comment_data = {
            "id": "InvalidInterviewID",
            "comment": "This is a test comment with invalid interview ID."
        }
        response = requests.put(self.TEST_URL, json=comment_data, headers=headers)
        response_data = response.json()
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(response_data.get('result'))
        self.assertEqual(response_data.get('msg'), "Interview data not found for the provided ID")

    def test_invalid_authorization_token(self):
        headers = {'Authorization': "TestUser"}

        comment_data = {
            "id": self.interview_id,
            "comment": "This is a test comment."
        }
        response = requests.put(self.TEST_URL, json=comment_data, headers=headers)
        response_data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertFalse(response_data.get('result'))
        self.assertEqual(response_data.get('msg'), "Invalid token")

        
    def tearDown(self):
        AzureData.containerInterviewData.delete_item(item=self.interview_id, partition_key=self.interview_id)


if __name__ == '__main__':
    unittest.main()