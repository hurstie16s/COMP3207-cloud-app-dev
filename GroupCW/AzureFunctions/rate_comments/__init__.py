import logging
import json
import AzureData
from shared_code import DBFunctions
from azure.functions import HttpRequest, HttpResponse


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request to rate a comment.')

    try:
        req_body = req.get_json()
        comment_id = req_body.get('comment_id')
        username = req_body.get('username')  
        rate_action = req_body.get('rate_action')  # 'like' for thumbs up, 'dislike' for thumbs down

        # Define the query with a parameter placeholder
        interview_data_query = "SELECT * FROM c WHERE ARRAY_CONTAINS(c.comments, {'id': @commentId}, true)"

        # Define the parameters
        parameters = [
            {"name": "@commentId", "value": comment_id}
        ]

        # Use DBFunctions to query the data
        interview_data_list = DBFunctions.query_items(
            query=interview_data_query,
            parameters=parameters,
            container=AzureData.containerInterviewData
        )

        if not interview_data_list:
            return HttpResponse(json.dumps({"result": False, "msg": "No interview data found"}), status_code=400, mimetype="application/json")

        interview_data = interview_data_list[0]
        comments_list = interview_data.get('comments', [])

        comment_to_rate = next((comment for comment in comments_list if comment['id'] == comment_id), None)
        if not comment_to_rate:
            return HttpResponse(json.dumps({"result": False, "msg": "Comment not found"}), status_code=400, mimetype="application/json")


        # Initialize lists if they don't exist
        comment_to_rate.setdefault('thumbs_up', [])
        comment_to_rate.setdefault('thumbs_down', [])

        # Handle rating logic
        if rate_action == 'like':
            if username in comment_to_rate['thumbs_up']:
                comment_to_rate['thumbs_up'].remove(username)
            else:
                if username in comment_to_rate['thumbs_down']:
                    comment_to_rate['thumbs_down'].remove(username)
                comment_to_rate['thumbs_up'].append(username)
        elif rate_action == 'dislike':
            if username in comment_to_rate['thumbs_down']:
                comment_to_rate['thumbs_down'].remove(username)
            else:
                if username in comment_to_rate['thumbs_up']:
                    comment_to_rate['thumbs_up'].remove(username)
                comment_to_rate['thumbs_down'].append(username)
        else:
            return HttpResponse(json.dumps({"result": False, "msg": "Invalid rate action"}), status_code=400, mimetype="application/json")

        # Update the comment in the list
        for i, comment in enumerate(comments_list):
            if comment['id'] == comment_id:
                comments_list[i] = comment_to_rate
                break

        DBFunctions.upsert_item(data=interview_data, container=AzureData.containerInterviewData)

        return HttpResponse(json.dumps({"result": True, "msg": "Comment rated successfully", "comment": comment_to_rate}), status_code=200, mimetype="application/json")
    
    except ValueError:
        return HttpResponse(json.dumps({"result": False, "msg": "Invalid request body"}), status_code=400, mimetype="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"result": False, "msg": f"Error processing request: {str(e)}"}), status_code=500, mimetype="application/json")