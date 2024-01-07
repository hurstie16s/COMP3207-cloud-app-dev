import unittest
import requests
import uuid
import json
from unittest.mock import patch
# Azure Imports
# Code base Imports
import AzureData
from shared_code import auth

class TestRateInterviewFunction(unittest.TestCase):
    TEST_URL = "http://localhost:7071/rate/interview"

    def setUp(self):
        self.token = auth.signJwt("TestUser")
        self.headers = {'Authorization': self.token}
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

    def test_valid_rating(self):
        rate_data = {
            "id": self.interview_id,
            "rating": 4
        }
        response = requests.put(self.TEST_URL, json=rate_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['result'], True)
        self.assertEqual(response_data['msg'], "Rating added successfully")

    def test_invalid_rating(self):
        rate_data = {
            "id": self.interview_id,
            "rating": 6  # Invalid rating
        }
        response = requests.put(self.TEST_URL, json=rate_data, headers=self.headers)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data['result'], False)
        self.assertIn("Rating must be a whole number between 1 and 5", response_data['msg'])

    def test_invalid_interview_id(self):
        rate_data = {
            "id": "non-existent-id",
            "rating": 3
        }
        response = requests.put(self.TEST_URL, json=rate_data, headers=self.headers)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data['result'], False)
        self.assertIn("Interview data not found", response_data['msg'])

        
    def tearDown(self):
        AzureData.containerInterviewData.delete_item(item=self.interview_id, partition_key=self.interview_id)


if __name__ == '__main__':
    unittest.main()