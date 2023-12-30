#System Imports
import unittest
import requests
import uuid
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
        pass

    def test_new_password_confirm_match(self):
        pass

    def test_password_change_success(self):
        pass