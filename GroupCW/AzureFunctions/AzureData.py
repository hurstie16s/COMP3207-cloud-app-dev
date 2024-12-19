import logging

from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import CosmosClient 
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.communication.email import EmailClient
from azure.core.credentials import AzureKeyCredential
import json
import os
import uuid


URL = os.environ.get('URL', 'your_url_here')
KEY = os.environ.get('KEY', 'your_key_here')
DATABASE = 'InterviewDB'
CONTAINER_InterviewQuestions = 'InterviewQuestions'
CONTAINER_Users = 'Users'
CONTAINER_InterviewData = 'InterviewData'


client = CosmosClient(URL, credential=KEY)

#To access these variables import AzureData and then write AzureData.(name of variable)
#CosmosDB Containers
database = client.get_database_client(DATABASE)

containerInterviewQuestions = database.get_container_client(CONTAINER_InterviewQuestions)

global containerUsers
containerUsers = database.get_container_client(CONTAINER_Users)
containerInterviewData = database.get_container_client(CONTAINER_InterviewData)


#DataStorage (blop) container
# Replace these values with your actual account details
account_name = os.environ.get('account_name')
account_key = os.environ.get('account_key')
connection_string = os.environ.get('connection_string')
container_name = os.environ.get('container_name')

# Create a BlobServiceClient
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

# Create a ContainerClient
blob_container = blob_service_client.get_container_client(container_name)


#Extra services

#Speech
speech_url = os.environ.get('speech_url')
speech_key= os.environ.get('speech_key')
speechPath = speech_url + speech_key

#translation
translation_url = os.environ.get('translation_url')
translation_key = os.environ.get('translation_key')
path = '/translate'
translationPath = translation_url + path



#service region
region = "uksouth"

#extra data for translation
supportedLanguages = ['en', 'cy', 'ga', 'fr', 'pl', 'es', 'zh-Hans']

translation_params = {
    'api-version': '3.0',
    'to': supportedLanguages
}

translation_headers = {
    'Ocp-Apim-Subscription-Key': translation_key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': region,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

global JWT_SIGNING_KEY
JWT_SIGNING_KEY = os.environ.get("jwt_key")

# Email Stuff
emailEndpoint = os.environ.get("email_endpoint")
emailCredential = AzureKeyCredential(os.environ.get("email_credential"))
emailConnectionString = ""
emailDomainName = os.environ.get("email_domain_name")
emailClient = EmailClient(emailEndpoint, emailCredential)
