# System Imports
# Azure Imports
import logging
from azure.functions import HttpRequest, HttpResponse
import azure.cognitiveservices.speech as speechsdk
from scipy.io import wavfile
import time
import requests
import json
import AzureData as AzureData
import os
import uuid
from moviepy.video.io import ffmpeg_tools
from chatGPTReview.__init__ import send_interview_to_ai
import datetime
import tempfile
from shared_code import DBFunctions, auth
from jwt.exceptions import InvalidTokenError
import ast

translation_params = {
    'api-version': '3.0',
    'to': AzureData.supportedLanguages
}

translation_headers = {
    'Ocp-Apim-Subscription-Key': AzureData.translation_key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': AzureData.region,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

#need to properly implement all available audio files and return appropiate error messages
def main(req: HttpRequest) -> HttpResponse:
    interviewId = req.route_params.get('id')

    # Fetch interview question data 
    questionsResult = DBFunctions.query_items(
        query="SELECT * FROM InterviewQuestions WHERE InterviewQuestions.id = @id",
        parameters=[{"name": "@id", "value": interviewId}],
        container=AzureData.containerInterviewQuestions
    )

    if len(questionsResult) == 0:
        return HttpResponse(body=json.dumps({"result": False, "msg" : "Question not found"}), mimetype="application/json", status_code=404)

    question = questionsResult[0]
    logging.info(json.dumps(question))

    #Json inputs from body
    try:
        username = auth.verifyJwt(req.headers.get('Authorization'))
    except InvalidTokenError:
        return HttpResponse(body=json.dumps({"result": False, "msg": "Invalid token"}), mimetype='application/json', status_code=401)
    
    #Json inputs from body
    industry = req.form.get("industry")
    interviewTitle = req.form.get("interviewTitle") #input("what do you want your prompt to be? : ") req.params.get('text')
    private = req.form.get("private") == "true" # Form data is always a string, so convert to bool
    webmFile = req.files["webmFile"]
    #setting up the file names
    temp_dir = tempfile.TemporaryDirectory()
    audioUuid = str(uuid.uuid4())
    webm_file_name = temp_dir.name + os.sep + username + audioUuid + ".webm"
    wav_file_name = temp_dir.name + os.sep + username + audioUuid + ".wav"

    try:        
        try:
            webmFile.save(webm_file_name)
            ffmpeg_tools.ffmpeg_extract_audio(webm_file_name, wav_file_name)
        except Exception as e:
            logging.exception("Error converting WebM to WAV: " + str(e), exc_info=True)
            raise ExceptionWithCreatingFiles
        
        try:
           
            #Azure Speech SDK
            speech_config = speechsdk.SpeechConfig(subscription=AzureData.speech_key, region=AzureData.region)
            
            audio_config = speechsdk.audio.AudioConfig(filename=wav_file_name)

            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

            done = False
            transcriptions = []
        
            def stop_cb(evt: speechsdk.SessionEventArgs):
                """callback that signals to stop continuous transcription upon receiving an event `evt`"""
                print('CLOSING {}'.format(evt))
                nonlocal done
                done = True
                
            def transcribed_cb(evt: speechsdk.ConnectionEventArgs):
                """Callback for handling transcribed events"""
                result_text = evt.result.text
                logging.info(evt.result.reason)
                logging.info(result_text)
                nonlocal transcriptions
                transcriptions.append(result_text)

            # Subscribe to the events fired by the conversation transcriber
            speech_recognizer.recognized.connect(transcribed_cb)
            speech_recognizer.session_stopped.connect(stop_cb)
            speech_recognizer.canceled.connect(stop_cb)
            
            timeSpent = 0
            speech_recognizer.start_continuous_recognition()
            #infinite loop that may need fixing
            while not done:
                logging.info("Done:" + str(done))
                time.sleep(.5)
                timeSpent += 0.5
                if(timeSpent > 300): raise
            speech_recognizer.stop_continuous_recognition()
            
            transcription = ""
            for text in transcriptions:
                transcription += text
            
            if transcription == "":
                logging.warn("Transcription was empty")    
                
            with open(webm_file_name, "rb") as data:
                bob_client = AzureData.blob_container.upload_blob(name=f"{audioUuid}.webm", data=data)       
        except:
            raise

        # ChatGPT Part
        # Call function with question + transcript as parameters
        # Store the return value (interview feedback)
        try:
            output_feedback = send_interview_to_ai(question['interviewQuestion'], transcription)
            if(output_feedback == ""): raise
            tips = output_feedback.split('\n')
            if(len(tips) == 3):
                del tips[1]
            tips[0] = ast.literal_eval(tips[0][len("Good Points: "):].strip())
            tips[1] = ast.literal_eval(tips[1][len("Improvement Points: "):].strip())
            # Extract the lists using ast.literal_eval
            
            
            
            # Need to sort out language part
            language = 'en'
        except:
            raise


        #Translation
        try:
            jsonText = [{
                'text': transcription
            }]
            
            request = requests.post(AzureData.translationPath, params=translation_params, headers=translation_headers, json=jsonText)
            response = request.json()[0]
        except:
            logging.exception("Error performing translation: " + str(e), exc_info=True)
            raise ExceptionWithTranslation
        
        #Json data to store to cosmosDB
        jsonBody = {
                "username": username,
                "industry": industry,
                "questionId": question['id'],
                "interviewTitle": interviewTitle,
                "interviewQuestion": question['interviewQuestion'],
                "interviewBlobURL": bob_client.url,
                "audioUuid": audioUuid,
                "interviewLanguage": response['detectedLanguage']["language"],
                "transcript": response['translations'],
                "comments": [],
                "ratings": [],
                "tips":  
                    {
                        "language": language,
                        "goodPoints": tips[0],
                        "improvementPoints": tips[1]
                    }
                ,
                "private": private,
                "timestamp": datetime.datetime.now().isoformat()
            }
        try:
            AzureData.containerInterviewData.create_item(jsonBody, enable_automatic_id_generation=True)
        except:
            logging.exception("Error storing interview data in CosmosDB: " + str(e), exc_info=True)
            raise ExceptionWithStoringToCosmosDB
        
        return HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json")
    except Exception as e:        
        #Check if files exists and delete them
        blob_file = AzureData.blob_service_client.get_blob_client(container=AzureData.container_name, blob=webm_file_name)
        if(blob_file.exists()): blob_file.delete_blob()
        
        #custom error messages
        if isinstance(e, ExceptionWithStoringToCosmosDB):
            print(f"Caught a Storing To CosmosDB exception: {e}")
            return HttpResponse(body=json.dumps({"result": False , "msg" : "Error with submitting data to CosmosDB, please try again."}),mimetype="application/json")
        elif isinstance(e, ExceptionWithTranslation):
            return HttpResponse(body=json.dumps({"result": False , "msg" : "Error with translating the transcription, please try again."}),mimetype="application/json")
        elif isinstance(e, ExceptionWithTranslation):
            return HttpResponse(body=json.dumps({"result": False , "msg" : "Error with creation of files, please try again."}),mimetype="application/json")
        elif isinstance(e, ExceptionWithTranscription):
            return HttpResponse(body=json.dumps({"result": False , "msg" : "Error with the creation of transcription, please try again."}),mimetype="application/json")
        else:
            return HttpResponse(body=json.dumps({"result": False , "msg" : "Unknown error: " + str(e)}),mimetype="application/json")       
    finally:
        try: # Remove WebM file if it exists
            os.remove(webm_file_name)
        except OSError:
            pass

        try: # Remove WAV file if it exists
            os.remove(wav_file_name)
        except OSError:
            pass

        try: # Remove temp directory
            temp_dir.cleanup()
        except:
            pass


class ExceptionWithStoringToCosmosDB(Exception):
    pass

class ExceptionWithTranslation(Exception):
    pass

class ExceptionWithCreatingFiles(Exception):
    pass

class ExceptionWithTranscription(Exception):
    pass