import unittest
import requests
import json
import logging

from azure.cosmos import CosmosClient

#
# This is an old test that was used intially to fetch the webm file from the correct conatiner.
# No longer in use.
#

class TestReceive(unittest.TestCase):
    
    LOCAL_DEV_URL="http://localhost:7071/interview/receive"
    TEST_URL = LOCAL_DEV_URL
    
    with open('../local.settings.json') as settings_file:
        settings = json.load(settings_file)

    # Test one is ensuring this webm file can be accessed in the backend
    # Change the filename accordingly
    def test_one(self):
        prompt = json.dumps({"interviewBlopURL": "https://interviewstorage.blob.core.windows.net/interview-blop/test30b7d227-651f-4237-941e-80a95291c771.webm"})
        response = requests.get(self.TEST_URL, data=prompt)

        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        self.assertEqual(200, response.status_code)
    
    # Test two tests if it is accessing the correct storage part in the backend
    # Should throw a 400 error
    def test_two(self):
        prompt = json.dumps({"interviewBlopURL": "https://interviewstoragegf.blob.core.windows.net/interview-blop/test30b7d227-651f-4237-941e-80a95291c771.webm"})
        response = requests.get(self.TEST_URL, data=prompt)

        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        self.assertEqual("Wrong storage name", response.text)
    
    # Test three has the incorrect container name
    # Backend cannot access this and the application throws a 500 internal server error
    def test_three(self):
        prompt = json.dumps({"interviewBlopURL": "https://interviewstorage.blob.core.windows.net/intervi/test30b7d227-651f-4237-941e-80a95291c771.webm"})
        response = requests.get(self.TEST_URL, data=prompt)

        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        self.assertEqual(500, response.status_code)

    # Test four give the incorrect name for a webm file
    # This should throw an internal server error, of error code 500
    def test_four(self):
        prompt = json.dumps({"interviewBlopURL": "https://interviewstorage.blob.core.windows.net/interview-blop/test-80a95291c771.webm"})
        response = requests.get(self.TEST_URL, data=prompt)

        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        self.assertEqual(500, response.status_code)
    