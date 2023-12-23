import unittest
import requests
import json
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
import base64
import AzureData

class TestLoginUserFunction(unittest.TestCase):  
    
    LOCAL_DEV_URL="http://localhost:7071/api/prompt/create"
    
    def test_sending_interview(self):
        print(dir(AzureData))
        print(AzureData.containerUsers)
        with open("./meme.webm", 'rb') as file:
            webm_content = base64.b64encode(file.read()).decode('utf-8')
        
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