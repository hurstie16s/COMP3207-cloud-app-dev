import datetime
import logging
import json
import uuid
from azure.functions import HttpRequest, HttpResponse
from shared_code import DBFunctions, auth
from jwt.exceptions import InvalidTokenError
import AzureData 

def main(req: HttpRequest) -> HttpResponse:
    try:
      responseId = req.route_params.get('responseId')
      
      query = "SELECT * FROM c WHERE c.id = @id"
      parameters = [{"name": "@id", "value": responseId}]
      items = DBFunctions.query_items(query, parameters, AzureData.containerInterviewData)

      if not items:
        return HttpResponse(json.dumps({"result": False, "msg": "Interview not found"}), status_code=404, mimetype="application/json")

      interview = items[0]

      try:
        username = auth.verifyJwt(req.headers.get('Authorization'))
      except InvalidTokenError:
        return HttpResponse(body=json.dumps({"result": False, "msg": "Invalid token"}), mimetype='application/json', status_code=401)
    
      if interview["username"] != username:
        return HttpResponse(json.dumps({"result": False, "msg": "You don't have permission to delete this interview"}), status_code=403, mimetype="application/json")

      # Delete audio file
      try:
        fileName = interview['audioUuid'] + ".webm"
        containerClient = AzureData.blob_service_client.get_container_client(AzureData.container_name)
        containerClient.delete_blob(blob=fileName)
      except Exception as e:
        logging.error(f"Failed to delete audio file (perhaps it never existed?): {str(e)}")

      DBFunctions.delete_item(responseId, AzureData.containerInterviewData)
      return HttpResponse(json.dumps({"result": True}), status_code=200, mimetype="application/json")
    except Exception as e:
      return HttpResponse(json.dumps({"result": False, "msg": f"Failed to get interview id: {str(e)}"}), status_code=500, mimetype="application/json")