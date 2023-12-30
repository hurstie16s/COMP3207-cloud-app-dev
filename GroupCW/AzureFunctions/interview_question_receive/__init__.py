# System Imports
import logging
import json
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
# Code base Imports
from shared_code import DBFunctions
import AzureData

def main(req: HttpRequest) -> HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    #Get data from JSON doc
    input = req.get_json()
    id = input.get("id")
    if id is None:
       output, code = getQuestionByID(id)
    else:
        output, code = getAllQuestions()

    # Return HttpResponse
    return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=code)

def getQuestionByID(id: str) -> (dict,int):
    
    # Get all interview questions
    # Add checks
    query = "SELECT * FROM InterviewQuestions WHERE InterviewQuestions.id = @id"
    params = [{"name": "@id", "value": id}]
    questionsResult = DBFunctions.query_items(
        query=query,
        parameters=params,
        container=AzureData.containerInterviewQuestions
    )

    questionFull = questionsResult[0]

    question = {
        "question" : questionFull.get("interviewQuestion"),
        "difficulty": questionFull.get("difficulty"),
        "regularity": questionFull.get("regularity"),
        "id": questionFull.get("id")
    }

    output = {"questions": [question]}

    return output, 200

def getAllQuestions() -> (dict,int):
    
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
            "regularity": question.get("regularity"),
            "id": question.get("id")
        }
        questions.append(questionDict)

    output = {"questions": questions}

    return output, 200