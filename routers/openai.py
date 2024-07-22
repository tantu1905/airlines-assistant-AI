from fastapi import APIRouter,Depends,Form
from fastapi.responses import JSONResponse
from databases.database import get_db,SessionLocal
from methods.openaimethod import get_baggage_info,get_checkin_info,get_gate_info,get_fly_info,extract_date,reserve_ticket,delete_reservation
import json
from databases.database import SessionLocal
from databases.models import Import,QuestionAnswer
import os
from openai import AzureOpenAI
from concurrent.futures import ThreadPoolExecutor
import asyncio
from config import settings


router = APIRouter()

executor = ThreadPoolExecutor()


@router.post("/openai",response_class=JSONResponse)
async def openai(all_text: str = Form(...), db: SessionLocal = Depends(get_db)):
    print ("test")
    result_text = ""
    deployment_name = settings.AZURE_OAI_DEPLOYMENT
    key = settings.AZURE_OAI_KEY
    endpoint = settings.AZURE_OAI_ENDPOINT
    flights = []
    
    print (all_text)
    
    client = AzureOpenAI(azure_endpoint=endpoint, api_key=key, api_version="2024-02-15-preview")
    conversation = [
        {"role": "system", "content": "You are a Turkish Airlines AI assistant in Sabiha Gökçen Airport. Answer only next 3 flights. If delete reservation is called, pnr code delete spaces in booking code"},
        # {"role": "user", "content":"I want to do check-in"},
        # {"role":"assistant","content":"Sure, I can help you with that. Please provide me your ticket number."},
        # {"role": "user", "content": "I want to reserve a ticket"},
        # {"role":"assistant","content":"Sure, I can help you with that. Please provide me your flight number, departure date, your name, departure airport(optional), destination airport(optional) and departure time(optional)."},
        ]
    conversation.append({"role": "user", "content": all_text})
    detected_date = extract_date(all_text)
    if detected_date:
        print ("detected")
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_fly_info",
                "description": "Get the next flight time between two locations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The departure airport eg. IST",
                        },
                        "destination": {
                            "type": "string",
                            "description": "The destination airport eg. LHR",
                        },
                        "dep_date_time_date": {
                            "type": "string",
                            "description": "The departure date of the flight eg. YYYY-MM-DD format",
                            "format": "date",
                            "default": None,
                        }
                    },
                    "required": ["location", "destination"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "reserve_ticket",
                "description": "Reserve a ticket for a flight",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "flight_number": {
                            "type": "string",
                            "description": "The flight number eg. TK2123",
                        },
                        "dep_date_time_date": {
                            "type": "string",
                            "description": "The departure date of the flight eg. YYYY-MM-DD format",
                            "format": "date",
                        },
                        "name": {
                            "type": "string",
                            "description": "The name of the passenger",
                        },
                        "loc_origin": {
                            "type": "string",
                            "description": "The departure airport eg. IST",
                            "default": None
                        },
                        "loc_destination": {
                            "type": "string",
                            "description": "The destination airport eg. LHR",
                            "default": None
                        },
                        "dep_date_time_hour": {
                            "type": "string",
                            "description": "The departure time of the flight eg. HH:MM format",
                            "format": "time",
                            "default": None
                        },
                    },
                    "required": ["flight_number", "dep_date_time_date", "name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_reservation",
                "description": "Delete a reservation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pnr_code": {
                            "type": "string",
                            "description": "The pnr_code eg. TT8UCF",
                        },
                    },
                    "required": ["pnr_code"],
                },
            },
        },
    ]
    #delete fonksiyonunu ekle rezervasyonu silebilsin.
    loop = asyncio.get_event_loop()
    
    
    response = await loop.run_in_executor(
        executor,
        lambda: client.chat.completions.create(
            temperature=0.2,
            model=deployment_name,
            messages=conversation,
            tools=tools,
            tool_choice="auto",
            
        )
    )   
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "get_fly_info": get_fly_info,
            "reserve_ticket": reserve_ticket,
            "delete_reservation": delete_reservation,
        }
        conversation.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            # conversation.append({"role": "assistant", "content": function_to_call(tool_call.parameters)})
            print ("loading")
            function_args = json.loads(tool_call.function.arguments)
            if function_name == "reserve_ticket":
                function_response = function_to_call(flight_number=function_args.get("flight_number"), dep_date_time_date=detected_date, name=function_args.get("name"), loc_origin=function_args.get("loc_origin"), loc_destination=function_args.get("loc_destination"), dep_date_time_hour=function_args.get("dep_date_time_hour"))
            elif function_name == "get_fly_info":
                if detected_date:
                    function_response = function_to_call(loc_origin=function_args.get("location"), loc_destination=function_args.get("destination"), dep_date_time_date=detected_date)
                    flights = json.loads(function_response)
                else:
                    function_response = function_to_call(loc_origin=function_args.get("location"), loc_destination=function_args.get("destination"))
            elif function_name == "delete_reservation":
                function_response = function_to_call(pnr_code=function_args.get("pnr_code"))
            conversation.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
            second_response = await loop.run_in_executor(
                executor,
                lambda: client.chat.completions.create(
                    model=deployment_name,
                    messages=conversation,
                    temperature=0.2,
                    


                )
            )
            result_text = second_response.choices[0].message.content


            qa = QuestionAnswer(question=all_text, answer=result_text)
            db.add(qa)
            db.commit()
            db.refresh(qa)
    else:
        print("loading")
        other_response = await loop.run_in_executor(
            executor,
            lambda: client.chat.completions.create(
                model=deployment_name,
                messages=conversation,
                temperature=0.2,
                

            )
        )
        result_text = other_response.choices[0].message.content
        qa = QuestionAnswer(question=all_text, answer=result_text)
        db.add(qa)
        db.commit()
        db.refresh(qa)
    print (result_text)
    with open("answer.txt", "w") as f:
        f.write(f"{result_text}\n")
    return JSONResponse({"response": result_text,"flights": flights})