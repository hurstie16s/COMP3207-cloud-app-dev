import unittest
import requests
import uuid
import json
# Azure Imports
# Code base Imports
import AzureData
from shared_code import DBFunctions, PasswordFunctions

class TestRegisterFunction(unittest.TestCase):
    TEST_URL = "http://localhost:7071/register"

    def setUp(self):
        self.valid_email = "testuser@test.com"
        self.valid_username = "testuser"
        self.valid_password = "ValidPassword123!"

        # Create a user to test duplicate email and username
        existing_user = {
            "email": self.valid_email,
            "username": self.valid_username,
            "hashed_password": PasswordFunctions.hash_password(self.valid_password)
        }
        DBFunctions.create_item(data=existing_user, container=AzureData.containerUsers)

    def test_valid_registration(self):
        unique_id = uuid.uuid4().hex
        new_email = f"{unique_id}@test.com"
        new_username = f"user_{unique_id}"
        data = json.dumps({
            "email": new_email,
            "username": new_username,
            "password": self.valid_password
        })
        response = requests.post(url=self.TEST_URL, data=data)
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

        self.assertEqual(response.status_code, 201, "Expected status code for successful registration is 201")
        self.assertTrue(response_data.get("result"), "Registration should be successful")
        self.assertIn("token", response_data, "Response should contain a token key")

    def test_duplicate_email(self):
        unique_id = uuid.uuid4().hex
        email = "testuser@test.com"
        username = f"newuser_{unique_id}"
        password = "ValidPassword123!"

        data = json.dumps({
            "email": email,
            "username": username,
            "password": password
        })

        response = requests.post(url=self.TEST_URL, data=data)

        try:
            response_data = response.json()
            expected_message = {"Email is already registered"}
            self.assertEqual(response_data, expected_message)
        except json.JSONDecodeError:
            self.assertIn("Email is already registered", response.text)

        self.assertEqual(response.status_code, 400)

    def test_invalid_email_format(self):
        unique_id = uuid.uuid4().hex
        email = "invalidemail"
        username = f"newuser_{unique_id}"
        password = "ValidPassword123!"

        data = json.dumps({
            "email": email,
            "username": username,
            "password": password
        })

        response = requests.post(url=self.TEST_URL, data=data)

        try:
            response_data = response.json()
            expected_message = {"Invalid email format"}
            self.assertEqual(response_data, expected_message)
        except json.JSONDecodeError:
            self.assertIn("Invalid email format", response.text)

        self.assertEqual(response.status_code, 400)

    def test_duplicate_username(self):
        unique_id = uuid.uuid4().hex
        email = f"{unique_id}@test.com"
        username = "testuser"
        password = "ValidPassword123!"

        data = json.dumps({
            "email": email,
            "username": username,
            "password": password
        })

        response = requests.post(url=self.TEST_URL, data=data)

        try:
            response_data = response.json()
            expected_message = {"Username is already taken"}
            self.assertEqual(response_data, expected_message)
        except json.JSONDecodeError:
            self.assertIn("Username is already taken", response.text)

        self.assertEqual(response.status_code, 400)

    def test_invalid_password_too_short(self):
        unique_id = uuid.uuid4().hex
        email = f"{unique_id}@test.com"
        username = f"newuser_{unique_id}"
        password = "Sh0rt!"

        data = json.dumps({
            "email": email,
            "username": username,
            "password": password
        })

        response = requests.post(url=self.TEST_URL, data=data)

        try:
            response_data = response.json()
            self.assertIn("Password is invalid for the following reason(s):", response_data.get("msg", ""))
            self.assertIn("Password must be at least 8 characters long", response_data.get("msg", ""))
        except json.JSONDecodeError:
            self.assertIn("Password is invalid for the following reason(s):", response.text)
            self.assertIn("Password must be at least 8 characters long", response.text)

        self.assertEqual(response.status_code, 400)

    def test_password_without_number(self):
        unique_id = uuid.uuid4().hex
        email = f"{unique_id}@test.com"
        username = f"newuser_{unique_id}"
        password = "Password!"

        data = json.dumps({
            "email": email,
            "username": username,
            "password": password
        })

        response = requests.post(url=self.TEST_URL, data=data)

        try:
            response_data = response.json()
            self.assertIn("Password is invalid for the following reason(s):", response_data.get("msg", ""))
            self.assertIn("Password must contain at least one number", response_data.get("msg", ""))
        except json.JSONDecodeError:
            self.assertIn("Password is invalid for the following reason(s):", response.text)
            self.assertIn("Password must contain at least one number", response.text)

    def test_password_without_letter(self):
        unique_id = uuid.uuid4().hex
        email = f"{unique_id}@test.com"
        username = f"newuser_{unique_id}"
        password = "12345678!"

        data = json.dumps({
            "email": email,
            "username": username,
            "password": password
        })

        response = requests.post(url=self.TEST_URL, data=data)

        try:
            response_data = response.json()
            self.assertIn("Password is invalid for the following reason(s):", response_data.get("msg", ""))
            self.assertIn("Password must contain at least one letter", response_data.get("msg", ""))
        except json.JSONDecodeError:
            self.assertIn("Password is invalid for the following reason(s):", response.text)
            self.assertIn("Password must contain at least one letter", response.text)

    def test_password_without_special_character(self):
        unique_id = uuid.uuid4().hex
        email = f"{unique_id}@test.com"
        username = f"newuser_{unique_id}"
        password = "Password1"

        data = json.dumps({
            "email": email,
            "username": username,
            "password": password
        })

        response = requests.post(url=self.TEST_URL, data=data)

        try:
            response_data = response.json()
            self.assertIn("Password is invalid for the following reason(s):", response_data.get("msg", ""))
            self.assertIn("Password must contain at least one special character", response_data.get("msg", ""))
        except json.JSONDecodeError:
            self.assertIn("Password is invalid for the following reason(s):", response.text)
            self.assertIn("Password must contain at least one special character", response.text)

    def tearDown(self):
        try:
            DBFunctions.delete_item(id=self.valid_username, container=AzureData.containerUsers)
            DBFunctions.delete_item(id="newuser", container=AzureData.containerUsers)
        except:
            pass

if __name__ == '__main__':
    unittest.main()