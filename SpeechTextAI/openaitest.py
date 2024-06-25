import openai
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from .text_to_speech import text_to_speech
import json
from .loading01 import typewriter
import requests
from thyfs import get_fly_info_thyapi
from databases.database import SessionLocal, engine,Base
from databases.models import Import

result_text = ""

def get_checkin_info(ticket_number):
    """burada checkin bilgileri alınacak"""


def get_baggage_info(ticket_number):
    """burada bagaj bilgileri alınacak"""
    
def get_gate_info(ticket_number):
    """burada gate bilgileri alınacak"""
    

def convert_city_to_airport(airport):
    if airport == "IST" or airport == "SAW":
        return "IST"
    elif airport == "LHR" or airport == "LGW" or airport == "STN":
        return "LON"
    elif airport == "CDG" or airport == "ORY":
        return "PAR"
    elif airport == "AMS":
        return "AMS"
    elif airport == "BER" or airport == "TXL" or airport == "SXF":
        return "BER"
    elif airport == "PRG":
        return "PRG"
    elif airport == "SVO" or airport == "DME" or airport == "VKO":
        return "MOW"
    elif airport == "LED":
        return "LED"
    elif airport == "SIN":
        return "SIN"
    elif airport == "SYD":
        return "SYD"
    elif airport == "HND" or airport == "NRT":
        return "TYO"
    elif airport == "KIX" or airport == "ITM":
        return "KIX"
    elif airport == "ICN" or airport == "GMP":
        return "SEL"
    elif airport == "ESB":
        return "ANK"
    elif airport == "ADB":
        return "IZM"
    elif airport == "GRZ":
        return "GRZ"
    elif airport == "GYD":
        return "BAK"
    elif airport == "FCO" or airport == "CIA":
        return "ROM"
    elif airport == "MXP" or airport == "LIN":
        return "MIL"
    else:
        return airport  # Eşleşmeyen kodlar için varsayılan olarak IATA kodunu döndür
        

def get_fly_info(loc_origin,loc_destination):
    
    db = SessionLocal()

    departure = convert_city_to_airport(loc_origin)
    arrival = convert_city_to_airport(loc_destination)
    # data = Import(departure,arrival)
    data2 = db.query(Import).filter(Import.departure == departure, Import.arrival == arrival).all()
    if not data2:
        return json.dumps({"location": loc_origin, "destination": loc_destination, "flight_number": "unknown"})
    else:
        return json.dumps({"location": data2[0].departure, "destination": data2[0].arrival, "departure_date_time": data2[0].dep_date_time_date.isoformat(),"dep_date_time_hour" : data2[0].dep_date_time_hour.isoformat(), "departure_airport": data2[0].dep_airport, "arrival_airport": data2[0].arr_airport, "flight_number": data2[0].flight_number})
    

# def get_fly_info(loc_origin,loc_destination):
#     """Get the flight information between two locations"""
#     """if "IST" in loc_origin.upper() and "LHR" in loc_destination.upper():
#         return json.dumps({"location": loc_origin, "destination": loc_destination, "next_flight_time": "16:00"})
#     elif "JFK" in loc_origin.upper() and "LAX" in loc_destination.upper():
#         return json.dumps({"location": "New York", "destination": "Los Angeles", "next_flight_time": "15:00"})
#     elif "CDG" in loc_origin.upper() and "JFK" in loc_destination.upper():
#         return json.dumps({"location": "Paris", "destination": "New York", "next_flight_time": "14:00"})
#     elif "AMS" in loc_origin.upper() and "IST" in loc_destination.upper():
#         return json.dumps({"location": "Amsterdam", "destination": "Istanbul", "next_flight_time": "17:00"})
#     elif "IST" in loc_origin.upper() and "ESB" in loc_destination.upper():
#         return json.dumps({"location": "Istanbul", "destination": "Ankara", "next_flight_time": "18:00"})"""
    # if loc_origin and loc_destination:
    #     flights = get_fly_info_thyapi(loc_origin,loc_destination)
    #     return json.dumps({"location": loc_origin, "destination": loc_destination, "departure_date_time": flights[0]["departure_date_time"], "departure_airport": flights[0]["departure_airport"], "arrival_airport": flights[0]["arrival_airport"], "flight_number": flights[0]["flight_number"]})
         
    # else:
    #     return json.dumps({"location": loc_origin, "destination": loc_destination, "flight_number": "unknown"})


def start_openai(all_text):
    
    global result_text

    load_dotenv()

    deployment_name = "gpt-new-test"
    key = os.getenv('AZURE_OAI_WHISPER_KEY')
    endpoint = os.getenv('AZURE_OAI_WHISPER_ENDPOINT')
    
    print (all_text)

    client = AzureOpenAI(azure_endpoint=endpoint, api_key=key, api_version="2024-02-15-preview")
    conversation = [
        {"role": "system", "content": "You are a Turkish Airlines AI assistant in Sabiha Gökçen Airport."},
        {"role": "user", "content":"I want to do check-in"},
        {"role":"assistant","content":"Sure, I can help you with that. Please provide me your ticket number."}
        ]
    conversation.append({"role": "user", "content": all_text})
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
                    },
                    "required": ["location", "destination"],
                },
            },
        }
    ]


    #text = input("Enter your message: ")

    response = client.chat.completions.create(temperature=0.2, model=deployment_name, messages=conversation,tools=tools,tool_choice="auto",max_tokens=60)
    #conversation.append({"role": "function", "name":"get_flight_info" ,"content": functions[0].)
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "get_fly_info": get_fly_info,
        }
        conversation.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            #typewriter("Loading... ▁ ▂ ▃ ▄ ▅ ▆ ▇ █ ▇ ▆ ▅ ▄ ▃ ▁", 0.08)
            print("loading")
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                loc_origin = function_args.get("location"),
                loc_destination = function_args.get("destination"),
            )
            conversation.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
            second_response = client.chat.completions.create(
                model=deployment_name,
                messages=conversation,
                temperature=0.2,
                #max_tokens=20
            )

            result_text = second_response.choices[0].message.content
    else:
        #typewriter("Loading... ▁ ▂ ▃ ▄ ▅ ▆ ▇ █ ▇ ▆ ▅ ▄ ▃ ▁", 0.08)
        print("loading")
        other_response = client.chat.completions.create(
            model=deployment_name,
            messages=conversation,
            temperature=0.2,
            max_tokens=60
        )
        result_text = other_response.choices[0].message.content
        
    

    #result_text = response.choices[0].message
    
    
    with open("answer.txt", "w") as f:
        f.write(f"{result_text}\n")
        
    #second_response = client.chat.completions.create(temperature=0.2, model=deployment_name, messages=conversation,max_tokens=20)
    
    #result2_text = response.choices[0].delta.content
    


    print (result_text)
    
    #save_txt(result_text)
    #text_to_speech(result_text)

            
    #os.remove ("transcript.txt")
    return result_text
