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

    input = req.get_json()
    question = input.get("question")
    difficulty = input.get("difficulty")
    regularity = input.get("regularity")

    # Check question is unique
    if checkQuestion(question):
        output = {"result": False, "msg": "Question already exists"}
        code = 403
    else:
        # Insert question into db
        data = {
            "interviewQuestion": question,
            "difficulty": difficulty,
            "regularity": regularity
        }
        DBFunctions.create_item(
            data=data,
            container=AzureData.containerInterviewQuestions
        )
        output = {"result": True, "msg": "Question submitted"}
        code = 201

    # Return HttpResponse
    return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=code)

def checkQuestion(question: str) -> bool:

    query = "SELECT * FROM InterviewQuestions WHERE InterviewQuestions.interviewQuestion = @question"
    params = [{"name": "@question", "value": question}]

    result = DBFunctions.query_items(
        query=query,
        parameters=params,
        container=AzureData.containerInterviewQuestions
    )

    return len(result) == 0
