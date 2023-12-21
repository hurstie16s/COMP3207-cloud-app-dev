# System Imports
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
import azure.cognitiveservices.speech as speechsdk
from scipy.io import wavfile
from azure.cosmos import CosmosClient 
import time
import logging
import requests
import uuid
import json

URL = 'https://interviewsystem-cosmosdb.documents.azure.com:443'
KEY = 'BXNLFntJdiwBLmWL25zDXmj6NINyLt88BHkbENeSL4Yf04pXMKsFphnubDNjHojUmvl4t6WZ5sOZACDb2GSpzA=='
DATABASE = 'InterviewDB'
CONTAINER_InterviewData = 'InterviewData'

client = CosmosClient(URL, credential=KEY)

database = client.get_database_client(DATABASE)

containerInterviewData = database.get_container_client(CONTAINER_InterviewData)

translation_url = 'https://api.cognitive.microsofttranslator.com/'
translation_key = 'c350c6f6ba1345c0a24699cdf8a22338'
path = '/translate'
translationPath = translation_url + path

supportedLanguages = ['en', 'cy', 'ga', 'fr', 'pl']

params = {
    'api-version': '3.0',
    'to': supportedLanguages
}

headers = {
    'Ocp-Apim-Subscription-Key': translation_key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': "uksouth",
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}


#need to properly implement all available audio files and return appropiate error messages
def main(req: HttpRequest) -> HttpResponse:
         
    '''
    # JsonInput
    jsonInput = req.get_json()
    
    username = jsonInput["username"] #input("what is your username? : ") req.params.get('username')
    interviewTitle = jsonInput["interviewTitle"] #input("what do you want your prompt to be? : ") req.params.get('text')
    interviewQuestion = jsonInput["interviewQuestion"] #input("what do you want your prompt to be? : ") req.params.get('text')
    private = jsonInput["private"]
    '''
    
    #'''
    #python input
    username = input("what is your username? : ")
    interviewTitle = input("what is the interview title? : ")
    interviewQuestion = input("what is your interview question? : ")
    privateChoice = input("should this be private? : yes or no?")
    private = False
    if(privateChoice == "yes"): private = True
    elif (privateChoice == "no"): private = False
    else: private = True 
    #'''
    
    #Audio Data
    channels = 1
    bits_per_sample = 16
    samples_per_second = 16000

    #Azure Speech SDK
    speech_config = speechsdk.SpeechConfig(subscription='1c275238685a4c0da6063fc8b65652da', region="uksouth")
    wave_format = speechsdk.audio.AudioStreamFormat(samples_per_second, bits_per_sample, channels)
    stream = speechsdk.audio.PushAudioInputStream(stream_format=wave_format)
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    transcriber = speechsdk.transcription.ConversationTranscriber(speech_config, audio_config)
    
    #Transcription 
    done = False
    error = False
    transcription = ''
    transcription_result = None
    
    def stop_cb(evt: speechsdk.SessionEventArgs):
            """callback that signals to stop continuous transcription upon receiving an event `evt`"""
            print('CLOSING {}'.format(evt))
            nonlocal done
            if(not done):
                nonlocal error
                error = True
               
            
    def transcribed_cb(evt: speechsdk.ConnectionEventArgs):
        """Callback for handling transcribed events"""
        print('TRANSCRIBED: {}'.format(evt))
        nonlocal transcription_result
        transcription_result = evt.result.reason
        nonlocal transcription
        transcription = evt.result.text
        nonlocal done
        done = True
        

    # Subscribe to the events fired by the conversation transcriber
    transcriber.transcribed.connect(transcribed_cb)
    transcriber.session_stopped.connect(stop_cb)
    transcriber.canceled.connect(stop_cb)
    
    
    
    transcriber.start_transcribing_async()
    wave_sps, wav_data = wavfile.read("./test.wav")
    print(wav_data)
    stream.write(wav_data.tobytes())
    stream.close()
    while not done:
        time.sleep(.5)
        if(error and not done):
         return HttpResponse(body=json.dumps({"result": False , "msg" : "Error with creating transcription"}),mimetype="application/json")
    transcriber.stop_transcribing_async()
    
    if transcription_result in [speechsdk.ResultReason.NoMatch, speechsdk.ResultReason.Canceled]:
        return HttpResponse(body=json.dumps({"result": False , "msg" : "Error while creating transcription, try again or submit a clearer audio file."}),mimetype="application/json")
    
    #translation
    jsonText = [{
            'text': transcription
    }]
    request = requests.post(translationPath, params=params, headers=headers, json=jsonText)
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
        containerInterviewData.create_item(jsonBody, enable_automatic_id_generation=True)
        return HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json")
    except Exception as e:
        return HttpResponse(body=json.dumps({"result": False , "msg" : "Error with submitting data to container"}),mimetype="application/json")
  

if __name__ == '__main__': 
    main('test')
    
    