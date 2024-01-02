import AzureData as AzureData
from azure.functions import HttpRequest, HttpResponse
import json

def main(req: HttpRequest) -> HttpResponse:
    
    
    JsonInput = req.get_json()
    username = JsonInput['username']
    interviewQuestion = JsonInput['interviewQuestion']
    query = ""
    if(interviewQuestion != ""): 
        query += "where interviewData.interviewQuestion = " + interviewQuestion
    
    if(username != ""):
        if(query == ""):
            query += "where interviewData.username = " + username
        else:
            query += " AND interviewData.username = " + username
    
    allInterviews = list(AzureData.containerInterviewData.query_items(query="SELECT * from interviewData " + query, enable_cross_partition_query=True))
    return HttpResponse(body=json.dumps(allInterviews),mimetype="application/json")
    
if __name__ == '__main__': 
    main('test')