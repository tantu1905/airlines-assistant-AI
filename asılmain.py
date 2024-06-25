from SpeechTextAI.openaitest import start_openai
from SpeechTextAI.speech_to_text import speech_to_text
from fastapi import FastAPI,WebSocket,Query,Request,Depends
from SpeechTextAI.text_to_speech import text_to_speech
from enum import Enum
from fastapi.responses import HTMLResponse
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from newtest import record_audio_test
from whispertest import whisper_test
from tts  import tts_test
from databases.database import SessionLocal,engine,Base
from databases.models import QuestionAnswer
import signal
from thyfs import get_fly_info_thyapi
from datetime import datetime
from databases.models import get_table_name
from arraybuilder import build_array
from databases.database import SessionLocal,engine,Base
from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
from sqlalchemy import MetaData,Table

template = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

done = False


        
    # print ("test")   

    # data = json.loads(json_import.data)
    #data = db.query(json_import).filter(json_import.id == 3).first()
    #data2 = json.loads(data.data)
    #stringi yazdırmak için
    #return data.departure
    #datanın tamamını yazdırmak için veya datadan belli bir indexi çekmek için aşağıdaki
    #return "Success"
    


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def test():
    db = SessionLocal()
    array1 = ["IST","SAW"]
    iata_codes = [
    "LON",  # Londra
    "PAR",  # Paris
    "AMS",  # Amsterdam
    "BER",  # Berlin
    "STR",  # Stuttgart
    "MUC",  # München
    "MRS",  # Marsilya
    "PRG",  # Prag
    "MOW",  # Moskova
    "LED",  # St.Petersburg
    "DXB",  # Dubai
    "SIN",  # Singapur
    "SYD",  # Sydney
    "TYO",  # Tokyo
    "KIX",  # Osaka
    "SEL",  # Seoul
    "TZX",  # Trabzon
    "MLX",  # Malatya
    "ESB",  # Ankara
    "ADB",  # Izmir
    "AYT",  # Antalya
    "ADA",  # Adana
    "DIY",  # Diyarbakır
    "KSY",  # Kars
    "MSR",  # Muş
    "GRZ",  # Graz
    "WAW",  # Varşova
    "ATH",  # Atina
    "GYD",  # Bakü
    "FCO",  # Roma
    "MXP",  # Milano
    "MAD",  # Madrid
    "BCN",  # Barcelona
    "ZRH",  # Zürih
    "BRU",   # Brüksel
    "KYA",  # Konya
    "OGU",  # Ordu-Giresun
    "GZT",  # Gaziantep
    "ASR",  # Kayseri
    ]

    for i in iata_codes:
        try:
            json_data = get_fly_info_thyapi("IST", i)
            data3 = json.dumps(json_data)
            data4 = json.loads(data3)
            for k in json_data:
                json_import = get_table_name(k["departure_loc"], k["arrival_loc"])
                # Tabloyu temizle
                db.query(json_import).delete()
                db.commit()
                print (f'IST and {k["arrival_loc"]} deleted')
                break  # Tabloyu bir kez temizledikten sonra döngüden çık
        except AttributeError:
            print(f'IST and {i} not found')
    for i in iata_codes:
        try:
            json_data = get_fly_info_thyapi("IST",i)
        #json['departure_date_time_date'] = json['departure_date_time_date'].isoformat()
            data3 = json.dumps(json_data)
            data4 = json.loads(data3)
            # db.query(json_import).delete()
            # db.commit()
            for k in json_data:
                # meta = MetaData()
                # table_to_drop = Table(f'IST_{i}', meta).drop(engine,checkfirst=True)
                # tablename = f'IST_{k["arrival_loc"]}'
                json_import = get_table_name(k["departure_loc"],k["arrival_loc"])

                
            # json_import = Import(departure=json_data[0]["departure_loc"],arrival=json_data[0]["arrival_loc"],data=data4).__init__(json_data[0]["departure_loc"],json_data[0]["arrival_loc"])
                dep_date_time = datetime.fromisoformat(k["departure_date_time"].replace("Z", "+00:00"))
                dep_date_time_date = dep_date_time.date()
                dep_date_time_hour = dep_date_time.time()
                import_instance = json_import(departure=k["departure_loc"],arrival=k["arrival_loc"],dep_airport=k["departure_airport"],arr_airport=k["arrival_airport"],dep_date_time_date=dep_date_time_date,dep_date_time_hour=dep_date_time_hour,flight_number=k["flight_number"])
                db.add(import_instance)
                print (f'added IST and {k["arrival_loc"]}')
                db.commit()
                db.refresh(import_instance)

                # Base.metadata.create_all(bind=engine)
            
        except AttributeError:
            print (f'IST and {i} not found')
            
    print ("test")
    Base.metadata.create_all(bind=engine)   


scheduler = BackgroundScheduler()
scheduler.add_job(test, 'interval', seconds=900,next_run_time=datetime.now())    
# @app.on_event("startup")
# async def startup_event():
#     # Drop all tables and create them again at startup
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)


