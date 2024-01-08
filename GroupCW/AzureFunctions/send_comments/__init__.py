import datetime
import logging
import json
import uuid
from azure.functions import HttpRequest, HttpResponse
from shared_code import DBFunctions, auth
import AzureData
from jwt.exceptions import InvalidTokenError

def main(req: HttpRequest) -> HttpResponse:
    logging.info('send_comment function processing a request.')

    try:
        username = auth.verifyJwt(req.headers.get('Authorization'))
    except InvalidTokenError:
        return HttpResponse(body=json.dumps({"result": False, "msg": "Invalid token"}), mimetype='application/json', status_code=401)

    try:
        # Extract data from the received JSON
        req_body = req.get_json()
        interview_id = req_body.get('id')
        comment_text = req_body.get('comment')

        query = "SELECT * FROM c WHERE c.id = @id"
        parameters = [{"name": "@id", "value": interview_id}]
        items = DBFunctions.query_items(query, parameters, AzureData.containerInterviewData)

        if not items:
            return HttpResponse(json.dumps({"result": False, "msg": "Interview data not found for the provided ID"}), status_code=400, mimetype="application/json")

        interview_data = items[0]
    
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
        DBFunctions.upsert_item(interview_data, AzureData.containerInterviewData)
        return HttpResponse(json.dumps({"result": True, "msg": "Comment added successfully", "data": comment_data}), status_code=200, mimetype="application/json")

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return HttpResponse(json.dumps({"result": False, "msg": f"Failed to add comment: {str(e)}"}), status_code=500, mimetype="application/json")