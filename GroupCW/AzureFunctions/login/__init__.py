# System Imports
import logging
import json
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
#Code base imports
from shared_code import PasswordFunctions, DBFunctions, FaultCheckers
import AzureData

# TODO: Check how requests should come in and how they should be sent out

def main(req: HttpRequest) -> HttpResponse:

    """
    Login Function:
    input: {username: string, password: string}
    output: {result: bool, msg: string}

    AuthFail:
        - user not found
        - username/email or password incorrect
        code = 401
        result = false
    AuthSuccess:
        result = true
        code = 200
    
    Endpoint: /login
    """
    
    logging.info('Python HTTP trigger function processed a request.')

    #Get data from JSON doc
    try:
        input = req.get_json()
    except ValueError:
        output = {"result": False, "msg": "Malformed Request"}
        code = 400
        return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=code)
    
    emailOrUsername = input.get("username")
    password = input.get("password")

    if FaultCheckers.checkParams([emailOrUsername, password]):
        output = {"result": False, "msg": "AuthFail"}
        code = 400
        return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=code)

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
        code = 401
        
    else:
        # Verify Password
        logging.info("CHECK MESSAGE:: hashed password type: "+str(type(result[0].get("password"))))
        verified = PasswordFunctions.verify(password, result[0].get("password"))

        if (verified):
            # AuthSuccess
            output = {"result": True, "msg": "AuthSuccess"}
            code = 200
        elif (result[0].get("change_password")):
            output = {"result": True, "msg": "Redirect to Change Password"}
            code = 203
        else :
            # AuthFail
            output = {"result": False, "msg": "Invalid Login"}
            code = 401

    # Return HttpResponse
    return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=code)