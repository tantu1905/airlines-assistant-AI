from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydub import AudioSegment
import speech_recognition as sr
from dotenv import load_dotenv
import os
import logging

load_dotenv()

router = APIRouter()

logging.basicConfig(level=logging.INFO)

@router.post("/s2t", response_class=JSONResponse)
async def s2t(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    key = os.getenv("AZURE_SPEECH_KEY")
    location = os.getenv("AZURE_SPEECH_REGION")
    lang = [
        "en-US", "tr-TR", "de-DE", "es-ES", "fr-FR",
        "it-IT", "ja-JP", "ko-KR", "pt-BR", "ru-RU", "zh-CN"
    ]
    final_text = ""
    countConf = 0

    try:
        # Save the uploaded file to a temporary location
        file_location = "temp_audio.wav"
        with open(file_location, "wb") as temp_file:
            temp_file.write(await file.read())
        logging.info(f"Uploaded file saved as {file_location}")
    except Exception as e:
        logging.error(f"Error saving uploaded file: {e}")
        raise HTTPException(status_code=500, detail="Error saving uploaded file")

    try:
        # Convert webm to wav
        audio = AudioSegment.from_file(file_location)
        audio.export("temp_audio.wav", format="wav")
        logging.info("File converted from webm to wav")
    except Exception as e:
        logging.error(f"Error converting file: {e}")
        raise HTTPException(status_code=500, detail="Error converting file")

    try:
        # Recognize speech using Azure
        with sr.AudioFile("temp_audio.wav") as source:
            audio_data = recognizer.record(source)
            for language in lang:
                try:
                    logging.info(f"Recognizing as {language}...")
                    text = recognizer.recognize_azure(audio_data, language=language, key=key, location=location)
                    logging.info(f"Recognition result: {text}")
                except sr.UnknownValueError:
                    text = None
                except sr.RequestError as e:
                    logging.error(f"RequestError: {e}")
                    text = None

                if text and text[1] > 0.70:
                    words = text[0].split()
                    if len(words) >= 3:
                        return JSONResponse(content={"transcript": text[0]})
                elif text and text[1] > countConf:
                    countConf = text[1]
                    final_text = text

        return JSONResponse(content={"transcript": final_text[0] if final_text else "Null"})
    except Exception as e:
        logging.error(f"Error in speech recognition: {e}")
        raise HTTPException(status_code=500, detail="Error in speech recognition")