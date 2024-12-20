# System Imports
import logging
import json
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
# Code base Imports
from shared_code import DBFunctions, auth
from jwt.exceptions import InvalidTokenError
import AzureData

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        username = auth.verifyJwt(req.headers.get('Authorization'))
    except InvalidTokenError:
        return HttpResponse(body=json.dumps({"msg": "Invalid token"}), mimetype='application/json', status_code=401)

    #Get data from JSON doc
    id = req.params.get('id')
    if id is None or id == "":
        output, code = getAllQuestions(username)
    else:
        output, code = getQuestionByID(id, username)

    # Return HttpResponse
    return HttpResponse(body=json.dumps(output),mimetype='application/json',status_code=code)

def getQuestionByID(id: str, username: str) -> (dict,int):    
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
    
    countResult = DBFunctions.query_items(
        query="SELECT VALUE COUNT(1) FROM c WHERE c.questionId = @id AND (c.private = false OR c.username = @username)",
        parameters=[
            {"name": "@id", "value": str(id)},
            {"name": "@username", "value": username}
        ],
        container=AzureData.containerInterviewData
    )

    responseCount = 0
    if len(countResult) > 0:
        responseCount = countResult[0]

    question = {
        "id": questionFull.get("id"),
        "question" : questionFull.get("interviewQuestion"),
        "difficulty": questionFull.get("difficulty"),
        "regularity": questionFull.get("regularity"),
        "numberOfResponses": responseCount,
        "tips": questionFull.get("tips")
    }

    output = {"msg": "Questions collected", "question": question}

    return output, 200

def getAllQuestions(username: str) -> (dict,int):
    # Get all interview questions
    query = "SELECT * FROM InterviewQuestions"
    questionsResult = DBFunctions.query_items(
        query=query,
        container=AzureData.containerInterviewQuestions
    )

    # Fetch response counts - Python CosmosDB SDK does not support GROUP BY with COUNT so we must aggregate manually
    responses = DBFunctions.query_items(
        query="SELECT * from c",
        container=AzureData.containerInterviewData
    )

    responseCounts = {}
    for response in responses:
        questionId = response.get("questionId")
        if response.get("private") == True and response.get("username") != username:
            continue

        responseCounts[questionId] = responseCounts.get(questionId, 0) + 1

    questions=[]
    for question in questionsResult :
        questionDict = {
            "id" : question.get("id"),
            "question" : question.get("interviewQuestion"),
            "difficulty": question.get("difficulty"),
            "regularity": question.get("regularity"),
            "numberOfResponses": responseCounts.get(question.get("id")) or 0
        }
        questions.append(questionDict)

    output = {"msg": "All questions collected", "questions": questions}

    return output, 200