# System Imports
import logging
import json
import secrets
import random
import string
import uuid
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
from azure.communication.email import EmailClient
from azure.identity import DefaultAzureCredential
# Code base imports
from shared_code import PasswordFunctions, DBFunctions, FaultCheckers
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

    # Create random password
    randomPassword = generateRandomPassword()

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
    sendEmail(userInfo, randomPassword, ref)

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

    return result[0]

def generateRandomPassword():

    length = random.randint(12,20)

    password = ""
    for i in range(length):
        password += secrets.choice(string.ascii_letters+string.digits)

    return password

def sendEmail(userInfo, randomPassword, ref):

    client = EmailClient(AzureData.emailEndpoint, AzureData.emailCredential)    

    text = "Tempoary Password: {}".format(randomPassword)

    message = {
        "senderAddress": AzureData.emailDomainName,
        "recipients": {
            "to": [
                {
                    "address": userInfo.get("email"),
                    "displayName": userInfo.get("username")
                }
            ]
        },
        "content": {
            "subject": "Password Reset, Reference:{}".format(ref),
            "plainText": text
        }
    }

    #poller = EmailClient.begin_send(client, message)
    poller = client.begin_send(message)
    return poller.result()