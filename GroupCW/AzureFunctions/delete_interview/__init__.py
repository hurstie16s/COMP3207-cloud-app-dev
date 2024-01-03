import datetime
import logging
import json
import uuid
from azure.functions import HttpRequest, HttpResponse
from shared_code import DBFunctions
import AzureData 

def main(req: HttpRequest) -> HttpResponse:
    try:
      responseId = req.route_params.get('responseId')
      
      query = "SELECT * FROM c WHERE c.id = @id"
      parameters = [{"name": "@id", "value": responseId}]
      items = DBFunctions.query_items(query, parameters, AzureData.containerInterviewData)

      if not items:
        return HttpResponse(json.dumps({"result": False, "msg": "Interview not found"}), status_code=400, mimetype="application/json")

      interview = items[0]

      # TODO: Get username from JWT and compare to username in interview data

      DBFunctions.delete_item(responseId, AzureData.containerInterviewData)
      return HttpResponse(json.dumps({"result": True}), status_code=200, mimetype="application/json")
    except Exception as e:
      return HttpResponse(json.dumps({"result": False, "msg": f"Failed to get interview id: {str(e)}"}), status_code=500, mimetype="application/json")