import unittest
import requests
import json
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient

class TestLoginUserFunction(unittest.TestCase):  
    
    #still need to finish
    def test_sending_interview(self):
        with open("./meme.webm", 'rb') as file:
            webm_content = file.read()
        
        validPrompt = json.dumps({"username":"Moonzyyy",
                                  "interviewTitle":"About me",
                                  "interviewQeustion":"Tell us about yourself",
                                  "audioFile": webm_content,
                                  "private": False,})
        response = requests.post(self.TEST_URL,data=validPrompt)
        self.assertEqual(200, response.status_code)
        self.assertEqual(b'OK', response.content)
        
if __name__ == '__main__':
    unittest.main()