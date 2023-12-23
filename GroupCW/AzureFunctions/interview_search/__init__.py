import AzureData as AzureData
from azure.functions import HttpRequest, HttpResponse
import json

def main(req: HttpRequest) -> HttpResponse:
    
    '''
    #Need to do this for searching
    JsonInput = req.get_json()
    '''
    allInterviews = list(AzureData.containerInterviewData.query_items(query="SELECT * from interviewData", enable_cross_partition_query=True))
    print(allInterviews)
    return HttpResponse(body=json.dumps(allInterviews),mimetype="application/json")
    
if __name__ == '__main__': 
    main('test')