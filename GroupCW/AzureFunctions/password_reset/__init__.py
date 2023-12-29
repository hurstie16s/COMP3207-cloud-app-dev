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
    
    logging.info('Python HTTP trigger function processed a request.')

    # Get data from JSON doc
    input = req.get_json()
    username = input.get("username")

    userInfo = getUserData(username)




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