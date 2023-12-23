#System Imports
import unittest
import requests
import uuid
import json
#Azure Imports
#Code base Imports
import AzureData
from shared_code import DBFunctions, PasswordFunctions

class TestAddUserFunction(unittest.TestCase):
    TEST_URL = "http://localhost:7071/login"

    def setUp(self):
        # Create Dummy Credentials
        self.testUsername = str(uuid.uuid1().hex)
        self.testEmail = self.testUsername+"@test.co.uk"
        self.testPassword = self.testUsername
        self.testPasswordHashed = PasswordFunctions.hash_password(self.testPassword)

        data = {
            "username": self.testUsername,
            "email": self.testEmail,
            "password": self.testPasswordHashed
        }

        DBFunctions.create_item(
            data=data,
            container=AzureData.containerUsers
        )
    
    def test_user_not_found(self):
        
        # Incorrect Username and Password
        username = "false User"
        password = "false Password"

        data = json.dumps({"username": username, "password": password})

        response = requests.get(url=self.TEST_URL, data=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'{"result": false, "msg": "User not found"}')

    def test_password_incorrect(self):

        # Incorrect Password
        password = "false Password"

        data = json.dumps({"username": self.testUsername, "password": password})

        response = requests.get(url=self.TEST_URL, data=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'{"result": false, "msg": "Invalid Login"}')

    def test_login_success(self):

        data = json.dumps({"username": self.testUsername, "password": self.testPassword})

        response = requests.get(url=self.TEST_URL, data=data)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        print("test")
        DBFunctions.delete_item(
            id=self.testUsername, 
            container=AzureData.containerUsers
        )
        