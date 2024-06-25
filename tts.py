from pathlib import Path
from openai import AzureOpenAI,OpenAI
from dotenv import load_dotenv
import os
import torch
import numpy as np
import io
from pydub import AudioSegment
from azure.communication.callautomation import TextSource,CallAutomationClient
#



def tts_test():
    client = AzureOpenAI(
    azure_endpoint="https://whisper-test-tan-oai.openai.azure.com/",
    api_key="31d522a434104fad8ecf983d54da4fa7",
    api_version="2024-02-15-preview"
    )

    with open('answer.txt', 'r') as file:
        result_text = file.read()
        #file.close()
        
    
    """
    Galata Sarayı Humayun Mektebi adıyla da bilinen bu kurum, enderuna (saray mektebi) üst düzeyde eğitimli görevli yetiştirirdi. O yıllarda enderun, Osmanlı sarayında padişahın günlük yaşamını geçirdiği, sarayın eğitim birimlerinin, kütüphanenin, hazine odasının yer aldığı büyük bahçe içine kurulu bir kompleksti."""

    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
    model="tts-tan", 
    voice="alloy",
    input=result_text,
    )

    # play_source = TextSource(text=result_text, voice_name="en-US-AlloyMultiLingualNeural")
    # call_automation_client.get_call_connection(1).play_media_to_all(play_source,operation_context="context")

    response.stream_to_file("output.mp3")
    
    

    
    
tts_test()