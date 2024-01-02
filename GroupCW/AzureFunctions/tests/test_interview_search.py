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
    TEST_URL="http://localhost:7071/interview/data/search"
    
    def test_searching_by_username_and_question(self):
        
            jsonData = json.dumps({"username": "Test", "interviewQuestion" : "Test"})
        
            response = requests.get(self.TEST_URL, data=jsonData)
        
            self.assertEqual(200, response.status_code)
            
    
    def test_searching_by_question(self):
        
            jsonData = json.dumps({"username": "", "interviewQuestion" : "Test"})
        
            response = requests.get(self.TEST_URL, data=jsonData)


            self.assertEqual(200, response.status_code)
            
    
    def test_searching_by_username(self):
        
            jsonData = json.dumps({"username": "Test", "interviewQuestion" : ""})
            response = requests.get(self.TEST_URL, data=jsonData)
        
            self.assertEqual(200, response.status_code)


    def tearDown(self):
        pass
        


if __name__ == '__main__':
    unittest.main()