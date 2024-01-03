# System Imports
import logging
import json
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
# Code base Imports
from shared_code import DBFunctions, FaultCheckers
import AzureData

def main(req: HttpRequest) -> HttpResponse:
    username = 'user1' # TODO: Get username from JWT
    interviewId = req.route_params.get('id')
    
    result = DBFunctions.query_items(
        query="SELECT * FROM interviewData WHERE interviewData.questionId = @id",
        parameters=[{"name": "@id", "value": str(interviewId)}],
        container=AzureData.containerInterviewData
    )

    # Filter non private interviews
    result = list(filter(lambda x: x.get("private") == False or x.get("username") == username, result))
    # Delete interviewBlobURL key from each interview
    result = list(map(lambda x: {k: v for k, v in x.items() if k != "interviewBlobURL" and not k.startswith('_')}, result))
    
    for item in result:
        total_ratings = sum(r['rating'] for r in item)
        average_rating = round(total_ratings / len(item['rating']), 1)
        item['average_rating'] = average_rating

    return HttpResponse(body=json.dumps(result), mimetype='application/json', status_code=200)
