# System Imports
import logging
import json
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
# Code base Imports
from shared_code import DBFunctions, auth
import AzureData
from jwt.exceptions import InvalidTokenError

def main(req: HttpRequest) -> HttpResponse:
    interviewId = req.route_params.get('id')
    
    result = DBFunctions.query_items(
        query="SELECT * FROM interviewData WHERE interviewData.questionId = @id",
        parameters=[{"name": "@id", "value": str(interviewId)}],
        container=AzureData.containerInterviewData
    )

    # Filter non private interviews
    try:
        username = auth.verifyJwt(req.headers.get('Authorization'))
    except InvalidTokenError:
        return HttpResponse(body=json.dumps({"result": False, "msg": "Invalid token"}), mimetype='application/json', status_code=401)

    result = list(filter(lambda x: x.get("private") == False or x.get("username") == username, result))
    # Delete interviewBlobURL key from each interview
    result = list(map(lambda x: {k: v for k, v in x.items() if k != "interviewBlobURL" and not k.startswith('_')}, result))
    
    return HttpResponse(body=json.dumps(result), mimetype='application/json', status_code=200)
