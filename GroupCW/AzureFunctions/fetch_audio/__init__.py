import logging
import json
from azure.functions import HttpRequest, HttpResponse
from shared_code import DBFunctions, auth
from jwt.exceptions import InvalidTokenError
import AzureData

def main(req: HttpRequest) -> HttpResponse:
    try:
      username = auth.verifyJwt(req.headers.get('Authorization'))
    except InvalidTokenError:
      return HttpResponse(body=json.dumps({"result": False, "msg": "Invalid token"}), mimetype='application/json', status_code=401)

    try:
      responseId = req.route_params.get('responseId')
      
      query = "SELECT * FROM c WHERE c.id = @id"
      parameters = [{"name": "@id", "value": responseId}]
      items = DBFunctions.query_items(query, parameters, AzureData.containerInterviewData)

      if not items:
        return HttpResponse(json.dumps({"result": False, "msg": "Interview not found"}), status_code=400, mimetype="application/json")

      interview = items[0]

      if interview.private and interview.username != username:
        return HttpResponse(json.dumps({"result": False, "msg": "You don't have permission to view this interview"}), status_code=403, mimetype="application/json")

      fileName = interview['audioUuid'] + ".webm"
      logging.info("container: " + AzureData.container_name)
      blobClient = AzureData.blob_service_client.get_blob_client(container=AzureData.container_name, blob=fileName)
      downloader = blobClient.download_blob(max_concurrency=1)
      audioBytes = downloader.readall()

      return HttpResponse(body=audioBytes, mimetype="audio/webm", status_code=200)
    except Exception as e:
      return HttpResponse(json.dumps({"result": False, "msg": f"Failed to get interview id: {str(e)}"}), status_code=500, mimetype="application/json")