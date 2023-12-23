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
         
    #'''
    # JsonInput
    username = req.form.get("username") #input("what is your username? : ") req.params.get('username')
    interviewTitle = req.form.get("interviewTitle") #input("what do you want your prompt to be? : ") req.params.get('text')
    interviewQuestion = req.form.get("interviewQuestion") #input("what do you want your prompt to be? : ") req.params.get('text')
    private = req.form.get("private")
    webmFile = req.files["webmFile"]
    #'''

    file_path = os.path.join(os.getcwd(), webmFile.filename)
    webmFile.save(file_path)
    
    logging.info(file_path)
    logging.info(webmFile.name)
    
    webm_file_name = "test.webm"
    wav_file_name = "output.wav"
    
    video_clip = VideoFileClip(webm_file_name)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(wav_file_name, codec='pcm_s16le', ffmpeg_params=['-ar', '16000'])
    
    channels = 1
    bits_per_sample = 16
    samples_per_second = 16000

    #Azure Speech SDK
    speech_config = speechsdk.SpeechConfig(subscription=AzureData.speech_key, region=AzureData.region)
    wave_format = speechsdk.audio.AudioStreamFormat(samples_per_second, bits_per_sample, channels)
    stream = speechsdk.audio.PushAudioInputStream(stream_format=wave_format)
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    transcriber = speechsdk.transcription.ConversationTranscriber(speech_config, audio_config)
    
    error = False
    done = False
    transcription = ''
    
    def stop_cb(evt: speechsdk.SessionEventArgs):
            """callback that signals to stop continuous transcription upon receiving an event `evt`"""
            print('CLOSING {}'.format(evt))
            nonlocal error
            nonlocal done
            if(not done):
                error = True
                done = True
            
    def transcribed_cb(evt: speechsdk.ConnectionEventArgs):
        """Callback for handling transcribed events"""
        print('TRANSCRIBED: {}'.format(evt))
        result_text = evt.result.text
        nonlocal transcription
        transcription = result_text
        nonlocal done
        done = True

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
        if(error and not done):
            return HttpResponse(body=json.dumps({"result": False , "msg" : "Error while creating transcription"}),mimetype="application/json")
    transcriber.stop_transcribing_async()
    
    with open(file_path, "rb") as data:
        bob_client = container_client.upload_blob(name=webmFile.filename, data=data)
    
    jsonText = [{
            'text': transcription
    }]
    request = requests.post(AzureData.translationPath, params=translation_params, headers=translation_headers, json=jsonText)
    response = request.json()[0]
    
    jsonBody = {
            "username": username,
            "private": private,
            "interviewTitle": interviewTitle,
            "interviewQuestion": interviewQuestion,
            "interviewBlopURL": bob_client.url,
            "interviewLanguage": response['detectedLanguage']["language"],
            "trasncript": response['translations'],
            "comments": [],
            "rating": 0,
            "flags": [],
        }
    try:
        AzureData.containerInterviewData.create_item(jsonBody, enable_automatic_id_generation=True)
        return HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json")
    except Exception as e:
        logging.error(e)
        return HttpResponse(body=json.dumps({"result": False , "msg" : "Error with submitting data to container"}),mimetype="application/json")
  
if __name__ == '__main__': 
    main('test')
    
class BinaryFileReaderCallback(speechsdk.audio.PullAudioInputStreamCallback):
        def __init__(self, filename: str):
            super().__init__()
            self._file_h = open(filename, "rb")

        def read(self, buffer: memoryview) -> int:
            try:
                size = buffer.nbytes
                frames = self._file_h.read(size)

                buffer[:len(frames)] = frames

                return len(frames)
            except Exception as ex:
                print('Exception in `read`: {}'.format(ex))
                raise

        def close(self) -> None:
            print('closing file')
            try:
                self._file_h.close()
            except Exception as ex:
                print('Exception in `close`: {}'.format(ex))
                raise