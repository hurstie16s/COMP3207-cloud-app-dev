# System Imports
import logging
# Azure Imports
from azure.functions import HttpRequest, HttpResponse # TODO: sort issue with import
#Code base imports

def main(req: HttpRequest) -> HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    #Get data from JSON doc
    input = req.get_json()
    username = input.get("username")
    password = input.get("password")

    # Check username exists, grab hashed password based off username
    