import logging
import json
import AzureData

from azure.functions import HttpRequest, HttpResponse


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request to rate a comment.')

    try:
        req_body = req.get_json()
        comment_id = req_body.get('comment_id')
        username = req_body.get('username')  
        rate_action = req_body.get('rate_action')  # 'like' for thumbs up, 'dislike' for thumbs down

        # Retrieve the interview data that contains the comment
        interview_data_query = f"SELECT * FROM c WHERE ARRAY_CONTAINS(c.comments, {{'id': '{comment_id}'}}, true)"
        interview_data_list = list(AzureData.containerInterviewData.query_items(
            query=interview_data_query,
            enable_cross_partition_query=True
        ))

        if not interview_data_list:
            return HttpResponse("No interview data found for the provided comment ID", status_code=404)

        interview_data = interview_data_list[0]  
        comments_list = interview_data.get('comments', [])

        comment_to_rate = next((comment for comment in comments_list if comment['id'] == comment_id), None)
        if not comment_to_rate:
            return HttpResponse("Comment not found", status_code=404)


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
            return HttpResponse("Invalid rate action", status_code=400)

        # Update the comment in the list
        for i, comment in enumerate(comments_list):
            if comment['id'] == comment_id:
                comments_list[i] = comment_to_rate
                break

        AzureData.containerInterviewData.replace_item(item=interview_data['id'], body=interview_data)

        return HttpResponse("Comment rated successfully", status_code=200)

    except ValueError:
        return HttpResponse("Invalid request body", status_code=400)
    except Exception as e:
        return HttpResponse(f"Error processing request: {str(e)}", status_code=500)
