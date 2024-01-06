#System Imports
import unittest
import requests
import uuid
import time
import json
#Azure Imports
#Code base Imports
import AzureData
from shared_code import DBFunctions, PasswordFunctions, auth

class TestAddUserFunction(unittest.TestCase):
    TEST_URL_PASSWORD_CHANGE = "http://localhost:7071/password/change"
    TEST_URL_LOGIN = "http://localhost:7071/login"

    def setUp(self):
        # Create Dummy Credentials
        self.testUsername = str(uuid.uuid1().hex)
        self.jwt = auth.signJwt(self.testUsername)
        self.testEmail = self.testUsername+"@test.co.uk"
        self.testPassword = self.testUsername

        data = {
            "username": self.testUsername,
            "email": self.testEmail,
            "hashed_password": PasswordFunctions.hash_password(self.testPassword)
        }

        DBFunctions.create_item(
            data=data,
            container=AzureData.containerUsers
        )

    # Test when the current password is incorrect
    def test_current_password_incorrect(self):
        falsePassword = str(time.time_ns())

        data = json.dumps({
            "username": self.testUsername,
            "currentPassword": falsePassword,
            "newPassword": falsePassword,
            "newPasswordConfirm": falsePassword
        })

        response = requests.put(url=self.TEST_URL_PASSWORD_CHANGE, data=data, headers={"Authorization": self.jwt})
        self.assertEqual(response.content, b'{"result": false, "msg": "AuthFail"}')
        self.assertEqual(response.status_code, 403)

    # Test when the new password does not match the confirmation
    def test_new_password_confirm_match_fail(self):
        
        newPassword = "newPassword"
        newPasswordConfirm = "newPasswordConfirmFail"

        data= json.dumps({
            "username": self.testUsername,
            "currentPassword": self.testPassword,
            "newPassword": newPassword,
            "newPasswordConfirm": newPasswordConfirm
        })

        response = requests.put(url=self.TEST_URL_PASSWORD_CHANGE, data=data)
        response = requests.put(url=self.TEST_URL_PASSWORD_CHANGE, data=data, headers={"Authorization": self.jwt})

        self.assertEqual(response.content, b'{"result": false, "msg": "Password does not match confirmation"}')

        self.assertEqual(response.status_code, 403)

    # Test a successful password change
    def test_password_change_success(self):
        newPassword = "newPassword"

        data= json.dumps({
            "username": self.testUsername,
            "currentPassword": self.testPassword,
            "newPassword": newPassword,
            "newPasswordConfirm": newPassword
        })

        response = requests.put(url=self.TEST_URL_PASSWORD_CHANGE, data=data, headers={"Authorization": self.jwt})
        self.assertEqual(response.content, b'{"result": true, "msg": "Password Changed"}')
        self.assertEqual(response.status_code, 200)

        # Test that password has changed
        data = json.dumps({
            "username": self.testUsername,
            "password": newPassword
        })

        response = requests.post(url=self.TEST_URL_LOGIN, data=data)

        #self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"result": true, "msg": "AuthSuccess"}')
