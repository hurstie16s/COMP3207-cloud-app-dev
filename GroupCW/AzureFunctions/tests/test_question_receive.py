import unittest
import requests
import json
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
import base64
import AzureData
import uuid

#need to improve this test
class TestLoginUserFunction(unittest.TestCase):  
    
    #TBD
    TEST_URL="http://localhost:7071/interview/question/receive"
    
    SETUP_URL = "http://localhost:7071/interview/question/submit"
    def setUp(self):
        
        jsonData = json.dumps({"question": "Why did you choose this company?", "difficulty" : 2, "regularity": 1})
        response = requests.post(self.TEST_URL, data=jsonData)
    
    def test_question_receive(self):
        
            jsonData = json.dumps({"id": ""})
            response = requests.get(self.TEST_URL, data=jsonData)
           
            print(response.content)
            self.assertEqual(200, response.status_code)
            
    
    def test_question_not_able_to_receive(self):
        
            jsonData = json.dumps({"id": "dasdsad"})
        
            response = requests.get(self.TEST_URL, data=jsonData)


            self.assertEqual(200, response.status_code)
            



    def tearDown(self):
        pass
        


if __name__ == '__main__':
    unittest.main()