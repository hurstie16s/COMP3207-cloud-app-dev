# System Imports
import logging
import json
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
# Code base Imports
from AzureData import AzureData
from shared_code import DBFunctions

def main(req: HttpRequest) -> HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    input = req.get_json()
    question = input.get("question")

    # Check question is unique
    if checkQuestion(question):
        output = {"result": False, "msg": "Question already exists"}
    else:
        # Insert question into db
        data = {"interviewQuestion": question}
        DBFunctions.create_item(
            data=data,
            container=AzureData.containerInterviewQuestions
        )
        output = {"result": True, "msg": "Question submitted"}

    # Return HttpResponse
    return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=200)

def checkQuestion(question: str) -> bool:

    query = "SELECT * FROM InterviewQuestions WHERE InterviewQuestions.interviewQuestion = @question"
    params = [{"name": "@question", "value": question}]

    result = DBFunctions.query_items(
        query=query,
        parameters=params,
        container=AzureData.containerInterviewQuestions
    )

    return len(result) == 0