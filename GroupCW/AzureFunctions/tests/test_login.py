#System Imports
import unittest
import requests
import uuid
#Azure Imports
#Code base Imports
import AzureData
from shared_code import DBFunctions

class TestAddUserFunction(unittest.TestCase):
    TEST_URL = "http://localhost:7071/login"

    def setUp(self):
        # Create Dummy Credentials
        self.testUsername = str(uuid.uuid1().hex)
        self.testEmail = self.testUsername+"@test.co.uk"
        self.testPassword = self.testUsername

        data = {
            "username": self.testUsername,
            "email": self.testEmail,
            "password": self.testPassword
        }

        DBFunctions.create_item(
            data=data,
            container=AzureData.containerUsers
        )
    
    def test_user_not_found(self):
        
        # Incorrect Username and Password
        username = "false User"
        password = "false Password"

        response = requests.get(url=self.TEST_URL, data={"username": username, "password": password})
        result = response.status_code == 401 and response.content == {"result": False, "msg": "User not found"}
        self.assertTrue(result)

    def test_password_incorrect(self):

        # Incorrect Password
        password = "false Password"

        response = requests.get(url=self.TEST_URL, data={"username": self.testUsername, "password": password})
        result = response.status_code == 401 and response.content == {"result": False, "msg": "Invalid Login"}
        self.assertTrue(result)

    def test_login_success(self):

        response = requests.get(url=self.TEST_URL, data={"username": self.testUsername, "password": self.testPassword})
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        print("test")
        DBFunctions.delete_item(
            id=self.testUsername, 
            container=AzureData.containerUsers
        )
        
if __name__ == '__main__':
    unittest.main()