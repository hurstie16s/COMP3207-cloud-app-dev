import AzureData as AzureData
from azure.functions import HttpRequest, HttpResponse
import json
import logging

def main(req: HttpRequest) -> HttpResponse:
    
    try:
        JsonInput = req.get_json()
        username = JsonInput.get('username')
        interviewQuestion = JsonInput.get('interviewQuestion')
        searchByVariables = ""
        if(interviewQuestion != ""): 
            searchByVariables += "where interviewData.interviewQuestion = " + "'" + interviewQuestion + "'"
        
        if(username != ""):
            if(searchByVariables == ""):
                searchByVariables += "where interviewData.username = " + "'" + username + "'"
            else:
                searchByVariables += " AND interviewData.username = " + "'" + username + "'"
        
        query = "SELECT * from interviewData " + searchByVariables
        logging.info("query to be passed: " + query)
        allInterviews = list(AzureData.containerInterviewData.query_items(query=query, enable_cross_partition_query=True))
        return HttpResponse(body=json.dumps(allInterviews),mimetype="application/json")
    except Exception as e:
        logging.warning(e)
    
if __name__ == '__main__': 
    main('test')