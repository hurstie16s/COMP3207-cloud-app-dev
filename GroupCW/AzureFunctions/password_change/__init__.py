# System Imports
import logging
import json
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
#Code base imports
from shared_code import FaultCheckers, DBFunctions, PasswordFunctions
import AzureData

# TODO: Check how requests should come in and how they should be sent out

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

    # Verify password
    if not PasswordFunctions.verify(currentPassword, result[0].get("password")):
        # Set JSON output
        output = {"result": False, "msg": "AuthFail"}
        code = 403
    elif newPassword != newPasswordConfirm :
        # Set JSON output
        output = {"result": False, "msg": "Password does not match confirmation"}
        code = 403
    else:
        # Hash new password
        newPasswordHash = PasswordFunctions.hash_password(password=newPassword)