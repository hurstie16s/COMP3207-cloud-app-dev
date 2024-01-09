import AzureData as AzureData
from azure.functions import HttpRequest, HttpResponse
import json
import logging
from shared_code import auth
from jwt.exceptions import InvalidTokenError

def main(req: HttpRequest) -> HttpResponse:
    try:
        selfUsername = auth.verifyJwt(req.headers.get('Authorization'))
    except InvalidTokenError:
        return HttpResponse(body=json.dumps({"result": False, "msg": "Invalid token"}), mimetype='application/json', status_code=401)

    try:
        body = req.get_json()
        username = body.get('username')
        interviewQuestion = body.get('interviewQuestion')

        if username is not None and username == "":
            username = None

        if interviewQuestion is not None and interviewQuestion == "":
            interviewQuestion = None

        query = ""
        parameters = []
        if interviewQuestion is None and username is None:
            query = "SELECT * from c"
        elif interviewQuestion is None:
            query = "SELECT * from c where c.username = @username"
            parameters=[
                {"name": "@username", "value": username}
            ]
        elif username is None:
            query = "SELECT * from c where c.interviewQuestion = @interviewQuestion"
            parameters=[
                {"name": "@interviewQuestion", "value": interviewQuestion}
            ]
        else:
            query = "SELECT * from c where c.interviewQuestion = @interviewQuestion AND c.username = @username"
            parameters=[
                {"name": "@username", "value": username},
                {"name": "@interviewQuestion", "value": interviewQuestion}
            ]

        logging.info("query to be passed: " + query)

        allInterviews = list(AzureData.containerInterviewData.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))
        allInterviews = list(filter(lambda x: x.get("private") == False or x.get("username") == selfUsername, allInterviews))
        return HttpResponse(body=json.dumps(allInterviews),mimetype="application/json")
    except Exception as e:
        logging.warning(e)
    
if __name__ == '__main__': 
    main('test')