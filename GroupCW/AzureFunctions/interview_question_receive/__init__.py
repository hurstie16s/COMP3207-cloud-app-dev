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
    id = req.params.get('id')
    if id is None or id == "":
        output, code = getAllQuestions()
    else:
        output, code = getQuestionByID(id)

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

    if len(questionsResult) == 0:
        return {"msg": "Question not found"}, 404

    questionFull = questionsResult[0]

    question = {
        "id": questionFull.get("id"),
        "question" : questionFull.get("interviewQuestion"),
        "difficulty": questionFull.get("difficulty"),
        "regularity": questionFull.get("regularity"),
        "numberOfResponses": questionFull.get("numberOfResponses")
    }

    output = {"msg": "Questions collected", "question": question}

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
            "id" : question.get("id"),
            "question" : question.get("interviewQuestion"),
            "difficulty": question.get("difficulty"),
            "regularity": question.get("regularity"),
            "numberOfResponses": question.get("numberOfResponses")
        }
        questions.append(questionDict)

    output = {"msg": "All questions collected", "questions": questions}

    return output, 200