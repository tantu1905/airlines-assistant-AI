from databases.database import SessionLocal
from databases.models import Import,Ticket
import json
from datetime import datetime
import dateparser
import spacy
import random
import string
import re

def get_checkin_info(ticket_number):
    """burada checkin bilgileri alınacak"""


def get_baggage_info(ticket_number):
    """burada bagaj bilgileri alınacak"""
    
def get_gate_info(ticket_number):
    """burada gate bilgileri alınacak"""
    
    
def create_seat_number(flight_number,dep_date_time_date):
    count = 0
    #counter koy eğer count sayısı koltuk sayısını geçerse dolu diye döndür.
    created = False
    db = SessionLocal()
    #kullanılan random sayı eğer datetime ile farklı günse kullanılabilir aksi durumda kullanılamaz ve hariç tutulur.
    if flight_number:
        while created == False:
            if count >4:
                return "unknown"
            seat_number = f'{random.randint(1, 46)}{random.choice("ABCDEF")}'
            query = db.query(Ticket).filter(Ticket.seat_number == seat_number)
            if query.count() == 0:
                created = True
                print (seat_number)
                return seat_number
            else:
                query = query.filter(Ticket.flight_number == flight_number, Ticket.dep_date_time_date == dep_date_time_date)
                #yerel uçuşlarla date bölümünü test et.
                if query.count() == 0:
                    created = True
                    print (seat_number)
                    return seat_number
                else:
                    print("have seat number")
                    count += 1
                    continue
    #kullanılan random sayı eğer datetime ile farklı günse kullanılabilir aksi durumda kullanılamaz ve hariç tutulur.
    # if flight_number:
    #     seat_number = f'{random.randint(1, 46)}{random.choice("ABCDEF")}'
    #     print (seat_number)
    #     return seat_number

def create_reservation_number(flight_number):
    #flight numberdan sonra seat numberin ilk indeksi ardından random sayılar ve 2. indeks yer alacak.
    #rezervasyon numarası 12 haneli olacak random sayıları ona göre belirlersin ve unique olacak
    #üstteki unique işini yapmayı unutma.
    characters = string.ascii_letters + string.digits
    reservation_number = ''.join(random.choices(characters, k=6))
    reservation_number = reservation_number.upper()
    return reservation_number
def reserve_ticket(flight_number,dep_date_time_date,name,loc_origin=None,loc_destination=None,dep_date_time_hour=None):
    print (dep_date_time_date)
    print("start reservation")
    db = SessionLocal()
    query = db.query(Import).filter(Import.flight_number == flight_number, Import.dep_date_time_date == dep_date_time_date)
    
    

    print (dep_date_time_date)
    print (flight_number)
    
    
    if loc_origin is not None:
        departure = convert_city_to_airport(loc_origin)
        query = query.filter(Import.departure == departure)
    if loc_destination is not None:
        arrival = convert_city_to_airport(loc_destination)
        query = query.filter(Import.arrival == arrival)
    if dep_date_time_hour is not None:
        query = query.filter(Import.dep_date_time_hour == dep_date_time_hour)
    # if query.filter(Import.empty_seats > 0) is not None:
    data = query.all()
    print (data)
    
    if query.count() == 0:
        print ("no data")
        return json.dumps({"name": name, "flight_number": flight_number, "seat_number": "unknown", "pnr_code": "unknown","message": "Flight not found"})
    #uçuş bulunamadı mesajı
        
    dep_date_time_date = datetime.strptime(dep_date_time_date, "%Y-%m-%d").date()
        
    seat_num = create_seat_number(flight_number,dep_date_time_date)
    if seat_num == "unknown":
        return json.dumps({"name": name, "flight_number": flight_number, "seat_number": "unknown", "pnr_code": "unknown","message": "Seat not found"})

    #eğer seat number oluşturulamazsa res num da oluşturulamasın ve hata versin
    pnr_code = create_reservation_number(flight_number)

    ticket = Ticket(name=name, flight_number=flight_number, seat_number=seat_num, pnr_code=pnr_code,dep_date_time_date=dep_date_time_date)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return json.dumps({"name": ticket.name, "flight_number": ticket.flight_number, "seat_number": ticket.seat_number, "pnr_code": ticket.pnr_code})
        
    
    
        
def delete_reservation(pnr_code):
    db = SessionLocal()
    pnr_code = pnr_code.replace(" ", "")
    pnr_code = pnr_code.upper()
    print (pnr_code)
    query = db.query(Ticket).filter(Ticket.pnr_code == pnr_code)
    if query.count() == 0:
        return json.dumps({"pnr_code": pnr_code, "message": "Reservation not found"})
    ticket = query.first()
    db.delete(ticket)
    db.commit()
    return json.dumps({"pnr_code": pnr_code, "message": "Reservation deleted"})
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
        
        
        
def extract_date(text):
    dates = []
    current_year = datetime.now().year
    
    # Tarih formatlarını tanımlayan düzenli ifadeler
    date_patterns = [
        r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # 12/31/2020 veya 31/12/2020
        r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # 12-31-2020 veya 31-12-2020
        r'\b\d{1,2} \w+ \d{2,4}\b',      # 31 December 2020
        r'\b\w+ \d{1,2}, \d{2,4}\b',     # December 31, 2020
        r'\b\d{1,2} \w+\b',              # 2 Temmuz
        r'\b\w+ \d{1,2}\b',  # July 2
        r'\b\d{1,2}. \w+\b',  # 2. Juli
        r'\b\w+ \d{1,2}(?:st|nd|rd|th)?\b'
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                # Bulunan tarihi doğrulama ve normalleştirme
                date = dateparser.parse(match)
                
                # Eğer tarih geçmişse, bir yıl ekleyin
                if date and date < datetime.now():
                    date = date.replace(year=date.year + 1)
                
                if date:
                    dates.append(date.strftime('%Y-%m-%d'))
            except ValueError:
                continue
    
    return dates[0] if dates else None
        
# nlp = spacy.load("en_core_web_sm")

# def extract_date(text):
#     doc = nlp(text)
#     dates = []
#     for ent in doc.ents:
#         if ent.label_ == "DATE":
#             parsed_date = dateparser.parse(ent.text)
#             if parsed_date:
#                 dates.append(parsed_date.strftime('%Y-%m-%d'))
#     return dates[0] if dates else None

def get_fly_info(loc_origin,loc_destination,dep_date_time_date= None):
    flights = []
    db = SessionLocal()
    
    #alembic ile devam edilecek.

    departure = convert_city_to_airport(loc_origin)
    arrival = convert_city_to_airport(loc_destination)
    # data = Import(departure,arrival)
    
    query = db.query(Import).filter(Import.departure == departure, Import.arrival == arrival)
    
    if dep_date_time_date is not None:
        query = query.filter(Import.dep_date_time_date == dep_date_time_date)
        print (dep_date_time_date)
    data2 = query.all()
    if not data2:
        return json.dumps({"location": loc_origin, "destination": loc_destination, "flight_number": "unknown"})
    else:
        
        for i in data2:
            flights.append({"location": i.departure, "destination": i.arrival, "departure_date_time": i.dep_date_time_date.isoformat(),"dep_date_time_hour" : i.dep_date_time_hour.isoformat(), "departure_airport": i.dep_airport, "arrival_airport": i.arr_airport, "flight_number": i.flight_number})
        return json.dumps(flights)
