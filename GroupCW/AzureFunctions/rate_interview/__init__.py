import logging
import json
import uuid
from azure.functions import HttpRequest, HttpResponse
from shared_code import DBFunctions
import AzureData


def main(req: HttpRequest) -> HttpResponse:
    logging.info('rate_interview function processing a request.')

    try:
        req_body = req.get_json()
        interview_id = req_body.get('id')
        username = req_body.get('username')
        rating = req_body.get('rating')

        # Validate the rating
        if rating < 1 or rating > 5 or not isinstance(rating, int):
            return HttpResponse(json.dumps({"result": False, "msg": "Rating must be a whole number between 1 and 5"}), status_code=400, mimetype="application/json")

        interview_data_query = "SELECT * FROM c WHERE c.id = @id"

        # Define the parameters
        parameters = [
            {"name": "@id", "value": interview_id}
        ]

        # Use DBFunctions to query the data
        interview_data_list = DBFunctions.query_items(
            query=interview_data_query,
            parameters=parameters,
            container=AzureData.containerInterviewData
        )

        # Retrieve the first item from the query results, if any
        interview_data = interview_data_list[0] if interview_data_list else None


        if not interview_data:
            return HttpResponse(json.dumps({"result": False, "msg": "Interview data not found for the provided ID"}), status_code=400, mimetype="application/json")

        # Check if user has already rated
        ratings = interview_data.get('ratings', [])
        existing_rating = next((r for r in ratings if r['username'] == username), None)
        if existing_rating:
            existing_rating['rating'] = rating
        else:
            ratings.append({"username": username, "rating": rating})

        interview_data['ratings'] = ratings

        # Update the interview data in the database
        AzureData.containerInterviewData.upsert_item(interview_data)
        return HttpResponse(json.dumps({"result": True, "msg": "Rating added successfully", "ratings": interview_data["ratings"]}), status_code=200, mimetype="application/json")

    except ValueError:
        return HttpResponse(json.dumps({"result": False, "msg": "Invalid request body"}), status_code=400, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return HttpResponse(json.dumps({"result": False, "msg": f"Failed to rate interview: {str(e)}"}), status_code=500, mimetype="application/json")