@app.get("/")
async def get(request: Request):
    return template.TemplateResponse("test.html", {"request": request})

@app.get("/s2t")
async def s2t():
    
    #data2 = await websocket.receive_text()
    #data2 = json.loads(data2)
    #text = data2["text"]
    #language = data2["language"]
    
    #language = "en-US"
    
    speech_to_text()
    #record_audio_test()
    #whisper_test()
    
    with open ('transcript.txt','r') as file:
        text = file.read()
        file.close()
        
    #if (text.find('send'))
    
    
    return({"transcript": text})

# @app.get("/thyTest")
# async def thyTest():
#     db = SessionLocal()
#     # array1 = ["IST"]
#     iata_codes = [
#     "LON",  # Londra
#     "PAR",  # Paris
#     "AMS",  # Amsterdam
#     "BER",  # Berlin
#     "STR",  # Stuttgart
#     "MUC",  # München
#     "MRS",  # Marsilya
#     "PRG",  # Prag
#     "MOW",  # Moskova
#     "LED",  # St.Petersburg
#     "DXB",  # Dubai
#     "SIN",  # Singapur
#     "SYD",  # Sydney
#     "TYO",  # Tokyo
#     "KIX",  # Osaka
#     "SEL",  # Seoul
#     "TZX",  # Trabzon
#     "MLX",  # Malatya
#     "ESB",  # Ankara
#     "ADB",  # Izmir
#     "AYT",  # Antalya
#     "ADA",  # Adana
#     "DIY",  # Diyarbakır
#     "KSY",  # Kars
#     "MSR",  # Muş
#     "GRZ",  # Graz
#     "WAW",  # Varşova
#     "ATH",  # Atina
#     "GYD",  # Bakü
#     "FCO",  # Roma
#     "MXP",  # Milano
#     "MAD",  # Madrid
#     "BCN",  # Barcelona
#     "ZRH",  # Zürih
#     "BRU",   # Brüksel
#     "KYA",  # Konya
#     "OGU",  # Ordu-Giresun
#     "GZT",  # Gaziantep
#     "ASR",  # Kayseri
#     ]

#     for i in iata_codes:
#         try:
#             json_data = get_fly_info_thyapi("IST",i)
#         #json['departure_date_time_date'] = json['departure_date_time_date'].isoformat()
#             data3 = json.dumps(json_data)
#             data4 = json.loads(data3)
#             for k in json_data:

#                 json_import = get_table_name(k["departure_loc"],k["arrival_loc"])
#             # json_import = Import(departure=json_data[0]["departure_loc"],arrival=json_data[0]["arrival_loc"],data=data4).__init__(json_data[0]["departure_loc"],json_data[0]["arrival_loc"])
#                 dep_date_time = datetime.fromisoformat(k["departure_date_time"].replace("Z", "+00:00"))
#                 dep_date_time_date = dep_date_time.date()
#                 dep_date_time_hour = dep_date_time.time()
#                 import_instance = json_import(departure=k["departure_loc"],arrival=k["arrival_loc"],dep_airport=k["departure_airport"],arr_airport=k["arrival_airport"],dep_date_time_date=dep_date_time_date,dep_date_time_hour=dep_date_time_hour,flight_number=k["flight_number"])
#                 db.add(import_instance)
#                 db.commit()
#                 db.refresh(import_instance)
                
#                 print (f'added IST and {k["arrival_loc"]}')
#         except AttributeError:
#             print (f'IST and {i} not found')
            
        
                    

    # data = json.loads(json_import.data)
    #data = db.query(json_import).filter(json_import.id == 3).first()
    #data2 = json.loads(data.data)
    #stringi yazdırmak için
    #return data.departure
    #datanın tamamını yazdırmak için veya datadan belli bir indexi çekmek için aşağıdaki
    # return "Success"
# burada istediğimiz kolonu yazarak çekebiliriz
    # date =  data.data[2].get("departure_date_time_date")
    # return  datetime.fromisoformat(date.replace("Z", "+00:00")).time()
    # return date2.date()

