from fastapi import APIRouter, Form
from fastapi.responses import FileResponse,StreamingResponse
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI
from pathlib import Path
from typing import Generator
from config import settings

router = APIRouter()

@router.post("/t2s", response_class=StreamingResponse)
async def t2s(text: str = Form(...)):
    
    
    client = AzureOpenAI(
    azure_endpoint=settings.AZURE_OAI_TTS_ENDPOINT,
    api_key=settings.AZURE_OAI_TTS_KEY,
    api_version="2024-02-15-preview"
    )

    # with open('answer.txt', 'r') as file:
    #     result_text = file.read()
    #     #file.close()
        
    """
    Galata Sarayı Humayun Mektebi adıyla da bilinen bu kurum, enderuna (saray mektebi) üst düzeyde eğitimli görevli yetiştirirdi. O yıllarda enderun, Osmanlı sarayında padişahın günlük yaşamını geçirdiği, sarayın eğitim birimlerinin, kütüphanenin, hazine odasının yer aldığı büyük bahçe içine kurulu bir kompleksti."""

    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
    model="tts-tan", 
    voice="alloy",
    input=text,
    )

    # play_source = TextSource(text=result_text, voice_name="en-US-AlloyMultiLingualNeural")
    # call_automation_client.get_call_connection(1).play_media_to_all(play_source,operation_context="context")
    
    def audio_stream() -> Generator[bytes, None, None]:
        for chunk in response.iter_bytes():
            yield chunk
            #oynatmayı deneyebilirsin.

    return StreamingResponse(audio_stream(), media_type="audio/mp3")

    # response.stream_to_file("output.mp3")
    # return FileResponse("output.mp3", media_type='audio/mp3', filename="output.mp3")
    # load_dotenv()
    
    # speech_key = os.getenv("AZURE_T2S_SPEECH_KEY")
    # service_region = os.getenv("AZURE_SPEECH_REGION")

    # speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # speech_config.speech_synthesis_voice_name = "en-US-AlloyMultilingualNeural"
    
    # audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
    # speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    # result = speech_synthesizer.speak_text_async(text).get()
    
    # if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    #     return FileResponse("output.wav", media_type='audio/wav', filename="output.wav")
    # elif result.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = result.cancellation_details
    #     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         print("Error details: {}".format(cancellation_details.error_details))
    #     return {"error": "Speech synthesis failed"}