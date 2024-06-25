from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk


#import pygame

# def play_audio(file):
#     pygame.mixer.init()
#     pygame.mixer.music.load(file)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
#     pygame.mixer.quit()

def text_to_speech(text):
    #load_dotenv()
    speech_key = "e155275b28bf4443a39a1325159509ef"
    service_region = "swedencentral"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    
    speech_config.speech_synthesis_voice_name = "en-US-ShimmerMultilingualNeural"
   #speech_config.speech_synthesis_language = "tr-TR"
    
    # speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat["Audio24Khz48KBitRateMonoMp3"])
    #speech_config.speech_synthesis_voice_name="en-US-AndrewNeural"
    #speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat["Audio24Khz48KBitRateMonoMp3"])
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_synthesizer.speak_text_async(text).get()
    
    stream = speechsdk.AudioDataStream(result)
    #stream.save_to_wav_file("output.mp3")
    
    #play_audio("output.mp3")
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        i=1
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print ("canceled")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
            #print("Error details: {}".format(cancellation_details.error_details))
            
            
    return result