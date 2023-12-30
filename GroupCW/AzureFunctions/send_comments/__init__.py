import datetime
import logging
import json
import uuid
from azure.functions import HttpRequest, HttpResponse
import AzureData 

def main(req: HttpRequest) -> HttpResponse:
    logging.info('send_comment function processing a request.')

    try:
        # Extract data from the received JSON
        req_body = req.get_json()
        interview_id = req_body.get('id')
        username = req_body.get('username')
        comment_text = req_body.get('comment')

        # Querying the database for the specific interview data
        interview_data = None
        for item in AzureData.containerInterviewData.query_items(
            query="SELECT * FROM c WHERE c.id = @id",
            parameters=[{"name": "@id", "value": interview_id}],
            enable_cross_partition_query=True):
            interview_data = item
            break

        if not interview_data:
            return HttpResponse(json.dumps({"result": False, "msg": "Interview data not found for the provided ID"}), status_code=400, mimetype="application/json")

        # Append the new comment to the 'comments' list
        comment_data = {
            "id": str(uuid.uuid4()),
            "username": username,
            "comment": comment_text,
            "timestamp": datetime.datetime.now().isoformat(),
            "thumbs_up": [],
            "thumbs_down": []
        }
        interview_data['comments'].append(comment_data)

        # Update the interview data in the database
        AzureData.containerInterviewData.upsert_item(interview_data)
        return HttpResponse(json.dumps({"result": True, "msg": "Comment added successfully"}), status_code=200, mimetype="application/json")

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return HttpResponse(json.dumps({"result": False, "msg": f"Failed to add comment: {str(e)}"}), status_code=500, mimetype="application/json")