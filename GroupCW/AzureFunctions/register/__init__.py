# System Imports
# Azure Imports
import asyncio
import uuid
from azure.functions import HttpRequest, HttpResponse
# Code base Imports
import AzureData
from shared_code.PasswordFunctions import hash_password, validate_password
from shared_code import auth
import re
import json

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

def main(req: HttpRequest) -> HttpResponse:
    try:
        req_body = req.get_json()
        email = req_body.get('email')
        username = req_body.get('username')
        password = req_body.get('password')
    except ValueError:
        return HttpResponse("Invalid request body", status_code=400)

    if not is_valid_email(email):
        return HttpResponse("Invalid email format", status_code=400)
    
    if not asyncio.run(is_email_unique(email)):
        return HttpResponse("Email is already registered", status_code=400)

    if not asyncio.run(is_username_unique(username)):
        return HttpResponse("Username is already taken", status_code=400)

    password_issues = validate_password(password)
    if password_issues:  # If the list is not empty, report the issues
        return HttpResponse(f"Password is invalid for the following reason(s): {'; '.join(password_issues)}", status_code=400)
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
        token = auth.signJwt(username)
        return HttpResponse(json.dumps({"result": True, "token": token}), status_code=201)
    except Exception as e:
        return HttpResponse(json.dumps({"result": False, "msg": f"Failed to create user: {str(e)}"}), status_code=500)
