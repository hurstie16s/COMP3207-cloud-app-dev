# System Imports
import logging
import json
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
# Code base Imports
from shared_code import DBFunctions, FaultCheckers
import AzureData
from chatGPTReview.__init__ import send_question_to_ai

def main(req: HttpRequest) -> HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    input = req.get_json()
    question = input.get("question")
    difficulty = input.get("difficulty")
    regularity = input.get("regularity")

    if FaultCheckers.checkParams([question, difficulty, regularity]):
        output = {"result": False, "msg": "Submission Failure"}
        output = 400
    # Check question is unique
    elif not checkQuestion(question):
        output = {"result": False, "msg": "Question already exists"}
        code = 403
    else:
        try: 
            output_feedback = send_question_to_ai(question)
            tips = output_feedback.replace('\n', '')
            if(tips[0] != '[' or tips[len(tips) - 1] != ']'):
                raise
        except Exception as e:
            logging.warning("Issue with ChatGPT service. " + e)
            output = {"result": False, "msg": "Error with ChatGPT Service."}
            
        # Insert question into db
        data = {
            "interviewQuestion": question,
            "difficulty": difficulty,
            "regularity": regularity,
            "tips": tips,
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
