# System Imports
# Azure Imports
from azure.functions import HttpRequest, HttpResponse
import azure.cognitiveservices.speech as speechsdk
from scipy.io import wavfile
import time
import AzureData.AzureData as azureData
import logging
import requests

#need to properly implement all available audio files and return appropiate error messages
def main(req: HttpRequest) -> HttpResponse:
    
    speech_config = speechsdk.SpeechConfig(subscription=azureData.speech_key, region=azureData.region)
    
    channels = 1
    bits_per_sample = 16
    samples_per_second = 16000

    # Create audio configuration using the push stream
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
    #transcriber.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    #transcriber.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    #transcriber.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous transcription on either session stopped or canceled events
    #transcriber.session_stopped.connect(stop_cb)
    #transcriber.canceled.connect(stop_cb)
    #transcriber.start_transcribing_async()




    # Read the whole wave files at once and stream it to sdk
    _, wav_data = wavfile.read("./test.wav")
    stream.write(wav_data.tobytes())
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
        
    request = requests.post(azureData.translationPath, params=azureData.params, headers=azureData.headers, json=jsonText)
    response = request.json()
    


if __name__ == '__main__': 
    main('test')