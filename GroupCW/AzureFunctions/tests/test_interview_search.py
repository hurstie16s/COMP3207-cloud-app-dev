import unittest
import requests
import json
import AzureData
import uuid
from shared_code import auth

#need to improve this test
class TestLoginUserFunction(unittest.TestCase):  
    
    #TBD
    TEST_URL="http://localhost:7071/interview/data/search"

    def setUp(self):
        self.testUsername = str(uuid.uuid1().hex)
        self.jwt = auth.signJwt(self.testUsername)
    
    def test_searching_by_username_and_question(self):
        jsonData = json.dumps({"username": "Test", "interviewQuestion" : "Test"})
        response = requests.post(self.TEST_URL, data=jsonData, headers={"Authorization": self.jwt})
        
        self.assertEqual(200, response.status_code)
    
    def test_searching_by_question(self):
        jsonData = json.dumps({"username": "", "interviewQuestion" : "Test"})
        response = requests.post(self.TEST_URL, data=jsonData, headers={"Authorization": self.jwt})

        self.assertEqual(200, response.status_code)
    
    def test_searching_by_username(self):
        jsonData = json.dumps({"username": "Test", "interviewQuestion" : ""})
        response = requests.post(self.TEST_URL, data=jsonData, headers={"Authorization": self.jwt})
        
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()