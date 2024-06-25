import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os, time
from .openaitest import start_openai
import asyncio,threading,concurrent

all_text = ""

sentence_end = [ ".", "!", "?" "。", "？","\n"]
lang=""
endpoint = ""

#executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

def speech_recongized(evt: speechsdk.SpeechRecognitionEventArgs):
    global speech_recognizer,all_text,speech_config,lang
    
    print('RECOGNIZED: {}'.format(evt.result.text))

    #await control_alltext()
    #process_openai(evt.result.text)
    """with open("transcript.txt", "w") as f:
        f.write(evt.result.text+"\n")"""
    lang = evt.result.properties.get(speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult)
    print (lang)
    all_text += evt.result.text + "\n"
    #eğer nokta virgül varsa save et
    asyncio.create_task(control_alltext())


            

        
def control_alltext():
    global all_text,speech_recognizer
    if all_text[-1] in sentence_end:
        speech_recognizer.stop_continuous_recognition_async()

        





    

    
def speech_recognizing(evt: speechsdk.SpeechRecognitionEventArgs):

    print('RECOGNIZING: {}'.format(evt.result.text))
    #controlLanguage(language)
    
    

def speech_session_started(evt: speechsdk.SessionEventArgs):
    print('SESSION STARTED: {}'.format(evt))
    
def speech_session_stopped(evt: speechsdk.SessionEventArgs):
    print('SESSION STOPPED: {}'.format(evt))

    
def speech_canceled(evt: speechsdk.SpeechRecognitionCanceledEventArgs):
    print('CANCELED: {}'.format(evt))
    
def save_txt(all_text):
    with open("transcript.txt", "w") as f:
        f.write(all_text+"\n")
        #all_text = ""
    # with open("language.txt", "w") as f:
    #     f.write(lang)
        
"""def controlLanguage(select):
    global lang
    global endpoint
    if select == "en-US":
        lang = "en-US"
        endpoint = os.getenv('AZURE_SPEECH_ID_EN')
    elif select == "tr-TR":
        lang = "tr-TR"
        endpoint = os.getenv('AZURE_SPEECH_ID_TR')
    elif select == "es-ES":
        lang = "es-ES"
        """
        
        


def speech_to_text():
    global all_text
    global speech_recognizer
    global result_future
    global lang

    load_dotenv()
    
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv('AZURE_SPEECH_KEY'), region=os.getenv('AZURE_SPEECH_REGION'))
    
    #controlLanguage(select)

    #autodetect = speechsdk.AutoDetectSourceLanguageConfig(languages=["en-US", "tr-TR"])
    speechsdk.languageconfig.SourceLanguageConfig("en-US", "bc5e43c5-8832-40f5-9490-90fc83ef6092")
    # en_language_config = speechsdk.languageconfig.SourceLanguageConfig("en-US", os.getenv('AZURE_SPEECH_ID_EN'))
    # tr_language_config = speechsdk.languageconfig.SourceLanguageConfig("tr-TR", os.getenv('AZURE_SPEECH_ID_TR'))
    # auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
    #     sourceLanguageConfigs=[en_language_config, tr_language_config])
    
    #OTOMATİK DİL TANIMA İŞİNİ YAPIP ARDINDAN ONA GÖRE TEXT TO SPEECH'İ SEÇTİR.
    
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    
    # speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, auto_detect_source_language_config=auto_detect_source_language_config)
    
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    
    done = False
    
    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))

        #speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True


        
    # Connect callbacks to the events fired by the speech recognizer
    #print (lang)
    speech_recognizer.recognizing.connect(speech_recognizing)
    
    speech_recognizer.recognized.connect(speech_recongized)
    speech_recognizer.session_started.connect(speech_session_started)
    speech_recognizer.session_stopped.connect(speech_session_stopped)
    speech_recognizer.canceled.connect(speech_canceled)
    
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)
    
    # Start continuous speech recognition
    
    speech_recognizer.start_continuous_recognition_async()

    
    
    

        
    
    while not done:
        time.sleep(.5)
    
    speech_recognizer.stop_continuous_recognition_async()
    
    save_txt(all_text)
    all_text = ""
    return all_text
    #exit()
    
    #async ile yap ve en önemlisi fastapiden çıkmamasını sağla (while kullanabilirsin)
    
        
    
    
#speech_to_text()

