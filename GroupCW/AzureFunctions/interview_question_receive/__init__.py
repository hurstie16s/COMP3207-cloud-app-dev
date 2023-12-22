# System Imports
import logging
import json
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
# Code base Imports
from shared_code import DBFunctions
from AzureData import AzureData

def main(req: HttpRequest) -> HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    # Get all interview questions
    # Add checks
    query = "SELECT * FROM InterviewQuestions"
    questionsResult = DBFunctions.query_items(
        query=query,
        container=AzureData.containerInterviewQuestions
    )

    questions=[]
    for question in questionsResult :
        questionDict = {
            "question" : question.get("interviewQuestion"),
            "difficulty": question.get("difficulty"),
            "regularity": question.get("regularity")
        }
        questions.append(questionDict)

    output = {"questions": questions}

    # Return HttpResponse
    return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=200)