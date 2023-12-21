# System Imports
import logging
import json
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
#Code base imports
from shared_code import PasswordFunctions, DBFunctions
from AzureData import AzureData

# TODO: Check how requests should come in and how they should be sent out

def main(req: HttpRequest) -> HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    #Get data from JSON doc
    input = req.get_json()
    emailOrUsername = input.get("username")
    password = input.get("password")

    # Check username exists, grab hashed password based off username
    query = "SELECT * FROM Users WHERE Users.email=@emailOrUsername OR Users.username=@emailOrUsername"
    params = [{"name": "@emailOrUsername", "value": emailOrUsername}]

    # Can garuntee only 1 result returned, at most
    result = DBFunctions.query_items(
        query=query, 
        parameters=params, 
        container=AzureData.containerUsers
    )

    if (len(result) == 0):
        # Email or Username incorrect
        # Auth Fail
        output = {"result": False, "msg": "User not found"}
        
    else:
        # Verify Password
        verified = PasswordFunctions.verify(password, result[0].get("password"))

        if (verified):
            # AuthSuccess
            output = {"result": True, "msg": "AuthSuccess"}
            return
        else :
            # AuthFail
            output = {"result": False, "msg": "Password Incorrect"}

    # Return HttpResponse
    return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=200)