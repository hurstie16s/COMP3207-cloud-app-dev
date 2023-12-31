# System Imports
import logging
import json
import asyncio
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
#Code base imports
from shared_code import FaultCheckers, DBFunctions, PasswordFunctions
import AzureData

def main(req: HttpRequest) -> HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    #Get data from JSON doc
    input = req.get_json()
    username = input.get("username")
    currentPassword = input.get("currentPassword")
    newPassword = input.get("newPassword")
    newPasswordConfirm = input.get("newPasswordConfirm")

    if FaultCheckers.checkParams([username, currentPassword, newPassword, newPasswordConfirm]):
        output = {"result": False, "msg": "AuthFail"}
        code = 400
        return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=code)
    
    # Get data for user
    query = "SELECT * FROM Users WHERE Users.username = @username"
    params = [{"name":"@username", "value": username}]

    # Can garuntee only 1 result returned, at most
    result = DBFunctions.query_items(
        query=query, 
        parameters=params, 
        container=AzureData.containerUsers
    )

    userInfo = result[0]

    password_issues = PasswordFunctions.validate_password(newPassword)

    # Verify password
    if not PasswordFunctions.verify(currentPassword, userInfo.get("hashed_password")):
        # Set JSON output
        output = {"result": False, "msg": "AuthFail"}
        code = 403
    elif newPassword != newPasswordConfirm :
        # Set JSON output
        output = {"result": False, "msg": "Password does not match confirmation"}
        code = 403
    elif password_issues:
        #Set JSON output
        output = {
            "result": False, 
            "msg": f"Password is invalid for the following reason(s): {'; '.join(password_issues)}"
        }
        code = 403
    else:
        # Hash new password
        newPasswordHash = PasswordFunctions.hash_password(password=newPassword)

        newDict = {
            "hashed_password": newPasswordHash,
            "change_password": False
        }

        # Update userInfo with new password and ensure flag is false
        userInfo.update(newDict)

        # Update database
        asyncio.run(update_password(userInfo))

        output = {"result": True, "msg": "Password Changed"}
        code = 200
    
    # Return HttpResponse
    return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=code)

async def update_password(data: dict):
    # Update database
    DBFunctions.upsert_item(data=data, container=AzureData.containerUsers)
    logging.info("Password Changed")