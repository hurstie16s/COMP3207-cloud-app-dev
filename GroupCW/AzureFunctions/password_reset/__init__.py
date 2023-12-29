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
#Code base imports
from shared_code import PasswordFunctions, DBFunctions, FaultCheckers
import AzureData

# TODO: Check how requests should come in and how they should be sent out

def main(req: HttpRequest) -> HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    # Get data from JSON doc
    input = req.get_json()
    username = input.get("username")

    userInfo = getUserData(username)

    # Create random password
    randomPassword = generateRandomPassword()

    # Hash random password
    randomPasswordHash = PasswordFunctions.hash_password(randomPassword)

    # Update User info
    newDict = {
        "password": randomPasswordHash,
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





def getUserData(username: str):
    # Get User Data
    query = "SELECT * FROM User WHERE User.username = @username"
    params = [{"name": "@username", "value": username}]
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

    # To use Azure Active Directory Authentication (DefaultAzureCredential) make sure to have AZURE_TENANT_ID, AZURE_CLIENT_ID and AZURE_CLIENT_SECRET as env variables.
    endpoint = "https://<resource-name>.communication.azure.com"
    client = EmailClient(endpoint, DefaultAzureCredential())

    text = """
Hello {}

Here your temporary password: {}
Login in with it and follow instructions
""".format(userInfo.get("username"), randomPassword)

    message = {
        "content": {
            "subject": "Password Rest, Reference:{}".format(ref),
            "plaintext": text
        },
        "recepients": {
            "to": [
                {
                    "address": userInfo.get("email"),
                    "displayName": userInfo.get("username")
                }
            ]
        },
        "senderAddress": "sender@sending.send"
    }

    poller = client.begin_send(message)
    return poller.result()