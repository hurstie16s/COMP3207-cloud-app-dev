import AzureData as AzureData
from azure.functions import HttpRequest, HttpResponse
import json

def main(req: HttpRequest) -> HttpResponse:
    
    
    JsonInput = req.get_json()
    industry = JsonInput['industry']
    query = ""
    if(industry == all): 
        query += "where interviewData.industry = " + industry
    allInterviews = list(AzureData.containerInterviewData.query_items(query="SELECT * from interviewData " + query, enable_cross_partition_query=True))
    print(allInterviews)
    return HttpResponse(body=json.dumps(allInterviews),mimetype="application/json")
    
if __name__ == '__main__': 
    main('test')