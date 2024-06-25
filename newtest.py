from pathlib import Path
from openai import AzureOpenAI
from dotenv import load_dotenv
import speech_recognition as sr
import os
import torch
import numpy as np
import io
from pydub import AudioSegment
#from .whispertest import main

def record_audio_test():

    r = sr.Recognizer()
    #m = sr.Microphone()
    #r.pause_threshold = 2
    
    # r.dynamic_energy_threshold = False
    # r.energy_threshold = 500
    #r.non_speaking_duration = 1


    #r.dynamic_energy_threshold = True


    #r.operation_timeout = 2

    with sr.Microphone() as source:
        print("Speak Anything :")
        r.adjust_for_ambient_noise(source,duration=1)
        print (r.energy_threshold)
        print("Done")
        
        #r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=5,phrase_time_limit=5)

        #torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int32).flatten().astype(np.float64) / 32768.0)
        audio.frame_data = audio.get_raw_data()
        #r.adjust_for_ambient_noise(source,duration=2)
        # while True:
        print (r.energy_threshold)
        #print (audio)
        #r.listen_in_background(source, , phrase_time_limit=2)
        

        with open("microphone-results.mp3", "wb") as f:
                f.write(audio.get_wav_data())
            
#main()
    # try:
    #     print("Duyduğum:", r.recognize_google(audio))
    # except sr.UnknownValueError:
    #     print("Anlayamadım")
    # except sr.RequestError as e:
    #     print("Servis hatası; {0}".format(e))
        
    

    

        


# def main():
#     client = AzureOpenAI(
#     azure_endpoint=os.getenv("AZURE_OAI_ENDPOINT"),
#     api_key=os.getenv("AZURE_OAI_KEY"),
#     api_version="2024-02-15-preview"
#     )

#     with open('answerWhisper.txt', 'r') as file:
#         result_text = file.read()
#         #file.close()
        
    
#     """
#     Galata Sarayı Humayun Mektebi adıyla da bilinen bu kurum, enderuna (saray mektebi) üst düzeyde eğitimli görevli yetiştirirdi. O yıllarda enderun, Osmanlı sarayında padişahın günlük yaşamını geçirdiği, sarayın eğitim birimlerinin, kütüphanenin, hazine odasının yer aldığı büyük bahçe içine kurulu bir kompleksti."""

#     speech_file_path = Path(__file__).parent / "speech.mp3"
#     response = client.audio.speech.create(
#     model="deployment_model_ismi TTS", 
#     voice="fable",
#     input=result_text
#     )

#     response.write_to_file(speech_file_path)