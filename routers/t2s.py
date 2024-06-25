from fastapi import APIRouter, Form
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk

router = APIRouter()

@router.post("/t2s", response_class=FileResponse)
async def t2s(text: str = Form(...)):
    load_dotenv()
    
    speech_key = os.getenv("AZURE_T2S_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = "en-US-AlloyMultilingualNeural"
    
    audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    result = speech_synthesizer.speak_text_async(text).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return FileResponse("output.wav", media_type='audio/wav', filename="output.wav")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return {"error": "Speech synthesis failed"}