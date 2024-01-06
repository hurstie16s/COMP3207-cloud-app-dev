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
    TEST_URL = "http://localhost:7071/password/reset"

    def setUp(self):
        # Create Dummy Credentials
        self.testUsername = str(uuid.uuid1().hex)
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