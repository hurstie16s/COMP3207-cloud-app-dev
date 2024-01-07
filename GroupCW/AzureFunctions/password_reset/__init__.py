# System Imports
import logging
import json
import secrets
import random
import string
import uuid
import asyncio
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
# Code base imports
from shared_code import PasswordFunctions, DBFunctions, FaultCheckers, EmailFunctions
import AzureData

def main(req: HttpRequest) -> HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    # Get data from JSON doc
    input = req.get_json()
    email = input.get("email")

    if FaultCheckers.checkParams([email]):
        output = {"result": False, "msg": "Bad Request"}
        code = 400
        return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=code)

    userInfo = getUserData(email)
    if userInfo is None:
        output = {"result": False, "msg": "User not Found"}
        code = 401
        return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=code)

    # Create random password
    randomPassword = PasswordFunctions.generateRandomPassword()

    # Hash random password
    randomPasswordHash = PasswordFunctions.hash_password(randomPassword)

    # Update User info
    newDict = {
        "hashed_password": randomPasswordHash,
        "change_password": True
    }

    userInfo.update(newDict)
    ref = str(uuid.uuid1().hex)

    # Update Database
    DBFunctions.upsert_item(data=userInfo, container=AzureData.containerUsers)

    # Send Email
    asyncio.run(EmailFunctions.sendEmail(userInfo, randomPassword, ref))

    # Return HttpResponse
    output = {"result": True, "msg": "Password Reset", "ref": ref}
    code = 203
    return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=code)





def getUserData(email: str):
    # Get User Data
    query = "SELECT * FROM User WHERE User.email = @email"
    params = [{"name": "@email", "value": email}]
    result = DBFunctions.query_items(
        query=query,
        parameters=params,
        container=AzureData.containerUsers
    )

    if len(result) == 0:
        return None

    return result[0]