# veriyi db'den çek ardından json.loads ile json'a dönüştür ardından dizi olarak jsonlar gelecek ve o jsonların içinde arama yapabileceksin
    #data jsonloads olarak gönderilir sql'e ardından veri çekmek istediğimiz zaman 

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,db: SessionLocal = Depends(get_db)):
    await websocket.accept()
    if not scheduler.running:
        scheduler.start()
    else:
        print("Scheduler is already running.")
    try:
        while True:
            try:
                data2 = await websocket.receive_text()
                data2 = json.loads(data2)
                #await websocket.send_text(json.dumps({"type": "system", "text": data2}))

                """text = data2["text"]
                    language = data2["language"]
                    
                    print (language)
                    
                    
                    text = speech_to_text(language)"""
                
                if "command" in data2 and data2["command"] == "start_speech_to_text":
                    # record_audio_test()
                    # whisper_test()
                    #language = data2["language"]
                    speech_to_text()
                    with open('transcript.txt', 'r') as file:
                        transcript = file.read().strip()
                    await websocket.send_text(json.dumps({"type": "user", "text": transcript}))
                    if 'send' in transcript.lower() or 'gönder' in transcript.lower():
                        await websocket.send_text(json.dumps({"type": "auto_send", "text": transcript, "language": language}))
                else:
                    text = data2["text"]
                    #await websocket.send_text(json.dumps({"type": "user", "text": text}))
                    language = data2["language"]
                    

                
                
                #data2 = await websocket.receive_text()
                
                with open('transcript.txt', 'r') as file:
                    data = file.read().strip()
                    file.close()
                if data == ('Stop.') or data == ('Bitir.'):
                    return "Conversation ended."
                #if 'send' in data.lower() or 'gönder' in data.lower():

                data = text

                if 'send' in data.lower():
                    data = data.replace('send', '')
                if 'gönder' in data.lower() or 'gönder' in data.lower() or 'gönder.' in data.lower():
                    data = data.replace('gönder', '')
                    
                with open('language.txt', 'r') as file:
                    language = file.read()
                    file.close()  
                    
                if 'en-us' in language.lower():
                    language = 'en-US'
                if 'tr-tr' in language.lower():
                    language = 'tr-TR'
                    

                
                
                    
                await websocket.send_text(json.dumps({"type": "user", "text": data}))
                
                
                
                #await websocket.send_text(f"Message text was: {data}")

                
                
                start_openai(data)
                

                
                

                
                with open ('answer.txt','r') as file:
                    result_text = file.read()
                    file.close()
                await websocket.send_text(json.dumps({"type": "openai", "text": result_text}))
                # tts_test()
                # play_audio()
                text_to_speech(result_text)
                
                qa = QuestionAnswer(question=data,answer=result_text)
                db.add(qa)
                db.commit()
                db.refresh(qa)

            except Exception as e:
                print(e)
                break
                
                

            
    except Exception as e:
        print("Hata")
        
        

        #await websocket.send_text(f"Message text was: {data}")
#full_text = ""
"""class Select(str, Enum):
    tr = "tr-TR"
    en = "en-US"
    es = "es-ES"
    

    


@app.get("/response/{Select}")"""
"""async def response(select : Select):
    global done,prompt
    #while True:

    speech_to_text(select)
    #return full_text
    with open('transcript.txt', 'r') as file:
        prompt = file.read().strip()
        #prompt = prompt.replace('\n', ' ')
        #file.close()
        if prompt == ('Stop.') or prompt == ('Bitir.'):
            return "Conversation ended."
        """

        
    #while True:   
"""  if prompt == ("Stop."): 
            done = True
            break
    if done == True:
        return "Conversation ended."""
    


    #return prompt"""
    
"""@app.post("/response/{Select}")
async def response(select : Select):
    global prompt,result_text
    return start_openai(prompt)
    
    """
    
"""@app.get("/response/{Select}/")
async def response(select : Select):
    with open('answer.txt', 'r') as file:
        result_text = file.read()
        #file.close()
        
    text_to_speech(result_text,select)
    
    return result_text
# 


    start_openai(prompt)
        
        with open('answer.txt', 'r') as file:
            result_text = file.read()
            #file.close()

        
        text_to_speech(result_text,select)"""























'''from fastapi import FastAPI
import os
import openai
from openai import AzureOpenAI
from dotenv import load_dotenv
import requests
from pydantic import BaseModel
from typing import Dict,Any

load_dotenv()
deploymentname = os.getenv("AZURE_OAI_DEPLOYMENT")
endpoint = os.getenv("AZURE_OAI_ENDPOINT")
key=os.getenv("AZURE_OAI_KEY")
version = "2024-02-15-preview"

client = AzureOpenAI(azure_endpoint=endpoint,api_key=key,api_version=version)
url = "{}openai/deployments/Dalle3/images/generations?api-version={}".format(endpoint,version)
headers = {"api-key":key,"Content-Type":"application/json"}



app = FastAPI()

def index():
    return 'test'


class AISettingsSystem(BaseModel):
    content:str
    temperature:float
    
settings : AISettingsSystem = AISettingsSystem(content="Stable AI Assistant", temperature=0.5)

    

@app.get("/")
async def root(prompt):
    response = client.chat.completions.create(model=deploymentname,
                                          messages=[{"role":"system","content":settings.content},
                                                    {"role":"user","content":prompt}],
                                          temperature=settings.temperature)
    
    testmessagereturn = response.choices[0].message.content;
    return testmessagereturn;


@app.post("/")
async def setAISettings(request:AISettingsSystem):
    settings.temperature = request.temperature
    settings.content=request.content
    return {'data':'AI Settings is changed.'}


@app.get("/images/{prompt}")
async def create_image(prompt):
    body = {"prompt":prompt,"n":1,"size":"1024x1024"}
    response = requests.post(url,headers=headers,json=body)
    return response.json()['data'][0]['url']
'''