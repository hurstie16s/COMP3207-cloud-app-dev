# System Imports
import logging
import json
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
# Code base Imports
import AzureData
from azure.storage.blob import BlobServiceClient
import urllib.parse


# Function to get the webmfile from the blob and return it
def main(req: HttpRequest) -> HttpResponse:

    logging.info('Function to get webmfile')

    # Retrieve JSON data from the request body
    req_body = req.get_json()
    
    # Extract the blob URL from the JSON data
    blob_url = req_body.get('interviewBlopURL')

    if not blob_url:
        return HttpResponse("Invalid request. Please provide interviewBlopURL parameter.", status_code=400)

    try:
         # Parse the blob URL to get blob name and container name
        parsed_url = urllib.parse.urlparse(blob_url)
        storage_name = parsed_url.netloc.split('.')[0]
        print(storage_name)
        
        blob_name = parsed_url.path.strip('/')
        print("Blob name and file name:", blob_name)

        blob_part = blob_name.split("/")[0]
        print("Blob part:", blob_part)

        if storage_name != "interviewstorage":
            return HttpResponse("Wrong storage name", status_code=400)

        file_name = blob_name.split('/')[-1]

        # Get the blob client 
        blob_client = AzureData.blob_container.get_blob_client(file_name)

        # Download the blob content 
        blob_content = blob_client.download_blob().readall()

        # Return the blob content as the response with the correct mimetype
        return HttpResponse(blob_content, status_code=200, mimetype="video/webm")

    except Exception as e:
        logging.error(f"Error retrieving webm file: {str(e)}")
        return HttpResponse("Internal Server Error", status_code=500)