import unittest
import requests
import json
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
import base64
import AzureData

#need to improve this test
class TestLoginUserFunction(unittest.TestCase):  
    
    TEST_URL="http://localhost:7071/interview/data/send"
    
    def test_sending_interview(self):
         with open("./test.webm", 'rb') as file:
            files = {'webmFile': ('meme.webm', file, 'video/webm')}
        
            jsonData = {
                "username": "Moonzyyy",
                "industry": "IT",
                "interviewTitle": "About me",
                "interviewQuestion": "Tell us about yourself",
                "private": False,
            }
        
            response = requests.post(self.TEST_URL, data=jsonData, files=files)
        
            self.assertEqual(200, response.status_code)
            self.assertEqual(b'{"result": true, "msg": "OK"}', response.content)
        
if __name__ == '__main__':
    unittest.main()