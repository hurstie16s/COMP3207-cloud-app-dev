# System Imports
# Azure Imports
import asyncio
import uuid
import json
from azure.functions import HttpRequest, HttpResponse
# Code base Imports
import AzureData
from shared_code.PasswordFunctions import hash_password
import re

# Helper function to check if the email is unique
async def is_email_unique(email):
    items = list(AzureData.containerUsers.query_items(
        query=f"SELECT * FROM c WHERE c.email = '{email}'",
        enable_cross_partition_query=True
    ))
    return len(items) == 0

# Helper function to check if the username is unique
async def is_username_unique(username):
    items = list(AzureData.containerUsers.query_items(
        query=f"SELECT * FROM c WHERE c.username = '{username}'",
        enable_cross_partition_query=True
    ))
    return len(items) == 0

# Helper function to validate email format
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Helper function to validate password strength and provide reasons for invalidity
def validate_password(password):
    reasons = []
    if len(password) < 8:
        reasons.append("Password must be at least 8 characters long.")
    if not re.search("[0-9]", password):
        reasons.append("Password must contain at least one number.")
    if not re.search("[A-Za-z]", password):
        reasons.append("Password must contain at least one letter.")
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        reasons.append("Password must contain at least one special character.")
    return reasons

def main(req: HttpRequest) -> HttpResponse:
    try:
        req_body = req.get_json()
        email = req_body.get('email')
        username = req_body.get('username')
        password = req_body.get('password')
    except ValueError:
        return HttpResponse(json.dumps({"result": False, "msg": "Invalid request body"}), status_code=400, mimetype="application/json")

    if not is_valid_email(email):
        return HttpResponse(json.dumps({"result": False, "msg": "Invalid email format"}), status_code=400, mimetype="application/json")
    
    if not asyncio.run(is_email_unique(email)):
        return HttpResponse(json.dumps({"result": False, "msg": "Email is already registered"}), status_code=400, mimetype="application/json")

    if not asyncio.run(is_username_unique(username)):
        return HttpResponse(json.dumps({"result": False, "msg": "Username is already taken"}), status_code=400, mimetype="application/json")

    password_issues = validate_password(password)
    if password_issues:  # If the list is not empty, report the issues
        return HttpResponse(json.dumps({"result": False, "msg": f"Password is invalid for the following reason(s): {'; '.join(password_issues)}"}), status_code=400, mimetype="application/json")
    hashed_password = hash_password(password)

    new_user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "username": username,
        "hashed_password": hashed_password,
        "change_password": False
    }
    
    try:
        AzureData.containerUsers.create_item(body=new_user)
        return HttpResponse(json.dumps({"result": True, "msg": "User registered successfully"}), status_code=200, mimetype="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"result": False, "msg": f"Failed to create user: {str(e)}"}), status_code=500, mimetype="application/json")
