# System Imports
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
import azure.cognitiveservices.speech as speechsdk
from scipy.io import wavfile
import time
import AzureData.AzureData as azureData
import logging
import requests
import json
import AzureData as AzureData
from pydub import AudioSegment
import io

#need to properly implement all available audio files and return appropiate error messages
def main(req: HttpRequest) -> HttpResponse:
         
    #'''
    # JsonInput
    jsonInput = req.get_json()
    
    username = jsonInput["username"] #input("what is your username? : ") req.params.get('username')
    interviewTitle = jsonInput["interviewTitle"] #input("what do you want your prompt to be? : ") req.params.get('text')
    interviewQuestion = jsonInput["interviewQuestion"] #input("what do you want your prompt to be? : ") req.params.get('text')
    audioFile = jsonInput["audioFile"]
    private = jsonInput["private"]
    #'''
    
    '''
    #python input
    username = input("what is your username? : ")
    interviewTitle = input("what is the interview title? : ")
    interviewQuestion = input("what is your interview question? : ")
    privateChoice = input("should this be private? : yes or no?")
    private = False
    if(privateChoice == "yes"): private = True
    elif (privateChoice == "no"): private = False
    else: private = True 
    '''
    
    #Audio Data
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
        print('TRANSCRIBED: {}'.format(evt))
        result_text = evt.result.text
        transcriptions.append(result_text)

    # Subscribe to the events fired by the conversation transcriber
    transcriber.transcribed.connect(transcribed_cb)
    transcriber.session_stopped.connect(stop_cb)
    transcriber.canceled.connect(stop_cb)
    
    webm_bytes_io = io.BytesIO(audioFile)

    # Load the WebM data using pydub
    audio = AudioSegment.from_file(webm_bytes_io, format="webm")

    # Export the audio to bytes
    audio_bytes = audio.raw_data
    
    
    transcriber.start_transcribing_async()
   
    stream.write(audio_bytes)
    stream.close()
    while not done:
        time.sleep(.5)

    transcriber.stop_transcribing_async()
    
    
    transcriptText = ''
    for transcription in transcriptions:
        transcriptText += transcription
    
    
    
    jsonText = [{
            'text': transcriptText
    }]
    request = requests.post(AzureData.translationPath, params=AzureData.translation_params, headers=AzureData.translation_headers, json=jsonText)
    response = request.json()[0]
    
    if(response['detectedLanguage']["score"] < 0.3):
        return HttpResponse(body=json.dumps({"result": False , "msg" : "Error with language translation, translation not reliable enough."}),mimetype="application/json")
    
    
    jsonBody = json.dumps(
        {
            "username": username,
            "private": private,
            "interviewTitle": interviewTitle,
            "interviewQuestion": interviewQuestion,
            "interviewBlop": "",
            "interviewLanguage": response['detectedLanguage']["language"],
            "trasncript": response['translations'],
            "comments": [],
            "rating": 0,
            "flags": [],
        })
    try:
        AzureData.containerInterviewData.create_item(jsonBody, enable_automatic_id_generation=True)
        return HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json")
    except Exception as e:
        return HttpResponse(body=json.dumps({"result": False , "msg" : "Error with submitting data to container"}),mimetype="application/json")
  

if __name__ == '__main__': 
    main('test')