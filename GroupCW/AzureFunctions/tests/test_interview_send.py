import unittest
import requests
import json
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
import base64
import AzureData
import uuid
from shared_code import auth

#need to improve this test
class TestLoginUserFunction(unittest.TestCase):  
    
    TEST_URL="http://localhost:7071/interview/data/send"

    def setUp(self):
        self.username = "test"
        self.jwt = auth.signJwt(self.username)
    
    def test_sending_interview(self):
         with open("./test.webm", 'rb') as file:
            files = {'webmFile': ('meme.webm', file, 'video/webm')}
        
            jsonData = {
                "username": self.username,
                "industry": "IT",
                "interviewTitle": "About me",
                "interviewQuestion": "Tell us about yourself",
                "private": False,
            }
        
            response = requests.post(self.TEST_URL, data=jsonData, files=files, headers={"Authorization": self.jwt})
        
            self.assertEqual(200, response.status_code)
            self.assertEqual(b'{"result": true, "msg": "OK"}', response.content)

    def test_send_interview_invalid_jwt(self):
        with open("./test.webm", 'rb') as file:
            files = {'webmFile': ('meme.webm', file, 'video/webm')}
        
            jsonData = {
                "username": self.username,
                "industry": "IT",
                "interviewTitle": "About me",
                "interviewQuestion": "Tell us about yourself",
                "private": False,
            }
        
            response = requests.post(self.TEST_URL, data=jsonData, files=files, headers={"Authorization": "invalid"})
        
            self.assertEqual(401, response.status_code)
            self.assertEqual("Invalid token", response.json()['msg'])

    '''

    def setUp(self):
        # Create Dummy Credentials
        self.testUsername = str(uuid.uuid1().hex)

        data = {
            "username": self.testUsername,
            "industry": self.testUsername,
            "interviewTitle": self.testUsername,
            "interviewQuestion": self.testUsername,
            "private": False,
        }

        DBFunctions.create_item(
            data=data,
            container=AzureData.containerInterviewData
        )

    def tearDown(self):
        pass
        


if __name__ == '__main__':
    unittest.main()
    
    '''
