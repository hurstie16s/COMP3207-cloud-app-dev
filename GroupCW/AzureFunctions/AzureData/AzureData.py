import logging

from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import CosmosClient 

import json
import os

URL = 'https://interviewsystem-cosmosdb.documents.azure.com:443'
KEY = 'BXNLFntJdiwBLmWL25zDXmj6NINyLt88BHkbENeSL4Yf04pXMKsFphnubDNjHojUmvl4t6WZ5sOZACDb2GSpzA=='
DATABASE = 'InterviewDB'
CONTAINER_InterviewQuestions = 'InterviewQuestions'
CONTAINER_Users = 'Users'
CONTAINER_Interviews = 'Interviews'
CONTAINER_InterviewData = 'InterviewData'

client = CosmosClient(URL, credential=KEY)

#To access these variables import AzureData and then write AzureData.(name of variable)

global database 
database = client.get_database_client(DATABASE)

global containerInterviewQuestions
containerInterviewQuestions = database.get_container_client(CONTAINER_InterviewQuestions)

global containerUsers
containerUsers = database.get_container_client(CONTAINER_Users)

global containerInterviews
containerInterviews = database.get_container_client(CONTAINER_Interviews)

global containerInterviewData
containerInterviewData = database.get_container_client(CONTAINER_InterviewData)


# TODO: return functions
