import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

load_dotenv()
# Azure abonelik anahtarınız ve bölgeniz
subscription_key = os.getenv("AZURE_SPEECH_KEY")
region = "swedencentral"

def speech_recognition_with_confidence_score():
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    autodetect = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "tr-TR"])
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config,auto_detect_source_language_config=autodetect)

    def recognized_cb(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
            # Confidence score'u elde etmek için n-best sonuçlarını kontrol edin
            detailed_result = result.properties[speechsdk.PropertyId.SpeechServiceResponse_JsonResult]
            print(detailed_result)
            print(detailed_result.get("PrimaryLanguage").get("Confidence"))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")

    def canceled_cb(evt):
        cancellation_details = evt.result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.canceled.connect(canceled_cb)

    print("Speak into your microphone.")
    speech_recognizer.start_continuous_recognition()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        speech_recognizer.stop_continuous_recognition()

speech_recognition_with_confidence_score()