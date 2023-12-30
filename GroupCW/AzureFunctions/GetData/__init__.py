import logging
import json
from azure.functions import HttpRequest, HttpResponse
import AzureData 

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Function processing a request to retrieve all interview data.')

    try:
        all_interview_data = list(AzureData.containerInterviewData.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True))

        if not all_interview_data:
            return HttpResponse("No interview data found", status_code=404)

        return HttpResponse(json.dumps(all_interview_data), status_code=200, mimetype="application/json")

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return HttpResponse(f"Failed to retrieve data: {str(e)}", status_code=500)
