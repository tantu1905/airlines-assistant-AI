from SpeechTextAI.openaitest import start_openai
from SpeechTextAI.speech_to_text import speech_to_text
from fastapi import FastAPI,WebSocket,Query,Request,Depends
from SpeechTextAI.text_to_speech import text_to_speech
from enum import Enum
from fastapi.responses import HTMLResponse
import json
from fastapi.staticfiles import StaticFiles
from databases.database import SessionLocal,engine,Base
from databases.models import QuestionAnswer
import signal
from thyfs import get_fly_info_thyapi
from datetime import datetime
from databases.database import SessionLocal,engine,Base
from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
from sqlalchemy import MetaData,Table
from contextlib import asynccontextmanager
from apitosql import test,reset_qa
from databases.database import get_db
from routers import webpage,s2t,t2s,openai

scheduler = BackgroundScheduler()
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not scheduler.running:
        scheduler.add_job(test, 'interval', seconds=900,next_run_time=datetime.now())  
        scheduler.add_job(reset_qa, 'interval', seconds=86400,next_run_time=datetime.now())
        scheduler.start()
        yield
    else:
        print("Scheduler is already running.")

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(webpage.router)
app.include_router(s2t.router)
app.include_router(openai.router)
app.include_router(t2s.router)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

