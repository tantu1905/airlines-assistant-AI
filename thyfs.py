import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

def get_fly_info_thyapi(loc_origin, loc_destination):
    test = loc_origin
    test2 = loc_destination
    now_date = datetime.now().date()
    scheduleType = "W"
    url = 'https://api.turkishairlines.com/test/getTimeTable'
    values = {
        "requestHeader": {
            "clientUsername": "OPENAPI",
            "clientTransactionId": "CLIENT_TEST_1",
            "channel": "WEB",
            "languageCode": "TR",
            "airlineCode": "TK"
        },
        "OTA_AirScheduleRQ": {
            "OriginDestinationInformation": {
                "DepartureDateTime": {
                    "WindowAfter": "P3D",
                    "WindowBefore": "P3D",
                    "Date": f'{now_date}'
                },
                "OriginLocation": {
                    "LocationCode": test,
                    "MultiAirportCityInd": True
                },
                "DestinationLocation": {
                    "LocationCode": test2,
                    "MultiAirportCityInd": True
                }
            },
            "AirlineCode": "TK",
            "FlightTypePref": {
                "DirectAndNonStopOnlyInd": True
            }
        },
        "scheduleType": scheduleType,
        "tripType": "O"
    }

    headers = {
        'apisecret': os.getenv("THY_API_SECRET"),
        'Content-Type': 'application/json',
        'apikey': os.getenv("THY_API_KEY")
    }

    response = requests.post(url, data=json.dumps(values), headers=headers)
    
    # Check the response status code
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return []

    # Check if the response content is empty
    if not response.content:
        print("Error: Received empty response")
        return []

    try:
        response_data = response.json()
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response")
        print(response.text)  # Print the raw response text for debugging
        return []

    with open("response.json", "w") as f:
        json.dump(response_data, f)

    flights = []

    extended_ota_air_schedule_rs = response_data.get("data", {}).get("timeTableOTAResponse", {}).get("extendedOTAAirScheduleRS", {})

    ota_air_schedule_rs = extended_ota_air_schedule_rs.get("OTA_AirScheduleRS", {})
    origin_destination_option = ota_air_schedule_rs.get("OriginDestinationOptions", {})
    origin_destination_options = origin_destination_option.get("OriginDestinationOption", [])

    for option in origin_destination_options:
        flight_segment = option.get("FlightSegment")
        departure = origin_destination_option.get("OriginCode", "N/A")
        arrival = origin_destination_option.get("DestinationCode", "N/A")

        if isinstance(flight_segment, dict):
            flight_segment = [flight_segment]

        for flight_seg in flight_segment:
            departure_airport = flight_seg.get("DepartureAirport", {}).get("LocationCode", "N/A")
            arrival_airport = flight_seg.get("ArrivalAirport", {}).get("LocationCode", "N/A")
            departure_date_time = flight_seg.get("DepartureDateTime", {})
            departure_date_time_date = datetime.fromisoformat(departure_date_time.replace("Z", "+00:00"))
            flight_number = flight_seg.get("FlightNumber", "N/A")

            flights.append({
                "departure_loc": departure,
                "arrival_loc": arrival,
                "departure_airport": departure_airport,
                "arrival_airport": arrival_airport,
                "departure_date_time": departure_date_time,
                "departure_date_time_date": departure_date_time_date.isoformat(),
                "flight_number": flight_number
            })

    flights.sort(key=lambda x: x["departure_date_time"])

    future_flights = []

    for flight in flights:
        now = datetime.now()
        if datetime.fromisoformat(flight["departure_date_time_date"]) < now:
            flights.pop(flights.index(flight))
        else:
            future_flights.append(flight)

    return future_flights

# Example usage
#get_fly_info_thyapi("IST", "IZM")
