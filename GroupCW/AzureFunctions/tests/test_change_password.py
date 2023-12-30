#System Imports
import unittest
import requests
import uuid
import time
#Azure Imports
#Code base Imports
import AzureData
from shared_code import DBFunctions

class TestAddUserFunction(unittest.TestCase):
    TEST_URL = "http://localhost:7071/password/change"

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

    def test_current_password_incorrect(self):
        
        falsePassword = str(time.time_ns())

        data={
            "username": self.testUsername,
            "currentPassword": falsePassword,
            "newPassword": falsePassword,
            "newPasswordConfirm": falsePassword
        }

        response = requests.get(url=self.TEST_URL, data=data)

        self.assertEqual(response.content, {"result": False, "msg": "AuthFail"})

        self.assertEqual(response.status_code, 403)


    def test_new_password_confirm_match_fail(self):
        
        newPassword = "newPassword"
        newPasswordConfirm = "newPasswordConfirmFail"

        data={
            "username": self.testUsername,
            "currentPassword": self.testPassword,
            "newPassword": newPassword,
            "newPasswordConfirm": newPasswordConfirm
        }

        response = requests.get(url=self.TEST_URL, data=data)

        self.assertEqual(response.content, {"result": False, "msg": "Password does not match confirmation"})

        self.assertEqual(response.status_code, 403)

    def test_password_change_success(self):
        
        newPassword = "newPassword"

        data={
            "username": self.testUsername,
            "currentPassword": self.testPassword,
            "newPassword": newPassword,
            "newPasswordConfirm": newPassword
        }

        response = requests.get(url=self.TEST_URL, data=data)

        self.assertEqual(response.content, {"result": True, "msg": "Password Changed"})

        self.assertEqual(response.status_code, 200)