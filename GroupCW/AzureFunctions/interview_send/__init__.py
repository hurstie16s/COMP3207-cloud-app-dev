# System Imports
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
import azure.cognitiveservices.speech as speechsdk
from scipy.io import wavfile
import time
import logging
import requests
import json
import AzureData as AzureData
import os
import uuid
import subprocess
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import ffmpeg
from moviepy.editor import VideoFileClip


# Replace these values with your actual account details
account_name = "interviewstorage"
account_key = "5KoTFTeA+9Y4rTAhL3Xc21NlwmLjkjXC1dE2pUfG4JXAfJ9iFxMcntHN70XMqAXyuXtBZVnAqgn7+AStmQ1SIQ=="
connection_string = "DefaultEndpointsProtocol=https;AccountName=interviewstorage;AccountKey=5KoTFTeA+9Y4rTAhL3Xc21NlwmLjkjXC1dE2pUfG4JXAfJ9iFxMcntHN70XMqAXyuXtBZVnAqgn7+AStmQ1SIQ==;EndpointSuffix=core.windows.net"
container_name = "interview-blop"

# Create a BlobServiceClient
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

# Create a ContainerClient
container_client = blob_service_client.get_container_client(container_name)

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
    
    #setting up the file names
    webm_file_name = username + str(uuid.uuid4()) + ".webm"
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
            channels = 1
            bits_per_sample = 16
            samples_per_second = 16000

            #Azure Speech SDK
            speech_config = speechsdk.SpeechConfig(subscription=AzureData.speech_key, region=AzureData.region)
            wave_format = speechsdk.audio.AudioStreamFormat(samples_per_second, bits_per_sample, channels)
            stream = speechsdk.audio.PushAudioInputStream(stream_format=wave_format)
            audio_config = speechsdk.audio.AudioConfig(stream=stream)
            transcriber = speechsdk.transcription.ConversationTranscriber(speech_config, audio_config)
        

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
                print("HELLO")
                print(evt.result.reason)
                #if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    #print("Recognized: {}".format(evt.text))
                #elif evt.result.reason == speechsdk.ResultReason.NoMatch:
                # print("No speech could be recognized: {}".format(evt.no_match_details))
                nonlocal transcriptions
                transcriptions.append(result_text)

            # Subscribe to the events fired by the conversation transcriber
            transcriber.transcribed.connect(transcribed_cb)
            transcriber.session_stopped.connect(stop_cb)
            transcriber.canceled.connect(stop_cb)
            
            
            
            transcriber.start_transcribing_async()
            _, wav_data = wavfile.read(wav_file_name)
            stream.write(wav_data.tobytes())
            stream.close()
            while not done:
                time.sleep(.5)
            transcriber.stop_transcribing_async()
            
            with open(webm_file_name, "rb") as data:
                bob_client = container_client.upload_blob(name=webm_file_name, data=data)
            
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
            blob_client = container_client.get_blob_client(webm_file_name)
            blob_exists = blob_client.exists()
            if(blob_exists): container_client.delete_blob(name=webm_file_name)
        
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