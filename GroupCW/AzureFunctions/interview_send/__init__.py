# System Imports
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
import azure.cognitiveservices.speech as speechsdk
from scipy.io import wavfile
import time
import requests
import json
import AzureData as AzureData
import os
import uuid
from moviepy.editor import VideoFileClip
import logging

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
    
    #Json inputs from body
    username = req.form.get("username") #input("what is your username? : ") req.params.get('username')
    industry = req.form.get("industry")
    interviewTitle = req.form.get("interviewTitle") #input("what do you want your prompt to be? : ") req.params.get('text')
    interviewQuestion = req.form.get("interviewQuestion") #input("what do you want your prompt to be? : ") req.params.get('text')
    private = req.form.get("private")
    webmFile = req.files["webmFile"]
    video_clip = None
    #setting up the file names
    webm_file_name =  username + str(uuid.uuid4()) + ".webm"
    wav_file_name = username + str(uuid.uuid4()) + ".wav"
    try:        
        try:
            webmFile.save(webm_file_name)
            video_clip = VideoFileClip(webm_file_name)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(wav_file_name, codec='pcm_s16le', ffmpeg_params=['-ar', '16000'])
        except:
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
            speech_recognizer.stop_continuous_recognition
            
            with open(webm_file_name, "rb") as data:
                bob_client = AzureData.blob_container.upload_blob(name=webm_file_name, data=data)
            
            transcription = ""
            for text in transcriptions:
                transcription += text
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
            raise ExceptionWithTranslation
        
        #Json data to store to cosmosDB
        jsonBody = {
                "username": username,
                "industry": industry,
                "interviewTitle": interviewTitle,
                "interviewQuestion": interviewQuestion,
                "interviewBlopURL": bob_client.url,
                "interviewLanguage": response['detectedLanguage']["language"],
                "trasncript": response['translations'],
                "comments": [],
                "rating": [],
                "flags": [],
                "private": private
            }
        try:
            AzureData.containerInterviewData.create_item(jsonBody, enable_automatic_id_generation=True)
        except:
            raise ExceptionWithStoringToCosmosDB
            
        #cleanup
        if video_clip:
            video_clip.close()
            if(os.path.exists(webm_file_name)): os.remove(webm_file_name)
            if(os.path.exists(wav_file_name)): os.remove(wav_file_name)
        
        return HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json")
            
        
    except Exception as e:
        
        #Check if files exists and delete them
        if video_clip:
            video_clip.close()
            if(os.path.exists(webm_file_name)): os.remove(webm_file_name)
            if(os.path.exists(wav_file_name)): os.remove(wav_file_name)
            blob_file = AzureData.blob_service_client.get_blob_client(container=AzureData.container_name, blob=webm_file_name)
            blob_exists = blob_file.exists()
            if(blob_exists): blob_file.delete_blob()
        
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
            return HttpResponse(body=json.dumps({"result": False , "msg" : "Unknown error, please try again."}),mimetype="application/json")       
            
class ExceptionWithStoringToCosmosDB(Exception):
    pass

class ExceptionWithTranslation(Exception):
    pass

class ExceptionWithCreatingFiles(Exception):
    pass

class ExceptionWithTranscription(Exception):
    pass