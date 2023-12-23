import logging
import json
from AzureData import AzureData
from azure.functions import HttpRequest, HttpResponse


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request to rate a comment.')

    try:
        # Extracting data from the request
        req_body = req.get_json()
        comment_id = req_body.get('comment_id')
        rate_action = req_body.get('rate_action')  # 'like' for thumbs up, 'dislike' for thumbs down

        # Retrieve the comment data
        comment_item = AzureData.containerInterviewData.read_item(item=comment_id, partition_key=comment_id)
        
        if rate_action == 'like':
            comment_item['thumbs_up'] += 1
        elif rate_action == 'dislike':
            comment_item['thumbs_down'] += 1
        else:
            return HttpResponse("Invalid rate action", status_code=400)

        # Update the comment item in the database
        AzureData.containerInterviewData.replace_item(item=comment_id, body=comment_item)

        return HttpResponse("Comment rated successfully", status_code=200)

    except ValueError:
        return HttpResponse("Invalid request body", status_code=400)
    except Exception as e:
        return HttpResponse(f"Error processing request: {str(e)}", status_code=500)
