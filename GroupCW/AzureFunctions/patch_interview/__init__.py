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

      body = req.get_json()
      
      query = "SELECT * FROM c WHERE c.id = @id"
      parameters = [{"name": "@id", "value": responseId}]
      items = DBFunctions.query_items(query, parameters, AzureData.containerInterviewData)

      if not items:
        return HttpResponse(json.dumps({"result": False, "msg": "Interview not found"}), status_code=400, mimetype="application/json")

      interview = items[0]

      # TODO: Get username from JWT and compare to username in interview data

      if 'private' in body:
        private = body.get('private')
        if not isinstance(private, bool):
          return HttpResponse(json.dumps({"result": False, "msg": "Field 'private' must be a boolean"}), status_code=400, mimetype="application/json")
        
        interview['private'] = private

      DBFunctions.upsert_item(interview, AzureData.containerInterviewData)
      return HttpResponse(json.dumps({"result": True, "data": interview}), status_code=200, mimetype="application/json")
    except Exception as e:
      return HttpResponse(json.dumps({"result": False, "msg": f"Failed to get interview id: {str(e)}"}), status_code=500, mimetype="application/json")