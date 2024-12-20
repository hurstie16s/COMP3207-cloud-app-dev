import logging

from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import CosmosClient 
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json
import os
import uuid


URL = 'https://interviewsystem-cosmosdb.documents.azure.com:443'
KEY = 'BXNLFntJdiwBLmWL25zDXmj6NINyLt88BHkbENeSL4Yf04pXMKsFphnubDNjHojUmvl4t6WZ5sOZACDb2GSpzA=='
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
account_name = "interviewstorage"
account_key = "5KoTFTeA+9Y4rTAhL3Xc21NlwmLjkjXC1dE2pUfG4JXAfJ9iFxMcntHN70XMqAXyuXtBZVnAqgn7+AStmQ1SIQ=="
connection_string = "DefaultEndpointsProtocol=https;AccountName=interviewstorage;AccountKey=5KoTFTeA+9Y4rTAhL3Xc21NlwmLjkjXC1dE2pUfG4JXAfJ9iFxMcntHN70XMqAXyuXtBZVnAqgn7+AStmQ1SIQ==;EndpointSuffix=core.windows.net"
container_name = "interview-blop"

# Create a BlobServiceClient
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

# Create a ContainerClient
blob_container = blob_service_client.get_container_client(container_name)


#Extra services

#Speech
speech_url = 'https://uksouth.api.cognitive.microsoft.com/'
speech_key= '1c275238685a4c0da6063fc8b65652da'
speechPath = speech_url + speech_key

#translation
translation_url = 'https://api.cognitive.microsofttranslator.com/'
translation_key = 'c350c6f6ba1345c0a24699cdf8a22338'
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

JWT_SIGNING_KEY = "2GKiZVZoOJsPvPIKxeClIEO0gCrG4gQ5"

# TODO: return functions
