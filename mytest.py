import speech_recognition as sr
import os

lang = ["en-US", "tr-TR", "de-DE", "es-ES", "fr-FR", "it-IT", "ja-JP", "ko-KR", "pt-BR", "ru-RU", "zh-CN"]

def transcribe_audio_from_mic():
    recognizer = sr.Recognizer()
    key = os.getenv("AZURE_SPEECH_KEY")
    location = "swedencentral"
    final_text = ""
    with sr.Microphone() as source:
        print("Konuşmanızı kaydediyorum... (Lütfen birkaç saniye konuşun)")
        audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=10)
        
        for language in lang:
            try:
                countConf = 0
                print(f"{language} olarak tanımlanıyor...")
                text = recognizer.recognize_azure(audio_data, language=language, key=key, location=location)
                print(text)
            except sr.UnknownValueError:
                text = None
            except sr.RequestError:
                text = None
            
            if text and text[1] > 0.70:
                words = text[0].split()
                if len(words) >= 3:
                    return text
            elif text and text[1] > countConf:
                countConf = text[1]
                final_text = text
                       
        return final_text

if __name__ == "__main__":
    text = transcribe_audio_from_mic()

    if text:
        print(f"Transcribed Text: {text[0]}")
        print(f"Confidence: {text[1]}")
    else:
        print("Could not transcribe the audio.")