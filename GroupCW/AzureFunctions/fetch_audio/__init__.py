import logging
import json
from azure.functions import HttpRequest, HttpResponse
from shared_code import DBFunctions
import AzureData

def main(req: HttpRequest) -> HttpResponse:
    try:
      responseId = req.route_params.get('responseId')
      logging.info("responseId: " + responseId)
      
      query = "SELECT * FROM c WHERE c.id = @id"
      parameters = [{"name": "@id", "value": responseId}]
      items = DBFunctions.query_items(query, parameters, AzureData.containerInterviewData)

      logging.info(json.dumps(items))

      if not items:
        return HttpResponse(json.dumps({"result": False, "msg": "Interview not found"}), status_code=400, mimetype="application/json")

      interview = items[0]

      # TODO: Get username from JWT and compare to username in interview data and check if the interview is private

      fileName = interview['audioUuid'] + ".webm"
      logging.info("container: " + AzureData.container_name)
      blobClient = AzureData.blob_service_client.get_blob_client(container=AzureData.container_name, blob=fileName)
      downloader = blobClient.download_blob(max_concurrency=1)
      audioBytes = downloader.readall()

      return HttpResponse(body=audioBytes, mimetype="audio/webm", status_code=200)
    except Exception as e:
      return HttpResponse(json.dumps({"result": False, "msg": f"Failed to get interview id: {str(e)}"}), status_code=500, mimetype="application/json")