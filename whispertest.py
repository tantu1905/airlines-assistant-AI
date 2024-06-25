import os
from openai import AzureOpenAI
import whisper


def whisper_test():
    client = AzureOpenAI(
        api_key="f4737d4288374dff9443ef94464e5ee9",
        api_version="2024-02-01",
        azure_endpoint = "https://new-speech-oai-tan.openai.azure.com/"
    )
    # model = whisper.load_model("base")
    # audio = whisper.load_audio("microphone-results.mp3")
    # audio = whisper.pad_or_trim(audio, 16000)
    # mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # _, probs = model.detect_language(mel)
    # print(probs)
    
    
    
    deployment_id = "test-tan-whisper" #This will correspond to the custom name you chose for your deployment when you deployed a model."
    audio_test_file = "./microphone-results.mp3"

    result = client.audio.transcriptions.create(
        file=open(audio_test_file, "rb"),            
        model=deployment_id,
        temperature=0,
        #language="en",
        #response_format="verbose_json"
        
        
    )
    
    with open('transcript.txt', 'w') as file:
        file.write(result.text)
        file.close()
    print(result.text)
    #return result.text
    
#main()