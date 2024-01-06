import unittest
import requests
import json
from shared_code import auth

#need to improve this test
class TestLoginUserFunction(unittest.TestCase):  
    
    #TBD
    TEST_URL="http://localhost:7071/interview/question/submit"

    def setUp(self):
        self.testUsername = "test"
        self.jwt = auth.signJwt(self.testUsername)  
    
    def test_submitting_question_company(self):
        
            jsonData = json.dumps({"question": "Why did you choose this company?", "difficulty" : 2, "regularity": 1})
        
            response = requests.post(self.TEST_URL, data=jsonData, headers={"Authorization": self.jwt})
        
            self.assertEqual(201, response.status_code)
    
    def test_submitting_question_yourself(self):
        
            jsonData = json.dumps({"question": "Tell me about yourself?", "difficulty" : 1, "regularity": 0})
        
            response = requests.post(self.TEST_URL, data=jsonData)
        
            self.assertEqual(201, response.status_code)
            
    def test_submitting_question_bring(self):
        
            jsonData = json.dumps({"question": "What would you bring to this team?", "difficulty" : 1, "regularity": 2})
        
            response = requests.post(self.TEST_URL, data=jsonData, headers={"Authorization": self.jwt})
        
            self.assertEqual(201, response.status_code)

    def tearDown(self):
        pass
        


if __name__ == '__main__':
    unittest.main()